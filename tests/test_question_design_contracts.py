from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1] / "skills" / "question-design"


class QuestionDesignResidualContractTests(unittest.TestCase):
    def test_mode_b_defines_orchestrator_conversion_and_all_residual_routes(self):
        text = (ROOT / "references" / "mode-b.md").read_text(encoding="utf-8")

        self.assertIn("AGENT 0·1·3은 끝까지 `ISSUES | CLEAN`만 반환한다", text)
        self.assertIn("사이클 수준 `STATUS: RESIDUAL`", text)
        self.assertIn("모든 RESIDUAL → AGENT 4", text)
        self.assertIn("RESIDUAL 사용자 결정 게이트", text)
        self.assertNotIn("잔여 위험`으로 명시해 다음 단계에 전달할 수 있다", text)
        self.assertIn("동일 구조적 이슈가\n  2회 연속 남거나 반복 상한에 닿으면", text)

    def test_agent4_fallback_preserves_latest_coordinator_draft_and_risks(self):
        text = (ROOT / "references" / "mode-b.md").read_text(encoding="utf-8")

        self.assertIn("최신 오케스트레이터 소유 중간 보완본", text)
        self.assertIn("RESIDUAL의 미해결 이슈를 `[잔여 위험]`에 보존", text)

    def test_reviewers_keep_issues_clean_contract_without_self_editing(self):
        for filename in (
            "domain-knowledge-reviewer.md",
            "adversarial-reviewer.md",
        ):
            text = (ROOT / "agents" / filename).read_text(encoding="utf-8")
            self.assertIn("`ISSUES | CLEAN`", text)
            self.assertIn("`RESIDUAL`을 직접 출력하거나 보완본을", text)

    def test_lite_clean_and_ambiguity_have_deterministic_routes(self):
        text = (ROOT / "references" / "mode-b.md").read_text(encoding="utf-8")

        self.assertIn("Lite에서 AGENT 1이 첫 회차에 CLEAN이면", text)
        self.assertIn("`AMBIGUITY: outcome-changing`을 반환하면", text)
        self.assertIn("사용자에게는 `NO_BLOCKERS_IN_SCOPE`로 표현한다", text)


if __name__ == "__main__":
    unittest.main()
