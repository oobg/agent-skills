import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "skills" / "new-space" / "scripts" / "new_space.py"


def run(*args, cwd=None, check=True):
    return subprocess.run(args, cwd=cwd, check=check, text=True, capture_output=True)


class NewSpaceScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        run("git", "init", "-q", "-b", "main", str(self.repo))
        run("git", "config", "user.name", "Synthetic User", cwd=self.repo)
        run("git", "config", "user.email", "synthetic@example.test", cwd=self.repo)
        (self.repo / "README.md").write_text("fixture\n", encoding="utf-8")
        run("git", "add", "README.md", cwd=self.repo)
        run("git", "commit", "-qm", "initial", cwd=self.repo)

    def tearDown(self):
        self.temp.cleanup()

    def script(self, *args, check=True):
        return run(sys.executable, str(SCRIPT), *args, check=check)

    def test_preflight_explicit_base(self):
        (self.repo / "draft.txt").write_text("unchanged\n", encoding="utf-8")
        before = run("git", "status", "--porcelain=v1", cwd=self.repo).stdout
        result = self.script(
            "preflight", "--repo", str(self.repo), "--branch", "feat/search-filter", "--base", "main"
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["base_ref"], "main")
        self.assertEqual(len(payload["base_sha"]), 40)
        self.assertEqual(run("git", "status", "--porcelain=v1", cwd=self.repo).stdout, before)

    def test_preflight_rejects_existing_branch(self):
        result = self.script(
            "preflight", "--repo", str(self.repo), "--branch", "main", "--base", "main", check=False
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("branch already exists", json.loads(result.stderr)["error"])

    def test_preflight_finds_one_unmerged_release(self):
        run("git", "checkout", "-qb", "release-work", cwd=self.repo)
        (self.repo / "release.txt").write_text("fixture\n", encoding="utf-8")
        run("git", "add", "release.txt", cwd=self.repo)
        run("git", "commit", "-qm", "release", cwd=self.repo)
        release_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        main_sha = run("git", "rev-parse", "main", cwd=self.repo).stdout.strip()
        run("git", "update-ref", "refs/remotes/upstream/release/1.2.0", release_sha, cwd=self.repo)
        run("git", "update-ref", "refs/remotes/upstream/main", main_sha, cwd=self.repo)
        result = self.script(
            "preflight",
            "--repo", str(self.repo),
            "--branch", "fix/payment-timeout",
            "--main-ref", "upstream/main",
            "--release-glob", "upstream/release/*",
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "active-release")
        self.assertEqual(payload["base_ref"], "upstream/release/1.2.0")

    def test_preflight_reports_multiple_active_releases(self):
        main_sha = run("git", "rev-parse", "main", cwd=self.repo).stdout.strip()
        run("git", "update-ref", "refs/remotes/upstream/main", main_sha, cwd=self.repo)
        for version in ("1.2.0", "1.3.0"):
            run("git", "checkout", "-qB", f"release-{version}", "main", cwd=self.repo)
            path = self.repo / f"release-{version}.txt"
            path.write_text("fixture\n", encoding="utf-8")
            run("git", "add", path.name, cwd=self.repo)
            run("git", "commit", "-qm", f"release {version}", cwd=self.repo)
            sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
            run("git", "update-ref", f"refs/remotes/upstream/release/{version}", sha, cwd=self.repo)
        result = self.script(
            "preflight",
            "--repo", str(self.repo),
            "--branch", "feat/search-filter",
            "--main-ref", "upstream/main",
            "--release-glob", "upstream/release/*",
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["decision"], "ambiguous-release")
        self.assertEqual(len(payload["active_release_refs"]), 2)

    def test_verify_detects_rewritten_branch_and_matching_base(self):
        base_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        run("git", "checkout", "-qb", "dev-feat-search-filter", cwd=self.repo)
        (self.repo / "draft.txt").write_text("unchanged\n", encoding="utf-8")
        before = run("git", "status", "--porcelain=v1", cwd=self.repo).stdout
        result = self.script(
            "verify",
            "--worktree", str(self.repo),
            "--expected-branch", "feat/search-filter",
            "--base-sha", base_sha,
            check=False,
        )
        self.assertEqual(result.returncode, 3)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["branch_rewritten"])
        self.assertEqual(payload["ahead"], 0)
        self.assertEqual(payload["behind"], 0)
        self.assertEqual(run("git", "status", "--porcelain=v1", cwd=self.repo).stdout, before)

    def test_verify_rejects_head_ahead_of_base(self):
        base_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        run("git", "checkout", "-qb", "feat/search-filter", cwd=self.repo)
        (self.repo / "change.txt").write_text("fixture\n", encoding="utf-8")
        run("git", "add", "change.txt", cwd=self.repo)
        run("git", "commit", "-qm", "change", cwd=self.repo)
        result = self.script(
            "verify",
            "--worktree", str(self.repo),
            "--expected-branch", "feat/search-filter",
            "--base-sha", base_sha,
            check=False,
        )
        self.assertEqual(result.returncode, 3)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["ahead"], 1)
        self.assertEqual(payload["behind"], 0)


if __name__ == "__main__":
    unittest.main()
