import ast
import importlib
import importlib.util
import sys
import json
import os
import stat
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
SKILL_DIR = ROOT / "skills" / "search-visibility"
SKILL = SKILL_DIR / "SKILL.md"
BOOST = SKILL_DIR / "references" / "ontology-boost.md"
MEASURE = SKILL_DIR / "references" / "measure.md"
TEMPLATES = SKILL_DIR / "references" / "templates.md"
AUDITOR = SKILL_DIR / "agents" / "visibility-auditor.md"
AUDIT_SCRIPT = SKILL_DIR / "scripts" / "crawl_audit.py"
COMPETITION = SKILL_DIR / "references" / "citation-competition.md"
NEO = SKILL_DIR / "references" / "neo-naver.md"
GEO = SKILL_DIR / "references" / "geo.md"


class SearchVisibilityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.boost = BOOST.read_text(encoding="utf-8")
        cls.measure = MEASURE.read_text(encoding="utf-8")
        cls.neo = NEO.read_text(encoding="utf-8")
        cls.geo = GEO.read_text(encoding="utf-8")
        cls.templates = TEMPLATES.read_text(encoding="utf-8")
        cls.auditor = AUDITOR.read_text(encoding="utf-8")
        cls.competition = COMPETITION.read_text(encoding="utf-8")
        sys.path.insert(0, str(AUDIT_SCRIPT.parent))
        cls.audit = importlib.import_module("checks_site")
        cls.page_mod = importlib.import_module("checks_page")
        cls.entry = importlib.import_module("crawl_audit")
        cls.script = "\n".join(f.read_text(encoding="utf-8")
                                for f in sorted(AUDIT_SCRIPT.parent.glob("*.py")))

    def test_every_lane_reference_exists(self):
        for name in ("seo", "aeo", "geo", "llmo", "neo-naver", "measure",
                     "citation-competition", "templates", "ontology-boost"):
            self.assertTrue((SKILL_DIR / "references" / f"{name}.md").is_file(), name)

    def test_guideline_violations_are_refused_even_when_requested(self):
        self.assertIn("사용자가 요청해도 수행하지 않는다", self.skill)
        self.assertIn("백링크 구매", self.skill)
        self.assertIn("클로킹", self.skill)
        # 거절은 침묵이 아니라 보고 항목이다.
        self.assertIn("거절 사실과", self.skill)
        self.assertIn("대신 할 수 있는 정공법을 제시한다", self.skill)
        self.assertIn("사용자가 요청해도 다음은 수행하지 않는다", self.neo)

    def test_completion_requires_crawler_observation_not_source_code(self):
        self.assertIn("자바스크립트 없이", self.skill)
        self.assertIn("`curl` 증빙 없이 완료로 보고하지 않는다", self.skill)
        self.assertIn("확인하지 못한 항목을 양호로 적지 않는다", self.skill)

    def test_completion_is_defined_once_in_two_named_stages(self):
        # 완료 정의가 두 개면 이 스킬이 막으려는 주장(관측 없는 완료)이 그대로 통과한다.
        self.assertIn("측정 계획 없이 완료를 주장하지 않는다", self.skill)
        self.assertIn("완료는 두 단계이고 이름이 다르다", self.skill)
        self.assertIn("| 작업 완료 |", self.skill)
        self.assertIn("| 측정 완료 |", self.skill)
        self.assertIn("효과는 측정 완료 전까지 주장하지 않는다", self.skill)
        # measure.md는 같은 두 이름을 쓰고 SKILL.md를 정본으로 가리킨다.
        self.assertIn("**작업 완료**", self.measure)
        self.assertIn("**측정 완료**", self.measure)
        self.assertIn("두 단계의 구분은 SKILL.md의", self.measure)

    def test_effect_is_never_reported_as_a_prediction(self):
        self.assertIn("효과를 예측 수치로 적지 않는다", self.skill)
        self.assertIn("예상 수치로 미리 채우지도 않는다", self.measure)

    def test_account_bound_work_is_handed_back_not_performed(self):
        self.assertIn("계정 접속이 필요한 작업", self.skill)
        self.assertIn("대신 하지 않고 절차를 안내한다", self.neo)

    def test_crawler_policy_stays_a_user_decision(self):
        self.assertIn("이 결정은 사용자의 것이다", self.geo)
        self.assertIn("승인을 받는다", self.geo)

    def test_ontology_boost_is_optional_and_closes_without_recall_doc(self):
        self.assertIn("있을 때만 편다", self.boost)
        self.assertIn("없으면 이 파일을 무시하고 본문대로", self.boost)
        self.assertIn("SQL을 지어내지 말고 이 모듈을 닫는다", self.boost)

    def test_ontology_boost_never_writes_to_the_graph(self):
        self.assertIn("제안만 한다", self.boost)
        self.assertIn("이 스킬은 온톨로지에 쓰지 않는다", self.boost)
        self.assertIn("domain-ontology", self.boost)

    def test_recall_is_not_evidence_of_the_current_site_state(self):
        # 사이트는 배포마다 바뀌므로 회수가 관측을 대체하면 진단 자체가 틀린다.
        self.assertIn("회수는 사이트의 현재 상태가 아니다", self.boost)
        self.assertIn("회수는 사이트의 현재 상태가 아니다", self.skill)
        self.assertIn("관측 결과만", self.boost)
        self.assertIn("정공법 원칙은 온톨로지에 무엇이 있든 그대로다", self.boost)

    def test_ontology_boost_does_not_duplicate_recall_sql(self):
        # recall.md가 정본이다. 여기에 SQL을 복제하면 규칙이 두 곳에서 갈라진다.
        self.assertNotIn("SELECT", self.boost)
        self.assertIn("recall.md", self.boost)

    def test_audit_script_is_executable_and_dependency_free(self):
        self.assertTrue(AUDIT_SCRIPT.is_file())
        self.assertTrue(os.stat(AUDIT_SCRIPT).st_mode & stat.S_IXUSR)
        # 저장소 요구사항은 Python 3.8 + 표준 라이브러리다. 서드파티 import가 들어오면
        # 스킬을 설치한 곳에서 진단이 그냥 실패한다.
        stdlib = {"argparse", "gzip", "json", "re", "ssl", "sys", "time", "urllib"}
        local = {f.stem for f in AUDIT_SCRIPT.parent.glob("*.py")}
        for f in sorted(AUDIT_SCRIPT.parent.glob("*.py")):
            imported = set()
            for node in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    imported.update(a.name.split(".")[0] for a in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[0])
            self.assertEqual(imported - stdlib - local, set(), f.name)

    def test_audit_script_observes_and_refuses_to_grade_lanes(self):
        self.assertIn("관측만 하고 레인 점수를 판정하지 않는다", self.script)
        self.assertIn("CHECK는 판정이 아니라 사람이 확인할 항목이다", self.script)
        self.assertIn("python3 scripts/crawl_audit.py", self.skill)
        self.assertIn("CHECK를 양호로 올리지 않는다", self.skill)

    def test_audit_script_does_not_impersonate_a_crawler_by_default(self):
        self.assertIn("search-visibility-audit/1.0", self.script)
        self.assertNotIn('DEFAULT_UA = "Googlebot', self.script)
        self.assertIn("공개 페이지에만 쓴다", self.script)
        self.assertIn("남의 사이트를 대량으로 훑는 용도가 아니다", self.script)

    def test_audit_script_reports_unset_ai_bot_policy_as_no_rule(self):
        # robots.txt 부재를 중립으로 읽으면 GEO 진단이 통째로 조용히 통과한다.
        self.assertIn('"규칙 없음"', self.script)
        self.assertIn("무정책은 중립이 아니므로", self.script)

    def test_audit_script_labels_where_a_bot_verdict_came_from(self):
        # 명시와 와일드카드를 같은 말로 적으면 "정책을 정했다"와 "덮인 것"이 섞인다.
        self.assertIn("루트(/) 접근 기준", self.script)
        self.assertIn("와일드카드나 기본값이 적용 중이다", self.script)

    def test_baseline_is_written_to_a_file(self):
        self.assertIn("프로젝트에 파일로 남긴다", self.skill)
        self.assertIn("측정 로그", self.templates)
        self.assertIn("인용 프로브 시트", self.templates)

    def test_templates_refuse_plausible_filler(self):
        self.assertIn("그럴듯한 값으로 메우지 않는다", self.templates)
        self.assertIn("예상 수치로 채우지 않는다", self.templates)

    def test_auditor_is_a_fresh_eyes_pass_that_does_not_rewrite(self):
        self.assertIn("결과만 보고", self.auditor)
        self.assertIn("기대 판정은 넘기지 않는다", self.auditor)
        self.assertIn("직접 다시 쓰지는 않는다", self.auditor)
        self.assertIn("새 기준을 만들지 않는다", self.auditor)

    def test_auditor_holds_instead_of_guessing_missing_evidence(self):
        self.assertIn("STATUS: HOLD — 관측 로그 없음", self.auditor)
        self.assertIn("추정으로 채워 채점하면", self.auditor)

    def test_auditor_escalates_guideline_and_authority_breaches(self):
        self.assertIn("가이드라인 위반과 권한 경계는 에이전트가 판단으로 넘길 문제가 아니다", self.auditor)

    def test_competition_pass_stays_scoped_to_citation(self):
        # 제품·시장 경쟁 분석까지 번지면 스킬 경계가 무너지고 ux-writing·기획 영역과 겹친다.
        self.assertIn("범위는 인용 경쟁으로 한정한다", self.competition)
        self.assertIn("제품 비교, 가격 포지셔닝, 시장 규모, SWOT은 이 스킬 밖이다", self.competition)
        self.assertIn("제품 비교, 가격 포지셔닝, 시장 규모 분석은 이 스킬 밖이다", self.skill)

    def test_competition_requires_enough_samples_to_tell_structure_from_choice(self):
        self.assertIn("4~5개를 같은 축으로 세워야", self.competition)
        self.assertIn("전수가 비운 칸", self.competition)
        self.assertIn("개별 선택", self.competition)

    def test_competition_turns_the_same_checks_on_our_own_pages(self):
        self.assertIn("같은 검산을 우리 페이지에 먼저 한다", self.competition)
        self.assertIn("이 대조도 우리 사이트에 먼저 적용한다", self.competition)

    def test_competition_records_counterexamples_not_just_defects(self):
        self.assertIn("반례를 같이 기록한다", self.competition)
        self.assertIn("성질", self.competition)

    def test_competition_separates_target_change_from_own_misreading(self):
        self.assertIn("관측 오류가 아니라 대상의 변화다", self.competition)
        self.assertIn("없는 비교를 추정으로 채우지 않는다", self.competition)

    def test_competition_allows_giving_up_a_question(self):
        # 점유자가 없다 = 빈자리가 아니라 인용이 일어나지 않는 질문일 수 있다.
        self.assertIn("포기도 결과다", self.competition)
        self.assertIn("인용 없음", self.competition)

    def test_competition_forbids_scraping_and_copying(self):
        self.assertIn("대량 스크래핑을 하지 않는다", self.competition)
        self.assertIn("복제하지 않는다", self.competition)
        self.assertIn("로그인, 결제, 접근 제한 뒤의 콘텐츠에 접근하지 않는다", self.competition)
        self.assertIn("판독 결과를 공개 산출물에 그대로 옮기지 않는다", self.competition)

    def test_skill_completes_without_paid_tooling(self):
        self.assertIn("유료 도구 없이 완결한다", self.skill)
        self.assertIn("구독을 전제로 계획을 세우지 않는다", self.skill)

    def test_fatal_findings_are_not_averaged_away(self):
        self.assertIn("치명 항목은 다른 항목으로 상쇄되지 않는다", self.skill)
        self.assertIn("좋은 항목을 세어 평균을 내지 않는다", self.skill)

    def test_questions_are_chosen_before_pages_are_built(self):
        self.assertIn("먼저 질문을 고르고, 그다음 페이지를 만든다", self.skill)
        self.assertIn("이길 수 없는 질문에 페이지를 쌓는다", self.skill)

    def test_robots_parser_shares_a_group_across_stacked_user_agents(self):
        # 연속된 User-agent 줄은 한 그룹을 공유한다. 마지막 이름에만 규칙을 붙이면
        # 함께 선언된 봇들의 정책이 통째로 사라진다.
        groups = self.audit.parse_robots_groups(
            "User-agent: GPTBot\nUser-agent: ClaudeBot\nDisallow: /\n"
        )
        self.assertEqual(groups["gptbot"], [("disallow", "/")])
        self.assertEqual(groups["claudebot"], [("disallow", "/")])

    def test_robots_verdict_falls_back_to_the_wildcard_group(self):
        # 이름이 명시되지 않았다고 무정책이 아니다. 와일드카드를 계산하지 않으면
        # 실제로 허용된 봇을 미지정으로 과대 경고한다.
        groups = self.audit.parse_robots_groups("User-agent: *\nAllow: /\n")
        self.assertEqual(self.audit.robots_verdict(groups, "GPTBot"), "허용(*)")
        blocked = self.audit.parse_robots_groups("User-agent: *\nDisallow: /\n")
        self.assertEqual(self.audit.robots_verdict(blocked, "GPTBot"), "차단(*)")

    def test_robots_verdict_prefers_the_named_group_over_the_wildcard(self):
        groups = self.audit.parse_robots_groups(
            "User-agent: *\nDisallow: /\n\nUser-agent: GPTBot\nAllow: /\n"
        )
        self.assertEqual(self.audit.robots_verdict(groups, "GPTBot"), "허용(명시)")
        self.assertEqual(self.audit.robots_verdict(groups, "PerplexityBot"), "차단(*)")

    def test_robots_verdict_reports_absence_as_no_rule(self):
        self.assertEqual(self.audit.robots_verdict({}, "GPTBot"), "규칙 없음")

    def test_robots_verdict_reads_partial_disallow_as_root_allowed(self):
        groups = self.audit.parse_robots_groups(
            "User-agent: GPTBot\nAllow: /\nDisallow: /private/\n"
        )
        self.assertEqual(self.audit.robots_verdict(groups, "GPTBot"), "허용(명시)")

    def test_robots_parser_ignores_comments(self):
        groups = self.audit.parse_robots_groups(
            "# comment\nUser-agent: GPTBot  # inline\nDisallow: /  # blocked\n"
        )
        self.assertEqual(groups["gptbot"], [("disallow", "/")])

    def test_intended_noindex_is_not_scored_as_a_defect(self):
        # 스테이징·파라미터 URL이 정상 사이트를 미흡으로 떨어뜨리면 판정이 못 쓰게 된다.
        self.assertIn("의도된 색인 제외는 결함이 아니다", self.skill)
        self.assertIn("확인 전에는 `확인 불가`로 두고 `미흡`으로 내리지 않는다", self.skill)
        self.assertIn("의도된 제외인지 확인한다", self.script)
        self.assertNotIn('("FAIL", "색인"', self.script)

    def test_no_citation_splits_into_two_causes_with_a_test(self):
        # "랜딩을 만들어도 인용이 생기지 않는다"는 measure.md의 O/X로 닫을 수 있는 명제다.
        # 관측 전에 단정하면 문서가 스스로 금지한 짐작이 된다.
        self.assertIn("아직 공급이 없는 자리", self.competition)
        self.assertIn("최소 실험 페이지를 만들고 잰다", self.competition)
        self.assertIn("시험 전에 \"랜딩을 만들어도 인용이 생기지 않는다\"고 단정하지 않는다",
                      self.competition)
        self.assertIn("재검토 주기를 함께 적는다", self.competition)

    def test_minority_column_is_not_discarded_when_it_is_the_occupant(self):
        # 표본을 "실제 인용되는 페이지"로 정의해 놓고 소수파를 버리면
        # 승자를 이기게 한 차별 요소를 정확히 골라서 버리게 된다.
        self.assertIn("그 한 곳이 실제 점유자라면", self.competition)
        self.assertIn("소수라는 이유로 버리기 전에", self.competition)
        self.assertIn("전수가 비었다고 채우면 이긴다는 뜻은 아니다", self.competition)

    def test_faq_source_is_verified_before_being_read_as_demand(self):
        self.assertIn("검색 노출용으로 심은 질문", self.competition)
        self.assertIn("출처 미상", self.competition)
        # 검색 콘솔은 fallback이 아니라 1순위다 (SKILL.md Phase 2와 일치해야 한다).
        self.assertIn("검색 콘솔 검색어가 1순위이고", self.competition)
        self.assertNotIn("그때는 검색 콘솔 검색어와 고객 문의로 돌아간다", self.competition)

    def test_prescriptions_without_official_backing_are_labeled(self):
        neo = (SKILL_DIR / "references" / "neo-naver.md").read_text(encoding="utf-8")
        self.assertIn("공식 문서로 확정된 요건이", neo)
        self.assertIn("검증 전에는 처방이 아니라 시험 대상으로 다룬다", neo)
        self.assertIn("어떤 소비자가 이 파일을 실제로 읽고 인용에 쓰는지는 확정되지 않았다", self.geo)

    def test_named_bot_rule_identical_to_wildcard_is_reported_as_no_difference(self):
        # 이름만 적고 규칙이 같으면 수집 권한은 그대로다. 선언 의도와 접근 차이를
        # 같은 말로 적으면 진단이 없는 차이를 보고한다.
        groups = self.audit.parse_robots_groups(
            "User-agent: *\nAllow: /\nDisallow: /private/\n\n"
            "User-agent: GPTBot\nAllow: /\nDisallow: /private/\n"
        )
        self.assertEqual(self.audit.robots_verdict(groups, "GPTBot"), "허용(명시=*)")
        self.assertIn("수집 권한 차이는 없다", self.script)

    def test_title_threshold_names_the_documented_range(self):
        # seo.md는 50~60자를 권장하는데 스크립트는 15자부터 통과시킨다.
        # 두 기준이 다르다는 사실이 출력과 문서 양쪽에 보여야 한다.
        seo = (SKILL_DIR / "references" / "seo.md").read_text(encoding="utf-8")
        self.assertIn("15자부터 통과시킨다", seo)
        self.assertIn("권장 50~60", self.script)

    def test_structured_data_is_compared_against_visible_text(self):
        # 이 스킬 원칙 2가 기계로 판정되는 유일한 자리다. 화면에 없는 문답을 구조화
        # 데이터가 선언하면 렌더링하지 않는 소비자에게 그 답변은 존재하지 않는다.
        html = """<html><body><h2>배송은 얼마나 걸리나요?</h2>
        <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":"배송은 얼마나 걸리나요?",
        "acceptedAnswer":{"@type":"Answer","text":"주문 후 영업일 기준 2일 안에 도착합니다."}}]}
        </script></body></html>"""
        nodes, _ = importlib.import_module("parse").jsonld_nodes(html)
        text = importlib.import_module("parse").visible_text(html)
        missing, soft, checked = self.page_mod._structured_vs_visible(nodes, text)
        self.assertEqual(checked, 2)
        self.assertEqual(soft, [])
        # 질문은 화면에 있고 답변은 없다 — datapuree에서 실제로 관측된 형태다.
        self.assertEqual(len(missing), 1)
        self.assertIn("답변", missing[0])

    def test_entity_name_mismatch_is_softer_than_missing_answers(self):
        # 다국어 사이트에서 name 표기 차이는 흔하다. 문답 누락과 같은 등급으로 매기면
        # 진짜 문제가 묻힌다.
        html = """<html><body><p>퓨레 HQ 소개</p>
        <script type="application/ld+json">{"@type":"SoftwareApplication","name":"Puree HQ"}
        </script></body></html>"""
        parse_mod = importlib.import_module("parse")
        nodes, _ = parse_mod.jsonld_nodes(html)
        missing, soft, _ = self.page_mod._structured_vs_visible(nodes, parse_mod.visible_text(html))
        self.assertEqual(missing, [])
        self.assertEqual(len(soft), 1)

    def test_numbers_without_a_basis_are_surfaced(self):
        loose = self.page_mod._numbers_without_basis("관리 지점 10,000+ 곳이고 유지율은 98%입니다")
        self.assertTrue(any("10,000" in n for n in loose))
        self.assertTrue(any("98" in n for n in loose))
        # 기준이 붙으면 잡지 않는다.
        self.assertEqual(
            self.page_mod._numbers_without_basis("2026년 8월 기준 관리 지점 10,000+ 곳"), [])

    def test_coverage_lists_what_the_script_does_not_do(self):
        # 문서가 자동 항목을 복제하면 스크립트가 바뀔 때 문서가 남아 거짓말을 한다.
        self.assertTrue(self.entry.COVERAGE)
        self.assertTrue(self.entry.MANUAL)
        self.assertIn("--coverage", self.skill)
        self.assertIn("이 목록을 문서에 옮겨 적지 않는다", self.skill)
        for _, item in self.entry.COVERAGE:
            self.assertNotIn(item, self.skill)

    def test_cross_page_checks_fold_redirect_duplicates(self):
        # base가 /ko로 리다이렉트되면 같은 페이지를 두 번 세어 없는 중복을 보고한다.
        pages = [
            {"status": 200, "title": "같은 제목", "url": "https://e.io", "final_url": "https://e.io/ko"},
            {"status": 200, "title": "같은 제목", "url": "https://e.io/ko", "final_url": "https://e.io/ko"},
        ]
        result = importlib.import_module("checks_cross").audit_cross(pages, [])
        self.assertEqual(result["checks"], [])

    def test_lifecycle_registers_the_skill(self):
        config = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))
        entry = config["skills"]["search-visibility"]
        self.assertEqual(entry["status"], "active")
        self.assertEqual(entry["providers"], ["claude", "codex", "gemini", "grok"])


if __name__ == "__main__":
    unittest.main()
