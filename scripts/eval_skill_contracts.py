#!/usr/bin/env python3
"""Evaluate deterministic, static skill contracts declared as JSON cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


KINDS = {"positive", "negative", "execution"}
FIELDS = {"id", "kind", "target", "all", "none"}


def _strings(case: dict, field: str) -> list[str]:
    value = case.get(field, [])
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field!r} must be a list of non-empty strings")
    return value


def evaluate(root: Path, suite: Path) -> list[str]:
    """Return one error per invalid or failed static contract."""
    try:
        payload = json.loads(suite.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{suite}: cannot load suite: {exc}"]

    cases = payload.get("cases") if isinstance(payload, dict) else None
    if not isinstance(cases, list):
        return [f"{suite}: top-level 'cases' must be a list"]

    errors: list[str] = []
    seen: set[str] = set()
    root = root.resolve()
    for index, case in enumerate(cases):
        label = f"case[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: must be an object")
            continue
        unknown = set(case) - FIELDS
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{label}: 'id' must be a non-empty string")
            continue
        label = case_id
        if case_id in seen:
            errors.append(f"{label}: duplicate id")
            continue
        seen.add(case_id)
        if unknown:
            errors.append(f"{label}: unknown fields: {', '.join(sorted(unknown))}")
        kind = case.get("kind")
        if kind not in KINDS:
            errors.append(f"{label}: kind must be one of {', '.join(sorted(KINDS))}")
        target_value = case.get("target")
        if not isinstance(target_value, str) or not target_value:
            errors.append(f"{label}: 'target' must be a non-empty string")
            continue
        try:
            required = _strings(case, "all")
            forbidden = _strings(case, "none")
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue
        if not required and not forbidden:
            errors.append(f"{label}: declare at least one 'all' or 'none' assertion")
            continue
        target = (root / target_value).resolve()
        if target != root and root not in target.parents:
            errors.append(f"{label}: target escapes repository root: {target_value}")
            continue
        try:
            text = target.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{label}: cannot read {target_value}: {exc}")
            continue
        for needle in required:
            if needle not in text:
                errors.append(f"{label}: missing required text {needle!r} in {target_value}")
        for needle in forbidden:
            if needle in text:
                errors.append(f"{label}: found forbidden text {needle!r} in {target_value}")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parents[1]
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--suite", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    suite = args.suite or root / "evals" / "static-contracts.json"
    errors = evaluate(root, suite.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("static skill contracts passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
