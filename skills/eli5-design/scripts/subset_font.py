#!/usr/bin/env python3
"""Inline a page-specific Pretendard subset into an eli5-design HTML page.

The subset holds only the glyphs the page uses and is embedded as a base64
@font-face, so the page makes no external request.
"""

from __future__ import annotations

import argparse
import base64
import html
import io
import re
import string
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

FONT_URL = (
    "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/"
    "pretendard/dist/web/variable/woff2/PretendardVariable.woff2"
)
DEFAULT_CACHE_DIR = Path("~/.cache/eli5-design").expanduser()
FONT_NAME = "PretendardVariable.woff2"
MARKER = "eli5-design font subset"
COMMENT = f"{MARKER}: orioncactus/pretendard v1.3.9, SIL OFL 1.1, page subset"
BASE_CHARS = string.printable.strip() + " " + "0123456789→←↑↓·…–—%~•✓×±≈≤≥“”‘’「」『』"
COMMON_SYMBOLS = "✕✓①②③④⑤←↑↓⋯※★"
SUGGESTIONS = {
    "✕": "× (U+00D7) 또는 SVG X",
    "✓": "SVG 체크 (path)",
    "①": "SVG 원 + 숫자 1 (circle + text)",
    "②": "SVG 원 + 숫자 2",
    "③": "SVG 원 + 숫자 3",
    "④": "SVG 원 + 숫자 4",
    "⑤": "SVG 원 + 숫자 5",
    "←": "SVG 화살표 또는 <",
    "↑": "SVG 화살표 또는 ^",
    "↓": "SVG 화살표 또는 v",
    "→": "SVG 화살표 또는 >",
    "⋯": "… (U+2026) 또는 ...",
    "※": "* 또는 `참고` 라벨",
    "★": "SVG 별 (polygon)",
}
ATTRS = {"title", "aria-label", "alt"}
SKIP_TAGS = {"script", "style"}

BLOCK_RE = re.compile(
    r"[ \t]*<style>\s*/\*\s*" + re.escape(MARKER) + r".*?</style>[ \t]*\n?", re.S
)
LINK_RE = re.compile(r"[ \t]*<link\b[^>]*>[ \t]*\n?", re.I)
FIRST_STYLE_RE = re.compile(r"<style\b", re.I)


class TextCollector(HTMLParser):
    """Collect visible text, attribute text, and non-ASCII glyphs from script/style."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self._skip += 1
        for name, value in attrs:
            if name in ATTRS and value:
                self.parts.append(value)

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip:
            # Script/style text is not shown directly, but JS strings and CSS
            # `content` can be. Keep only non-ASCII glyphs from it.
            self.parts.append("".join(c for c in html.unescape(data) if ord(c) > 127))
        else:
            self.parts.append(data)


def used_chars(source: str) -> str:
    """Glyphs the page actually uses (visible text, attributes, script/style non-ASCII)."""
    collector = TextCollector()
    collector.feed(source)
    collector.close()
    text = html.unescape(" ".join(collector.parts))
    text = re.sub(r"\s+", " ", text)
    return "".join(sorted(c for c in set(text) if c.isprintable() or c == " "))


def page_chars(source: str) -> str:
    """Used glyphs plus the base and common symbol sets kept in every subset."""
    chars = set(used_chars(source)) | set(BASE_CHARS) | set(COMMON_SYMBOLS)
    return "".join(sorted(c for c in chars if c.isprintable() or c == " "))


def load_font(font_arg: str | None, cache_dir: Path) -> bytes:
    if font_arg:
        return Path(font_arg).expanduser().read_bytes()
    cached = cache_dir / FONT_NAME
    if cached.is_file():
        return cached.read_bytes()
    print(f"downloading {FONT_URL}", file=sys.stderr)
    with urllib.request.urlopen(FONT_URL, timeout=60) as response:
        data = response.read()
    if len(data) < 100_000:
        raise OSError(f"unexpected font size: {len(data)} bytes")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(data)
    return data


def subset(font_bytes: bytes, chars: str) -> tuple[bytes, list[str]]:
    from fontTools import subset as ft_subset
    from fontTools.ttLib import TTFont

    options = ft_subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    options.notdef_outline = True
    font = TTFont(io.BytesIO(font_bytes))
    subsetter = ft_subset.Subsetter(options)
    subsetter.populate(text=chars)
    subsetter.subset(font)
    cmap = font.getBestCmap()
    missing = [c for c in chars if ord(c) not in cmap and not c.isspace()]
    out = io.BytesIO()
    font.flavor = "woff2"
    font.save(out)
    return out.getvalue(), missing


def font_block(woff2: bytes) -> str:
    b64 = base64.b64encode(woff2).decode("ascii")
    return (
        "<style>\n"
        f"/* {COMMENT} */\n"
        "@font-face {\n"
        '  font-family: "Pretendard Variable";\n'
        f'  src: url(data:font/woff2;base64,{b64}) format("woff2");\n'
        "  font-weight: 45 920;\n"
        "  font-display: swap;\n"
        "}\n"
        "</style>\n"
    )


def inline_font(source: str, block: str) -> tuple[str, int]:
    result = BLOCK_RE.sub("", source)
    removed = 0

    def drop_link(match: re.Match) -> str:
        nonlocal removed
        tag = match.group(0).lower()
        if "pretendard" in tag or "cdn.jsdelivr.net" in tag:
            removed += 1
            return ""
        return match.group(0)

    result = LINK_RE.sub(drop_link, result)
    head_end = re.search(r"</head\s*>", result, re.I)
    limit = head_end.start() if head_end else len(result)
    style = FIRST_STYLE_RE.search(result, 0, limit)
    pos = style.start() if style else limit
    return result[:pos] + block + result[pos:], removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="HTML page to process")
    parser.add_argument("-o", "--output", type=Path, help="output path (default: <name>.font.html)")
    parser.add_argument("--font", help="local PretendardVariable.woff2 (default: cache or download)")
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR, help="font cache directory")
    args = parser.parse_args()

    source = args.input.read_text(encoding="utf-8")
    out_path = args.output or args.input.with_suffix(".font.html")
    if out_path.resolve() == args.input.resolve():
        print("error: output must differ from input", file=sys.stderr)
        return 1

    try:
        import brotli  # noqa: F401
        from fontTools import subset as _  # noqa: F401
    except ImportError:
        print("error: fonttools and brotli are required: pip install fonttools brotli", file=sys.stderr)
        return 3

    try:
        font_bytes = load_font(args.font, args.cache_dir.expanduser())
    except (OSError, ValueError) as exc:
        print(f"error: cannot get Pretendard font ({exc}); input left unchanged", file=sys.stderr)
        return 2

    chars = page_chars(source)
    woff2, missing = subset(font_bytes, chars)
    # Warn only for glyphs the page uses; base/common sets missing from the font are not the page's problem.
    used = set(used_chars(source))
    missing = [c for c in missing if c in used]
    if missing:
        shown = "".join(sorted(set(missing)))
        print(f"warning: {len(set(missing))} chars not in font cmap: {shown}", file=sys.stderr)
        for c in sorted(set(missing)):
            hint = SUGGESTIONS.get(c, "SVG 도형 또는 비슷한 ASCII/폰트 지원 글자")
            print(f"  suggest: {c} (U+{ord(c):04X}) -> {hint}", file=sys.stderr)

    result, removed = inline_font(source, font_block(woff2))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result, encoding="utf-8")
    print(f"chars: {len(chars)}  woff2: {len(woff2)} bytes  links removed: {removed}  output: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
