import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class SkillRoutingContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dark_saas = (
            ROOT / "skills" / "dark-saas-design" / "SKILL.md"
        ).read_text(encoding="utf-8")
        feature_analysis = (
            ROOT / "skills" / "feature-analysis" / "SKILL.md"
        ).read_text(encoding="utf-8")
        cls.dark_saas = " ".join(dark_saas.split())
        cls.feature_analysis = " ".join(feature_analysis.split())

    def test_dark_saas_marks_design_audit_as_external_and_optional(self):
        self.assertIn("`design-slop-audit`은 이 저장소에 포함되지 않은 외부 선택 경로다", self.dark_saas)
        self.assertIn("사용할 수 없으면 그 사실을 알리고", self.dark_saas)
        self.assertIn("진단만 요청한 작업을 이 스킬의 구현 작업으로 바꾸지 않는다", self.dark_saas)

    def test_feature_analysis_marks_out_of_scope_routes_as_external_and_optional(self):
        for route in ("code-review", "design-slop-audit", "prd-generator"):
            with self.subTest(route=route):
                self.assertIn(f"`{route}`", self.feature_analysis)
        self.assertIn("이 저장소에 포함되지 않은 외부 선택", self.feature_analysis)
        self.assertIn("경로를 사용할 수 없으면 그 사실과 처리하지 못한 범위를 알린다", self.feature_analysis)
        self.assertIn("현재 스킬의 분석 범위와 산출물 계약을 조용히 넓히지 않는다", self.feature_analysis)


if __name__ == "__main__":
    unittest.main()
