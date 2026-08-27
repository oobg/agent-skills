#!/usr/bin/env python3
"""페이지 단위 관측.

판정 규칙은 하나다 — 자바스크립트 없이 받은 응답에서 확인되는 것만 사실로 센다.
기계적으로 참·거짓이 갈리는 항목만 OK/FAIL을 주고, 문맥이 필요한 것은 CHECK로 남긴다.
"""

import re

import fetch
import parse

TITLE_MIN, TITLE_MAX = 15, 60          # 권장은 seo.md의 50~60. 짧은 브랜드 홈을 감안한 하한이다.
DESC_MIN, DESC_MAX = 80, 165
TEXT_THIN = 500
ANSWER_PROBE = 30                       # 긴 답변은 앞부분만 대조한다(마크업 중간 태그 삽입 회피).
NUMBER_RE = re.compile(r"[0-9][0-9,\.]*\s*(?:%|퍼센트|배|만|억|천|건|개|명|시간|분|일)?\+?")
BASIS_RE = re.compile(r"(20\d{2}|기준|현재|누적|집계|분기|월말|as of)", re.I)
BASIS_WINDOW = 40


def _numbers_without_basis(text):
    """기준 시점·집계 방법이 붙지 않은 수치를 센다. 판정이 아니라 확인 목록이다."""
    out = []
    for m in NUMBER_RE.finditer(text):
        token = m.group(0).strip()
        # 한두 자리 맨숫자는 목록·연도·버전일 확률이 높아 잡지 않는다.
        if len(re.sub(r"[^0-9]", "", token)) < 2:
            continue
        if not (token.endswith("%") or "+" in token or len(re.sub(r"[^0-9]", "", token)) >= 3):
            continue
        around = text[max(0, m.start() - BASIS_WINDOW):m.end() + BASIS_WINDOW]
        if not BASIS_RE.search(around):
            out.append(token)
    return out


def _structured_vs_visible(nodes, text):
    """구조화 데이터가 화면에 없는 것을 말하는지 본다.

    이 스킬의 원칙 2가 기계로 판정되는 유일한 자리다. FAQ 답변이 JSON-LD에만 있고
    가시 마크업에 없으면, 렌더링하지 않는 소비자에게 그 답변은 존재하지 않는다.
    """
    flat = parse.normalize(text)
    missing, soft_missing, checked = [], [], 0
    for node in nodes:
        types = parse.node_types(node)
        if "FAQPage" in types:
            for qa in node.get("mainEntity") or []:
                if not isinstance(qa, dict):
                    continue
                name = qa.get("name") or ""
                answer = (qa.get("acceptedAnswer") or {}).get("text") or ""
                if name:
                    checked += 1
                    if parse.normalize(name) not in flat:
                        missing.append("질문 '{}'".format(name[:20]))
                if answer:
                    checked += 1
                    if parse.normalize(answer)[:ANSWER_PROBE] not in flat:
                        missing.append("답변 '{}…'".format(answer[:20]))
        for key in ("headline", "name"):
            value = node.get(key)
            if isinstance(value, str) and value and types and types[0] in (
                "Article", "BlogPosting", "NewsArticle", "Product", "SoftwareApplication"
            ):
                checked += 1
                if parse.normalize(value) not in flat:
                    # 이름은 다국어 표기 차이로 갈리는 일이 흔하다. 스팸 신호가 아니라
                    # 엔티티 표기 분열 신호이므로 확인 항목으로 내린다.
                    soft_missing.append("{} {} '{}'".format(types[0], key, value[:20]))
    return missing, soft_missing, checked


def audit_page(url, ua, timeout, verify_assets=True):
    status, final, headers, html, hops, error = fetch.fetch(url, ua, timeout)
    page = {"url": url, "final_url": final, "status": status, "redirect_hops": hops,
            "error": error, "checks": []}
    add = page["checks"].append
    if error or status is None:
        add(("FAIL", "요청", error or "응답 없음"))
        return page
    if status >= 400:
        add(("FAIL", "응답", "HTTP {}".format(status)))
        return page

    text = parse.visible_text(html)
    title = parse.title_of(html)
    desc = parse.meta_content(html, "description")
    robots_meta = (parse.meta_content(html, "robots") or "").lower()
    canonical = parse.link_href(html, "canonical")
    og_image = parse.meta_content(html, "og:image", attr="property")
    nodes, ld_errors = parse.jsonld_nodes(html)
    ld_types = sorted({t for n in nodes for t in parse.node_types(n)})
    langs = parse.hreflangs(html)
    same_as = sorted({s for n in nodes for s in (n.get("sameAs") or [])
                      if isinstance(n.get("sameAs"), list) and isinstance(s, str)})
    org_names = sorted({n.get("name") for n in nodes
                        if "Organization" in parse.node_types(n) and isinstance(n.get("name"), str)})

    page.update({
        "bytes": len(html), "text_chars": len(text), "title": title,
        "title_len": len(title) if title else 0,
        "description_len": len(desc) if desc else 0,
        "h1_count": parse.tag_count(html, "h1"), "h2_count": parse.tag_count(html, "h2"),
        "h3_count": parse.tag_count(html, "h3"), "table_count": parse.tag_count(html, "table"),
        "list_count": parse.tag_count(html, "ul") + parse.tag_count(html, "ol"),
        "canonical": canonical, "og_image": og_image,
        "hreflang": langs, "jsonld_types": ld_types, "same_as": same_as,
        "org_names": org_names,
        "noindex": "noindex" in robots_meta,
        "viewport": bool(parse.meta_content(html, "viewport")),
    })

    add(("OK" if hops <= 1 else "CHECK", "리다이렉트", "{}홉".format(hops)))
    if page["noindex"]:
        # 스테이징·파라미터 변형·중복 억제는 의도된 제외다. 스크립트는 의도를 모른다.
        add(("CHECK", "색인", "meta robots에 noindex — 의도된 제외인지 확인한다"))
    add(("CHECK" if page["text_chars"] < TEXT_THIN else "OK", "본문 노출",
         "가시 텍스트 {}자{}".format(page["text_chars"],
                                " — 500자 미만이면 CSR 여부를 직접 확인한다"
                                if page["text_chars"] < TEXT_THIN else "")))
    add(("OK" if page["h1_count"] == 1 else "CHECK", "h1", "{}개".format(page["h1_count"])))
    if not title:
        add(("FAIL", "title", "없음"))
    else:
        add(("OK" if TITLE_MIN <= page["title_len"] <= TITLE_MAX else "CHECK", "title",
             "{}자 (권장 50~60, 짧은 브랜드 홈을 감안해 15자부터 통과)".format(page["title_len"])))
    if not desc:
        add(("FAIL", "description", "없음"))
    else:
        add(("OK" if DESC_MIN <= page["description_len"] <= DESC_MAX else "CHECK",
             "description", "{}자 (권장 {}~{})".format(page["description_len"], DESC_MIN, DESC_MAX)))

    if not canonical:
        add(("CHECK", "canonical", "없음"))
    else:
        add(("OK" if canonical.rstrip("/") == final.rstrip("/") else "CHECK", "canonical",
             canonical if canonical.rstrip("/") == final.rstrip("/") else
             "{} — 이 URL이 아닌 곳을 가리킨다".format(canonical)))

    if langs:
        add(("OK" if any(l.lower() == "x-default" for l, _ in langs) else "CHECK", "hreflang",
             "{}건{}".format(len(langs), "" if any(l.lower() == "x-default" for l, _ in langs)
                             else " — x-default 없음")))

    add(("OK" if page["viewport"] else "FAIL", "viewport",
         "있음" if page["viewport"] else "없음 — 모바일 우선 엔진에서 불리하다"))

    if og_image and verify_assets:
        code, ctype, _ = fetch.head_status(fetch.join(final, og_image), ua, timeout)
        ok = code == 200 and ctype.startswith("image/")
        add(("OK" if ok else "FAIL", "og:image",
             "{} ({})".format(code, ctype) if ok else "응답 {} {}".format(code, ctype)))
    else:
        add(("OK" if og_image else "CHECK", "og:image", "있음" if og_image else "없음"))

    if ld_errors:
        add(("FAIL", "JSON-LD", "파싱 실패 {}블록".format(ld_errors)))
    add(("OK" if ld_types else "CHECK", "JSON-LD", ", ".join(ld_types) if ld_types else "없음"))

    missing, soft_missing, checked = _structured_vs_visible(nodes, text)
    page["ld_missing"] = missing
    page["ld_name_mismatch"] = soft_missing
    if checked:
        if missing:
            # 화면에 없는 문답을 구조화 데이터가 선언하면, 렌더링하지 않는 소비자에게
            # 그 답변은 존재하지 않는다. 원칙 2가 기계로 판정되는 자리다.
            add(("FAIL", "구조화 데이터 대조",
                 "문답 {}건이 가시 텍스트에 없음: {}".format(
                     len(missing), ", ".join(missing[:3]) + ("…" if len(missing) > 3 else ""))))
        else:
            add(("OK", "구조화 데이터 대조", "문답 대조 통과 (검사 {}건)".format(checked)))
        if soft_missing:
            add(("CHECK", "엔티티 표기 대조",
                 "{}건이 화면 표기와 다름: {}".format(
                     len(soft_missing), ", ".join(soft_missing[:3]))))

    add(("OK" if page["table_count"] or page["list_count"] >= 3 else "CHECK", "인용 단위 구조",
         "표 {}개 · 목록 {}개 · h2 {} · h3 {}".format(
             page["table_count"], page["list_count"], page["h2_count"], page["h3_count"])))

    loose = _numbers_without_basis(text)
    page["numbers_without_basis"] = loose
    if loose:
        add(("CHECK", "수치 기준 표기",
             "기준 없는 수치 {}건: {}".format(len(loose), ", ".join(loose[:5]))))

    if same_as:
        add(("OK", "sameAs", "{}건".format(len(same_as))))
    return page
