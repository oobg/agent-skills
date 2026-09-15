import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPTS = ROOT / "skills" / "ux-writing" / "scripts"


def load_module(name):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UxWritingCliTests(unittest.TestCase):
    def run_script(self, name, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / f"{name}.py"), *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_checkers_reject_malformed_arguments(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "copy.md"
            target.write_text("저장해요", encoding="utf-8")
            for name in ("glossary_check", "register_check"):
                self.assertEqual(self.run_script(name, target, "--as").returncode, 2)
                self.assertEqual(self.run_script(name, target, "one", "two").returncode, 2)
            self.assertEqual(self.run_script("markup_check").returncode, 2)
            self.assertEqual(self.run_script("markup_check", target, "extra").returncode, 2)

    def test_all_checkers_report_missing_target_without_traceback(self):
        missing = ROOT / "does-not-exist.md"
        for name in ("ai_lint", "glossary_check", "register_check"):
            result = self.run_script(name, missing)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

        missing_html = ROOT / "does-not-exist.html"
        result = self.run_script("markup_check", missing_html)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_ai_lint_rejects_invalid_pattern_schema(self):
        module = load_module("ai_lint")
        original = module.PATTERNS_PATH
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "patterns.json"
            path.write_text(json.dumps({
                "version": "1.0",
                "patterns": [{
                    "id": "bad", "label": "bad", "regex": "x",
                    "layer": "harrd", "status": "verified"
                }],
            }), encoding="utf-8")
            module.PATTERNS_PATH = str(path)
            try:
                with self.assertRaisesRegex(ValueError, "layer"):
                    module.load_patterns()
            finally:
                module.PATTERNS_PATH = original

    def test_ai_lint_treats_every_middle_dot_as_hard(self):
        module = load_module("ai_lint")
        hard, advisory = module.lint("이름·이메일·연락처\n보기·숨기기", [])
        self.assertEqual(len(hard["가운뎃점"]), 2)
        self.assertNotIn("가운뎃점(둘 묶기)", advisory)

    def test_ai_lint_normalizes_entities_without_moving_positions(self):
        module = load_module("ai_lint")
        source = "앞 &mdash; 뒤 &ldquo;인용&rdquo; 끝"
        normalized, count = module.normalize_char_refs(source)

        self.assertEqual(count, 3)
        self.assertEqual(len(normalized), len(source))
        self.assertEqual(normalized.index("—"), source.index("&mdash;"))
        self.assertEqual(normalized.index("“"), source.index("&ldquo;"))
        self.assertEqual(normalized.index("”"), source.index("&rdquo;"))

    def test_ai_lint_keeps_line_separator_entities_for_position_safety(self):
        module = load_module("ai_lint")
        source = "앞&#8232;뒤&#8233;끝"

        normalized, count = module.normalize_char_refs(source)

        self.assertEqual(count, 0)
        self.assertEqual(normalized, source)

    def test_ai_lint_masks_markup_and_code_before_normalizing_entities(self):
        module = load_module("ai_lint")
        source = '<div title="&mdash;">본문 &mdash; 설명</div>'
        masked, _ = module.mask_markup(source)
        normalized, count = module.normalize_char_refs(masked)
        self.assertEqual(count, 1)
        self.assertEqual(len(normalized), len(source))
        self.assertEqual(normalized.index("—"), source.rindex("&mdash;"))

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "copy.html"
            target.write_text(
                '<div title="&mdash;">본문 &mdash; 설명</div>\n'
                '`&mdash;`\n```\n&ldquo;코드&rdquo;\n```\n',
                encoding="utf-8",
            )
            result = self.run_script("ai_lint", target)

        self.assertEqual(result.returncode, 0)
        self.assertIn("대시: 1", result.stdout)
        self.assertIn("곱슬따옴표: 0", result.stdout)
        self.assertIn("HTML 문자 참조 1건", result.stdout)
        self.assertIn("코드블록 1줄", result.stdout)
        self.assertIn("마크업 태그", result.stdout)

    def test_ai_lint_applies_hard_patterns_to_entities(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "copy.html"
            target.write_text("<p>이름&middot;이메일</p>", encoding="utf-8")
            result = self.run_script("ai_lint", target)

        self.assertEqual(result.returncode, 1)
        self.assertIn("가운뎃점: 1", result.stdout)
        self.assertIn("HTML 문자 참조 1건", result.stdout)

    def test_ai_lint_keeps_prose_around_inline_code_in_register_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "copy.md"
            target.write_text(
                "이 값은 반드시 설정합니다.\n"
                "다음 단계로 넘어갑니다.\n"
                "기본 경로는 `config.json` 입니다.\n"
                "캐시는 자동으로 지웁니다 `--no-cache`\n"
                "로그는 파일로 남습니다 `app.log`\n",
                encoding="utf-8",
            )
            result = self.run_script("ai_lint", target)

        self.assertEqual(result.returncode, 0)
        self.assertIn("합니다체로 일관됨 (5문장)", result.stdout)
        self.assertNotIn("xxxx", result.stdout)

    def test_markup_check_accepts_balanced_table_with_colspan(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "table.html"
            target.write_text(
                "<table><tr><th colspan='2'>제목</th></tr>"
                "<tr><td>하나</td><td>둘</td></tr></table>",
                encoding="utf-8",
            )
            result = self.run_script("markup_check", target)

        self.assertEqual(result.returncode, 0)
        self.assertIn("구조 통과", result.stdout)

    def test_markup_check_accepts_balanced_table_with_rowspan(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "rowspan.html"
            target.write_text(
                "<table><tr><th>구분</th><th>항목</th><th>값</th></tr>"
                "<tr><td rowspan='2'>공통</td><td>이름</td><td>서비스</td></tr>"
                "<tr><td>버전</td><td>1.0</td></tr></table>",
                encoding="utf-8",
            )
            result = self.run_script("markup_check", target)

        self.assertEqual(result.returncode, 0)
        self.assertIn("구조 통과", result.stdout)

    def test_markup_check_accepts_html5_nonvoid_self_closing_syntax(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "self-closing.html"
            target.write_text("<div/><p>안내 문구입니다.</p></div>", encoding="utf-8")
            result = self.run_script("markup_check", target)

        self.assertEqual(result.returncode, 0)
        self.assertIn("구조 통과", result.stdout)

    def test_markup_check_rejects_table_cells_outside_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "missing-row.html"
            target.write_text("<table><td>하나</td><td>둘</td></table>", encoding="utf-8")
            result = self.run_script("markup_check", target)

        self.assertEqual(result.returncode, 1)
        self.assertIn("<td>는 <tr> 안에 있어야 합니다", result.stderr)

    def test_markup_check_reports_tag_and_table_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "broken.html"
            target.write_text(
                "<main><span>문구</main>\n"
                "<table><tr><td>하나</td></tr>"
                "<tr><td>둘</td><td>셋</td></tr></table>",
                encoding="utf-8",
            )
            result = self.run_script("markup_check", target)

        self.assertEqual(result.returncode, 1)
        self.assertIn("<span>를 닫기 전에 </main>", result.stderr)
        self.assertIn("table 행의 열 폭이 다릅니다", result.stderr)

    def test_markup_check_skips_non_html_template_syntax(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "component.tsx"
            target.write_text("export const View = () => <Widget value={a > b} />;", encoding="utf-8")
            result = self.run_script("markup_check", target)

        self.assertEqual(result.returncode, 0)
        self.assertIn("검사 생략", result.stdout)

    def test_register_check_supports_noun_ending_register(self):
        module = load_module("register_check")
        self.assertEqual(module.to_register("명사형"), "명사")
        self.assertEqual(module.to_register("명사 종결"), "명사")
        self.assertEqual(module.check("저장 완료\n검토 필요\n문서 개요", "명사"), [])

        hits = module.check("저장해요\n검토합니다\n작업을 마친다", "명사")
        self.assertEqual([hit[1] for hit in hits], ["해요", "합니다", "한다"])


if __name__ == "__main__":
    unittest.main()
