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


if __name__ == "__main__":
    unittest.main()
