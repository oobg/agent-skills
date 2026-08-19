#!/usr/bin/env python3
"""Promote and park canonical skills using ontology observations.

The ontology is read-only. This script owns only provider symlinks that resolve
to this repository's skills directory.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "lifecycle.json"
VALID_STATES = {"candidate", "active", "pinned", "parked", "retired"}


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text())
    if config.get("version") != 1:
        raise ValueError("unsupported lifecycle config version")
    unknown = {
        item.get("status")
        for item in config.get("skills", {}).values()
        if item.get("status") not in VALID_STATES
    }
    if unknown:
        raise ValueError(f"invalid skill status: {sorted(unknown)}")
    for name, classification in config.get("candidate_classifications", {}).items():
        if not isinstance(classification, dict):
            raise ValueError(f"invalid candidate classification for {name!r}")
        if classification.get("kind") != "procedure":
            raise ValueError(f"candidate {name!r} must have kind 'procedure'")
        if classification.get("reusable") is not True:
            raise ValueError(f"candidate {name!r} must be explicitly reusable")
        rationale = classification.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError(f"candidate {name!r} must include a rationale")
    return config


def cutoff(days: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).isoformat()


def query_rows(db_path: Path, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
    uri = f"file:{db_path}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        conn.row_factory = sqlite3.Row
        return list(conn.execute(sql, params))


def skill_usage(config: dict) -> dict[str, dict[str, int]]:
    db = Path(config["ontology_db"]).expanduser()
    days = config["thresholds"]["park_after_days"]
    rows = query_rows(
        db,
        """
        SELECT sk.name,
               SUM(ss.count) AS total_uses,
               SUM(CASE WHEN s.last_ts >= ? THEN ss.count ELSE 0 END) AS recent_uses,
               COUNT(DISTINCT ss.session_id) AS sessions
        FROM session_skills ss
        JOIN skills sk ON sk.id = ss.skill_id
        JOIN sessions s ON s.session_id = ss.session_id
        GROUP BY sk.id
        """,
        (cutoff(days),),
    )
    return {row["name"]: dict(row) for row in rows}


def repeated_concepts(config: dict) -> list[dict]:
    """Return frequent concepts as observations, not inferred skill candidates."""
    db = Path(config["ontology_db"]).expanduser()
    threshold = config["thresholds"]["candidate_min_sessions"]
    days = config["thresholds"]["candidate_window_days"]
    excluded = set(config.get("candidate_exclusions", []))
    existing = set(config.get("skills", {}))
    rows = query_rows(
        db,
        """
        SELECT c.name, COUNT(DISTINCT sc.session_id) AS recent_sessions
        FROM concepts c
        JOIN session_concepts sc ON sc.concept_id = c.id
        JOIN sessions s ON s.session_id = sc.session_id
        WHERE s.last_ts >= ?
        GROUP BY c.id
        HAVING recent_sessions >= ?
        ORDER BY recent_sessions DESC, c.name
        """,
        (cutoff(days), threshold),
    )
    return [
        dict(row)
        for row in rows
        if row["name"] not in excluded and row["name"] not in existing
    ]


def concept_candidates(config: dict) -> list[dict]:
    """Return only concepts explicitly reviewed as procedural and reusable.

    Frequency alone says that a subject recurs; it does not establish an
    input/action/check/stop procedure that can be packaged as a skill.  Keep
    that distinction conservative by requiring a human-maintained
    classification in lifecycle.json.
    """
    classifications = config.get("candidate_classifications", {})
    candidates = []
    for item in repeated_concepts(config):
        classification = classifications.get(item["name"], {})
        if (
            classification.get("kind") != "procedure"
            or classification.get("reusable") is not True
        ):
            continue
        candidates.append(
            {
                **item,
                "rationale": classification["rationale"],
            }
        )
    return candidates


def expected_links(config: dict) -> list[tuple[str, Path, Path]]:
    result = []
    for name, meta in sorted(config.get("skills", {}).items()):
        if meta["status"] not in {"active", "pinned"}:
            continue
        source = (ROOT / "skills" / name).resolve()
        for provider in meta.get("providers", []):
            result.append(
                (provider, Path(config["providers"][provider]).expanduser() / name, source)
            )
    return result


def owned_link(link: Path, source: Path) -> bool:
    return link.is_symlink() and link.resolve(strict=False) == source


def sync(config: dict, apply: bool) -> int:
    errors = 0
    expected = {(link, source) for _, link, source in expected_links(config)}

    for provider, link, source in expected_links(config):
        if not (source / "SKILL.md").is_file():
            print(f"ERROR missing canonical skill: {source}", file=sys.stderr)
            errors += 1
            continue
        if owned_link(link, source):
            print(f"ok     {provider:7} {link}")
            continue
        if os.path.lexists(link):
            print(f"ERROR unmanaged target exists: {link}", file=sys.stderr)
            errors += 1
            continue
        print(f"{'link' if apply else 'would-link':10} {provider:7} {link} -> {source}")
        if apply:
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(source, target_is_directory=True)

    canonical = (ROOT / "skills").resolve()
    for provider, folder in config.get("providers", {}).items():
        base = Path(folder).expanduser()
        if not base.is_dir():
            continue
        for link in base.iterdir():
            if not link.is_symlink():
                continue
            target = link.resolve(strict=False)
            if canonical not in target.parents:
                continue
            if (link, target) in expected:
                continue
            print(f"{'unlink' if apply else 'would-unlink':12} {provider:7} {link}")
            if apply:
                link.unlink()
    return errors


def report(config: dict) -> None:
    usage = skill_usage(config)
    max_recent = config["thresholds"]["park_max_recent_uses"]
    print("SKILLS")
    for name, meta in sorted(config.get("skills", {}).items()):
        counts = usage.get(name, {})
        measured = name in usage
        recent = counts.get("recent_uses", 0) or 0
        suggestion = ""
        if measured and meta["status"] == "active" and recent <= max_recent:
            suggestion = " -> review-for-parking"
        if not measured:
            suggestion = " -> unmeasured; never auto-park"
        print(
            f"{name:28} {meta['status']:8} "
            f"total={counts.get('total_uses', 0) or 0:4} "
            f"recent={recent:4}{suggestion}"
        )

    print("\nSKILL CANDIDATES (explicit procedure + reusable)")
    candidates = concept_candidates(config)
    if not candidates:
        print("(none)")
    for item in candidates:
        print(
            f"{item['name']:28} sessions={item['recent_sessions']} "
            f"rationale={item['rationale']}"
        )

    print("\nREPEATED CONCEPTS (signals only; not skill candidates)")
    observations = repeated_concepts(config)
    if not observations:
        print("(none)")
    for item in observations:
        if any(candidate["name"] == item["name"] for candidate in candidates):
            continue
        print(f"{item['name']:28} sessions={item['recent_sessions']}")

    print("\nLINK PLAN")
    sync(config, apply=False)


def doctor(config: dict) -> int:
    errors = sync(config, apply=False)
    db = Path(config["ontology_db"]).expanduser()
    if not db.is_file():
        print(f"ERROR ontology DB not found: {db}", file=sys.stderr)
        errors += 1
    for name in config.get("skills", {}):
        if not (ROOT / "skills" / name / "SKILL.md").is_file():
            print(f"ERROR skill missing SKILL.md: {name}", file=sys.stderr)
            errors += 1
    print(f"doctor: {'PASS' if errors == 0 else f'FAIL ({errors})'}")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("report")
    sync_parser = sub.add_parser("sync")
    sync_parser.add_argument("--apply", action="store_true")
    sub.add_parser("doctor")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.command == "report":
        report(config)
        return 0
    if args.command == "sync":
        return 1 if sync(config, args.apply) else 0
    return doctor(config)


if __name__ == "__main__":
    raise SystemExit(main())
