import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "skills" / "new-space" / "scripts" / "new_space.py"


def run(*args, cwd=None, check=True, env=None):
    return subprocess.run(args, cwd=cwd, check=check, text=True, capture_output=True, env=env)


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

    def script(self, *args, check=True, env=None):
        return run(sys.executable, str(SCRIPT), *args, check=check, env=env)

    def linked_worktree(self):
        linked = Path(self.temp.name) / "linked"
        run("git", "worktree", "add", "-qb", "dev-feat-search-filter", str(linked), "main", cwd=self.repo)
        return linked

    def fake_orca(self, worktree, branch="feat/search-filter", head=None, exit_code=0):
        executable = Path(self.temp.name) / "fake-orca"
        resolved_head = head or run("git", "rev-parse", "HEAD", cwd=worktree).stdout.strip()
        worktree_id = f"synthetic-repo::{worktree}"
        executable.write_text(
            "#!/bin/sh\n"
            + (f"exit {exit_code}\n" if exit_code else
               "printf '%s\\n' '{\"ok\":true,\"result\":{\"worktree\":{\"id\":\""
               + worktree_id + "\",\"path\":\"" + str(worktree) + "\",\"branch\":\"refs/heads/"
               + branch + "\",\"head\":\"" + resolved_head + "\",\"git\":{\"branch\":\"refs/heads/"
               + branch + "\",\"head\":\"" + resolved_head + "\"}}}}'\n"),
            encoding="utf-8",
        )
        executable.chmod(0o755)
        return executable

    def fake_folder_orca(
        self,
        worktree,
        *,
        repo_id="folder-repo",
        repo_response_id=None,
        repo_path=None,
        repo_kind="folder",
        worktree_id=None,
        worktree_repo_id=None,
        path=None,
        host_id="local",
        include_host_id=True,
        is_main=False,
        branch="",
        head="",
        git_branch="",
        git_head="",
        include_git=True,
        repo_mode="ok",
        worktree_mode="ok",
    ):
        executable = Path(self.temp.name) / "fake-folder-orca"
        expected_id = f"{repo_id}::{worktree}::workspace:synthetic"
        repo_payload = {
            "ok": True,
            "result": {
                "repo": {
                    "id": repo_response_id if repo_response_id is not None else repo_id,
                    "path": str(repo_path if repo_path is not None else worktree),
                    "kind": repo_kind,
                }
            },
        }
        worktree_payload = {
            "ok": True,
            "result": {
                "worktree": {
                    "id": worktree_id if worktree_id is not None else expected_id,
                    "repoId": worktree_repo_id if worktree_repo_id is not None else repo_id,
                    "path": str(path if path is not None else worktree),
                    **({"hostId": host_id} if include_host_id else {}),
                    "isMainWorktree": is_main,
                    "branch": branch,
                    "head": head,
                    **({"git": {"branch": git_branch, "head": git_head}} if include_git else {}),
                }
            },
        }
        def response(mode, payload):
            if mode == "nonzero":
                return "exit 7"
            if mode == "malformed":
                return "printf '%s\\n' 'not-json'"
            if mode == "ok-false":
                payload = {"ok": False, "result": payload.get("result")}
            if mode == "missing-result":
                payload = {"ok": True}
            if mode == "missing-object":
                payload = {"ok": True, "result": {}}
            return "printf '%s\\n' " + repr(json.dumps(payload, separators=(",", ":")))

        executable.write_text(
            "#!/bin/sh\n"
            "if [ \"$1 $2\" = \"repo show\" ]; then\n  "
            + response(repo_mode, repo_payload)
            + "\nelif [ \"$1 $2\" = \"worktree show\" ]; then\n  "
            + response(worktree_mode, worktree_payload)
            + "\nelse\n  exit 64\nfi\n",
            encoding="utf-8",
        )
        executable.chmod(0o755)
        return executable, repo_id, expected_id

    def workspace_verify_args(self, folder, executable, repo_id, worktree_id, *extra):
        return (
            "workspace-verify",
            "--worktree", str(folder),
            "--repo-id", repo_id,
            "--worktree-id", worktree_id,
            "--orca-executable", str(executable),
            *extra,
        )

    def finalize_args(self, worktree, base_sha, executable):
        return (
            "finalize",
            "--worktree", str(worktree),
            "--worktree-id", f"synthetic-repo::{worktree}",
            "--created-branch", "dev-feat-search-filter",
            "--expected-branch", "feat/search-filter",
            "--base-sha", base_sha,
            "--orca-executable", str(executable),
        )

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

    def test_git_only_command_rejects_non_git_directory(self):
        folder = Path(self.temp.name) / "folder-project"
        folder.mkdir()
        result = self.script(
            "preflight", "--repo", str(folder), "--branch", "feat/example", "--base", "main",
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Orca folder workspace flow", json.loads(result.stderr)["error"])

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

    def test_finalize_dry_run_requires_repair_without_mutation(self):
        base_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        linked = self.linked_worktree()
        result = self.script(*self.finalize_args(linked, base_sha, self.fake_orca(linked)), check=False)
        self.assertEqual(result.returncode, 4)
        self.assertEqual(run("git", "branch", "--show-current", cwd=linked).stdout.strip(),
                         "dev-feat-search-filter")

    def test_finalize_apply_repairs_and_verifies_orca(self):
        base_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        linked = self.linked_worktree()
        result = self.script(
            *self.finalize_args(linked, base_sha, self.fake_orca(linked)), "--apply", check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertTrue(payload["branch_repaired"])
        self.assertEqual(run("git", "branch", "--show-current", cwd=linked).stdout.strip(),
                         "feat/search-filter")

    def test_finalize_refuses_dirty_or_colliding_worktree(self):
        base_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        linked = self.linked_worktree()
        (linked / "draft.txt").write_text("dirty\n", encoding="utf-8")
        dirty = self.script(*self.finalize_args(linked, base_sha, self.fake_orca(linked)), "--apply", check=False)
        self.assertEqual(dirty.returncode, 1)
        (linked / "draft.txt").unlink()
        run("git", "branch", "feat/search-filter", cwd=self.repo)
        collision = self.script(*self.finalize_args(linked, base_sha, self.fake_orca(linked)), "--apply", check=False)
        self.assertEqual(collision.returncode, 1)
        self.assertEqual(run("git", "branch", "--show-current", cwd=linked).stdout.strip(),
                         "dev-feat-search-filter")

    def test_finalize_refuses_base_mismatch(self):
        base_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        linked = self.linked_worktree()
        (linked / "change.txt").write_text("fixture\n", encoding="utf-8")
        run("git", "add", "change.txt", cwd=linked)
        run("git", "commit", "-qm", "change", cwd=linked)
        result = self.script(*self.finalize_args(linked, base_sha, self.fake_orca(linked)), "--apply", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(run("git", "branch", "--show-current", cwd=linked).stdout.strip(),
                         "dev-feat-search-filter")

    def test_finalize_blocks_success_when_orca_readback_fails(self):
        base_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        linked = self.linked_worktree()
        result = self.script(
            *self.finalize_args(linked, base_sha, self.fake_orca(linked, exit_code=7)), "--apply", check=False
        )
        self.assertEqual(result.returncode, 3)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["branch_repaired"])
        self.assertEqual(run("git", "branch", "--show-current", cwd=linked).stdout.strip(),
                         "feat/search-filter")

    def test_workspace_verify_accepts_folder_readback_without_invoking_git(self):
        folder = Path(self.temp.name) / "folder-workspace"
        folder.mkdir()
        executable, repo_id, worktree_id = self.fake_folder_orca(folder)
        bin_dir = Path(self.temp.name) / "bin"
        bin_dir.mkdir()
        marker = Path(self.temp.name) / "git-was-called"
        fake_git = bin_dir / "git"
        fake_git.write_text(f"#!/bin/sh\ntouch {marker}\nexit 99\n", encoding="utf-8")
        fake_git.chmod(0o755)
        env = dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")

        result = self.script(
            *self.workspace_verify_args(folder, executable, repo_id, worktree_id), env=env
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["workspace_kind"], "folder")
        self.assertEqual(payload["repo_id"], repo_id)
        self.assertEqual(payload["worktree_id"], worktree_id)
        self.assertEqual(payload["path"], str(folder.resolve()))
        self.assertFalse(marker.exists())

    def test_workspace_verify_rejects_different_id_or_path(self):
        folder = Path(self.temp.name) / "folder-workspace"
        folder.mkdir()
        cases = (
            {"worktree_id": "different-id", "message": "different workspace id"},
            {"path": Path(self.temp.name) / "different-path", "message": "different workspace path"},
        )
        for case in cases:
            with self.subTest(case=case["message"]):
                executable, repo_id, expected_id = self.fake_folder_orca(
                    folder,
                    worktree_id=case.get("worktree_id"),
                    path=case.get("path"),
                )
                result = self.script(
                    *self.workspace_verify_args(folder, executable, repo_id, expected_id), check=False
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn(case["message"], json.loads(result.stderr)["error"])

    def test_workspace_verify_rejects_git_state_or_main_workspace(self):
        folder = Path(self.temp.name) / "folder-workspace"
        folder.mkdir()
        cases = (
            {"branch": "feat/not-folder"},
            {"head": "0123456789abcdef"},
            {"git_branch": "refs/heads/main"},
            {"git_head": "fedcba9876543210"},
            {"include_git": False},
            {"is_main": True},
        )
        for case in cases:
            with self.subTest(case=case):
                executable, repo_id, worktree_id = self.fake_folder_orca(folder, **case)
                result = self.script(
                    *self.workspace_verify_args(folder, executable, repo_id, worktree_id), check=False
                )
                self.assertEqual(result.returncode, 1)
                self.assertFalse(json.loads(result.stderr)["ok"])

    def test_workspace_verify_rejects_missing_local_directory(self):
        folder = Path(self.temp.name) / "missing-folder-workspace"
        executable, repo_id, worktree_id = self.fake_folder_orca(folder)
        result = self.script(
            *self.workspace_verify_args(folder, executable, repo_id, worktree_id), check=False
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("not an existing directory", json.loads(result.stderr)["error"])

    def test_workspace_verify_remote_path_uses_matching_orca_readback(self):
        folder = Path("/paired-host/synthetic-folder")
        executable, repo_id, worktree_id = self.fake_folder_orca(
            folder, host_id="ssh:synthetic-host"
        )
        result = self.script(
            *self.workspace_verify_args(
                folder, executable, repo_id, worktree_id, "--path-host", "remote"
            )
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["path_host"], "remote")
        self.assertEqual(payload["host_id"], "ssh:synthetic-host")

    def test_workspace_verify_remote_path_rejects_local_or_invalid_host_id(self):
        folder = Path("/paired-host/synthetic-folder")
        cases = (
            {"host_id": "local"},
            {"host_id": ""},
            {"host_id": None},
            {"host_id": 42},
            {"include_host_id": False},
        )
        for options in cases:
            with self.subTest(options=options):
                executable, repo_id, worktree_id = self.fake_folder_orca(folder, **options)
                result = self.script(
                    *self.workspace_verify_args(
                        folder, executable, repo_id, worktree_id, "--path-host", "remote"
                    ),
                    check=False,
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("non-local Orca worktree hostId", json.loads(result.stderr)["error"])

    def test_workspace_verify_rejects_repo_or_workspace_identity_mismatch(self):
        folder = Path(self.temp.name) / "folder-workspace"
        folder.mkdir()
        cases = (
            ({"repo_response_id": "different-repo"}, "different repo id"),
            ({"repo_kind": "git"}, "not kind: folder"),
            ({"repo_path": Path(self.temp.name) / "different-repo-path"}, "different repo path"),
            ({"worktree_repo_id": "different-repo"}, "repoId does not match"),
        )
        for options, message in cases:
            with self.subTest(message=message):
                executable, repo_id, worktree_id = self.fake_folder_orca(folder, **options)
                result = self.script(
                    *self.workspace_verify_args(folder, executable, repo_id, worktree_id), check=False
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn(message, json.loads(result.stderr)["error"])

    def test_workspace_verify_rejects_orca_lookup_failures(self):
        folder = Path(self.temp.name) / "folder-workspace"
        folder.mkdir()
        for lookup in ("repo", "worktree"):
            for mode in (
                "nonzero",
                "malformed",
                "ok-false",
                "missing-result",
                "missing-object",
            ):
                with self.subTest(lookup=lookup, mode=mode):
                    executable, repo_id, worktree_id = self.fake_folder_orca(
                        folder, **{f"{lookup}_mode": mode}
                    )
                    result = self.script(
                        *self.workspace_verify_args(folder, executable, repo_id, worktree_id),
                        check=False,
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertFalse(json.loads(result.stderr)["ok"])

    def test_new_space_docs_do_not_offer_plain_git_fallback(self):
        documents = (
            ROOT / "skills" / "new-space" / "SKILL.md",
            ROOT / "skills" / "new-space" / "README.md",
            ROOT / "skills" / "new-space" / "references" / "orca.md",
        )
        for document in documents:
            with self.subTest(document=document.name):
                content = document.read_text(encoding="utf-8").lower()
                self.assertNotIn("plain git fallback", content)
                self.assertNotIn("fallback을 선택", content)


if __name__ == "__main__":
    unittest.main()
