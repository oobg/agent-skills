from pathlib import Path
import re
import unittest


SKILL = Path(__file__).parents[1] / "skills" / "domain-ontology" / "SKILL.md"


class DomainOntologyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_recall_is_the_default_when_applicability_is_unclear(self):
        # The trigger must be decidable before recall. Gating on "would the answer
        # change" is only knowable after reading, so it collapses into never firing.
        self.assertIn("적용 여부가 불확실하면 조회가 기본값이다", self.text)
        self.assertIn("주제 신호가 하나라도 있는가", self.text)
        self.assertIn("애매한 것은 차단 목록에 넣지 않는다", self.text)
        self.assertNotIn("could materially change the answer", self.text)

    def test_code_work_is_not_by_itself_an_exclusion(self):
        self.assertIn("코드·저장소 작업이라는 사실 자체는 제외 사유가 아니다", self.text)
        self.assertIn("스킬·프롬프트 설계", self.text)

    def test_local_files_do_not_substitute_for_recall(self):
        # Removing an exclusion is insufficient if the agent still treats repository
        # files as a substitute for recall.
        self.assertIn("저장소 안에 답이 있어도 조회를 대신하지 못한다", self.text)
        self.assertIn("답에 왜가 빠져 있다는 신호다", self.text)

    def test_skipping_recall_must_be_declared(self):
        # A silent skip is indistinguishable from the skill never firing, which is
        # how under-triggering stays invisible.
        self.assertIn("건너뛰기로 했으면 그 판단을 한 줄로 밝힌다", self.text)

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

    def test_all_authoritative_tenants_are_routable_for_ingestion(self):
        expected = {"company", "personal", "shared", "novel", "blog"}

        tenant_row = next(
            line for line in self.text.splitlines() if line.startswith("| tenant key |")
        )
        table_tenants = set(re.findall(r"`([a-z]+)`", tenant_row))

        load_command = re.search(
            r"docs\.py load <json> --tenant <([^>]+)>", self.text
        )
        self.assertIsNotNone(load_command)
        cli_tenants = set(load_command.group(1).split("|"))

        self.assertEqual(expected, table_tenants)
        self.assertEqual(expected, cli_tenants)

    def test_creative_tenants_keep_scope_and_source_boundaries(self):
        contracts = {
            "novel": ("novel + shared", "tenants/novel/sources/works/<work-slug>/<file>"),
            "blog": ("blog + shared", "tenants/blog/sources/series/<series-slug>/<file>"),
        }
        for tenant, (scope, source_path) in contracts.items():
            with self.subTest(tenant=tenant):
                self.assertIn(scope, self.text)
                self.assertIn(source_path, self.text)


if __name__ == "__main__":
    unittest.main()
