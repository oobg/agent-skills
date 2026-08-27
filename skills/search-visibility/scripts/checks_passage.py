#!/usr/bin/env python3
"""문단 단위 관측 — 인용은 페이지가 아니라 문단째로 잘려 나간다.

geo.md가 "문단이 인용 단위가 된다"고 말하므로 측정 단위도 문단이어야 한다.
여기서는 **점수를 매기지 않는다.** 문단이 자체적으로 사실을 말하는지 가르는 관측치만
내고, 몇 개가 인용 단위로 설 수 있는지 센다. 가중치를 둔 종합 점수는 근거가 없어 만들지 않는다.
"""

import re

BLOCK_RE = re.compile(r"<(p|li|blockquote)\b[^>]*>(.*?)</\1>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
# 맥락 의존 신호. "위에서 말한 그 수치"처럼 앞 문단에 기대는 문장은 추출되면 무의미해진다.
DEIXIS_KO = ("이것", "그것", "저것", "이는", "그는", "이러한", "그러한", "해당", "위에서",
             "앞서", "아래에서", "다음과 같", "이때", "그때", "여기서")
# 영어는 단어 경계를 걸지 않으면 profit·limit 같은 단어가 걸린다.
DEIXIS_EN = re.compile(r"\b(this|that|these|those|it|above|below)\b", re.I)
BASIS = re.compile(r"(20\d{2}|기준|현재|누적|집계|출처|according to|as of|source)", re.I)
NUMBER = re.compile(r"[0-9][0-9,\.]*\s*(?:%|퍼센트|배|만|억|원|건|개|명|시간|분|일|년)?")
# aeo.md가 "첫 문단이 직답이다. 40자 내외 한 문장"이라고 규정한다. 그 40자가 이 파일의
# 유일한 문서 근거이며, 아래 값들은 판정선이 아니라 목록에서 잡음을 걷어내는 하한이다.
# 근거 없는 상한으로 OK/CHECK를 가르지 않는다 — 남의 매직넘버를 버리면서 내 매직넘버를
# 만들면 같은 잘못이다.
LEAD_IDEAL = 40                # aeo.md의 직답 권장 길이. 관측치를 이 값과 나란히 보여 준다.
NOISE_FLOOR = 15               # 버튼·라벨 같은 조각을 문단으로 세지 않기 위한 하한


def _text(chunk):
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", chunk)).strip()


def passages(html):
    """본문 블록을 순서대로 뽑는다. 스크립트 안은 이미 제거된 HTML을 받는다.

    짧다고 버리지 않는다. aeo.md가 이상형으로 규정한 40자 내외 직답이 바로 짧은 문단이라,
    길이로 거르면 문서가 쓰라고 한 형태를 도구가 문단으로 세지 않게 된다.
    """
    return [t for t in (_text(m.group(2)) for m in BLOCK_RE.finditer(html))
            if len(t) >= NOISE_FLOOR]


def classify(text):
    """문단 하나의 관측치. 판정이 아니라 사실만 담는다."""
    deixis = sum(1 for d in DEIXIS_KO if d in text) + len(DEIXIS_EN.findall(text))
    numbers = NUMBER.findall(text)
    numeric = [n for n in numbers if len(re.sub(r"[^0-9]", "", n)) >= 2]
    return {
        "chars": len(text),
        "deixis": deixis,
        "has_number": bool(numeric),
        "has_basis": bool(BASIS.search(text)),
        # 자체 완결: 맥락 지시어가 없고, 수치가 있으면 그 근거·시점도 함께 있다.
        "self_contained": deixis == 0 and (not numeric or bool(BASIS.search(text))),
    }


def audit_passages(html):
    out = {"checks": []}
    blocks = passages(html)
    if not blocks:
        out["checks"].append(("CHECK", "문단 구조", "본문 블록을 찾지 못했다 — 마크업을 직접 본다"))
        return out

    marks = [classify(b) for b in blocks]
    citable = [m for m in marks if m["self_contained"]]
    context_bound = [m for m in marks if m["deixis"]]
    loose_numbers = [m for m in marks if m["has_number"] and not m["has_basis"]]
    longest = max(m["chars"] for m in marks)

    out.update({"passage_count": len(blocks), "citable_count": len(citable),
                "longest_passage": longest,
                "context_bound": len(context_bound), "loose_number_passages": len(loose_numbers)})
    out["checks"].append((
        "OK" if citable else "CHECK", "인용 가능 문단",
        "{}개 중 {}개가 자체 완결".format(len(blocks), len(citable))))
    if context_bound:
        out["checks"].append((
            "CHECK", "맥락 의존 문단",
            "{}개가 앞뒤 문단에 기댄다 — 추출되면 뜻이 사라진다".format(len(context_bound))))
    if loose_numbers:
        out["checks"].append((
            "CHECK", "근거 없는 수치 문단",
            "{}개 문단이 수치를 말하면서 기준·출처를 함께 적지 않는다".format(len(loose_numbers))))
    out["checks"].append(("OK", "문단 길이", "가장 긴 문단 {}자".format(longest)))

    # 첫 문단이 직답인지는 의미 판정이라 기계가 가르지 못한다. 관측치와 문서 권장값을
    # 나란히 놓고 판단은 사람에게 넘긴다.
    lead = blocks[0]
    out["checks"].append((
        "CHECK", "첫 문단",
        "{}자 (aeo.md 권장 {}자 내외) — 직답인지 직접 확인한다".format(len(lead), LEAD_IDEAL)))
    return out
