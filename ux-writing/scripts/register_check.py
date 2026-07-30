#!/usr/bin/env python3
"""
register_check.py — 문장 끝맺음(어체) 검사. '가능하면' 층의 소프트 게이트.

references/register.md의 표를 읽어, 대상 파일의 경로로 적용할 어체를 정한다.
  - 파일 경로가 '프로젝트 단위' 표의 어떤 경로 밑이면 그 프로젝트 어체
  - 아니면 '전역 기본' 어체
  - 둘 다 (미지정)이면 강제하지 않고 통과 (README 같은 평서체 문서 보호)

그 어체로 끝나지 않는 문장을 잡는다. 명사 종결("저장 완료"), 코드블록, 헤딩,
어미가 또렷하지 않은 조각은 검사에서 빠진다.

경로 해석 주의:
    프로젝트 어체는 '대상 파일의 경로'로 정한다. 출력 파일을 임시 폴더(예:
    /mnt/.../outputs)에 새로 만드는 샌드박스/파일 생성 환경에선 그 경로가 실제
    프로젝트 경로(/Users/...)와 안 맞아 프로젝트 어체가 조용히 안 걸린다. 이럴 땐
    --as 로 실제 적용처를 넘긴다.

사용법:
    python register_check.py <대상파일> [--as <실제적용경로>] [register.md 경로]

    --as <경로>  : 어체 매칭에 쓸 경로를 대상파일 경로 대신 이걸로 본다.
                   (글 내용은 여전히 <대상파일>에서 읽는다.)

종료 코드: 어긋난 문장이 있으면 1, 없으면 0.
"""

import sys
import os
import re

TARGETS = {
    "해요체": "해요", "합니다체": "합니다", "한다체": "한다", "음슴체": "음슴",
    "해요": "해요", "합니다": "합니다", "한다": "한다", "음슴": "음슴", "개조식": "음슴",
}
LABEL = {"해요": "해요체", "합니다": "합니다체", "한다": "한다체", "음슴": "음슴체"}


def find_default_register():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "..", "references", "register.md")


def to_register(s):
    s = re.sub(r"^[_`*]+|[_`*]+$", "", s.strip()).strip()
    if not s or "미지정" in s or s in ("(미지정)", "-", "—"):
        return None
    for key, val in TARGETS.items():
        if key in s:
            return val
    return None


def cells_of(line):
    return [re.sub(r"^[_`*]+|[_`*]+$", "", c.strip()).strip()
            for c in line.split("|")[1:-1]]


def parse_register(path):
    """(전역 어체 or None, [(이름, 절대경로, 어체), ...]) 반환."""
    global_reg, projects = None, []
    if not os.path.exists(path):
        return None, []
    for line in open(path, encoding="utf-8"):
        if "|" not in line:
            continue
        cells = cells_of(line)
        if not cells or all(set(c) <= set("-: ") for c in cells):
            continue
        if len(cells) == 2:
            col0, col1 = cells
            if col0 in ("범위", "어체"):
                continue
            if "전역" in col0:
                global_reg = to_register(col1)
        elif len(cells) >= 3:
            col0, col1, col2 = cells[0], cells[1], cells[2]
            if col0 == "프로젝트":
                continue
            if "(예)" in col0 or not col1 or not col2:
                continue
            reg = to_register(col2)
            if reg:
                ppath = os.path.abspath(os.path.expanduser(col1))
                projects.append((col0, ppath, reg))
    return global_reg, projects


def resolve(resolve_path, global_reg, projects):
    """적용할 (어체, 출처라벨, 프로젝트경로_있는데_안맞음 여부)."""
    tgt = os.path.abspath(os.path.expanduser(resolve_path))
    best, best_len = None, -1
    for name, ppath, reg in projects:
        root = ppath.rstrip(os.sep)
        if tgt == ppath or tgt.startswith(root + os.sep):
            if len(root) > best_len:
                best, best_len = (reg, f"프로젝트 '{name}'"), len(root)
    if best:
        return best[0], best[1], False
    unmatched_projects = bool(projects)
    if global_reg:
        return global_reg, "전역 기본", unmatched_projects
    return None, None, unmatched_projects


def classify(tok):
    if not tok:
        return None
    for suf in ("습니까", "ㅂ니까", "입니까", "니까", "습니다",
                "ㅂ니다", "입니다", "니다", "십시오", "ㅂ시오"):
        if tok.endswith(suf):
            return "합니다"
    if tok.endswith("요"):
        return "해요"
    for suf in ("ㄴ다", "는다", "한다", "된다", "이다", "았다", "었다",
                "였다", "겠다", "린다", "난다", "온다"):
        if tok.endswith(suf):
            return "한다"
    if tok.endswith("다"):
        return "한다"
    return None  # 음슴·명사 종결은 분류하지 않음(명사 오탐 방지)


def last_token(segment):
    s = re.sub(r'[\s"\'”’」』）)\]\.\!\?…,]+$', "", segment.strip())
    return s.split()[-1] if s.split() else ""


def check(text, target):
    lines, hits, inblock = text.splitlines(), [], False
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            inblock = not inblock
            continue
        if inblock:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        body = re.sub(r"^\s*([-*>]|\d+\.)\s+", "", line)
        for seg in re.split(r"[.!?。]\s*", body):
            tok = last_token(seg)
            if not tok or not re.search(r"[가-힣]$", tok):
                continue
            cls = classify(tok)
            if cls is not None and cls != target:
                ctx = stripped if len(stripped) <= 46 else stripped[:44] + "…"
                hits.append((n, cls, tok, ctx))
    return hits


def parse_args(argv):
    """(대상파일, 해석경로, register경로) 반환. --as 플래그 처리."""
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
    reg_path = rest[1] if len(rest) > 1 else find_default_register()
    return target, (as_path or target), reg_path


def main():
    target_file, resolve_path, reg_path = parse_args(sys.argv[1:])
    if target_file is None:
        print("사용법: python register_check.py <대상파일> [--as <실제적용경로>] [register.md 경로]")
        sys.exit(2)

    global_reg, projects = parse_register(reg_path)
    target, source, unmatched = resolve(resolve_path, global_reg, projects)

    print("=" * 52)
    print("  어체(문장 끝맺음) 검사  [가능하면 층]")
    print("=" * 52)

    if resolve_path != target_file:
        print(f"\n  경로 해석 기준: {resolve_path}  (--as)")

    # 프로젝트 어체는 있는데 경로가 하나도 안 맞으면 조용히 넘기지 않고 알린다.
    if unmatched:
        print("\n  ⚠ 프로젝트별 어체가 정의돼 있지만 이 경로엔 하나도 안 걸렸어요.")
        print("    출력 파일을 임시 폴더에 만든 경우일 수 있어요(샌드박스).")
        print("    실제 적용처를 알면 --as <실제경로>로 다시 돌리세요.")

    if target is None:
        print("\n  적용할 어체 없음 — 강제 생략. (전역 기본/프로젝트 어체 미지정)")
        sys.exit(0)

    print(f"\n  적용 어체: {LABEL[target]}  ({source})")

    text = open(target_file, encoding="utf-8").read()
    hits = check(text, target)

    print("\n" + "-" * 52)
    if not hits:
        print(f"  통과. 모든 문장이 {LABEL[target]}이거나 검사 대상이 아님.")
        print("-" * 52)
        sys.exit(0)

    print(f"  어긋난 문장 {len(hits)}건 — {LABEL[target]}로 맞춘다. (의도된 예외면 사람이 판단)")
    print("-" * 52)
    for n, cls, tok, ctx in hits:
        print(f"  L{n}: {LABEL.get(cls, cls)}로 끝남 ('…{tok}')   ({ctx})")
    sys.exit(1)


if __name__ == "__main__":
    main()
