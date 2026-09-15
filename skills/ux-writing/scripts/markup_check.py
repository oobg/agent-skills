#!/usr/bin/env python3
"""의존성 없는 HTML 구조 게이트.

HTML/HTM 파일의 태그 균형과 표 행의 열 폭(colspan 포함)을 검사한다.
JSX/TSX/Vue는 HTML과 문법이 달라 오탐을 피하기 위해 검사하지 않는다.

종료 코드: 구조 오류 1, 통과 또는 안전한 미지원 형식 생략 0, 입력 오류 2.
"""

import os
import sys
from collections import Counter
from html.parser import HTMLParser


SUPPORTED_EXTS = {".html", ".htm"}
SKIPPED_EXTS = {".jsx", ".tsx", ".vue"}
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
OPTIONAL_END_TAGS = {
    "colgroup", "dd", "dt", "li", "option", "p", "tbody", "td", "tfoot",
    "th", "thead", "tr",
}
BLOCK_STARTS = {
    "address", "article", "aside", "blockquote", "div", "dl", "fieldset",
    "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr",
    "main", "nav", "ol", "p", "pre", "section", "table", "ul",
}


class MarkupParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.tables = []
        self.table_stack = []
        self.issues = []

    def location(self):
        line, col = self.getpos()
        return line, col + 1

    def add_issue(self, message, position=None):
        line, col = position or self.location()
        self.issues.append(f"L{line}:C{col}: {message}")

    def close_optional_for_start(self, tag):
        if not self.stack:
            return
        top = self.stack[-1][0]
        same_group = (
            (top == "li" and tag == "li")
            or (top in {"dt", "dd"} and tag in {"dt", "dd"})
            or (top in {"td", "th"} and tag in {"td", "th"})
            or (top == "tr" and tag == "tr")
            or (top == "option" and tag == "option")
            or (top == "p" and tag in BLOCK_STARTS)
        )
        if same_group:
            self.stack.pop()

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        position = self.location()
        self.close_optional_for_start(tag)
        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, position))

        if tag == "table":
            table = {"position": position, "rows": [], "active_row": None}
            self.tables.append(table)
            self.table_stack.append(table)
        elif tag == "tr" and self.table_stack:
            table = self.table_stack[-1]
            row = {"position": position, "width": 0}
            table["rows"].append(row)
            table["active_row"] = row
        elif tag in {"td", "th"} and self.table_stack:
            table = self.table_stack[-1]
            row = table["active_row"]
            if row is not None:
                raw_colspan = dict(attrs).get("colspan", "1")
                try:
                    colspan = int(raw_colspan)
                    if colspan < 1:
                        raise ValueError
                except (TypeError, ValueError):
                    self.add_issue(f"{tag}의 colspan은 양의 정수여야 합니다: {raw_colspan!r}")
                    colspan = 1
                row["width"] += colspan

    def handle_startendtag(self, tag, attrs):
        # HTML의 명시적 self-closing 태그는 균형 스택에 남기지 않는다.
        if tag.lower() in {"td", "th", "tr", "table"}:
            self.handle_starttag(tag, attrs)
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in VOID_ELEMENTS:
            return

        matching = next(
            (index for index in range(len(self.stack) - 1, -1, -1)
             if self.stack[index][0] == tag),
            None,
        )
        if matching is None:
            self.add_issue(f"여는 태그가 없는 </{tag}>입니다")
        else:
            blockers = [entry for entry in self.stack[matching + 1:]
                        if entry[0] not in OPTIONAL_END_TAGS]
            if blockers:
                open_tag, open_pos = blockers[-1]
                self.add_issue(
                    f"<{open_tag}>를 닫기 전에 </{tag}>가 나왔습니다 "
                    f"(여는 위치 L{open_pos[0]}:C{open_pos[1]})"
                )
            del self.stack[matching:]

        if tag == "tr" and self.table_stack:
            self.table_stack[-1]["active_row"] = None
        elif tag == "table" and self.table_stack:
            self.table_stack.pop()

    def finish(self):
        for tag, position in self.stack:
            if tag not in OPTIONAL_END_TAGS:
                self.add_issue(f"닫히지 않은 <{tag}> 태그입니다", position)

        for table in self.tables:
            rows = table["rows"]
            if len(rows) < 2:
                continue
            widths = [row["width"] for row in rows]
            expected = Counter(widths).most_common(1)[0][0]
            if len(set(widths)) == 1:
                continue
            details = ", ".join(
                f"L{row['position'][0]}={row['width']}열" for row in rows
            )
            line, col = table["position"]
            self.issues.append(
                f"L{line}:C{col}: table 행의 열 폭이 다릅니다 "
                f"(기준 {expected}열, {details})"
            )
        return self.issues


def check(text):
    parser = MarkupParser()
    parser.feed(text)
    parser.close()
    return parser.finish()


def main():
    if len(sys.argv) != 2:
        print("사용법: python3 markup_check.py <HTML 파일경로>", file=sys.stderr)
        sys.exit(2)

    path = sys.argv[1]
    ext = os.path.splitext(path)[1].lower()
    if ext in SKIPPED_EXTS:
        print(f"구조 검사 생략: {ext} 문법은 HTML 구조 게이트의 지원 범위가 아닙니다.")
        sys.exit(0)
    if ext not in SUPPORTED_EXTS:
        print("마크업 검사 입력 오류: .html 또는 .htm 파일이 필요합니다.", file=sys.stderr)
        sys.exit(2)

    try:
        with open(path, encoding="utf-8") as file:
            text = file.read()
        issues = check(text)
    except (OSError, UnicodeError) as exc:
        print(f"마크업 검사 입력 오류: {exc}", file=sys.stderr)
        sys.exit(2)

    if issues:
        print(f"마크업 구조 보류: {len(issues)}건", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        sys.exit(1)

    print("마크업 구조 통과: 태그 균형과 table 행 열 폭이 일치합니다.")
    sys.exit(0)


if __name__ == "__main__":
    main()
