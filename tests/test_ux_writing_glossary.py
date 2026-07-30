import importlib.util
from pathlib import Path
import unittest


SCRIPT = (
    Path(__file__).parents[1]
    / "skills"
    / "ux-writing"
    / "scripts"
    / "glossary_check.py"
)
SPEC = importlib.util.spec_from_file_location("glossary_check", SCRIPT)
glossary_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(glossary_check)


class GlossaryScopeTests(unittest.TestCase):
    def test_global_and_only_deepest_project_scope_apply(self):
        global_pairs = [("login", "sign in")]
        project_pairs = [
            ("parent", "/workspace/product", "user", "member"),
            ("child", "/workspace/product/admin", "user", "operator"),
            ("child", "/workspace/product/admin", "settings", "configuration"),
        ]

        pairs, matched = glossary_check.resolve_pairs(
            "/workspace/product/admin/copy.md", global_pairs, project_pairs
        )

        self.assertEqual(
            pairs,
            [
                ("login", "sign in"),
                ("user", "operator"),
                ("settings", "configuration"),
            ],
        )
        self.assertEqual(matched, ["child"])

    def test_parent_scope_applies_when_no_deeper_scope_matches(self):
        pairs, matched = glossary_check.resolve_pairs(
            "/workspace/product/readme.md",
            [],
            [
                ("parent", "/workspace/product", "user", "member"),
                ("child", "/workspace/product/admin", "user", "operator"),
            ],
        )

        self.assertEqual(pairs, [("user", "member")])
        self.assertEqual(matched, ["parent"])


if __name__ == "__main__":
    unittest.main()
