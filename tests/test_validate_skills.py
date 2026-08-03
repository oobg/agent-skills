import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateSkillsTests(unittest.TestCase):
    def make_skill(self, root, directory="demo", name="demo", link="references/rule.md"):
        skill = root / "skills" / directory
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: demo\n---\n\nSee `{link}`.\n",
            encoding="utf-8",
        )
        (skill / "README.md").write_text("rule.md\n", encoding="utf-8")
        (skill / "references" / "rule.md").write_text("ok\n", encoding="utf-8")

    def test_current_repository_is_valid(self):
        self.assertEqual(MODULE.validate(Path(__file__).parents[1]), [])

    def test_broken_reference_and_name_mismatch_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_skill(root, name="wrong", link="references/missing.md")
            errors = MODULE.validate(root)
            self.assertTrue(any("must match directory" in item for item in errors))
            self.assertTrue(any("broken local reference" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
