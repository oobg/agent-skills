#!/usr/bin/env python3
"""페이지 간 대조 — 한 페이지만 봐서는 드러나지 않는 것."""

import parse


def audit_cross(pages, sitemap_locs):
    """메타 중복, 엔티티 표기 분열, 사이트맵 누락을 본다."""
    out = {"checks": []}
    # base가 /ko로 리다이렉트되는 식이면 같은 페이지를 두 번 세게 된다.
    # 최종 URL 기준으로 접어야 없는 중복을 보고하지 않는다.
    unique, seen_urls = [], set()
    for p in pages:
        if p.get("status") != 200 or not p.get("title"):
            continue
        key = (p.get("final_url") or p["url"]).rstrip("/")
        if key in seen_urls:
            continue
        seen_urls.add(key)
        unique.append(p)
    seen = unique
    if len(seen) < 2:
        return out

    dup_title, dup_desc = {}, {}
    for p in seen:
        dup_title.setdefault(p["title"], []).append(p["url"])
        if p.get("description_len"):
            dup_desc.setdefault((p["title"], p["description_len"]), []).append(p["url"])
    repeated = [urls for urls in dup_title.values() if len(urls) > 1]
    out["checks"].append((
        "OK" if not repeated else "FAIL", "메타 중복",
        "{}개 페이지 전부 고유".format(len(seen)) if not repeated else
        "제목이 같은 페이지 {}쌍: {}".format(len(repeated), " / ".join(u[0] for u in repeated[:3]))))

    # 같은 엔티티가 페이지마다 다른 이름으로 선언되면 모델 안에서 갈라진다.
    org_names = sorted({n for p in seen for n in p.get("org_names", [])})
    if len(org_names) > 1:
        out["checks"].append(("CHECK", "엔티티 표기",
                              "Organization 이름이 {}종: {}".format(len(org_names), ", ".join(org_names))))

    if sitemap_locs:
        indexed = {u.rstrip("/") for u in sitemap_locs}
        missing = [p["url"] for p in seen if p["url"].rstrip("/") not in indexed
                   and p.get("final_url", "").rstrip("/") not in indexed]
        out["checks"].append((
            "OK" if not missing else "CHECK", "사이트맵 포함",
            "관측한 페이지 전부 등재" if not missing else
            "사이트맵에 없는 페이지 {}건: {}".format(len(missing), ", ".join(missing[:3]))))
    return out
