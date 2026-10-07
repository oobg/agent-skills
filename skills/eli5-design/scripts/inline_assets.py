#!/usr/bin/env python3
"""Fill eli5-design asset placeholders in an HTML file.

The page or deck skeleton keeps one comment per canonical asset, for example
``/* eli5:page.css */`` inside the main ``<style>``. This script replaces each
comment with the file contents so the agent never has to read the CSS or JS.

    python3 scripts/inline_assets.py page out.html
    python3 scripts/inline_assets.py deck out.html -o final.html

Placeholders per mode (tokens.css first in the main <style>):

    page: tokens.css, page.css, page.js
    deck: tokens.css, page.css, deck.css, deck-shapes.css, deck-enhance.css, deck.js

``deck-shapes.css`` holds the rules that only apply when slides use the
shared diagram shapes (``d0-s-*``). It is filled only when the HTML uses such
a class and is otherwise replaced with nothing.

tokens.css comes from the sibling ``day0-design`` skill, searched in the order
of references/day0.md (sibling path, then global skill directories). Pass
``--tokens PATH`` to use another file. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS = SKILL_DIR / "assets"
MODES = {
    "page": ["tokens.css", "page.css", "page.js"],
    "deck": ["tokens.css", "page.css", "deck.css", "deck-shapes.css", "deck-enhance.css", "deck.js"],
}
ALL_NAMES = sorted({name for names in MODES.values() for name in names})
GLOBAL_SKILL_DIRS = [
    "~/.agents/skills",
    "~/.claude/skills",
    "~/.codex/skills",
    "~/.gemini/skills",
    "~/.grok/skills",
]
PLACEHOLDER_RE = re.compile(r"/\*\s*eli5:([a-z0-9.-]+)\s*\*/")
SHAPE_RE = re.compile(r"class=\"[^\"]*\bd0-s-[a-z]")


def find_tokens(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise SystemExit(f"tokens.css not found: {path}")
        return path
    candidates = [SKILL_DIR.parent / "day0-design"]
    candidates += [Path(d).expanduser() / "day0-design" for d in GLOBAL_SKILL_DIRS]
    for base in candidates:
        if (base / "SKILL.md").is_file() and (base / "references" / "tokens.css").is_file():
            return base / "references" / "tokens.css"
    raise SystemExit(
        "day0-design tokens.css not found. Follow references/day0.md "
        "(sibling, global skill directories, public repository) and pass --tokens PATH."
    )


def inline(html: str, mode: str, tokens: Path) -> tuple[str, list[str]]:
    wanted = MODES[mode]
    found = PLACEHOLDER_RE.findall(html)
    unknown = [name for name in found if name not in ALL_NAMES]
    if unknown:
        raise SystemExit(f"unknown placeholder(s): {', '.join(unknown)}")
    foreign = [name for name in found if name not in wanted]
    if foreign:
        raise SystemExit(f"placeholder(s) not used in {mode} mode: {', '.join(foreign)}")
    missing = [name for name in wanted if name not in found]
    if missing:
        raise SystemExit(f"missing placeholder(s) for {mode}: {', '.join(missing)}")
    dupes = sorted({name for name in found if found.count(name) > 1})
    if dupes:
        raise SystemExit(f"placeholder(s) appear more than once: {', '.join(dupes)}")

    uses_shapes = bool(SHAPE_RE.search(html))
    filled = []

    def content(name: str) -> str:
        if name == "tokens.css":
            text = tokens.read_text(encoding="utf-8")
        elif name == "deck-shapes.css" and not uses_shapes:
            return ""
        else:
            text = (ASSETS / name).read_text(encoding="utf-8")
        filled.append(name)
        return text.rstrip("\n")

    return PLACEHOLDER_RE.sub(lambda m: content(m.group(1)), html), filled


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=sorted(MODES))
    parser.add_argument("html", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="write here instead of overwriting the input")
    parser.add_argument("--tokens", help="path to day0-design references/tokens.css")
    args = parser.parse_args(argv)

    html = args.html.read_text(encoding="utf-8")
    tokens = find_tokens(args.tokens)
    result, filled = inline(html, args.mode, tokens)
    out = args.output or args.html
    out.write_text(result, encoding="utf-8")
    print(f"inlined {', '.join(filled)} into {out} (tokens: {tokens})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
