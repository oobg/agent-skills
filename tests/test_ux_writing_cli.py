import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPTS = ROOT / "skills" / "ux-writing" / "scripts"


def load_module(name):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UxWritingCliTests(unittest.TestCase):
    def run_script(self, name, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / f"{name}.py"), *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_checkers_reject_malformed_arguments(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "copy.md"
            target.write_text("저장해요", encoding="utf-8")
            for name in ("glossary_check", "register_check"):
                self.assertEqual(self.run_script(name, target, "--as").returncode, 2)
                self.assertEqual(self.run_script(name, target, "one", "two").returncode, 2)

    def test_all_checkers_report_missing_target_without_traceback(self):
        missing = ROOT / "does-not-exist.md"
        for name in ("ai_lint", "glossary_check", "register_check"):
            result = self.run_script(name, missing)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_ai_lint_rejects_invalid_pattern_schema(self):
        module = load_module("ai_lint")
        original = module.PATTERNS_PATH
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "patterns.json"
            path.write_text(json.dumps({
                "version": "1.0",
                "patterns": [{
                    "id": "bad", "label": "bad", "regex": "x",
                    "layer": "harrd", "status": "verified"
                }],
            }), encoding="utf-8")
            module.PATTERNS_PATH = str(path)
            try:
                with self.assertRaisesRegex(ValueError, "layer"):
                    module.load_patterns()
            finally:
                module.PATTERNS_PATH = original


if __name__ == "__main__":
    unittest.main()
