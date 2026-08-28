#!/usr/bin/env python3
"""사이트 단위 관측 — robots.txt, 사이트맵, llms.txt, 404 처리."""

import re

import fetch
import parse

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
           "PerplexityBot", "Google-Extended", "Applebot-Extended", "Yeti"]
SITEMAP_URL_LIMIT = 50000
SITEMAP_BYTE_LIMIT = 50 * 1024 * 1024
LLMS_POLICY_HINTS = ("출처", "갱신", "인용", "source", "update", "cite", "license")


def parse_robots_groups(body):
    """robots.txt를 그룹 단위로 읽는다.

    연속된 User-agent 줄은 하나의 그룹을 공유한다. 이걸 무시하고 마지막 이름에만
    규칙을 붙이면 함께 선언된 봇들의 정책이 통째로 사라진다.
    """
    groups = {}
    current, after_agent = [], False
    for line in body.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        low = key.lower()
        if low == "user-agent":
            if not after_agent:
                current = []
            current.append(value.lower())
            groups.setdefault(value.lower(), [])
            after_agent = True
        elif low in ("allow", "disallow"):
            after_agent = False
            for agent in current:
                groups[agent].append((low, value))
    return groups


def robots_verdict(groups, bot):
    """봇 하나의 루트(/) 접근 정책을 판정한다.

    이름이 명시된 그룹이 있으면 그것만 적용되고 와일드카드는 무시된다(robots.txt 규약).
    다만 이름을 적어 두었어도 규칙이 와일드카드와 같으면 수집 권한은 달라지지 않는다 —
    선언 의도와 접근 차이를 같은 말로 적으면 없는 차이를 보고하게 된다.
    부분 경로 차단은 루트 접근을 막지 않으므로 여기서는 허용으로 읽는다.
    """
    named, wildcard = groups.get(bot.lower()), groups.get("*")
    entries, source = named, "명시"
    if entries is None:
        entries, source = wildcard, "*"
    if entries is None:
        return "규칙 없음"
    if named is not None and wildcard is not None and sorted(named) == sorted(wildcard):
        source = "명시=*"
    if any(rule == "disallow" and value == "/" for rule, value in entries):
        return "차단({})".format(source)
    return "허용({})".format(source)


def audit_robots(base, ua, timeout):
    status, _, _, body, _, error = fetch.fetch(fetch.join(base, "/robots.txt"), ua, timeout)
    out = {"status": status, "error": error, "sitemaps": [], "bots": {}, "checks": []}
    if status != 200 or not body:
        # robots.txt가 없으면 어떤 봇에도 규칙이 없다. 무정책은 중립이 아니므로
        # 봇 표를 비우지 않고 그대로 보여준다.
        out["bots"] = {bot: "규칙 없음" for bot in AI_BOTS}
        out["checks"] += [("FAIL", "robots.txt", "없음 또는 HTTP {}".format(status)),
                          ("CHECK", "AI 크롤러 정책", "robots.txt가 없어 전부 규칙 없음")]
        return out
    out["sitemaps"] = [m.strip() for m in parse.find_all(r"^\s*Sitemap:\s*(\S+)", body, re.I | re.M)]
    rules = parse_robots_groups(body)
    out["bots"] = {bot: robots_verdict(rules, bot) for bot in AI_BOTS}
    out["disallow_paths"] = sorted({v for entries in rules.values()
                                    for k, v in entries if k == "disallow" and v not in ("", "/")})
    unnamed = [b for b, v in out["bots"].items() if "명시" not in v]
    same = [b for b, v in out["bots"].items() if "명시=*" in v]
    blocked = [b for b, v in out["bots"].items() if v.startswith("차단")]
    out["checks"].append(("OK", "robots.txt", "HTTP 200"))
    out["checks"].append(("OK" if out["sitemaps"] else "FAIL", "Sitemap 지시자",
                          ", ".join(out["sitemaps"]) if out["sitemaps"] else "없음"))
    out["checks"].append(("OK" if not unnamed else "CHECK", "AI 크롤러 정책",
                          "전부 명시" if not unnamed else
                          "명시 안 됨 {}: {} — 와일드카드나 기본값이 적용 중이다".format(
                              len(unnamed), ", ".join(unnamed))))
    if same:
        out["checks"].append(("CHECK", "명시=와일드카드",
                              "{}: {} — 이름은 적혀 있으나 규칙이 User-agent: * 와 같아 "
                              "수집 권한 차이는 없다".format(len(same), ", ".join(same))))
    if out["disallow_paths"]:
        # 루트는 열려 있어도 일부 경로가 막혀 있으면 "다 가져갈 수 있다"로 읽힌다.
        out["checks"].append(("CHECK", "차단된 경로",
                              "{} — 루트 판정과 별개다".format(", ".join(out["disallow_paths"][:6]))))
    if blocked:
        out["checks"].append(("CHECK", "차단된 봇",
                              "{}: {} — 의도한 차단인지 확인한다".format(len(blocked), ", ".join(blocked))))
    return out


def audit_sitemap(base, ua, timeout, sitemaps):
    target = sitemaps[0] if sitemaps else fetch.join(base, "/sitemap.xml")
    status, final, _, body, _, error = fetch.fetch(target, ua, timeout)
    out = {"url": target, "final_url": final, "status": status, "error": error,
           "locs": [], "checks": []}
    if status != 200 or not body:
        out["checks"].append(("FAIL", "sitemap", "{} — HTTP {}".format(target, status)))
        return out
    is_index = "<sitemapindex" in body.lower()
    locs = parse.find_all(r"<loc>\s*(.*?)\s*</loc>", body)
    lastmods = parse.find_all(r"<lastmod>", body)
    out.update({"is_index": is_index, "locs": locs, "loc_count": len(locs),
                "bytes": len(body.encode("utf-8")), "lastmod_count": len(lastmods)})
    near_limit = len(locs) >= SITEMAP_URL_LIMIT * 0.8 or out["bytes"] >= SITEMAP_BYTE_LIMIT * 0.8
    out["checks"].append(("OK", "sitemap", "{} ({})".format(target, "index" if is_index else "urlset")))
    if is_index:
        out["checks"].append(("CHECK", "규모",
                              "하위 사이트맵 {}개 — 이 도구는 하위를 따라가지 않는다".format(len(locs))))
    else:
        out["checks"].append(("CHECK" if near_limit else "OK", "규모",
                              "URL {}개 / {:.1f}MB — 한도(5만·50MB)에 근접하면 미리 샤딩한다".format(
                                  len(locs), out["bytes"] / 1024 / 1024)))
    if not is_index:
        out["checks"].append(("OK" if len(lastmods) == len(locs) else "CHECK", "lastmod",
                              "{}/{} URL".format(len(lastmods), len(locs))))
    return out


def audit_llms(base, ua, timeout):
    out = {"checks": []}
    for path in ("/llms.txt", "/llms-full.txt"):
        status, final, headers, body, _, _ = fetch.fetch(fetch.join(base, path), ua, timeout)
        ctype = fetch.header(headers, "Content-Type").split(";")[0]
        ok = status == 200 and body.strip() and "<html" not in body[:400].lower()
        tokens = parse.estimate_tokens(body) if ok else 0
        out[path] = {"status": status, "bytes": len(body), "content_type": ctype,
                     "tokens": tokens}
        out["checks"].append((
            "OK" if ok else "CHECK", path,
            "{}바이트 · 토큰 {:,} 추정 ({})".format(len(body), tokens, ctype or "타입 미상") if ok
            else "없음 또는 HTML 응답 (HTTP {})".format(status)))
        # 안내서가 길면 그 자체가 컨텍스트를 먹어 정작 본문을 읽을 자리가 줄어든다.
        # 5,000은 검증된 임계가 아니라 권고이므로 CHECK까지만 낸다.
        if ok and path == "/llms.txt" and tokens > 5000:
            out["checks"].append(("CHECK", "llms.txt 분량",
                                  "토큰 {:,} 추정 — 안내서는 5,000 이하를 권한다".format(tokens)))
        if ok and path == "/llms.txt":
            if not any(h in body.lower() for h in LLMS_POLICY_HINTS):
                out["checks"].append(("CHECK", "llms.txt 데이터 정책",
                                      "출처·갱신 주기·인용 표기가 안 보인다"))
            relative = [u for u in parse.find_all(r"\]\(([^)]+)\)", body)
                        if not u.startswith(("http://", "https://", "#"))]
            if relative:
                out["checks"].append(("CHECK", "llms.txt 링크",
                                      "상대 경로 {}건: {} — 절대 URL을 권장한다".format(
                                          len(relative), ", ".join(relative[:3]))))
    return out


def audit_notfound(base, ua, timeout):
    url = fetch.join(base, "/__search-visibility-probe-404__")
    status, _, _, _, _, error = fetch.fetch(url, ua, timeout)
    out = {"url": url, "status": status, "error": error, "checks": []}
    if status == 404:
        out["checks"].append(("OK", "404 처리", "없는 경로가 404를 반환"))
    elif status == 200:
        out["checks"].append(("FAIL", "404 처리", "없는 경로가 200 — soft 404"))
    else:
        out["checks"].append(("CHECK", "404 처리", "HTTP {}".format(status)))
    return out
