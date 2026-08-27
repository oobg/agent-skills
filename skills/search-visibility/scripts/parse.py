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


def jsonld_nodes(html):
    """(nodes, parse_errors) — @graph를 펼쳐 dict 목록으로 돌려준다."""
    nodes, errors = [], 0
    for block in LD_BLOCK.findall(html):
        try:
            data = json.loads(block.strip())
        except ValueError:
            errors += 1
            continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if "@graph" in node and isinstance(node["@graph"], list):
                    stack.extend(node["@graph"])
                    continue
                nodes.append(node)
            elif isinstance(node, list):
                stack.extend(node)
    return nodes, errors


def node_types(node):
    t = node.get("@type")
    return t if isinstance(t, list) else [t] if t else []


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
