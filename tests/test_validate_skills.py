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

    def test_missing_skills_directory_is_reported_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = MODULE.validate(Path(tmp))
            self.assertEqual(1, len(errors))
            self.assertIn("missing skills directory", errors[0])

    def test_missing_yaml_dependency_fails_closed_with_install_hint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_skill(root)
            original = MODULE.yaml
            MODULE.yaml = None
            try:
                errors = MODULE.validate(root)
            finally:
                MODULE.yaml = original
            self.assertTrue(any("requirements-dev.txt" in item for item in errors))

    def test_invalid_discovery_name_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_skill(root, directory="Bad_Name", name="Bad_Name")
            errors = MODULE.validate(root)
            self.assertTrue(any("invalid skill name" in item for item in errors))

    def test_discovery_name_allows_64_characters_and_rejects_65(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_skill(root, directory="a" * 64, name="a" * 64)
            self.make_skill(root, directory="b" * 65, name="b" * 65)
            errors = MODULE.validate(root)
            self.assertFalse(any("a" * 64 in item and "invalid skill name" in item for item in errors))
            self.assertTrue(any("b" * 65 in item and "invalid skill name" in item for item in errors))

    def test_frontmatter_uses_yaml_and_requires_string_fields(self):
        variants = {
            "description: [unterminated": "invalid YAML frontmatter",
            "- name\n- demo": "top-level mapping",
            "name: 42\ndescription: demo": "name must be a string",
            "name: demo\ndescription:\n  nested: value": "description must be a string",
            "name: demo\ndescription: '   '": "missing description",
        }
        for body, expected in variants.items():
            with self.subTest(body=body), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.make_skill(root)
                skill_file = root / "skills" / "demo" / "SKILL.md"
                skill_file.write_text(f"---\n{body}\n---\n", encoding="utf-8")
                self.assertTrue(any(expected in item for item in MODULE.validate(root)))

    def test_valid_yaml_scalar_styles_and_description_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_skill(root)
            skill_file = root / "skills" / "demo" / "SKILL.md"
            for description in ('"quoted value"', "plain value # inline comment", ">\n  folded value"):
                with self.subTest(description=description):
                    skill_file.write_text(f"---\nname: demo\ndescription: {description}\n---\n", encoding="utf-8")
                    self.assertFalse(any("description" in item for item in MODULE.validate(root)))
            skill_file.write_text(
                f"---\nname: demo\ndescription: {'x' * 1025}\n---\n", encoding="utf-8"
            )
            self.assertTrue(any("exceeds 1024" in item for item in MODULE.validate(root)))

    def test_plain_routed_reference_and_duplicate_basenames_are_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_skill(root)
            skill = root / "skills" / "demo"
            (skill / "SKILL.md").write_text(
                "---\nname: demo\ndescription: demo\n---\n\nRead references/missing.md.\n",
                encoding="utf-8",
            )
            for folder in ("a", "b"):
                (skill / "references" / folder).mkdir()
                (skill / "references" / folder / "config.json").write_text("{}\n", encoding="utf-8")
            (skill / "README.md").write_text("rule.md\nconfig.json\n", encoding="utf-8")
            errors = MODULE.validate(root)
            self.assertTrue(any("references/missing.md" in item for item in errors))
            self.assertTrue(any("references/a/config.json" in item for item in errors))
            self.assertTrue(any("references/b/config.json" in item for item in errors))

    def test_plain_routed_scanner_ignores_urls_absolute_paths_and_placeholders(self):
        text = "https://example.test/references/remote.md /tmp/references/local.md references/<file>.md"
        with tempfile.TemporaryDirectory() as tmp:
            skill_file = Path(tmp) / "SKILL.md"
            skill_file.write_text(text, encoding="utf-8")
            self.assertEqual([], list(MODULE.local_targets(skill_file)))


if __name__ == "__main__":
    unittest.main()
