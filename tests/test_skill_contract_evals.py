import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "eval_skill_contracts.py"
SPEC = importlib.util.spec_from_file_location("eval_skill_contracts", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class StaticSkillContractTests(unittest.TestCase):
    def write_suite(self, root, cases):
        suite = root / "suite.json"
        suite.write_text(json.dumps({"cases": cases}), encoding="utf-8")
        return suite

    def test_current_repository_contracts_pass(self):
        root = Path(__file__).parents[1]
        suite = root / "evals" / "static-contracts.json"
        if not suite.exists():
            self.skipTest("로컬 평가 suite는 공개 clone에 포함되지 않는다")
        self.assertEqual(MODULE.evaluate(root, suite), [])

    def test_cli_reports_a_missing_local_or_explicit_suite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = [
                (["--root", str(root)], "로컬 정적 계약 suite가 없다"),
                (["--root", str(root), "--suite", str(root / "missing.json")], "지정한 정적 계약 suite를 찾을 수 없다"),
            ]
            for argv, expected in cases:
                with self.subTest(argv=argv):
                    stderr = io.StringIO()
                    with redirect_stderr(stderr):
                        code = MODULE.main(argv)
                    self.assertNotEqual(0, code)
                    self.assertIn(expected, stderr.getvalue())

    def test_reports_missing_and_forbidden_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text("forbidden\n", encoding="utf-8")
            suite = self.write_suite(root, [{
                "id": "demo", "kind": "execution", "target": "SKILL.md",
                "all": ["required"], "none": ["forbidden"]
            }])
            errors = MODULE.evaluate(root, suite)
            self.assertTrue(any("missing required" in error for error in errors))
            self.assertTrue(any("found forbidden" in error for error in errors))

    def test_rejects_duplicate_ids_and_escaping_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = [
                {"id": "same", "kind": "positive", "target": "../outside", "all": ["x"]},
                {"id": "same", "kind": "positive", "target": "missing", "all": ["x"]},
            ]
            errors = MODULE.evaluate(root, self.write_suite(root, cases))
            self.assertTrue(any("escapes repository root" in error for error in errors))
            self.assertTrue(any("duplicate id" in error for error in errors))

    def test_rejects_empty_assertions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            errors = MODULE.evaluate(root, self.write_suite(root, [
                {"id": "empty", "kind": "negative", "target": "SKILL.md"}
            ]))
            self.assertTrue(any("at least one" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
