from pathlib import Path
import unittest


SKILL = Path(__file__).parents[1] / "skills" / "domain-ontology" / "SKILL.md"


class DomainOntologyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_read_preflight_and_tenant_filter_are_required(self):
        self.assertIn("read it before\nquerying or ingesting", self.text)
        self.assertIn("Every bridge or aggregate query must carry an active-tenant predicate", self.text)
        self.assertIn("do not invent SQL or treat the failure as", self.text)

    def test_tenant_confirmation_is_never_inherited(self):
        self.assertIn("tenant는 문서마다 다시 확정한다", self.text)
        self.assertIn("Tenant confirmation is per document", self.text)

    def test_provenance_commit_uses_pathspec(self):
        self.assertIn('git commit -m "ingest: add <file>" -- tenants/', self.text)
        self.assertIn("pathspec-free `git commit`", self.text)


if __name__ == "__main__":
    unittest.main()
