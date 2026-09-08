import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).parents[1]
    / "skills"
    / "deploy-staging"
    / "scripts"
    / "preflight.py"
)
SPEC = importlib.util.spec_from_file_location("deploy_staging_preflight", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def run_git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


class DeployStagingPreflightTests(unittest.TestCase):
    def test_reports_revisions_changes_and_target_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sample"
            root.mkdir()
            run_git(root, "init", "-b", "feature/sample")
            run_git(root, "config", "user.name", "Example User")
            run_git(root, "config", "user.email", "example@example.invalid")
            (root / "tracked.txt").write_text("first\n", encoding="utf-8")
            run_git(root, "add", "tracked.txt")
            run_git(root, "commit", "-m", "initial")
            run_git(root, "branch", "integration")

            target_tree = Path(tmp) / "integration tree\tcopy"
            run_git(root, "worktree", "add", str(target_tree), "integration")
            (root / "tracked.txt").write_text("changed\n", encoding="utf-8")
            (root / "new.txt").write_text("new\n", encoding="utf-8")

            before_head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            before_status = subprocess.run(
                ["git", "-C", str(root), "status", "--porcelain=v1", "-z"],
                check=True,
                capture_output=True,
            ).stdout

            report = MODULE.collect(root, "integration", "origin")

            self.assertEqual(report["current"]["branch"], "feature/sample")
            self.assertEqual(report["current"]["sha"], report["target"]["local_sha"])
            self.assertEqual(report["changes"]["unstaged"], 1)
            self.assertEqual(report["changes"]["untracked"], 1)
            self.assertFalse(report["changes"]["clean"])
            self.assertFalse(report["remote"]["configured"])
            self.assertEqual(
                report["target"]["occupied_worktrees"][0]["branch"], "integration"
            )
            self.assertEqual(
                Path(report["target"]["occupied_worktrees"][0]["path"]).resolve(),
                target_tree.resolve(),
            )
            after_head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            after_status = subprocess.run(
                ["git", "-C", str(root), "status", "--porcelain=v1", "-z"],
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(before_head, after_head)
            self.assertEqual(before_status, after_status)

    def test_does_not_expose_remote_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sample"
            root.mkdir()
            run_git(root, "init", "-b", "main")
            run_git(root, "config", "user.name", "Example User")
            run_git(root, "config", "user.email", "example@example.invalid")
            (root / "file.txt").write_text("content\n", encoding="utf-8")
            run_git(root, "add", "file.txt")
            run_git(root, "commit", "-m", "initial")
            secret_url = "https://user:secret@example.invalid/repo.git"
            run_git(root, "remote", "add", "origin", secret_url)

            report = MODULE.collect(root, None, "origin")

            self.assertTrue(report["remote"]["configured"])
            self.assertNotIn(secret_url, str(report))


if __name__ == "__main__":
    unittest.main()
