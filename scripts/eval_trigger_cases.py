#!/usr/bin/env python3
"""Run the trigger cases and check whether the ontology skill actually fires.

`eval_skill_contracts.py` reads SKILL.md and proves the rule is *written*. This script
sends a real request to a real agent and looks at what came back, which is the only way
to see whether the rule *fires*. Under-triggering lives in that gap.

Grading uses one proxy: `recall.md` requires a `근거:` line on an answer grounded in the
knowledge base, so this runner checks for that line. The proxy can produce false
positives or false negatives; it does not independently prove that a lookup happened.

Each case costs one agent session, so a plain run only prints the plan. `--run` is the
flag that spends usage.

The runner accepts an argv template instead of assuming a particular agent CLI. Put the
provider's transcript-isolation option in that template when one exists. This runner
cannot verify external hooks or logs, so the audit excludes exact eval case text from
its measurement and never copies response text or command arguments into its report.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "trigger-cases.json"
DEFAULT_REPORTS = ROOT / "evals" / "reports"
EXPECTATIONS = {"recall", "skip"}
EVIDENCE_MARK = "근거:"
REQUEST_PLACEHOLDER = "{request}"


def load_cases(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"케이스 파일을 찾을 수 없다: {path} (--cases 로 지정)")
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise SystemExit(f"{path}: 'cases' must be a non-empty list")
    seen = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise SystemExit(f"case[{index}]: must be an object")
        label = case.get("id") or f"case[{index}]"
        for field in ("id", "expect", "request", "origin"):
            if not isinstance(case.get(field), str) or not case[field]:
                raise SystemExit(f"{label}: '{field}' must be a non-empty string")
        if case["expect"] not in EXPECTATIONS:
            raise SystemExit(f"{label}: 'expect' must be one of {', '.join(sorted(EXPECTATIONS))}")
        if case["id"] in seen:
            raise SystemExit(f"{label}: duplicate id")
        seen.add(case["id"])
    return payload


def grade(case: dict, output: str) -> tuple[bool, str]:
    cited = EVIDENCE_MARK in output
    if case["expect"] == "recall":
        return cited, "근거 줄 있음" if cited else "근거 줄 없음 — 조회 흔적 없음"
    return not cited, "조회 없이 진행" if not cited else "차단 케이스인데 조회함"


def case_cwd(case: dict, fallback: Path) -> tuple[Path, bool]:
    """Where to run the case. The observed repository is the point — a case seen in a
    code repository must be asked inside one — so fall back only when it is missing."""
    declared = case.get("cwd")
    if not declared:
        return fallback, True
    path = Path(declared).expanduser()
    if not path.is_dir():
        return fallback, False
    return path, True


def command_template(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--command-json must be a JSON argv array: {exc}")
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise SystemExit("--command-json must be a non-empty JSON array of non-empty strings")
    if REQUEST_PLACEHOLDER in value[0]:
        raise SystemExit(f"--command-json executable cannot contain {REQUEST_PLACEHOLDER!r}")
    if sum(item.count(REQUEST_PLACEHOLDER) for item in value) != 1:
        raise SystemExit(f"--command-json must contain {REQUEST_PLACEHOLDER!r} exactly once")
    return value


def build_command(template: list[str], request: str) -> list[str]:
    return [item.replace(REQUEST_PLACEHOLDER, request) for item in template]


def plan(payload: dict, cases: list[dict], fallback: Path, template: list[str] | None) -> None:
    wanted = sum(1 for case in cases if case["expect"] == "recall")
    print(f"스킬: {payload.get('skill')} · 케이스 {len(cases)}건 (조회 기대 {wanted} · 차단 기대 {len(cases) - wanted})")
    print()
    missing = []
    for case in cases:
        mark = "조회" if case["expect"] == "recall" else "차단"
        path, found = case_cwd(case, fallback)
        if not found:
            missing.append(case["id"])
        print(f"  [{mark}] {case['id']:<24} {path}{'  ← 없어서 폴백' if not found else ''}")
        print(f"         {case['request'][:88]}")
    print()
    if missing:
        print(f"경고: 선언된 디렉터리가 없어 폴백한 케이스 {len(missing)}건 — {', '.join(missing)}")
        print("      관측된 저장소 밖에서 돌면 코드 저장소 안의 판단이라는 조건이 빠진다.")
        print()
    print(f"실행하면 케이스마다 에이전트 세션 하나가 뜬다 — 총 {len(cases)}회, 사용량이 차감된다.")
    print("실행 provider의 transcript 비저장 옵션은 --command-json 템플릿에 직접 넣는다.")
    print("외부 훅과 별도 로그의 동작은 이 도구가 검증하지 않으므로 실행 환경에서 확인해야 한다.")
    if template:
        print(f"실행 파일: {template[0]} (인자는 출력하거나 리포트에 저장하지 않음)")
    else:
        print(f"실행할 때 --command-json '[\"<agent>\", \"...\", \"{REQUEST_PLACEHOLDER}\"]'을 지정한다.")
    print("실제로 채점하려면 --run 을 붙인다.")


def run_case(case: dict, fallback: Path, template: list[str], timeout: int) -> dict:
    started = time.time()
    cwd, found = case_cwd(case, fallback)
    try:
        completed = subprocess.run(
            build_command(template, case["request"]),
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = completed.stdout or ""
        error = ""
        if completed.returncode:
            error = f"exit code {completed.returncode}"
    except FileNotFoundError:
        raise SystemExit(f"에이전트 실행 파일을 찾을 수 없다: {template[0]}")
    except subprocess.TimeoutExpired:
        output, error = "", f"timeout after {timeout}s"

    passed, reason = grade(case, output)
    if error:
        passed, reason = False, f"실행 실패: {error}"
    return {
        "id": case["id"],
        "expect": case["expect"],
        "origin": case["origin"],
        "cwd": str(cwd),
        "cwd_as_declared": found,
        "passed": passed,
        "reason": reason,
        "elapsed_s": round(time.time() - started, 1),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--case", action="append", help="이 id만 실행 (반복 가능)")
    parser.add_argument("--run", action="store_true", help="실제로 에이전트를 호출한다 (사용량 차감)")
    parser.add_argument(
        "--command-json",
        help=f"에이전트 argv JSON 배열. {REQUEST_PLACEHOLDER!r}를 정확히 한 번 포함한다",
    )
    parser.add_argument("--agent", dest="removed_agent", help=argparse.SUPPRESS)
    parser.add_argument("--cwd", type=Path, default=ROOT, help="케이스에 선언된 디렉터리가 없을 때 쓸 폴백")
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="케이스당 상한. 너무 짧으면 트리거 결과 대신 타임아웃을 채점할 수 있다",
    )
    parser.add_argument("--out", type=Path, help="리포트 JSON 경로 (기본: evals/reports/trigger-<날짜>.json)")
    args = parser.parse_args(argv)
    if args.removed_agent:
        parser.error("--agent was replaced by --command-json; pass the complete provider argv template")
    template = command_template(args.command_json)

    payload = load_cases(args.cases)
    cases = payload["cases"]
    if args.case:
        wanted = set(args.case)
        cases = [case for case in cases if case["id"] in wanted]
        missing = wanted - {case["id"] for case in cases}
        if missing:
            raise SystemExit(f"unknown case id(s): {', '.join(sorted(missing))}")

    if not args.run:
        plan(payload, cases, args.cwd.resolve(), template)
        return 0

    if template is None:
        parser.error("--run requires --command-json; --agent was replaced by a provider-neutral argv template")

    results = []
    for index, case in enumerate(cases, 1):
        print(f"[{index}/{len(cases)}] {case['id']} … ", end="", flush=True)
        result = run_case(case, args.cwd.resolve(), template, args.timeout)
        results.append(result)
        print(f"{'PASS' if result['passed'] else 'FAIL'} — {result['reason']} ({result['elapsed_s']}s)")

    passed = sum(1 for result in results if result["passed"])
    print()
    print(f"통과 {passed}/{len(results)}")
    for result in results:
        if not result["passed"]:
            print(f"  FAIL {result['id']}: {result['reason']}")

    out = args.out or DEFAULT_REPORTS / f"trigger-{date.today().isoformat()}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "skill": payload.get("skill"),
                "ran_on": date.today().isoformat(),
                "fallback_cwd": str(args.cwd.resolve()),
                "runner": Path(template[0]).name,
                "passed": passed,
                "total": len(results),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"리포트: {out}")
    print("이 성적을 개정 이력에 남긴다: scripts/trigger_revisions.py add --help")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
