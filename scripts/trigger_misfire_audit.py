#!/usr/bin/env python3
"""Count the times a user had to invoke the ontology skill by hand.

A request that says "온톨로지 기반으로" is a recall the skill should have started on
its own. Those phrases are therefore the observable trace of a trigger that did not
fire, and this script counts them from the ontology's own request log.

The ontology is read-only here. The script opens the database in `mode=ro` and never
writes, so it can run against a live knowledge base.

Two limits are deliberate and must stay visible:

- **This counts explicit lookup requests, not misfires.** It cannot prove whether the
  skill would have stayed silent. A domain question answered with no recall and no
  explicit request is invisible here because assistant replies are not in this schema.
  The count is neither the number of misfires nor a lower bound for it.
- **Do not tune the patterns to move the number.** The patterns describe explicit
  requests for recall. Narrowing them lowers the count while the underlying
  misfires continue, which is the whole failure mode this measurement exists to expose.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

DEFAULT_DB = Path.home() / ".ontology" / "ontology.db"
DEFAULT_CASES = Path(__file__).resolve().parents[1] / "evals" / "trigger-cases.json"

# Hand-started recall: the user is telling the skill to read what it already should have.
NUDGE_PATTERNS = [
    "온톨로지 기반",
    "온톨로지기반",
    "온톨로지 참고",
    "온톨로지 참조",
    "온톨로지 조회",
    "온톨로지 확인",
    "온톨로지에서 찾",
    "온톨로지에서 검색",
    "온톨로지 봐",
    "온톨로지 보고",
    "온톨로지 읽",
    "온톨로지 뒤져",
    "kb 조회",
    "kb 확인",
]

# Working *on* the ontology. Explicit by nature, so never a missed trigger.
WORK_PATTERNS = [
    "적재",
    "ingest",
    "온톨로지에 넣",
    "온톨로지 스키마",
    "온톨로지 구조",
    "온톨로지 만들",
    "온톨로지 고쳐",
    "온톨로지 수정",
    "테넌트",
    "tenant",
    "docs.py",
    "recall.py",
    "build.py",
    "lint.py",
    "ontology.db",
]

CLASSES = ("nudge", "ontology_work", "mention_only")


def classify(text: str) -> tuple[str, list[str]]:
    """Return the request's class and the patterns that matched it."""
    low = text.lower()
    nudges = [p for p in NUDGE_PATTERNS if p in low]
    if nudges:
        return "nudge", nudges
    work = [p for p in WORK_PATTERNS if p in low]
    if work:
        return "ontology_work", work
    return "mention_only", []


def resolve_tenants(conn: sqlite3.Connection, keys: list[str]) -> list[str]:
    known = {row[0] for row in conn.execute("SELECT key FROM tenants")}
    unknown = [key for key in keys if key not in known]
    if unknown:
        raise SystemExit(
            f"unknown tenant(s): {', '.join(unknown)} — known: {', '.join(sorted(known))}"
        )
    return keys


def case_requests(path: Path) -> set[str]:
    """Requests the trigger eval sends itself.

    Running the eval leaves its own prompts in the request log, and those would then be
    counted as observations of the very behavior they measure. Excluding them by exact
    text keeps the measurement independent of how often it is taken."""
    if not path.exists():
        raise SystemExit(
            f"제외할 시험 케이스 파일을 찾을 수 없다: {path} "
            "(--cases 로 지정하거나 --no-exclude 사용)"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {" ".join(case["request"].split()) for case in payload.get("cases", [])}


def collect(conn: sqlite3.Connection, tenants: list[str], excluded: set[str]) -> tuple[list[dict], int]:
    placeholders = ",".join("?" for _ in tenants)
    rows = conn.execute(
        f"""
        SELECT tn.key, r.ts, s.title, s.cwd, r.text, r.session_id, r.id
        FROM fts_requests f
        JOIN requests r ON r.id = f.request_id
        JOIN sessions s ON s.session_id = f.session_id
        JOIN tenants tn ON tn.id = s.tenant_id
        WHERE fts_requests MATCH '온톨로지 OR KB'
          AND tn.key IN ({placeholders})
        ORDER BY r.ts
        """,
        tenants,
    ).fetchall()

    hits = []
    skipped = 0
    for tenant, ts, title, cwd, text, session_id, request_id in rows:
        text = " ".join((text or "").split())
        if text in excluded:
            skipped += 1
            continue
        kind, matched = classify(text)
        hits.append(
            {
                "tenant": tenant,
                "ts": ts,
                "month": month_of(ts),
                "session_title": title,
                "cwd": cwd,
                "session_id": session_id,
                "request_id": request_id,
                "kind": kind,
                "matched": matched,
                "text": text,
            }
        )
    return hits, skipped


def month_of(ts: str | None) -> str:
    """Bucket by month, keeping non-timestamp ts values visible instead of sorting them
    into a fake month — some early rows carry an ordinal instead of a date."""
    if ts and re.fullmatch(r"\d{4}-\d{2}.*", ts):
        return ts[:7]
    return "(시점 미상)"


def repo_of(cwd: str | None) -> str:
    if not cwd:
        return "(unknown)"
    return Path(cwd).name or cwd


def report(hits: list[dict], tenants: list[str], sample: int, skipped: int) -> None:
    by_kind = Counter(hit["kind"] for hit in hits)
    nudges = [hit for hit in hits if hit["kind"] == "nudge"]

    print(f"스코프: {' + '.join(tenants)} · 요청 {len(hits)}건" + (f" · 시험 케이스 실행 {skipped}건 제외" if skipped else ""))
    print()
    print("■ 분류")
    for kind in CLASSES:
        print(f"  {kind:<14} {by_kind.get(kind, 0):>4}")
    print()

    if not nudges:
        print("손으로 켠 흔적 0건 — 이 스코프에서는 트리거 미발동의 근거가 없다.")
        return

    print(f"■ 손으로 켠 요청 {len(nudges)}건 — 월별")
    for month, count in sorted(Counter(hit["month"] for hit in nudges).items()):
        print(f"  {month}  {'█' * count} {count}")
    print()

    print("■ 어디서 일어났나 (작업 디렉터리)")
    for repo, count in Counter(repo_of(hit["cwd"]) for hit in nudges).most_common():
        print(f"  {count:>3}  {repo}")
    print()

    print(f"■ 표본 (최근 {min(sample, len(nudges))}건 — 시험 케이스 후보)")
    for hit in nudges[-sample:]:
        head = hit["text"][:96]
        stamp = hit["ts"][:10] if hit["month"] != "(시점 미상)" else "시점 미상"
        print(f"  {stamp} · {'/'.join(hit['matched'])}")
        print(f"    {head}")
    print()
    print("이 수치를 낮추는 방향으로 패턴을 고치지 않는다. 패턴은 명시적 조회 요청 표현이고,")
    print("좁히면 미발동은 그대로인데 숫자만 내려간다.")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--tenant",
        required=True,
        help="쉼표로 구분한 tenant 키. 스코프를 밝히지 않는 집계는 만들지 않는다.",
    )
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--sample", type=int, default=12, help="표본으로 출력할 최근 건수")
    parser.add_argument("--json", type=Path, help="전체 히트를 JSON으로 저장할 경로")
    parser.add_argument(
        "--cases",
        type=Path,
        default=DEFAULT_CASES,
        help="이 파일의 케이스 문구와 똑같은 요청은 시험 실행으로 보고 제외한다",
    )
    parser.add_argument("--no-exclude", action="store_true", help="시험 실행도 함께 센다")
    args = parser.parse_args(argv)

    if not args.db.exists():
        print(f"온톨로지를 찾을 수 없다: {args.db}", file=sys.stderr)
        return 1

    keys = [key.strip() for key in args.tenant.split(",") if key.strip()]
    if not keys:
        print("--tenant 가 비어 있다", file=sys.stderr)
        return 1

    conn = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    try:
        tenants = resolve_tenants(conn, keys)
        excluded = set() if args.no_exclude else case_requests(args.cases)
        hits, skipped = collect(conn, tenants, excluded)
    finally:
        conn.close()

    report(hits, tenants, args.sample, skipped)

    if args.json:
        args.json.write_text(
            json.dumps({"tenants": tenants, "hits": hits}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"저장: {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
