#!/usr/bin/env python3
"""Validate the two public synthetic evaluation fixtures without external services."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


FIXTURES = {
    "static": Path("tests/fixtures/public-evals/static-contracts.json"),
    "trigger": Path("tests/fixtures/public-evals/trigger-cases.json"),
}
STATIC_FIELDS = {"id", "kind", "target", "all", "none"}
STATIC_KINDS = {"positive", "negative", "execution"}
TRIGGER_FIELDS = {"id", "expect", "request", "origin"}
TRIGGER_EXPECTATIONS = {"recall", "skip"}
TRIGGER_ORIGIN = "authored synthetic case"

PRIVATE_PATTERNS = (
    ("email pattern", re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.IGNORECASE)),
    ("absolute user-home path", re.compile(r"(?:/Users/|/home/)[^\s/\\]+(?:[/\\]|$)")),
    ("Windows user-home path", re.compile(r"(?:[A-Za-z]:[/\\]|[/\\]{2}[^\s/\\]+[/\\][^\s/\\]+[/\\])Users[/\\][^\s/\\]+", re.IGNORECASE)),
    ("private-key header", re.compile(r"-----BEGIN(?: [A-Z0-9]+)* PRIVATE KEY-----")),
)


class Issue:
    def __init__(self, code: int, fixture: Path, kind: str, location: str | None = None):
        self.code = code
        self.fixture = fixture
        self.kind = kind
        self.location = location


def _issue(code: int, fixture: Path, kind: str, location: str | None = None) -> Issue:
    return Issue(code, fixture, kind, location)


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _load(root: Path, fixture: Path) -> tuple[Any | None, list[Issue]]:
    candidate = root / fixture
    if not candidate.exists():
        return None, [_issue(2, fixture, "missing fixture")]
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError):
        return None, [_issue(2, fixture, "unsafe fixture path")]
    if not _inside(resolved, root):
        return None, [_issue(2, fixture, "fixture path escapes root")]
    try:
        text = resolved.read_text(encoding="utf-8")
        return json.loads(text), []
    except UnicodeError:
        return None, [_issue(2, fixture, "invalid UTF-8")]
    except json.JSONDecodeError:
        return None, [_issue(2, fixture, "invalid JSON")]
    except OSError:
        return None, [_issue(2, fixture, "fixture read failure")]


def _string_locations(value: Any, location: str = "top-level"):
    if isinstance(value, str):
        yield location, value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _string_locations(item, f"{location}[{index}]")
    elif isinstance(value, dict):
        for index, (key, item) in enumerate(value.items()):
            yield from _string_locations(key, f"{location}.field-name")
            yield from _string_locations(item, f"{location}.value[{index}]")


def _privacy_issues(payload: Any, fixture: Path) -> list[Issue]:
    issues = []
    for location, value in _string_locations(payload):
        for label, pattern in PRIVATE_PATTERNS:
            if pattern.search(value):
                issues.append(_issue(1, fixture, label, location))
    return issues


def _base_issues(payload: Any, fixture: Path) -> tuple[list[Issue], list[Any] | None]:
    if not isinstance(payload, dict):
        return [_issue(1, fixture, "top-level must be an object")], None
    issues = []
    if payload.get("synthetic") is not True:
        issues.append(_issue(1, fixture, "synthetic must be true", "top-level.synthetic"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        issues.append(_issue(1, fixture, "cases must be a non-empty list", "top-level.cases"))
        return issues, None
    return issues, cases


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_non_empty_string(item) for item in value)


def _validate_static(payload: Any, fixture: Path) -> list[Issue]:
    issues, cases = _base_issues(payload, fixture)
    if cases is None:
        return issues + _privacy_issues(payload, fixture)
    seen = set()
    kinds = set()
    for index, case in enumerate(cases):
        base = f"cases[{index}]"
        if not isinstance(case, dict):
            issues.append(_issue(1, fixture, "case must be an object", base))
            continue
        unknown = set(case) - STATIC_FIELDS
        if unknown:
            issues.append(_issue(1, fixture, "unknown static case field", base))
        case_id = case.get("id")
        if not _non_empty_string(case_id):
            issues.append(_issue(1, fixture, "id must be a non-empty string", f"{base}.id"))
        elif case_id in seen:
            issues.append(_issue(1, fixture, "duplicate id", f"{base}.id"))
        else:
            seen.add(case_id)
        kind = case.get("kind")
        if kind not in STATIC_KINDS:
            issues.append(_issue(1, fixture, "invalid static kind", f"{base}.kind"))
        else:
            kinds.add(kind)
        target = case.get("target")
        if not _non_empty_string(target):
            issues.append(_issue(1, fixture, "target must be a non-empty string", f"{base}.target"))
        else:
            pure = PurePosixPath(target)
            if pure.is_absolute() or len(pure.parts) < 2 or pure.parts[0] != "skills" or ".." in pure.parts:
                issues.append(_issue(1, fixture, "static target must stay under skills", f"{base}.target"))
        required = case.get("all", [])
        forbidden = case.get("none", [])
        if not _string_list(required):
            issues.append(_issue(1, fixture, "all must be a list of non-empty strings", f"{base}.all"))
        if not _string_list(forbidden):
            issues.append(_issue(1, fixture, "none must be a list of non-empty strings", f"{base}.none"))
        if _string_list(required) and _string_list(forbidden) and not required and not forbidden:
            issues.append(_issue(1, fixture, "case must declare an assertion", base))
    if kinds != STATIC_KINDS:
        issues.append(_issue(1, fixture, "static cases must include every kind", "top-level.cases"))
    return issues + _privacy_issues(payload, fixture)


def _validate_trigger(payload: Any, fixture: Path) -> list[Issue]:
    issues, cases = _base_issues(payload, fixture)
    if not isinstance(payload, dict):
        return issues + _privacy_issues(payload, fixture)
    if payload.get("skill") != "domain-ontology":
        issues.append(_issue(1, fixture, "unexpected trigger skill", "top-level.skill"))
    if cases is None:
        return issues + _privacy_issues(payload, fixture)
    seen = set()
    expectations = set()
    for index, case in enumerate(cases):
        base = f"cases[{index}]"
        if not isinstance(case, dict):
            issues.append(_issue(1, fixture, "case must be an object", base))
            continue
        if "cwd" in case:
            issues.append(_issue(1, fixture, "trigger case must not declare cwd", f"{base}.cwd"))
        if set(case) != TRIGGER_FIELDS:
            issues.append(_issue(1, fixture, "trigger case fields do not match the public schema", base))
        for field in TRIGGER_FIELDS:
            if not _non_empty_string(case.get(field)):
                issues.append(_issue(1, fixture, "field must be a non-empty string", f"{base}.{field}"))
        case_id = case.get("id")
        if _non_empty_string(case_id):
            if case_id in seen:
                issues.append(_issue(1, fixture, "duplicate id", f"{base}.id"))
            else:
                seen.add(case_id)
        expect = case.get("expect")
        if expect not in TRIGGER_EXPECTATIONS:
            issues.append(_issue(1, fixture, "invalid trigger expectation", f"{base}.expect"))
        else:
            expectations.add(expect)
        if case.get("origin") != TRIGGER_ORIGIN:
            issues.append(_issue(1, fixture, "trigger origin must identify an authored synthetic case", f"{base}.origin"))
    if expectations != TRIGGER_EXPECTATIONS:
        issues.append(_issue(1, fixture, "trigger cases must include recall and skip", "top-level.cases"))
    return issues + _privacy_issues(payload, fixture)


def check(root: Path) -> list[Issue]:
    try:
        resolved_root = root.resolve(strict=True)
    except (OSError, RuntimeError):
        return [_issue(2, path, "unsafe repository root") for path in FIXTURES.values()]
    if not resolved_root.is_dir():
        return [_issue(2, path, "repository root is not a directory") for path in FIXTURES.values()]
    issues = []
    for name, fixture in FIXTURES.items():
        payload, load_issues = _load(resolved_root, fixture)
        issues.extend(load_issues)
        if load_issues:
            continue
        validator = _validate_static if name == "static" else _validate_trigger
        issues.extend(validator(payload, fixture))
    return issues


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    issues = check(args.root)
    if issues:
        for issue in issues:
            location = f" at {issue.location}" if issue.location else ""
            print(f"FAIL: {issue.fixture.as_posix()}: {issue.kind}{location}", file=sys.stderr)
        return 2 if any(issue.code == 2 for issue in issues) else 1
    print("public evaluation fixtures passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
