#!/usr/bin/env python3
"""Record why a skill's trigger was changed, and what it scored before and after.

Keeping each trigger change with its reason and score makes repeated divergence
distinguishable from a one-off result. A commit message alone does not provide a
structured comparison across evaluation runs.

Every row pins the SKILL.md blob sha (`git hash-object`, which works before the commit
exists). A verdict whose subject cannot be identified cannot be compared across
revisions, so the sha is required rather than optional.

The ontology's `bin/evals.py` keeps the same three stages for the checker's instructions
— log, review, revise. This is the same discipline applied to a skill's trigger, kept in
this repository because the skill is canonical here.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "evals" / "trigger-revisions.json"
REQUIRED = ("date", "skill", "blob_sha", "reason", "changed")


def blob_sha(path: Path) -> str:
    """Blob sha of the file as it stands now — available before it is committed."""
    result = subprocess.run(
        ["git", "hash-object", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise SystemExit(f"git hash-object failed: {result.stderr.strip()}")
    return result.stdout.strip()


def load(path: Path) -> dict:
    if not path.exists():
        return {"revisions": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload.get("revisions"), list):
        raise SystemExit(f"{path}: 'revisions' must be a list")
    for index, row in enumerate(payload["revisions"]):
        for field in REQUIRED:
            if field not in row:
                raise SystemExit(f"revisions[{index}]: missing '{field}'")
    return payload


def save(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_list(args) -> int:
    payload = load(args.log)
    rows = payload["revisions"]
    if not rows:
        print("개정 이력이 비어 있다.")
        return 0
    for row in rows:
        nudges = row.get("observed_nudges")
        print(f"{row['date']} · {row['skill']} · {row['blob_sha'][:12]}")
        print(f"  이유: {row['reason']}")
        for change in row["changed"]:
            print(f"  고침: {change}")
        runs = row.get("runs") or []
        if not runs:
            print("  성적: 아직 안 재봤다")
        for run in runs:
            print(f"  성적: {run['date']} {run['score']}" + (f" — {run['note']}" if run.get("note") else ""))
            if run.get("report"):
                print(f"        {run['report']}")
        if nudges is not None:
            print(f"  손으로 켠 횟수: {nudges}")
        print()
    return 0


def cmd_score(args) -> int:
    """Attach a run result to the revision that produced it.

    A score is not a revision. One SKILL.md can be measured many times — before and
    after a case is fixed, after a timeout is raised — so a run belongs on the row whose
    blob sha it was measured against, and `add` rightly refuses to invent a new row for
    it. Matching by sha is what makes the before/after comparison mean anything."""
    skill_file = (ROOT / "skills" / args.skill / "SKILL.md").resolve()
    if not skill_file.exists():
        raise SystemExit(f"스킬을 찾을 수 없다: {skill_file}")

    sha = blob_sha(skill_file)
    payload = load(args.log)
    rows = [row for row in payload["revisions"] if row["blob_sha"] == sha and row["skill"] == args.skill]
    if not rows:
        print(
            f"이 판본({sha[:12]})의 개정 행이 없다. 먼저 add 로 무엇을 왜 고쳤는지 남긴다.",
            file=sys.stderr,
        )
        return 1

    row = rows[-1]
    run = {
        "date": args.date or date.today().isoformat(),
        "score": args.score,
        "report": str(args.report) if args.report else None,
        "note": args.note,
    }
    row.setdefault("runs", []).append(run)
    row["trigger_score"] = args.score
    if args.nudges is not None:
        row["observed_nudges"] = args.nudges
    save(args.log, payload)
    print(f"성적 기록: {row['date']} 개정({sha[:12]}) ← {args.score}")
    return 0


def cmd_add(args) -> int:
    skill_file = (ROOT / "skills" / args.skill / "SKILL.md").resolve()
    if not skill_file.exists():
        raise SystemExit(f"스킬을 찾을 수 없다: {skill_file}")

    payload = load(args.log)
    row = {
        "date": args.date or date.today().isoformat(),
        "skill": args.skill,
        "blob_sha": blob_sha(skill_file),
        "reason": args.reason,
        "changed": args.changed,
        "trigger_score": args.score,
        "observed_nudges": args.nudges,
        "report": str(args.report) if args.report else None,
    }
    if any(existing["blob_sha"] == row["blob_sha"] for existing in payload["revisions"]):
        print("같은 blob sha가 이미 기록되어 있다 — SKILL.md가 바뀌지 않았다.", file=sys.stderr)
        return 1

    payload["revisions"].append(row)
    save(args.log, payload)
    print(f"기록: {row['date']} · {args.skill} · {row['blob_sha'][:12]}")
    if row["trigger_score"] is None:
        print("성적이 비어 있다. 개정 전후를 비교하려면 scripts/eval_trigger_cases.py --run 을 돌려 채운다.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    sub = parser.add_subparsers(dest="command", required=True)

    lister = sub.add_parser("list", help="개정 이력을 시간순으로 본다")
    lister.set_defaults(func=cmd_list)

    adder = sub.add_parser("add", help="개정 한 건을 기록한다")
    adder.add_argument("--skill", required=True, help="skills/<이름>")
    adder.add_argument("--reason", required=True, help="왜 고쳤나 — 한 문장")
    adder.add_argument("--changed", required=True, action="append", help="무엇을 고쳤나 (반복 가능)")
    adder.add_argument("--score", help="트리거 케이스 성적, 예: 7/9")
    adder.add_argument("--nudges", type=int, help="이 시점의 손으로 켠 횟수 (trigger_misfire_audit.py)")
    adder.add_argument("--report", type=Path, help="근거 리포트 경로")
    adder.add_argument("--date", help="기본은 오늘")
    adder.set_defaults(func=cmd_add)

    scorer = sub.add_parser("score", help="현재 판본의 개정 행에 실행 성적을 붙인다")
    scorer.add_argument("--skill", required=True, help="skills/<이름>")
    scorer.add_argument("--score", required=True, help="예: 3/9")
    scorer.add_argument("--report", type=Path, help="리포트 경로")
    scorer.add_argument("--note", help="이 실행에서 무엇이 드러났나")
    scorer.add_argument("--nudges", type=int, help="이 시점의 손으로 켠 횟수")
    scorer.add_argument("--date", help="기본은 오늘")
    scorer.set_defaults(func=cmd_score)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
