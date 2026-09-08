#!/usr/bin/env python3
"""Validate structural contracts shared by every skill in this repository."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
ROUTED_PATH_RE = re.compile(r"`((?:references|agents|scripts)/[^`\s]+)`")
PLAIN_ROUTED_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_/])((?:references|agents|scripts)/(?:[A-Za-z0-9_.-]+/)*"
    r"[A-Za-z0-9_.-]+?\.[A-Za-z0-9]+)(?=$|[\s,;:!?)}\]가-힣]|\.(?:\s|$))"
)
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    if yaml is None:
        raise ValueError("PyYAML is required; install it with 'python3 -m pip install -r requirements-dev.txt'")
    try:
        values = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter: {exc}") from exc
    if not isinstance(values, dict):
        raise ValueError("YAML frontmatter must be a top-level mapping")
    return values


def local_targets(path: Path):
    text = path.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        target = raw.strip().split("#", 1)[0]
        if target and not target.startswith(("http://", "https://", "app://", "/", "#")):
            yield target
    if path.name == "SKILL.md":
        yield from dict.fromkeys(ROUTED_PATH_RE.findall(text) + PLAIN_ROUTED_PATH_RE.findall(text))


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return [f"{skills_root}: missing skills directory"]
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
        description = meta.get("description")
        if not isinstance(name, str):
            errors.append(f"{skill_file}: name must be a string")
            name = None
        if not isinstance(description, str):
            errors.append(f"{skill_file}: description must be a string")
            description = None
        if name != skill_dir.name:
            errors.append(f"{skill_file}: name {name!r} must match directory {skill_dir.name!r}")
        if name and (len(name) > 64 or not SKILL_NAME_RE.fullmatch(name)):
            errors.append(f"{skill_file}: invalid skill name {name!r}")
        if not description or not description.strip():
            errors.append(f"{skill_file}: missing description")
        elif len(description) > 1024:
            errors.append(f"{skill_file}: description exceeds 1024 characters")
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
            assets = sorted(p for p in skill_dir.rglob("*") if p.is_file())
            basename_counts = {asset.name: sum(other.name == asset.name for other in assets) for asset in assets}
            for asset in assets:
                if asset.name in {"SKILL.md", "README.md"} or "__pycache__" in asset.parts:
                    continue
                label = asset.relative_to(skill_dir).as_posix() if basename_counts[asset.name] > 1 else asset.name
                if label not in inventory:
                    errors.append(f"{readme}: operational asset not inventoried: {label}")
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
