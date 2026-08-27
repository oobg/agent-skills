import ast
import importlib.util
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
        cls.script = AUDIT_SCRIPT.read_text(encoding="utf-8")
        cls.competition = COMPETITION.read_text(encoding="utf-8")
        spec = importlib.util.spec_from_file_location("crawl_audit", AUDIT_SCRIPT)
        cls.audit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.audit)

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

    def test_completion_requires_a_scheduled_remeasurement(self):
        self.assertIn("측정 계획 없이 완료를 주장하지 않는다", self.skill)
        self.assertIn("재측정 날짜를 보고에 명시하는 것까지가 완료 조건이다", self.skill)
        self.assertIn("재측정 결과 줄이 채워지기 전까지는 완료가 아니다", self.measure)

    def test_effect_is_never_reported_as_a_prediction(self):
        self.assertIn("효과를 예측 수치로 적지 않는다", self.skill)
        self.assertIn("예상 수치로 그 줄을 미리 채우지 않는다", self.measure)

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
        allowed = {
            "argparse", "gzip", "json", "re", "ssl", "sys", "time", "urllib",
        }
        tree = ast.parse(self.script)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertEqual(imported - allowed, set())

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

    def test_lifecycle_registers_the_skill(self):
        config = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))
        entry = config["skills"]["search-visibility"]
        self.assertEqual(entry["status"], "active")
        self.assertEqual(entry["providers"], ["claude", "codex", "gemini", "grok"])


if __name__ == "__main__":
    unittest.main()
