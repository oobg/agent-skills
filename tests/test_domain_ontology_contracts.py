from pathlib import Path
import unittest


SKILL = Path(__file__).parents[1] / "skills" / "domain-ontology" / "SKILL.md"


class DomainOntologyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_read_preflight_and_tenant_filter_are_required(self):
        self.assertIn("read it before\nquerying or ingesting", self.text)
        # The step-by-step SQL and leak rules live in recall.md; the skill must delegate
        # to it and must keep the scope predicate and the no-fabrication rule visible here.
        self.assertIn("절차의 정본은 `~/.ontology/docs/recall.md`다", self.text)
        self.assertIn("스코프 누수 금지", self.text)
        self.assertIn("SQL을 지어내지 말고", self.text)
        self.assertIn("조회도 답변도 활성 스코프 안에 머문다", self.text)

    def test_tenant_confirmation_is_never_inherited(self):
        self.assertIn("tenant는 문서마다 다시 확정한다", self.text)
        self.assertIn("Tenant confirmation is per document", self.text)

    def test_provenance_commit_uses_pathspec(self):
        self.assertIn('git commit -m "ingest: add <file>" -- tenants/', self.text)
        self.assertIn("pathspec-free `git commit`", self.text)


if __name__ == "__main__":
    unittest.main()
