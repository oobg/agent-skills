"""Each skill must work without the ontology and must gate its boost module the same way."""

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
BOOST_SKILLS = (
    "conventional-commits",
    "gpt-image-gen",
    "question-design",
    "ux-writing",
)


def boost_path(skill: str) -> Path:
    return ROOT / "skills" / skill / "references" / "ontology-boost.md"


def skill_path(skill: str) -> Path:
    return ROOT / "skills" / skill / "SKILL.md"


class OntologyBoostContractTests(unittest.TestCase):
    def test_every_boost_module_exists(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                self.assertTrue(boost_path(skill).is_file())

    def test_boost_is_optional_and_gated_on_the_database(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = boost_path(skill).read_text(encoding="utf-8")
                self.assertIn("~/.ontology/ontology.db", text)
                self.assertIn("있을 때만 편다", text)
                self.assertIn("없으면 이 파일을 무시하고", text)

    def test_boost_delegates_the_recall_procedure(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = boost_path(skill).read_text(encoding="utf-8")
                self.assertIn("~/.ontology/docs/recall.md", text)
                self.assertIn("여기 복제하", text)

    def test_boost_carries_the_point_in_time_guard(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = boost_path(skill).read_text(encoding="utf-8")
                self.assertIn(
                    "회수는 무엇을 봐야 하는가를 알려주는 것이고, 지금 어떤 상태인가의 증거가 아니다",
                    text,
                )

    def test_boost_keeps_scope_inside_the_active_tenants(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = boost_path(skill).read_text(encoding="utf-8")
                self.assertIn("스코프 밖 tenant", text)

    def test_skill_entrypoint_routes_the_boost_conditionally(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = skill_path(skill).read_text(encoding="utf-8")
                self.assertIn("references/ontology-boost.md", text)
                self.assertIn("~/.ontology/ontology.db", text)
                self.assertIn("온톨로지가 없어도", text)

    def test_domain_ontology_owns_the_shared_consumption_rules(self):
        text = (ROOT / "skills" / "domain-ontology" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "회수는 무엇을 봐야 하는가를 알려주는 것이고, 지금 어떤 상태인가의 증거가 아니다",
            text,
        )
        self.assertIn("조치 사실도 claim으로 남긴다", text)
        self.assertIn("게이트·판정 기준·실행 권한을 넓히지 않는다", text)

    def test_boost_does_not_widen_write_or_execution_permissions(self):
        commits = boost_path("conventional-commits").read_text(encoding="utf-8")
        self.assertIn("메시지 작성 요청만으로 `git commit`·`push`를 실행하지 않는다", commits)
        self.assertIn("이 스킬은 온톨로지에 쓰지 않는다", commits)

        image = boost_path("gpt-image-gen").read_text(encoding="utf-8")
        self.assertIn("비용 게이트는 이 모듈이 열려 있어도 그대로다", image)

        writing = boost_path("ux-writing").read_text(encoding="utf-8")
        self.assertIn("HARD 0", writing)
        self.assertIn("`ai_lint`를 대체하지 않는다", writing)

        question = boost_path("question-design").read_text(encoding="utf-8")
        self.assertIn("결과 경로를 바꾸는 모호성만 먼저 질문한다", question)
        self.assertIn("회수 결과는 리뷰의 **입력**이지 판정이 아니다", question)

    def test_every_boost_declares_what_it_leaves_unchanged(self):
        # Asserting only on required strings catches deletion but not contradiction.
        # Each module must carry the section that names its own untouched gates.
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                self.assertIn("## 바뀌지 않는 것", boost_path(skill).read_text(encoding="utf-8"))

    def test_no_boost_grants_an_exemption_from_its_skill_gates(self):
        # "없이도" is how a permission-widening sentence reads in this codebase:
        # "사용자 지시 없이도 실행", "동의 없이도 적재". A gate that is genuinely
        # unchanged is written as a prohibition, which does not match this form.
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = boost_path(skill).read_text(encoding="utf-8")
                self.assertNotIn("없이도", text)
                self.assertNotIn("게이트를 건너뛴다", text)
                self.assertNotIn("생략해도 된다", text)

    def test_boost_closes_itself_when_the_recall_procedure_is_missing(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                # The sentence wraps differently per file; compare on collapsed whitespace.
                text = " ".join(boost_path(skill).read_text(encoding="utf-8").split())
                self.assertIn("`recall.md`가 없으면 SQL을 지어내지 말고 이 모듈을 닫는다", text)

    def test_domain_ontology_keeps_its_consent_guard(self):
        text = (ROOT / "skills" / "domain-ontology" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Ask before ingesting", text)
        self.assertIn("Never silent", text)
        self.assertIn("tenant는 문서마다 다시 확정한다", text)
        self.assertNotIn("동의 없이도", text)


if __name__ == "__main__":
    unittest.main()
