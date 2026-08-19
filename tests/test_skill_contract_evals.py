import importlib.util
import json
import tempfile
import unittest
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
        self.assertEqual(MODULE.evaluate(root, root / "evals" / "static-contracts.json"), [])

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
