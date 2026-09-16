import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "check_public_eval_fixtures.py"
SPEC = importlib.util.spec_from_file_location("check_public_eval_fixtures", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def valid_static():
    return {
        "synthetic": True,
        "cases": [
            {"id": "positive", "kind": "positive", "target": "skills/a/SKILL.md", "all": ["rule"], "none": []},
            {"id": "negative", "kind": "negative", "target": "skills/b/SKILL.md", "all": ["boundary"], "none": []},
            {"id": "execution", "kind": "execution", "target": "skills/c/SKILL.md", "all": ["gate"], "none": []},
        ],
    }


def valid_trigger():
    return {
        "skill": "domain-ontology",
        "synthetic": True,
        "cases": [
            {
                "id": "recall",
                "expect": "recall",
                "request": "저장소의 기존 검토 규칙을 확인해줘.",
                "origin": "authored synthetic case",
            },
            {
                "id": "skip",
                "expect": "skip",
                "request": "확정된 항목을 정렬해줘.",
                "origin": "authored synthetic case",
            },
        ],
    }


class PublicEvalFixtureTests(unittest.TestCase):
    def make_root(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        fixtures = root / "tests" / "fixtures" / "public-evals"
        fixtures.mkdir(parents=True)
        self.write(fixtures / "static-contracts.json", valid_static())
        self.write(fixtures / "trigger-cases.json", valid_trigger())
        return temporary, root, fixtures

    def write(self, path, payload):
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def run_check(self, root):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = MODULE.main(["--root", str(root)])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_repository_public_fixtures_pass_preflight(self):
        code, stdout, stderr = self.run_check(ROOT)
        self.assertEqual(0, code)
        self.assertIn("passed", stdout)
        self.assertEqual("", stderr)

    def test_missing_fixture_is_an_input_error(self):
        temporary, root, fixtures = self.make_root()
        with temporary:
            (fixtures / "static-contracts.json").unlink()
            code, _stdout, stderr = self.run_check(root)
        self.assertEqual(2, code)
        self.assertIn("missing fixture", stderr)

    def test_invalid_json_is_an_input_error(self):
        temporary, root, fixtures = self.make_root()
        with temporary:
            (fixtures / "trigger-cases.json").write_text("{invalid", encoding="utf-8")
            code, _stdout, stderr = self.run_check(root)
        self.assertEqual(2, code)
        self.assertIn("invalid JSON", stderr)
        self.assertNotIn("{invalid", stderr)

    def test_non_object_top_level_is_rejected(self):
        temporary, root, fixtures = self.make_root()
        with temporary:
            self.write(fixtures / "static-contracts.json", [])
            code, _stdout, stderr = self.run_check(root)
        self.assertEqual(1, code)
        self.assertIn("top-level must be an object", stderr)

    def test_synthetic_marker_empty_cases_and_duplicate_ids_are_rejected(self):
        mutations = []
        missing = valid_static()
        missing.pop("synthetic")
        mutations.append((missing, "synthetic must be true"))
        false_marker = valid_static()
        false_marker["synthetic"] = False
        mutations.append((false_marker, "synthetic must be true"))
        empty = valid_static()
        empty["cases"] = []
        mutations.append((empty, "cases must be a non-empty list"))
        duplicate = valid_static()
        duplicate["cases"][1]["id"] = duplicate["cases"][0]["id"]
        mutations.append((duplicate, "duplicate id"))

        for payload, expected in mutations:
            with self.subTest(expected=expected):
                temporary, root, fixtures = self.make_root()
                with temporary:
                    self.write(fixtures / "static-contracts.json", payload)
                    code, _stdout, stderr = self.run_check(root)
                self.assertEqual(1, code)
                self.assertIn(expected, stderr)

    def test_trigger_observed_origin_and_cwd_are_rejected(self):
        temporary, root, fixtures = self.make_root()
        with temporary:
            payload = valid_trigger()
            payload["cases"][0]["origin"] = "observed synthetic source"
            payload["cases"][1]["cwd"] = "~/synthetic-repo"
            self.write(fixtures / "trigger-cases.json", payload)
            code, _stdout, stderr = self.run_check(root)
        self.assertEqual(1, code)
        self.assertIn("origin", stderr)
        self.assertIn("must not declare cwd", stderr)

    def test_static_target_escape_is_rejected(self):
        temporary, root, fixtures = self.make_root()
        with temporary:
            payload = valid_static()
            payload["cases"][0]["target"] = "skills/../outside.txt"
            self.write(fixtures / "static-contracts.json", payload)
            code, _stdout, stderr = self.run_check(root)
        self.assertEqual(1, code)
        self.assertIn("must stay under skills", stderr)

    def test_fixture_symlink_escape_is_rejected_before_reading(self):
        temporary, root, fixtures = self.make_root()
        outside = tempfile.TemporaryDirectory()
        with temporary, outside:
            outside_fixture = Path(outside.name) / "outside.json"
            self.write(outside_fixture, valid_static())
            local_fixture = fixtures / "static-contracts.json"
            local_fixture.unlink()
            local_fixture.symlink_to(outside_fixture)
            code, _stdout, stderr = self.run_check(root)
        self.assertEqual(2, code)
        self.assertIn("fixture path escapes root", stderr)

    def test_clear_private_value_patterns_are_rejected_without_echoing_values(self):
        private_values = [
            "contact@example.invalid",
            "/Users/synthetic-person/project",
            "/home/synthetic-person/project",
            "C:\\Users\\synthetic-person\\project",
            "-----BEGIN PRIVATE KEY-----",
        ]
        for private_value in private_values:
            with self.subTest(pattern=private_value.split("/")[0]):
                temporary, root, fixtures = self.make_root()
                with temporary:
                    payload = valid_trigger()
                    payload["cases"][0]["request"] = f"do not echo {private_value}"
                    self.write(fixtures / "trigger-cases.json", payload)
                    code, stdout, stderr = self.run_check(root)
                self.assertEqual(1, code)
                self.assertNotIn(private_value, stdout)
                self.assertNotIn(private_value, stderr)
                self.assertNotIn("do not echo", stdout + stderr)

    def test_generalized_path_examples_are_allowed(self):
        temporary, root, fixtures = self.make_root()
        with temporary:
            payload = valid_static()
            payload["cases"][0]["all"] = ["~/...", "<placeholder>"]
            self.write(fixtures / "static-contracts.json", payload)
            code, _stdout, stderr = self.run_check(root)
        self.assertEqual(0, code, stderr)

    def test_temporary_root_needs_no_private_evals_database_or_provider(self):
        temporary, root, _fixtures = self.make_root()
        with temporary:
            self.assertFalse((root / "evals").exists())
            self.assertFalse((root / ".ontology").exists())
            code, _stdout, stderr = self.run_check(root)
        self.assertEqual(0, code, stderr)


if __name__ == "__main__":
    unittest.main()
