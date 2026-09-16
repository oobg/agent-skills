"""Each skill must work without the ontology and must gate its boost module the same way."""

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
BOOST_PATHS = tuple(sorted((ROOT / "skills").glob("*/references/ontology-boost.md")))
BOOST_SKILLS = tuple(path.parents[1].name for path in BOOST_PATHS)


def boost_path(skill: str) -> Path:
    return ROOT / "skills" / skill / "references" / "ontology-boost.md"


def skill_path(skill: str) -> Path:
    return ROOT / "skills" / skill / "SKILL.md"


class OntologyBoostContractTests(unittest.TestCase):
    def test_boost_modules_are_discovered_deterministically(self):
        self.assertTrue(BOOST_PATHS)
        self.assertEqual(BOOST_PATHS, tuple(sorted(BOOST_PATHS)))
        self.assertEqual(len(BOOST_PATHS), len(set(BOOST_SKILLS)))

    def test_boost_is_optional_and_gated_on_the_database(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = boost_path(skill).read_text(encoding="utf-8")
                self.assertIn("~/.ontology/ontology.db", text)
                self.assertIn("때만", text)
                self.assertIn("없으면", text)

    def test_boost_delegates_the_recall_procedure(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = boost_path(skill).read_text(encoding="utf-8")
                self.assertIn("~/.ontology/docs/recall.md", text)
                self.assertIn("SQL", text)
                self.assertIn("지어내지", text)

    def test_boost_carries_the_point_in_time_guard(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = " ".join(boost_path(skill).read_text(encoding="utf-8").split())
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
                self.assertTrue("때만" in text or "필요가 있을 때" in text)

    def test_search_visibility_requires_both_database_and_relevant_situation(self):
        skill = skill_path("search-visibility").read_text(encoding="utf-8")
        boost = boost_path("search-visibility").read_text(encoding="utf-8")
        self.assertIn("DB 존재만으로 열지 않는다", skill)
        self.assertIn("「언제 여는가」에 적힌 상황 중 하나", skill)
        for technical_check in ("SEO 기술 체크리스트", "`curl` 판정", "구조화 데이터 문법"):
            with self.subTest(technical_check=technical_check):
                self.assertIn(technical_check, skill)
                self.assertIn(technical_check, boost)

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

        design = boost_path("dark-saas-design").read_text(encoding="utf-8")
        self.assertIn("이 스킬은 온톨로지에 쓰지 않는다", design)
        self.assertIn("파생 규칙은 온톨로지에 무엇이 있든 그대로다", design)
        self.assertIn("판독 기록은 참고 자료이지 재현 허가가 아니다", design)

    def test_every_boost_declares_what_it_leaves_unchanged(self):
        for skill in BOOST_SKILLS:
            with self.subTest(skill=skill):
                text = boost_path(skill).read_text(encoding="utf-8")
                self.assertIn("## 바뀌지 않는 것", text)
                self.assertIn("온톨로지는 입력만 보강한다", text)
                self.assertIn("발동 조건·게이트·판정 기준·실행 권한을 넓히지 않는다", text)
                self.assertIn("이 스킬은 온톨로지에 쓰지 않는다", text)

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
                text = " ".join(boost_path(skill).read_text(encoding="utf-8").split())
                self.assertRegex(
                    text,
                    r"`?recall\.md`?가 없으면 SQL을 지어내지 말고 .*모듈을 닫는다",
                )
                self.assertTrue(
                    any(
                        marker in text
                        for marker in (
                            "본문대로",
                            "기본값으로 진행",
                            "그대로 넘긴다",
                            "diff만으로",
                            "본문 기본값",
                            "기본 경로를 계속한다",
                        )
                    )
                )

                # A missing canonical recall procedure must close this optional module;
                # wording that continues querying or recalling would reopen the gate.
                self.assertNotRegex(
                    text,
                    r"`?recall\.md`?[^.。]*없어도[^.。]*(?:조회|회수|쿼리)[^.。]*한다",
                )
                self.assertNotRegex(
                    text,
                    r"`?recall\.md`?[^.。]*없으면[^.。]*(?:조회|회수|쿼리)[^.。]*한다",
                )

    def test_domain_ontology_keeps_its_consent_guard(self):
        text = (ROOT / "skills" / "domain-ontology" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Ask before ingesting", text)
        self.assertIn("Never silent", text)
        self.assertIn("tenant는 문서마다 다시 확정한다", text)
        self.assertNotIn("동의 없이도", text)


if __name__ == "__main__":
    unittest.main()
