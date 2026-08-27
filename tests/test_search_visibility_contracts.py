import ast
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

    def test_every_lane_reference_exists(self):
        for name in ("seo", "aeo", "geo", "llmo", "neo-naver", "measure", "ontology-boost"):
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
        self.assertIn("허가받은 사이트에만 쓴다", self.script)

    def test_audit_script_reports_unset_ai_bot_policy_as_undecided(self):
        # robots.txt 부재를 중립으로 읽으면 GEO 진단이 통째로 조용히 통과한다.
        self.assertIn('"미지정"', self.script)
        self.assertIn("무정책은 중립이 아니라 미지정이므로", self.script)

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

    def test_lifecycle_registers_the_skill(self):
        config = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))
        entry = config["skills"]["search-visibility"]
        self.assertEqual(entry["status"], "active")
        self.assertEqual(entry["providers"], ["claude", "codex", "gemini", "grok"])


if __name__ == "__main__":
    unittest.main()
