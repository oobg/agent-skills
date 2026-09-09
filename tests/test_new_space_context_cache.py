import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "skills" / "new-space" / "scripts" / "context_cache.py"


class NewSpaceContextCacheTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True)
        (self.repo / "AGENTS.md").write_text("# Synthetic policy\n", encoding="utf-8")
        self.stub = self.root / "orca-stub.md"
        self.stub.write_text("synthetic stub\n", encoding="utf-8")
        self.contract = self.root / "contract.md"
        self.contract.write_text("synthetic recipe\n", encoding="utf-8")
        self.recipe = self.root / "reviewed-recipe.md"
        self.recipe.write_text("Use only the reviewed synthetic command schema.\n", encoding="utf-8")
        self.count = self.root / "fetch-count"
        self.fail_marker = self.root / "fail-fetch"
        self.orca = self.root / "fake-orca"
        self.write_orca("1.0.0")
        self.env = {**os.environ, "XDG_STATE_HOME": str(self.root / "state"),
                    "XDG_CACHE_HOME": str(self.root / "cache"),
                    "FETCH_COUNT": str(self.count), "FAIL_MARKER": str(self.fail_marker)}

    def tearDown(self):
        self.temp.cleanup()

    def write_orca(self, version, fail_fetch=False):
        fetch = (
            '[ -f "$FAIL_MARKER" ] && exit 9; '
            'n=0; [ ! -f "$FETCH_COUNT" ] || n=$(cat "$FETCH_COUNT"); '
            'n=$((n + 1)); printf "%s" "$n" > "$FETCH_COUNT"; '
            'printf \'%s\\n\' \'{"name":"orca-cli","full":true,"markdown":"synthetic full guide"}\''
        )
        self.orca.write_text(
            "#!/bin/sh\n"
            f"if [ \"$1\" = \"--version\" ]; then printf '%s\\n' '{version}'; exit 0; fi\n"
            f"if [ \"$1\" = \"skills\" ]; then {fetch}; exit 0; fi\n"
            "exit 8\n",
            encoding="utf-8",
        )
        self.orca.chmod(0o755)

    def run_script(self, *args, check=True):
        return subprocess.run([sys.executable, str(SCRIPT), *args], check=check, text=True,
                              capture_output=True, env=self.env)

    def guide_args(self):
        return ("orca-guide", "--orca-executable", str(self.orca), "--stub-file", str(self.stub),
                "--contract-file", str(self.contract))

    def fetches(self):
        return int(self.count.read_text()) if self.count.exists() else 0

    def prepare_guide(self):
        fetched = self.run_script(*self.guide_args(), check=False)
        self.assertEqual(fetched.returncode, 2)
        payload = json.loads(fetched.stdout)
        self.run_script("orca-remember", "--orca-executable", str(self.orca),
                        "--stub-file", str(self.stub), "--contract-file", str(self.contract),
                        "--guide-sha256", payload["guide_sha256"],
                        "--recipe-file", str(self.recipe))
        return payload

    def test_guide_hit_does_not_fetch_source_again(self):
        first = self.prepare_guide()
        second = json.loads(self.run_script(*self.guide_args()).stdout)
        self.assertEqual(first["status"], "needs-review")
        self.assertEqual(second["status"], "hit")
        self.assertEqual(self.fetches(), 1)
        self.assertNotIn("guide_source", second)

    def test_guide_invalidates_for_executable_stub_contract_and_refresh(self):
        self.prepare_guide()
        self.write_orca("1.0.1")
        self.assertEqual(json.loads(self.run_script(*self.guide_args(), check=False).stdout)["status"],
                         "needs-review")
        self.stub.write_text("changed stub\n", encoding="utf-8")
        self.assertEqual(json.loads(self.run_script(*self.guide_args(), check=False).stdout)["status"],
                         "needs-review")
        self.contract.write_text("changed recipe\n", encoding="utf-8")
        self.assertEqual(json.loads(self.run_script(*self.guide_args(), check=False).stdout)["status"],
                         "needs-review")
        refreshed = self.run_script(*self.guide_args(), "--refresh", check=False)
        self.assertEqual(json.loads(refreshed.stdout)["status"], "needs-review")
        self.assertEqual(self.fetches(), 5)

    def test_failed_refresh_does_not_replace_last_valid_cache(self):
        self.prepare_guide()
        self.fail_marker.write_text("fail\n", encoding="utf-8")
        failed = self.run_script(*self.guide_args(), "--refresh", check=False)
        self.assertEqual(failed.returncode, 1)
        self.fail_marker.unlink()
        retried = self.run_script(*self.guide_args(), check=False)
        self.assertEqual(json.loads(retried.stdout)["status"], "needs-review")
        self.assertEqual(self.fetches(), 2)

    def test_remember_rejects_recipe_for_a_different_guide_hash(self):
        self.run_script(*self.guide_args(), check=False)
        result = self.run_script("orca-remember", "--orca-executable", str(self.orca),
                                 "--stub-file", str(self.stub),
                                 "--contract-file", str(self.contract),
                                 "--guide-sha256", "0" * 64,
                                 "--recipe-file", str(self.recipe), check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("guide hash changed", json.loads(result.stderr)["error"])

    def test_project_memory_is_shared_by_git_common_dir_and_stales_on_policy_change(self):
        preferences = json.dumps({"base_policy": "use the remote default"})
        stored = self.run_script("project-set", "--repo", str(self.repo),
                                 "--preferences-json", preferences)
        self.assertEqual(json.loads(stored.stdout)["status"], "stored")
        linked = self.root / "linked"
        subprocess.run(["git", "-C", str(self.repo), "worktree", "add", "-q", "-b", "topic",
                        str(linked)], check=True)
        (linked / "AGENTS.md").write_text("# Synthetic policy\n", encoding="utf-8")
        hit = self.run_script("project-get", "--repo", str(linked))
        self.assertEqual(json.loads(hit.stdout)["status"], "hit")
        (linked / "AGENTS.md").write_text("# Changed synthetic policy\n", encoding="utf-8")
        stale = self.run_script("project-get", "--repo", str(linked), check=False)
        self.assertEqual(stale.returncode, 3)
        self.assertEqual(json.loads(stale.stdout)["status"], "stale")

    def test_project_memory_rejects_runtime_authority_and_ephemeral_ids(self):
        for field in ("approval_policy", "sandbox_mode", "worktree_id", "terminal_handle"):
            result = self.run_script("project-set", "--repo", str(self.repo),
                                     "--preferences-json", json.dumps({field: "synthetic"}), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot be stored", json.loads(result.stderr)["error"])

    def test_missing_policy_is_supported_and_malformed_memory_is_invalid(self):
        (self.repo / "AGENTS.md").unlink()
        stored = json.loads(self.run_script(
            "project-set", "--repo", str(self.repo),
            "--preferences-json", json.dumps({"handoff_preference": "ask once"}),
        ).stdout)
        self.assertEqual(json.loads(self.run_script(
            "project-get", "--repo", str(self.repo)).stdout)["status"], "hit")
        Path(stored["memory_path"]).write_text("[]\n", encoding="utf-8")
        invalid = self.run_script("project-get", "--repo", str(self.repo), check=False)
        self.assertEqual(invalid.returncode, 4)
        self.assertEqual(json.loads(invalid.stdout)["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
