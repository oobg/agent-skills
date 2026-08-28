#!/usr/bin/env python3
"""HTML 파싱 유틸 — 정규식만 쓰며 렌더링하지 않는다.

여기서 뽑는 '가시 텍스트'는 스크립트를 제거한 뒤의 마크업 텍스트다. 자바스크립트가
만들어내는 DOM은 포함되지 않으며, 그것이 이 스킬의 판정 기준이다.
"""

import json
import re

SCRIPTISH = re.compile(r"<(script|style|template|noscript)\b.*?</\1>", re.S | re.I)
LD_BLOCK = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)


def visible_text(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", SCRIPTISH.sub(" ", html))).strip()


def find_all(pattern, html, flags=re.I | re.S):
    return re.findall(pattern, html, flags)


def tag_count(html, tag):
    return len(re.findall(r"<{}\b".format(tag), html, re.I))


def title_of(html):
    hit = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    return re.sub(r"\s+", " ", hit.group(1)).strip() if hit else None


def meta_content(html, key, attr="name"):
    hit = re.search(
        r'<meta[^>]+{}=["\']{}["\'][^>]*content=["\'](.*?)["\']'.format(attr, key), html, re.I | re.S
    ) or re.search(
        r'<meta[^>]+content=["\'](.*?)["\'][^>]*{}=["\']{}["\']'.format(attr, key), html, re.I | re.S
    )
    return hit.group(1).strip() if hit else None


def link_href(html, rel):
    hit = re.search(r'<link[^>]+rel=["\']{}["\'][^>]*href=["\'](.*?)["\']'.format(rel), html, re.I | re.S)
    return hit.group(1).strip() if hit else None


def hreflangs(html):
    """[(lang, href)] — 선언 순서를 유지한다."""
    out = []
    for tag in find_all(r"<link[^>]+hreflang=[^>]*>", html):
        lang = re.search(r'hreflang=["\'](.*?)["\']', tag, re.I)
        href = re.search(r'href=["\'](.*?)["\']', tag, re.I)
        if lang and href:
            out.append((lang.group(1).strip(), href.group(1).strip()))
    return out


def _flatten(node, ctx, out):
    """@context를 물려주며 노드를 펼친다.

    @graph 자식은 감싼 노드의 @context를 상속한다(JSON-LD 규약). 노드만 평탄화하면
    그 상속이 사라져, 상속받은 노드와 @context가 아예 없는 노드가 구분되지 않는다.
    """
    if isinstance(node, list):
        for item in node:
            _flatten(item, ctx, out)
        return
    if not isinstance(node, dict):
        return
    ctx = node.get("@context", ctx)
    graph = node.get("@graph")
    if isinstance(graph, (list, dict)):
        _flatten(graph, ctx, out)      # @graph 컨테이너 자체는 노드가 아니다
        return
    out.append((ctx, node))


def jsonld_pairs(html):
    """([(context, node)], parse_errors) — 노드마다 유효한 @context를 붙여 돌려준다."""
    pairs, errors = [], 0
    for block in LD_BLOCK.findall(html):
        try:
            data = json.loads(block.strip())
        except ValueError:
            errors += 1
            continue
        _flatten(data, None, pairs)
    return pairs, errors


def jsonld_nodes(html):
    """(nodes, parse_errors) — @context가 필요 없는 호출자를 위한 얇은 래퍼."""
    pairs, errors = jsonld_pairs(html)
    return [node for _, node in pairs], errors


SCHEMA_CTX = re.compile(r"^https?://schema\.org/?$", re.I)


def context_state(ctx):
    """@context 판정 — "ok" | "other" | "none".

    schema.org는 http와 https 표기가 모두 통용되고(네이버 공식 예제가 http를 쓴다)
    끝의 슬래시도 갈린다. 객체 형태는 용어 정의를 직접 싣는 경우라 기계로 단정하지
    않고 "other"로 넘겨 사람이 본다.
    """
    if ctx is None:
        return "none"
    if isinstance(ctx, str):
        return "ok" if SCHEMA_CTX.match(ctx.strip()) else "other"
    if isinstance(ctx, list):
        return "ok" if any(context_state(c) == "ok" for c in ctx) else "other"
    if isinstance(ctx, dict):
        vocab = ctx.get("@vocab")
        return "ok" if isinstance(vocab, str) and SCHEMA_CTX.match(vocab.strip()) else "other"
    return "other"


ITEMTYPE = re.compile(r'itemtype=["\']([^"\']+)["\']', re.I)
SCHEMA_TYPE_URL = re.compile(r"schema\.org/(\w+)", re.I)


def microdata_types(html):
    """Microdata로 선언된 schema.org 타입 목록.

    네이버는 Microdata와 JSON-LD를 나란히 권장한다. JSON-LD만 보면 Microdata로
    마크업한 사이트가 '구조화 데이터 없음'으로 잘못 관측된다.
    """
    out = set()
    for raw in ITEMTYPE.findall(SCRIPTISH.sub(" ", html)):
        for url in raw.split():
            hit = SCHEMA_TYPE_URL.search(url)
            if hit:
                out.add(hit.group(1))
    return sorted(out)


def node_types(node):
    t = node.get("@type")
    return t if isinstance(t, list) else [t] if t else []


HANGUL = re.compile(r"[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f]")


def estimate_tokens(text):
    """토큰 수 추정. 정확한 수가 아니라 자릿수를 보기 위한 값이다.

    널리 쓰이는 문자수÷4 어림은 **영어 기준이다.** 한글은 음절 하나가 토큰 1~2개로
    쪼개지는 경우가 많아 같은 식을 쓰면 3~4배 과소 추정된다. 한글을 분리해 센다.
    토크나이저마다 갈리므로 판정 근거로 쓰지 않고 관측치로만 낸다.
    """
    if not text:
        return 0
    hangul = len(HANGUL.findall(text))
    return int(hangul / 1.5 + (len(text) - hangul) / 4)


def normalize(text):
    """대조용 정규화 — 공백과 따옴표 변형을 지운다."""
    text = re.sub(r"[‘’“”]", "'", text or "")
    return re.sub(r"\s+", "", text)


FRAMEWORK_ROOTS = ("root", "__next", "app", "__nuxt", "___gatsby", "svelte")
ROOT_OPEN = r'<div[^>]*\sid=["\']{}["\'][^>]*>'
DIV_EDGE = re.compile(r"<div\b[^>]*>|</div\s*>", re.I)


def _subtree(html, start):
    """여는 div 바로 뒤부터 짝이 맞는 </div>까지를 돌려준다.

    그리디 캡처로 문서 끝까지 가져오면 루트 뒤의 푸터가 루트 안으로 계산돼,
    본문이 비어 있는 CSR 페이지가 통과한다. 과대 측정은 한 방향으로만 틀린다.
    """
    depth = 1
    for m in DIV_EDGE.finditer(html, start):
        depth += 1 if m.group(0).lower().startswith("<div") else -1
        if depth == 0:
            return html[start:m.start()]
    return html[start:]          # 닫히지 않은 마크업. 있는 만큼만 본다.


def framework_root_text(html):
    """프레임워크 루트 컨테이너 안의 텍스트 길이. 못 찾으면 None.

    전체 가시 텍스트만 보면 헤더·푸터가 SSR인 사이트가 통과한다. 반대로 프리렌더를
    쓰는 사이트를 CSR로 오인하기도 한다. 루트 안을 따로 재면 둘 다 줄어든다.
    """
    for rid in FRAMEWORK_ROOTS:
        m = re.search(ROOT_OPEN.format(re.escape(rid)), html, re.I)
        if m:
            return rid, len(visible_text(_subtree(html, m.end())))
    return None
