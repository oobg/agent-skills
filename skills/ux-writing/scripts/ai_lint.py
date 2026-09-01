#!/usr/bin/env python3
"""
ai_lint.py — UX 라이팅 스킬의 '기계적 AI 티' 린트 게이트.

판단이 필요 없이 결정적으로 잡히는 티만 검사한다.
(의미 과장, 부정 병렬, 사무체 같은 판단형 티는 사람이 읽어야 하므로 여기서 다루지 않는다.)

쓰는 이유: 이런 티는 "안다"고 안 잡힌다. 생성 시점엔 내용에 집중하느라 떠오르지 않기
때문이다. 그래서 내보내기 직전에 무조건 돌리는 게이트로 만든다.

사용법:
    python3 ai_lint.py <파일경로>
    echo "...텍스트..." | python3 ai_lint.py -

종료 코드: HARD 항목이 하나라도 있으면 1 (출력 보류), 없으면 0 (통과).
ADVISORY 항목은 종료 코드에 영향을 주지 않고 참고용으로만 보고한다.
"""

import sys
import re
import os
import json

# --- 패턴 정의는 patterns.json에서 읽는다 ---
# 코드를 안 고치고 데이터만 고쳐서 패턴을 넣고 뺄 수 있게 분리했다.
# (about.md의 '가지치기 원칙' — 안 걸리는 패턴은 빼고, 걸린 패턴은 status로 표시)
PATTERNS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patterns.json")

MIDDLE_DOTS = "·・ㆍ‧"

# 코드블록/인라인 코드 — 검사에서 제외한다.
# 코드블록엔 명령어, 파일 트리, '일부러 티 나게 쓴 나쁜 예시'가 들어간다.
# 이걸 잡으면 예시 있는 문서는 게이트를 영영 못 지나서 게이트가 소음이 된다.
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")

# 마크업 태그 — 문장이 아니라 구조라서 검사에서 제외한다.
# `</td>` 같은 줄은 마지막 글자가 '>'라서 종결어미 검사가 '>'를 어미로 오인한다.
# 확장자로 마크업 파일임이 분명할 때만 적용한다. 마크다운은 **볼드**·리스트가
# 검사 대상 자체라서 제외 대상이 아니고, stdin(-)은 확장자가 없어 판단 근거가 없다.
MARKUP_EXTS = {".html", ".htm", ".jsx", ".tsx", ".vue"}
# 주석은 태그보다 먼저 지운다. `<!-- 1 > 2 -->`의 부등호를 태그 규칙에 맡기면
# 앞부분만 잘려 나가고 `2 -->`가 검사 입력에 남는다.
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# 태그 시작을 엄격히 본다. '<' 다음에 태그명 시작 문자(영문자, /, !, ?)가 와야
# 태그로 인정한다. 그래야 산문의 부등호 쌍을 태그로 오인해 문장을 지우지 않는다 —
# `재고가 10 < 20 이고 판매가 30 > 5`의 '< 20'은 공백이 뒤따라 매칭되지 않는다.
# 산문을 마스킹하면 그 안의 진짜 티를 놓친다. 과다 마스킹이 과소 마스킹보다 나쁘다.
# 따옴표로 감싼 속성값 안의 부등호는 태그를 끝내지 않는다 — `<div title="1 > 0">`.
# 각 대안이 첫 글자로 갈리므로(따옴표냐 아니냐) 위치마다 선택이 하나뿐이고,
# 백트래킹이 폭발하지 않는다.
# 알려진 한계: JSX 중괄호 표현식(`<Component value={a > b}>`)은 첫 부등호에서
# 잘린다. 중괄호 중첩은 정규식으로 온전히 못 가른다. 파서를 들이지 않기로 한
# 결정에 따라 의도된 경계로 둔다 — 잔여물이 남을 뿐 줄·열 위치는 보존된다.
TAG_RE = re.compile(r"""</?[A-Za-z!?](?:[^<>"']|"[^"]*"|'[^']*')*>""", re.S)


def load_patterns():
    with open(PATTERNS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    if data.get("version") != "1.0" or not isinstance(data.get("patterns"), list):
        raise ValueError("patterns.json은 version 1.0과 patterns 배열이 필요합니다")
    allowed_layers = {"hard", "advisory"}
    allowed_statuses = {"verified", "experimental"}
    seen_ids, seen_labels = set(), set()
    out = []
    # 패턴 하나에서 바로 멈추면 뒤 패턴의 오류가 영영 안 보인다.
    # patterns[0]의 문제 때문에 patterns[1]의 id 중복을 못 보는 식이다.
    # 그래서 치명 오류는 모아 두고 루프가 끝난 뒤 한 번에 보고한다.
    errors, warnings = [], []
    for index, p in enumerate(data["patterns"], 1):
        if not isinstance(p, dict):
            errors.append(f"pattern #{index}는 객체여야 합니다")
            continue
        missing = {"id", "label", "regex", "layer", "status"} - set(p)
        if missing:
            # 필수 필드가 없으면 이후 검증이 성립하지 않는다. 이 패턴만 건너뛴다.
            errors.append(f"pattern #{index} 필수 필드 누락: {', '.join(sorted(missing))}")
            continue

        # 한 패턴의 오류는 problems에 모아 errors로 넘긴 뒤 그 패턴을 건너뛴다.
        # 오류를 담기만 하고 계속 진행하면 잘못된 값이 뒤 코드로 흘러가
        # TypeError로 터진다 — 설정 오류는 exit 2로 끝나야 하므로 반드시 건너뛴다.
        problems = []

        # 타입을 가장 먼저 본다. id/label이 리스트 같은 비해시 값이면
        # 중복 검사의 집합 조회 자체가 TypeError를 낸다.
        for key in ("id", "label", "regex", "layer", "status"):
            if not isinstance(p[key], str):
                problems.append(f"pattern #{index}의 {key}는 문자열이어야 합니다: {p[key]!r}")
        if problems:
            errors.extend(problems)
            continue

        # 여기부터 다섯 필수 필드가 모두 문자열이라 집합 조회·비교가 안전하다.
        if p["id"] in seen_ids or p["label"] in seen_labels:
            problems.append(f"pattern #{index}의 id 또는 label이 중복됩니다: {p['id']}")
        if p["layer"] not in allowed_layers:
            problems.append(f"pattern {p['id']}의 layer가 잘못됐습니다: {p['layer']}")
        if p["status"] not in allowed_statuses:
            problems.append(f"pattern {p['id']}의 status가 잘못됐습니다: {p['status']}")
        raw_flags = p.get("flags", "")
        if not isinstance(raw_flags, str) or raw_flags not in ("", "M"):
            problems.append(f"pattern {p['id']}의 flags가 잘못됐습니다: {raw_flags!r}")
        threshold = p.get("threshold")
        if threshold is not None and (not isinstance(threshold, int) or threshold < 1):
            problems.append(f"pattern {p['id']}의 threshold는 양의 정수여야 합니다")
        if problems:
            errors.extend(problems)
            continue

        # ref는 사람이 읽을 참조 문서 링크다. 없어도 린트는 돈다 — 경고로만 남긴다.
        # 타입이 틀려도 경고에 그친다. 치명이 아닌 항목이 린트를 멈추면 안 된다.
        ref = p.get("ref")
        if isinstance(ref, str) and ref.strip():
            ref_name = ref.split()[0]
            ref_path = os.path.join(os.path.dirname(PATTERNS_PATH), "..", "references", ref_name)
            if not os.path.isfile(ref_path):
                warnings.append(f"pattern {p['id']}의 ref 문서가 없습니다: {ref_name}")
        elif ref is not None:
            warnings.append(f"pattern {p['id']}의 ref가 문서 이름이 아닙니다: {ref!r}")

        seen_ids.add(p["id"])
        seen_labels.add(p["label"])
        flags = re.M if "M" in raw_flags else 0
        try:
            compiled = re.compile(p["regex"], flags)
        except re.error as exc:
            errors.append(f"pattern {p['id']}의 regex가 잘못됐습니다: {exc}")
            continue
        out.append({**p, "_rx": compiled})

    for w in warnings:
        print(f"UX lint 경고: {w}", file=sys.stderr)
    if errors:
        raise ValueError(
            f"patterns.json 오류 {len(errors)}건:\n" + "\n".join(f"  - {e}" for e in errors)
        )
    return out


def is_hamnida(s):
    """'니다/니까'로 끝나는 게 합니다체인지 판별.

    '아니다'처럼 니다로 끝나도 합니다체가 아닌 말이 있다. 합니다체(습니다/입니다/
    합니다/갑니다...)는 '니다' 바로 앞 글자의 받침이 항상 ㅂ이라는 규칙으로 가른다.
    """
    m = re.search(r"(.)(니다|니까)$", s)
    if not m:
        return False
    ch = m.group(1)
    if not ("가" <= ch <= "힣"):
        return False
    return (ord(ch) - 0xAC00) % 28 == 17  # 받침 ㅂ


STYLE_RES = [
    ("합니다체", is_hamnida),
    ("해요체", lambda s: s.endswith("요")),
    ("한다체", lambda s: s.endswith("다") and not is_hamnida(s)),
]


def mask_code(text):
    """펜스 코드블록 내용을 빈 줄로 바꾼다(줄 번호는 그대로 유지).

    코드블록 안의 티는 대부분 의도된 것이다 — ❌ 예시, 명령어, 파일 트리.
    이걸 HARD로 잡으면 예시가 있는 문서는 영원히 통과 못 해서, 게이트를
    습관적으로 무시하게 된다. 그래서 아예 검사 대상에서 뺀다.
    반환: (마스킹된 텍스트, 건너뛴 줄 수)
    """
    out, inside, skipped = [], False, 0
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            inside = not inside
            out.append("")
            continue
        if inside:
            out.append("")
            skipped += 1
        else:
            out.append(line)
    return "\n".join(out), skipped


def is_markup_path(arg):
    """대상이 마크업 파일인지 확장자로 판단한다. stdin(-)은 판단 근거가 없어 False."""
    if arg == "-":
        return False
    return os.path.splitext(arg)[1].lower() in MARKUP_EXTS


def mask_markup(text):
    """마크업 태그를 같은 길이의 공백으로 바꾼다.

    지우지 않고 공백으로 채우는 이유: 줄 번호와 열 위치가 그대로 남아야
    snippet 출력이 실제 파일 위치를 가리킨다.
    `&lt;a href&gt;` 같은 인라인 엔티티는 '<' 문자가 아니라서 마스킹되지 않는다 —
    화면에 보이는 글자이므로 검사 대상으로 남는 게 맞다.
    반환: (마스킹된 텍스트, 마스킹한 글자 수)
    """
    masked = 0

    def blank(m):
        nonlocal masked
        s = m.group()
        masked += sum(1 for c in s if c != "\n")
        return "".join("\n" if c == "\n" else " " for c in s)

    # 주석 → 태그 순서. 주석 안의 부등호가 태그 규칙에 먼저 걸리면 안 된다.
    text = COMMENT_RE.sub(blank, text)
    return TAG_RE.sub(blank, text), masked


def snippet(line, idx, width=18):
    """문제 위치 주변을 잘라 보여준다."""
    start = max(0, idx - width)
    end = min(len(line), idx + width)
    s = line[start:end].strip()
    return ("…" if start > 0 else "") + s + ("…" if end < len(line) else "")


def check_register_mix(text):
    """문서 안에서 어체가 섞였는지 본다.

    register_check.py는 '목표 어체 대비' 검사라 목표가 (미지정)이면 아무것도 안 한다.
    하지만 '한 문서 안에서 합니다체와 해요체가 섞이는' 건 목표가 없어도 잡을 수 있다.
    (ai-tells.md의 '경어법 일관성 손실' 패턴을 기계화한 것.)

    코드블록·인라인 코드는 제외한다 — ❌/✅ 예시가 일부러 다른 어체를 쓰기 때문.
    """
    body = FENCE_RE.sub(" ", text)
    body = INLINE_CODE_RE.sub(" ", body)

    counts = {name: [] for name, _ in STYLE_RES}
    for raw in re.split(r"[.!?\n]", body):
        s = raw.strip().rstrip("\"'”’)》」]")
        if len(s) < 2:
            continue
        for name, match in STYLE_RES:
            if match(s):
                counts[name].append(s[-24:])
                break
    # 2회 이상 나온 어체만 '쓰이고 있다'고 본다 (한두 번은 인용·제목일 수 있음)
    used = {k: v for k, v in counts.items() if len(v) >= 2}
    return counts, used


def lint(text, patterns):
    """patterns.json의 정규식 패턴 + 코드로만 되는 검사(가운뎃점, 인덱싱 런)."""
    # 인라인 코드는 검사 대상이 아니다. 공백 대신 'x'로 채운다 —
    # 공백으로 지우면 "- Debian/Ubuntu: `apt install`" 이 "- Debian/Ubuntu:   "가 돼서
    # 멀쩡한 리스트 항목 콜론이 '문장 끝 콜론'으로 잘못 잡힌다.
    text = INLINE_CODE_RE.sub(lambda m: "x" * len(m.group()), text)
    lines = text.splitlines()

    hard, advisory = {}, {}
    for p in patterns:
        (hard if p["layer"] == "hard" else advisory).setdefault(p["label"], [])
    # 코드로만 되는 검사 (정규식 하나로 안 되는 것들)
    hard.setdefault("가운뎃점", [])
    advisory.setdefault("숫자 괄호 인덱싱", [])

    for n, line in enumerate(lines, 1):
        for p in patterns:
            if p.get("flags"):  # 멀티라인 패턴은 아래에서 전체 텍스트로 한 번에
                continue
            bucket = hard if p["layer"] == "hard" else advisory
            for m in p["_rx"].finditer(line):
                bucket[p["label"]].append(f"  L{n}: {snippet(line, m.start())}")

        # 가운뎃점은 개수나 용도와 관계없이 반드시 제거한다.
        for m in re.finditer(r"\S*[" + MIDDLE_DOTS + r"]\S*", line):
            token = m.group()
            hard["가운뎃점"].append(f"  L{n}: {token}")

    # 멀티라인 플래그가 붙은 패턴은 전체 텍스트에 한 번
    for p in patterns:
        if not p.get("flags"):
            continue
        bucket = hard if p["layer"] == "hard" else advisory
        for m in p["_rx"].finditer(text):
            ln = text[:m.start()].count("\n") + 1
            bucket[p["label"]].append(f"  L{ln}: {lines[ln-1][-30:] if ln-1 < len(lines) else ''}")

    # 숫자 괄호 인덱싱 — 1) 2) 3)처럼 연속 증가하는 3개 이상 런만 신호
    hits = []
    for n, line in enumerate(lines, 1):
        for m in re.finditer(r"(?<!\d)([1-9][0-9]?)\)(?!\d)", line):
            hits.append((n, int(m.group(1)), snippet(line, m.start())))
    run = []
    for h in hits:
        if run and h[1] == run[-1][1] + 1:
            run.append(h)
        else:
            if len(run) >= 3:
                advisory["숫자 괄호 인덱싱"] += [f"  L{r[0]}: {r[1]}) {r[2]}" for r in run]
            run = [h]
    if len(run) >= 3:
        advisory["숫자 괄호 인덱싱"] += [f"  L{r[0]}: {r[1]}) {r[2]}" for r in run]

    return hard, advisory


def check_ending_streak(text, min_run=4):
    """같은 종결어미가 연속 4문장 이상 이어지는 구간을 센다.

    본문 표의 '같은 종결어미 반복'을 기계화한 것. 리듬이 균일하다는 신호다.
    (im-not-ai의 da_streak_rate 접근을 참고했다.)
    """
    body = INLINE_CODE_RE.sub(" ", FENCE_RE.sub(" ", text))
    sents = [x.strip() for x in re.split(r"[.!?\n]", body) if len(x.strip()) >= 2]
    runs, cur, prev = [], [], None
    for s in sents:
        end = s[-1]
        if end == prev:
            cur.append(s)
        else:
            if len(cur) >= min_run:
                runs.append((prev, len(cur), cur[0][-20:]))
            cur, prev = [s], end
    if len(cur) >= min_run:
        runs.append((prev, len(cur), cur[0][-20:]))
    return runs


# 서술형 어체에서 문장을 끝맺는 음절. 여기 없는 글자로 끝나면 명사구 종결로 본다.
# 다 담으려 하면 오히려 다 통과시켜 검사가 무의미해지므로, 실제로 쓰이는 것만 넣는다.
SENTENCE_ENDINGS = tuple("다요음함죠까라자니네지오군걸텐줘봐해게어아야세소")

# 헤더, 표, 목록, 인용은 원래 명사구로 끝내는 자리다(register.md의 허용 조건).
NOT_PROSE_RE = re.compile(r"^\s*(#|\||>|\d+[.)]\s|[-*+]\s)")


# 이 비율을 넘고 건수도 최소치를 넘을 때만 신호로 본다.
# 명사구 단문은 그 자체로 흔한 문체다 — 이 저장소 문서만 해도 12개 파일에 56건
# 나오는데 전부 의도된 단문이었다. 건수로 보면 소음이고 밀도로 봐야 갈린다.
# 값의 근거는 2026-09-01 모델 비교 실측이다(about.md `모델 비교 기록`). 압축 압력을
# 건 산출물이 40%, 80%, 100%였고 규칙을 넣은 쪽은 셋 다 0%였다. 이 저장소 문서 12개는
# worked-examples.md(50%)만 넘고 나머지는 전부 29% 이하였다. 표본이 작으니 재현이
# 쌓이면 다시 본다.
#
# 넘는다고 항상 전보체는 아니다. 어체가 `명사형`이나 `음슴체`면 통째로 오탐이고,
# worked-examples.md가 실제로 그 경우다. 그래서 ADVISORY이고 판단은 사람이 한다.
NOUN_FINAL_RATIO = 0.35
NOUN_FINAL_MIN = 2


def check_noun_final(text, min_len=8):
    """서술형 문장이 종결어미 없이 명사구로 끝난 비율을 잰다 — 전보체 신호.

    SKILL.md의 `반대 방향의 실패`를 기계화한 것이다. 압축 압력이 걸리면 조사와
    어미가 먼저 떨어져 나가는데, 그 결과가 여기 잡힌다.

    ADVISORY이고 status는 experimental이다. 건수가 아니라 밀도로 판정하며,
    어체가 `명사형`이나 `음슴체`면 검사 전체가 오탐이므로 판단은 사람이 한다.
    해체 명령(`다듬어`)도 한 번씩 걸린다.

    반환: (hits, 산문 문장 수)
    """
    hits, total = [], 0
    incode = False
    for lineno, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("```"):
            incode = not incode
            continue
        if incode or not line.strip() or NOT_PROSE_RE.match(line):
            continue
        clean = INLINE_CODE_RE.sub(" ", line)
        for sent in re.split(r"(?<=[.!?])\s+", clean):
            sent = sent.strip()
            if len(sent) < min_len or not sent.endswith("."):
                continue
            tail = sent.rstrip(".").rstrip("\"'\u201d\u2019)]\uff09").rstrip()
            # 인라인 코드를 지운 자리에 구두점만 남은 조각은 문장이 아니다.
            if len(re.findall(r"[\uac00-\ud7a3]", tail)) < 4:
                continue
            if not re.search(r"[\uac00-\ud7a3]$", tail):
                continue
            total += 1
            if not tail.endswith(SENTENCE_ENDINGS):
                hits.append((lineno, sent[-40:]))
    return hits, total


def report(hard, advisory, used=None, thresholds=None, streaks=None, nounfinal=None):
    hard_total = sum(len(v) for v in hard.values())
    adv_total = sum(len(v) for v in advisory.values())
    mixed = used is not None and len(used) >= 2
    thresholds = thresholds or {}

    print("=" * 52)
    print("  AI 티 린트 (기계적 항목)")
    print("=" * 52)

    print("\n[HARD — 0이어야 함. 각 항목이 의도된 것만 남기고 나머지는 고친다]")
    for name, hits in hard.items():
        mark = "✗" if hits else "○"  # 콘솔 표시용(출력물 아님)
        print(f"  {mark} {name}: {len(hits)}")
        for h in hits[:30]:
            print(h)
        if len(hits) > 30:
            print(f"    … 외 {len(hits) - 30}건")

    print("\n[ADVISORY — 밀도 판단. 0일 필요는 없고, 몰려 있으면 줄인다]")
    for name, hits in advisory.items():
        note = ""
        th = thresholds.get(name)
        if th and len(hits) >= th:
            note = f"  ({th}회 이상 — patterns.json의 why 참고)"
        print(f"  · {name}: {len(hits)}{note}")
        for h in hits[:15]:
            print(h)
        if len(hits) > 15:
            print(f"    … 외 {len(hits) - 15}건")

    if streaks:
        print("\n[종결어미 연속 — 4문장 이상 같은 끝맺음이 이어지는 구간]")
        for end, cnt, sample in streaks:
            print(f"  · '{end}' {cnt}문장 연속  (…{sample})")
        print("    → 리듬이 균일하다는 신호. 일부를 다른 끝맺음으로 바꾼다.")

    if nounfinal:
        hits, total = nounfinal
        ratio = len(hits) / total if total else 0
        loud = len(hits) >= NOUN_FINAL_MIN and ratio >= NOUN_FINAL_RATIO
        print("\n[명사구 종결 — ADVISORY, experimental. 전보체 신호]")
        print(f"  · {len(hits)}건 / 산문 {total}문장 ({ratio:.0%})")
        if loud:
            for lineno, sample in hits[:15]:
                print(f"  · L{lineno}: {sample}")
            if len(hits) > 15:
                print(f"    … 외 {len(hits) - 15}건")
            print(f"    → {NOUN_FINAL_RATIO:.0%}를 넘었다. 압축하다 조사와 어미가 빠졌는지 본다"
                  " (SKILL.md `반대 방향의 실패`).")
            print("    → 어체가 `명사형`이나 `음슴체`면 이 항목 전체가 오탐이다.")
        else:
            print("    → 밀도가 낮다. 의도된 명사구 단문으로 보고 넘어간다.")

    if used is not None:
        print("\n[어체 일관성 — ADVISORY, 의도된 혼용인지 확인]")
        if not used:
            print("  · 판정할 문장 부족 — 생략")
        elif not mixed:
            only = list(used)[0]
            print(f"  ○ {only}로 일관됨 ({len(used[only])}문장)")
        else:
            names = ", ".join(f"{k} {len(v)}문장" for k, v in used.items())
            print(f"  · 혼용: {names}")
            for k, v in used.items():
                print(f"    [{k}] 예: {v[0]}")
            print("    → 프로젝트 register와 장르를 확인한다. 의도하지 않은 혼용만 고친다.")

    blocking = hard_total
    print("\n" + "-" * 52)
    if blocking == 0:
        print(f"  통과 (HARD 0건). ADVISORY {adv_total}건은 밀도만 확인.")
    else:
        print(f"  보류 (HARD {hard_total}건). 고치고 다시 돌린다.")
    print("-" * 52)
    return blocking


def main():
    # `ai_lint.py file | head` 처럼 파이프가 먼저 닫히면 트레이스백이 뜬다. 조용히 끝낸다.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass  # Windows에는 SIGPIPE가 없다

    if len(sys.argv) != 2:
        print("사용법: python3 ai_lint.py <파일경로>  또는  ... | python3 ai_lint.py -")
        sys.exit(2)
    arg = sys.argv[1]
    try:
        text = sys.stdin.read() if arg == "-" else open(arg, encoding="utf-8").read()
        patterns = load_patterns()
    # TypeError까지 잡는다. patterns.json의 값 타입이 틀려 어떤 경로로든 터지더라도
    # 설정 문제는 traceback이 아니라 exit 2로 끝나야 한다.
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"UX lint 입력 또는 설정 오류: {exc}", file=sys.stderr)
        sys.exit(2)
    # 순서가 중요하다. 코드블록을 먼저 비워야 코드블록 안의 `<div>` 예시가
    # 태그 마스킹에 걸리지 않는다 — '코드블록 안은 검사 제외' 계약을 지키는 순서다.
    body, skipped = mask_code(text)
    masked_chars = 0
    if is_markup_path(arg):
        body, masked_chars = mask_markup(body)
    hard, advisory = lint(body, patterns)
    _, used = check_register_mix(body)
    streaks = check_ending_streak(body)
    thresholds = {p["label"]: p["threshold"] for p in patterns if p.get("threshold")}
    nounfinal = check_noun_final(body)
    blocking = report(hard, advisory, used, thresholds, streaks, nounfinal)
    if skipped:
        print(f"  (코드블록 {skipped}줄은 검사 제외 — 예시·명령어는 의도된 것으로 본다)")
    if masked_chars:
        print(f"  (마크업 태그 {masked_chars}자는 검사 제외 — 문장이 아니라 구조로 본다)")
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
