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
DEIXIS = ("이것", "그것", "저것", "이는", "그는", "이러한", "그러한", "해당", "위에서",
          "앞서", "아래에서", "다음과 같", "이때", "그때", "여기서",
          "this ", "that ", "these ", "those ", "it ", "above", "below")
BASIS = re.compile(r"(20\d{2}|기준|현재|누적|집계|출처|according to|as of|source)", re.I)
NUMBER = re.compile(r"[0-9][0-9,\.]*\s*(?:%|퍼센트|배|만|억|원|건|개|명|시간|분|일|년)?")
SHORT, LONG = 40, 700          # 인용 단위로 서기에 너무 짧거나 긴 문단의 경계
LEAD_ANSWER = 150              # 첫 문단이 직답이라면 이 정도 안에서 끝난다


def _text(chunk):
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", chunk)).strip()


def passages(html):
    """본문 블록을 순서대로 뽑는다. 스크립트 안은 이미 제거된 HTML을 받는다."""
    return [t for t in (_text(m.group(2)) for m in BLOCK_RE.finditer(html)) if len(t) >= SHORT]


def classify(text):
    """문단 하나의 관측치. 판정이 아니라 사실만 담는다."""
    lowered = text.lower()
    deixis = sum(1 for d in DEIXIS if d in lowered)
    numbers = NUMBER.findall(text)
    numeric = [n for n in numbers if len(re.sub(r"[^0-9]", "", n)) >= 2]
    return {
        "chars": len(text),
        "deixis": deixis,
        "has_number": bool(numeric),
        "has_basis": bool(BASIS.search(text)),
        # 자체 완결: 맥락 지시어가 없고, 수치가 있으면 그 근거·시점도 함께 있다.
        "self_contained": deixis == 0 and (not numeric or bool(BASIS.search(text))),
        "citable_length": SHORT <= len(text) <= LONG,
    }


def audit_passages(html):
    out = {"checks": []}
    blocks = passages(html)
    if not blocks:
        out["checks"].append(("CHECK", "문단 구조", "본문 블록을 찾지 못했다 — 마크업을 직접 본다"))
        return out

    marks = [classify(b) for b in blocks]
    citable = [m for m in marks if m["self_contained"] and m["citable_length"]]
    context_bound = [m for m in marks if m["deixis"]]
    loose_numbers = [m for m in marks if m["has_number"] and not m["has_basis"]]
    too_long = [m for m in marks if m["chars"] > LONG]

    out.update({"passage_count": len(blocks), "citable_count": len(citable),
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
    if too_long:
        out["checks"].append((
            "CHECK", "긴 문단",
            "{}개가 {}자를 넘는다 — 문단째 인용되기 어렵다".format(len(too_long), LONG)))

    lead = blocks[0]
    out["checks"].append((
        "OK" if len(lead) <= LEAD_ANSWER else "CHECK", "첫 문단",
        "{}자{}".format(len(lead), "" if len(lead) <= LEAD_ANSWER
                        else " — 직답이 맨 앞에 있는지 직접 확인한다")))
    return out
