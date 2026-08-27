#!/usr/bin/env python3
"""
crawl_audit.py — 크롤러의 눈으로 사이트를 관측한다.

자바스크립트를 실행하지 않고 받은 응답만으로 SEO·AEO·GEO·NEO 표면을 훑어
관측치를 낸다. 표준 라이브러리만 쓰므로 별도 설치가 필요 없다.

이 스크립트는 **관측만 하고 레인 점수를 판정하지 않는다.** 기계적으로 참·거짓이
갈리는 항목만 OK/FAIL로 찍고, 문맥이 필요한 항목은 CHECK로 남긴다. 최종 판정은
SKILL.md의 4상태(양호/주의/미흡/확인 불가)로 사람이나 에이전트가 내린다.
CHECK를 양호로 올리지 않는다.

사용법:
    python3 crawl_audit.py https://example.com
    python3 crawl_audit.py https://example.com --pages /pricing,/docs/faq
    python3 crawl_audit.py https://example.com --json > audit.json

주의:
    자기 사이트, 또는 판독 대상의 공개 페이지에만 쓴다. 로그인·결제·접근 제한 뒤의
    콘텐츠는 대상이 아니다. 기본값은 홈 + 지정 페이지로 요청 수를 제한하고 요청 사이에
    지연을 두며, 크롤러 UA를 사칭하지 않는다(--user-agent로 바꿀 수는 있다).
    남의 사이트를 대량으로 훑는 용도가 아니다.

종료 코드: 관측을 마치면 0, 대상에 전혀 접속하지 못하면 2.
"""

import argparse
import gzip
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_UA = "search-visibility-audit/1.0 (+skill: search-visibility)"
AI_BOTS = [
    "GPTBot",
    "OAI-SearchBot",
    "ChatGPT-User",
    "ClaudeBot",
    "Claude-SearchBot",
    "PerplexityBot",
    "Google-Extended",
    "Applebot-Extended",
    "Yeti",
]
SITEMAP_URL_LIMIT = 50000
SITEMAP_BYTE_LIMIT = 50 * 1024 * 1024
TAG_RE = re.compile(r"<(script|style|template|noscript)\b.*?</\1>", re.S | re.I)


def fetch(url, ua, timeout, max_bytes=3_000_000):
    """한 번 요청하고 (status, final_url, headers, body, hops, error)를 돌려준다."""
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "gzip"})
    hops = 0

    class Counter(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            nonlocal hops
            hops += 1
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = urllib.request.build_opener(Counter, urllib.request.HTTPSHandler(context=ctx))
    try:
        with opener.open(req, timeout=timeout) as resp:
            raw = resp.read(max_bytes)
            if resp.headers.get("Content-Encoding") == "gzip":
                try:
                    raw = gzip.decompress(raw)
                except OSError:
                    pass
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.status, resp.geturl(), dict(resp.headers), raw.decode(charset, "replace"), hops, None
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read(max_bytes).decode("utf-8", "replace")
        except Exception:  # noqa: BLE001 - 본문은 부가 정보다
            pass
        return exc.code, url, dict(exc.headers or {}), body, hops, None
    except Exception as exc:  # noqa: BLE001 - 네트워크 오류를 관측 결과로 남긴다
        return None, url, {}, "", hops, "{}: {}".format(type(exc).__name__, exc)


def visible_text(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", TAG_RE.sub(" ", html))).strip()


def find_all(pattern, html, flags=re.I | re.S):
    return re.findall(pattern, html, flags)


def meta_content(html, key, attr="name"):
    hit = re.search(
        r'<meta[^>]+{}=["\']{}["\'][^>]*content=["\'](.*?)["\']'.format(attr, key), html, re.I | re.S
    ) or re.search(
        r'<meta[^>]+content=["\'](.*?)["\'][^>]*{}=["\']{}["\']'.format(attr, key), html, re.I | re.S
    )
    return hit.group(1).strip() if hit else None


def audit_page(url, ua, timeout):
    status, final, headers, html, hops, error = fetch(url, ua, timeout)
    page = {
        "url": url,
        "final_url": final,
        "status": status,
        "redirect_hops": hops,
        "error": error,
        "checks": [],
    }
    if error or status is None:
        page["checks"].append(("FAIL", "요청", error or "응답 없음"))
        return page
    if status >= 400:
        page["checks"].append(("FAIL", "응답", "HTTP {}".format(status)))
        return page

    text = visible_text(html)
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    title = re.sub(r"\s+", " ", title.group(1)).strip() if title else None
    desc = meta_content(html, "description")
    robots_meta = (meta_content(html, "robots") or "").lower()
    h1 = find_all(r"<h1\b", html)
    ld_blocks = find_all(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html)
    ld_types, ld_broken = [], 0
    for block in ld_blocks:
        try:
            data = json.loads(block.strip())
        except ValueError:
            ld_broken += 1
            continue
        for node in data if isinstance(data, list) else [data]:
            if isinstance(node, dict):
                t = node.get("@type")
                ld_types.extend(t if isinstance(t, list) else [t] if t else [])

    page.update(
        {
            "bytes": len(html),
            "text_chars": len(text),
            "title": title,
            "title_len": len(title) if title else 0,
            "description_len": len(desc) if desc else 0,
            "h1_count": len(h1),
            "canonical": bool(find_all(r'<link[^>]+rel=["\']canonical["\']', html)),
            "og_image": bool(meta_content(html, "og:image", attr="property")),
            "hreflang_count": len(find_all(r'<link[^>]+hreflang=', html)),
            "jsonld_blocks": len(ld_blocks),
            "jsonld_types": sorted(set(ld_types)),
            "jsonld_parse_errors": ld_broken,
            "noindex": "noindex" in robots_meta,
        }
    )

    add = page["checks"].append
    add(("OK" if hops <= 1 else "CHECK", "리다이렉트", "{}홉".format(hops)))
    if page["noindex"]:
        add(("FAIL", "색인", "meta robots에 noindex"))
    add(
        ("CHECK" if page["text_chars"] < 500 else "OK", "본문 노출",
         "가시 텍스트 {}자 — 500자 미만이면 CSR 여부를 직접 확인한다".format(page["text_chars"])
         if page["text_chars"] < 500 else "가시 텍스트 {}자".format(page["text_chars"]))
    )
    add(("OK" if page["h1_count"] == 1 else "CHECK", "h1", "{}개".format(page["h1_count"])))
    if not title:
        add(("FAIL", "title", "없음"))
    else:
        add((
            "OK" if 15 <= page["title_len"] <= 60 else "CHECK",
            "title",
            "{}자".format(page["title_len"]),
        ))
    if not desc:
        add(("FAIL", "description", "없음"))
    else:
        add((
            "OK" if 80 <= page["description_len"] <= 165 else "CHECK",
            "description",
            "{}자".format(page["description_len"]),
        ))
    add(("OK" if page["canonical"] else "CHECK", "canonical", "있음" if page["canonical"] else "없음"))
    add(("OK" if page["og_image"] else "CHECK", "og:image", "있음" if page["og_image"] else "없음"))
    if ld_broken:
        add(("FAIL", "JSON-LD", "파싱 실패 {}블록".format(ld_broken)))
    add((
        "OK" if page["jsonld_types"] else "CHECK",
        "JSON-LD",
        ", ".join(page["jsonld_types"]) if page["jsonld_types"] else "없음",
    ))
    return page


def audit_robots(base, ua, timeout):
    status, _, _, body, _, error = fetch(urllib.parse.urljoin(base, "/robots.txt"), ua, timeout)
    out = {"status": status, "error": error, "sitemaps": [], "bots": {}, "checks": []}
    if status != 200 or not body:
        # robots.txt가 없으면 모든 봇이 무정책이다. 무정책은 중립이 아니라 미지정이므로
        # 봇 표를 비우지 않고 그대로 보여준다.
        out["bots"] = {bot: "미지정" for bot in AI_BOTS}
        out["checks"].append(("FAIL", "robots.txt", "없음 또는 HTTP {}".format(status)))
        out["checks"].append(("CHECK", "AI 크롤러 정책", "robots.txt가 없어 전부 미지정"))
        return out
    out["sitemaps"] = [m.strip() for m in find_all(r"^\s*Sitemap:\s*(\S+)", body, re.I | re.M)]
    agent, rules = None, {}
    for line in body.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = (p.strip() for p in line.split(":", 1))
        low = key.lower()
        if low == "user-agent":
            agent = value
            rules.setdefault(agent.lower(), [])
        elif low in ("allow", "disallow") and agent is not None:
            rules[agent.lower()].append((low, value))
    for bot in AI_BOTS:
        entries = rules.get(bot.lower())
        if entries is None:
            out["bots"][bot] = "미지정"
        elif any(k == "disallow" and v == "/" for k, v in entries):
            out["bots"][bot] = "차단"
        else:
            out["bots"][bot] = "허용"
    out["checks"].append(("OK", "robots.txt", "HTTP 200"))
    out["checks"].append((
        "OK" if out["sitemaps"] else "FAIL",
        "Sitemap 지시자",
        ", ".join(out["sitemaps"]) if out["sitemaps"] else "없음",
    ))
    undecided = [b for b, v in out["bots"].items() if v == "미지정"]
    out["checks"].append((
        "OK" if not undecided else "CHECK",
        "AI 크롤러 정책",
        "전부 명시" if not undecided else "미지정 {}: {}".format(len(undecided), ", ".join(undecided)),
    ))
    return out


def audit_sitemap(base, ua, timeout, sitemaps):
    target = sitemaps[0] if sitemaps else urllib.parse.urljoin(base, "/sitemap.xml")
    status, final, _, body, _, error = fetch(target, ua, timeout)
    out = {"url": target, "final_url": final, "status": status, "error": error, "checks": []}
    if status != 200 or not body:
        out["checks"].append(("FAIL", "sitemap", "{} — HTTP {}".format(target, status)))
        return out
    is_index = "<sitemapindex" in body.lower()
    locs = find_all(r"<loc>\s*(.*?)\s*</loc>", body)
    lastmods = find_all(r"<lastmod>", body)
    out.update({"is_index": is_index, "loc_count": len(locs), "bytes": len(body.encode("utf-8")),
                "lastmod_count": len(lastmods)})
    out["checks"].append(("OK", "sitemap", "{} ({})".format(target, "index" if is_index else "urlset")))
    out["checks"].append((
        "CHECK" if out["loc_count"] >= SITEMAP_URL_LIMIT * 0.8 or out["bytes"] >= SITEMAP_BYTE_LIMIT * 0.8 else "OK",
        "규모",
        "URL {}개 / {:.1f}MB — 한도(5만·50MB)에 근접하면 미리 샤딩한다".format(
            out["loc_count"], out["bytes"] / 1024 / 1024
        ),
    ))
    if not is_index:
        out["checks"].append((
            "OK" if lastmods else "CHECK",
            "lastmod",
            "{}건".format(len(lastmods)) if lastmods else "없음",
        ))
    out["checks"].append(("CHECK", "포함 범위", "상세 페이지가 전부 들어 있는지는 사이트 구조를 알아야 판정된다"))
    return out


def audit_llms(base, ua, timeout):
    out = {"checks": []}
    for path in ("/llms.txt", "/llms-full.txt"):
        status, _, _, body, _, _ = fetch(urllib.parse.urljoin(base, path), ua, timeout)
        ok = status == 200 and body.strip() and "<html" not in body[:400].lower()
        out[path] = {"status": status, "bytes": len(body)}
        out["checks"].append((
            "OK" if ok else ("FAIL" if path == "/llms.txt" else "CHECK"),
            path,
            "{}바이트".format(len(body)) if ok else "없음 또는 HTML 응답 (HTTP {})".format(status),
        ))
    return out


def audit_notfound(base, ua, timeout):
    url = urllib.parse.urljoin(base, "/__search-visibility-probe-404__")
    status, _, _, body, _, error = fetch(url, ua, timeout)
    out = {"url": url, "status": status, "error": error, "checks": []}
    if status == 404:
        out["checks"].append(("OK", "404 처리", "없는 경로가 404를 반환"))
    elif status == 200:
        out["checks"].append(("FAIL", "404 처리", "없는 경로가 200 — soft 404"))
    else:
        out["checks"].append(("CHECK", "404 처리", "HTTP {}".format(status)))
    return out


def render(result):
    lines = []
    icon = {"OK": "OK   ", "CHECK": "CHECK", "FAIL": "FAIL "}
    for section, data in result["sections"]:
        lines.append("\n[{}]".format(section))
        for state, label, detail in data.get("checks", []):
            lines.append("  {} {:<14} {}".format(icon[state], label, detail))
    bots = {}
    for section, data in result["sections"]:
        if section == "robots.txt":
            bots = data.get("bots") or {}
            break
    if bots:
        lines.append("\n[AI 크롤러 정책]")
        for bot, verdict in bots.items():
            lines.append("  {:<20} {}".format(bot, verdict))
    counts = result["summary"]
    lines.append(
        "\n관측 완료: OK {ok} · CHECK {check} · FAIL {fail}".format(**counts)
    )
    lines.append("CHECK는 판정이 아니라 사람이 확인할 항목이다. 양호로 올리지 않는다.")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("base", help="진단할 사이트의 루트 URL")
    parser.add_argument("--pages", default="", help="추가로 볼 경로를 쉼표로 구분 (예: /pricing,/faq)")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--delay", type=float, default=0.5, help="요청 사이 지연(초)")
    parser.add_argument("--user-agent", default=DEFAULT_UA)
    parser.add_argument("--json", action="store_true", help="관측 결과를 JSON으로 출력")
    args = parser.parse_args(argv)

    base = args.base if "://" in args.base else "https://" + args.base
    ua, timeout = args.user_agent, args.timeout

    home = audit_page(base, ua, timeout)
    if home.get("error") and home.get("status") is None:
        print("대상에 접속하지 못했다: {}".format(home["error"]), file=sys.stderr)
        return 2

    time.sleep(args.delay)
    robots = audit_robots(base, ua, timeout)
    time.sleep(args.delay)
    sitemap = audit_sitemap(base, ua, timeout, robots["sitemaps"])
    time.sleep(args.delay)
    llms = audit_llms(base, ua, timeout)
    time.sleep(args.delay)
    notfound = audit_notfound(base, ua, timeout)

    sections = [("robots.txt", robots), ("sitemap", sitemap), ("llms.txt", llms),
                ("404 처리", notfound), ("페이지: {}".format(base), home)]
    for path in [p.strip() for p in args.pages.split(",") if p.strip()]:
        time.sleep(args.delay)
        url = urllib.parse.urljoin(base, path)
        sections.append(("페이지: {}".format(url), audit_page(url, ua, timeout)))

    summary = {"ok": 0, "check": 0, "fail": 0}
    for _, data in sections:
        for state, _, _ in data.get("checks", []):
            summary[state.lower()] += 1

    result = {"base": base, "user_agent": ua, "sections": sections, "summary": summary}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
