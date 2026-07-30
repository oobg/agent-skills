#!/usr/bin/env python3
"""
glossary_check.py — 프로젝트 고정 표기 검사.

references/glossary.md의 두 표를 읽어, 대상 글에서 '일반 표현'(쓰면 안 되는 쪽)을
그대로 쓴 곳을 찾는다.
  - 전역 표기: 모든 글에 적용
  - 프로젝트별 표기: 대상 파일이 그 경로 밑일 때만 적용 (전역과 함께)
둘 다 비어 있으면 검사를 생략하고 통과한다.

ai_lint.py가 보편적 기계 티를 본다면, 이건 이 프로젝트에서만 통하는 표기를 본다.

경로 해석 주의:
    프로젝트별 표기는 '대상 파일의 경로'로 적용 여부를 정한다. 레포 안에서 직접
    편집할 땐 맞지만, 출력 파일을 임시 폴더(예: /mnt/.../outputs)에 새로 만드는
    샌드박스/파일 생성 환경에선 그 경로가 실제 프로젝트 경로(/Users/...)와 안 맞아
    프로젝트 규칙이 조용히 안 걸린다. 이럴 땐 --as 로 실제 적용처를 넘긴다.

사용법:
    python glossary_check.py <대상파일> [--as <실제적용경로>] [glossary.md 경로]

    --as <경로>  : 프로젝트 매칭에 쓸 경로를 대상파일 경로 대신 이걸로 본다.
                   (글 내용은 여전히 <대상파일>에서 읽는다.)

종료 코드: 위반이 있으면 1, 없으면 0.
"""

import sys
import os
import re


def find_default_glossary():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "..", "references", "glossary.md")


def cells_of(line):
    return [re.sub(r"^[_`*]+|[_`*]+$", "", c.strip()).strip()
            for c in line.split("|")[1:-1]]


def is_placeholder(s):
    return (not s) or s.startswith("(아직") or "아직 없음" in s or "(예)" in s


def parse_glossary(path):
    """(전역 [(일반,표기)], 프로젝트 [(이름, 절대경로, 일반, 표기)]) 반환."""
    global_pairs, project_pairs = [], []
    if not os.path.exists(path):
        return [], []
    for line in open(path, encoding="utf-8"):
        if "|" not in line:
            continue
        cells = cells_of(line)
        if not cells or all(set(c) <= set("-: ") for c in cells):
            continue
        if len(cells) == 3:                       # 전역 표기: 일반 | 표기 | 비고
            general, project_term = cells[0], cells[1]
            if general in ("일반 표현",) or is_placeholder(general) or not project_term:
                continue
            global_pairs.append((general, project_term))
        elif len(cells) >= 4:                      # 프로젝트별: 이름 | 경로 | 일반 | 표기
            name, ppath, general, term = cells[0], cells[1], cells[2], cells[3]
            if name in ("프로젝트",) or is_placeholder(name):
                continue
            if not ppath or not general or not term:
                continue
            project_pairs.append((name, os.path.abspath(os.path.expanduser(ppath)),
                                  general, term))
    return global_pairs, project_pairs


def resolve_pairs(resolve_path, global_pairs, project_pairs):
    """전역 + (경로가 맞는 프로젝트) 표기 쌍과, 매칭된 프로젝트 이름을 합친다."""
    tgt = os.path.abspath(os.path.expanduser(resolve_path))
    pairs = list(global_pairs)
    matched = []
    for name, ppath, general, term in project_pairs:
        root = ppath.rstrip(os.sep)
        if tgt == ppath or tgt.startswith(root + os.sep):
            pairs.append((general, term))
            matched.append(name)
    return pairs, matched


def spans(text, term):
    out, start = [], 0
    while True:
        i = text.find(term, start)
        if i < 0:
            break
        out.append((i, i + len(term)))
        start = i + 1
    return out


def check(text, pairs):
    lines, hits = text.splitlines(), []
    for n, line in enumerate(lines, 1):
        for general, term in pairs:
            if general not in line:
                continue
            term_spans = spans(line, term) if general in term else []
            for s, e in spans(line, general):
                if any(ps <= s and e <= pe for ps, pe in term_spans):
                    continue
                ctx = line.strip()
                if len(ctx) > 50:
                    j = line.find(general)
                    ctx = ("…" if j > 20 else "") + line[max(0, j - 20):j + 30].strip() + "…"
                hits.append((n, general, term, ctx))
    return hits


def parse_args(argv):
    """(대상파일, 해석경로, glossary경로) 반환. --as 플래그 처리."""
    as_path, rest, i = None, [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--as":
            i += 1
            as_path = argv[i] if i < len(argv) else None
        elif a.startswith("--as="):
            as_path = a[len("--as="):]
        else:
            rest.append(a)
        i += 1
    if not rest:
        return None, None, None
    target = rest[0]
    glossary_path = rest[1] if len(rest) > 1 else find_default_glossary()
    return target, (as_path or target), glossary_path


def main():
    target, resolve_path, glossary_path = parse_args(sys.argv[1:])
    if target is None:
        print("사용법: python glossary_check.py <대상파일> [--as <실제적용경로>] [glossary.md 경로]")
        sys.exit(2)

    global_pairs, project_pairs = parse_glossary(glossary_path)
    pairs, matched = resolve_pairs(resolve_path, global_pairs, project_pairs)

    print("=" * 52)
    print("  프로젝트 고정 표기 검사")
    print("=" * 52)

    if resolve_path != target:
        print(f"\n  경로 해석 기준: {resolve_path}  (--as)")

    # 프로젝트 규칙은 있는데 경로가 하나도 안 맞으면 조용히 넘기지 않고 경고한다.
    if project_pairs and not matched:
        print("\n  ⚠ 프로젝트별 표기가 정의돼 있지만 이 경로엔 하나도 안 걸렸어요.")
        print("    출력 파일을 임시 폴더에 만든 경우일 수 있어요(샌드박스).")
        print("    실제 적용처를 알면 --as <실제경로>로 다시 돌리세요.")
        print("    지금은 전역 표기만 검사합니다.")

    if not pairs:
        print("\n  적용할 표기 없음 — 검사 생략 (전역/프로젝트 표기 미지정).")
        sys.exit(0)

    print(f"\n  적용 규칙 {len(pairs)}개: " +
          ", ".join(f"{g}→{p}" for g, p in pairs[:8]) +
          (" …" if len(pairs) > 8 else ""))

    text = open(target, encoding="utf-8").read()
    hits = check(text, pairs)

    print("\n" + "-" * 52)
    if not hits:
        print("  통과. 표준 표기를 어긴 곳 없음.")
        print("-" * 52)
        sys.exit(0)

    print(f"  위반 {len(hits)}건 — 일반 표현 대신 프로젝트 표기로 고친다.")
    print("-" * 52)
    for n, general, term, ctx in hits:
        print(f"  L{n}: '{general}' → '{term}'   ({ctx})")
    sys.exit(1)


if __name__ == "__main__":
    main()
