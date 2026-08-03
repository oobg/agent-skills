#!/usr/bin/env python3
"""Validate structural contracts shared by every skill in this repository."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
ROUTED_PATH_RE = re.compile(r"`((?:references|agents|scripts)/[^`\s]+)`")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def local_targets(path: Path):
    text = path.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        target = raw.strip().split("#", 1)[0]
        if target and not target.startswith(("http://", "https://", "app://", "/", "#")):
            yield target
    if path.name == "SKILL.md":
        yield from ROUTED_PATH_RE.findall(text)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    seen_names: dict[str, Path] = {}
    for skill_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        readme = skill_dir / "README.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue
        try:
            meta = frontmatter(skill_file)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{skill_file}: {exc}")
            continue
        name = meta.get("name")
        if name != skill_dir.name:
            errors.append(f"{skill_file}: name {name!r} must match directory {skill_dir.name!r}")
        if not meta.get("description"):
            errors.append(f"{skill_file}: missing description")
        if name in seen_names:
            errors.append(f"{skill_file}: duplicate skill name {name!r} (also {seen_names[name]})")
        elif name:
            seen_names[name] = skill_file

        for doc in sorted(skill_dir.rglob("*.md")):
            for target in local_targets(doc):
                resolved = (doc.parent / target).resolve()
                if not resolved.exists():
                    errors.append(f"{doc}: broken local reference {target!r}")

        if not readme.is_file():
            errors.append(f"{skill_dir}: missing README.md")
        else:
            inventory = readme.read_text(encoding="utf-8")
            for asset in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
                if asset.name in {"SKILL.md", "README.md"} or "__pycache__" in asset.parts:
                    continue
                if asset.name not in inventory:
                    errors.append(f"{readme}: operational asset not inventoried: {asset.name}")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
