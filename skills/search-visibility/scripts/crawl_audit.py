#!/usr/bin/env python3
"""
crawl_audit.py — 크롤러의 눈으로 사이트를 관측한다.

자바스크립트를 실행하지 않고 받은 응답만으로 SEO·AEO·GEO·NEO 표면을 훑어 관측치를 낸다.
표준 라이브러리만 쓰므로 별도 설치가 필요 없다.

이 스크립트는 **관측만 하고 레인 점수를 판정하지 않는다.** 기계적으로 참·거짓이 갈리는
항목만 OK/FAIL로 찍고, 문맥이 필요한 항목은 CHECK로 남긴다. 최종 판정은 SKILL.md의
4상태(양호/주의/미흡/확인 불가)로 사람이나 에이전트가 내린다. CHECK를 양호로 올리지 않는다.

사용법:
    python3 crawl_audit.py https://example.com
    python3 crawl_audit.py https://example.com --pages /pricing,/docs/faq
    python3 crawl_audit.py https://example.com --json > audit.json
    python3 crawl_audit.py --coverage          # 무엇을 자동으로 보는지 목록

주의:
    자기 사이트, 또는 판독 대상의 공개 페이지에만 쓴다. 로그인·결제·접근 제한 뒤의
    콘텐츠는 대상이 아니다. 기본값은 홈 + 지정 페이지로 요청 수를 제한하고 요청 사이에
    지연을 두며, 크롤러 UA를 사칭하지 않는다(--user-agent로 바꿀 수는 있다).
    남의 사이트를 대량으로 훑는 용도가 아니다.

종료 코드: 관측을 마치면 0, 대상에 전혀 접속하지 못하면 2.
"""

import argparse
import json
import sys
import time

import checks_cross
import checks_page
import checks_passage
import checks_site
import fetch

# 자동으로 보는 항목. 문서에 이 목록을 복제하지 않는다 — 두 곳에 적으면 갈라진다.
COVERAGE = [
    ("SEO", "robots.txt 존재와 Sitemap 지시자, 사이트맵 규모·lastmod 충족률"),
    ("SEO", "본문 SSR 노출량, h1 개수, title·description 길이"),
    ("SEO", "canonical 존재와 self 여부, hreflang 건수와 x-default"),
    ("SEO", "리다이렉트 홉, 없는 경로의 404 응답(soft 404 탐지), meta noindex"),
    ("SEO", "og:image 실제 응답 확인, 페이지 간 제목 중복, 사이트맵 포함 여부"),
    ("AEO", "JSON-LD가 선언한 문답·제목이 가시 텍스트에 실제로 있는지 대조"),
    ("SEO", "구글 규칙표 대조 — 타입별 필수 속성, 조건부 필수, 열거값(availability 등)"),
    ("NEO", "네이버 규칙표 대조 — 타입별 필수 속성. 구글과 다른 표를 쓴다"),
    ("SEO", "@context 존재와 schema.org 여부, 상용 목록에 없는 타입 이름(오타 탐지)"),
    ("SEO", "날짜(ISO 8601)·기간(duration)·숫자·URL 절대경로 형식"),
    ("SEO", "구글이 리치 결과를 내린 타입(FAQPage·HowTo) 사용 여부"),
    ("NEO", "사이트 연관채널 — 루트의 name·url·sameAs와 네이버 인식 채널 포함 여부"),
    ("NEO", "Microdata 선언 탐지 — 네이버가 JSON-LD와 나란히 권장하는 형식이다"),
    ("AEO", "표·목록·h2·h3 개수(인용 단위 구조), 기준 표기 없는 수치"),
    ("AEO", "문단 단위 관측 — 자체 완결 문단 수, 맥락 지시어에 기댄 문단, 첫 문단 길이"),
    ("SEO", "프레임워크 루트 안의 본문 길이(헤더·푸터만 SSR인 경우 탐지)"),
    ("GEO", "llms.txt·llms-full.txt 존재와 타입, 데이터 정책 문구, 상대 경로 링크"),
    ("GEO", "AI 크롤러 9종의 루트 접근 정책과 와일드카드 동일 여부"),
    ("LLMO", "Organization sameAs 건수, 페이지 간 Organization 이름 분열"),
    ("NEO", "Yeti 접근 정책, viewport 선언"),
]
MANUAL = [
    "인용 실측(질문별 O/X) — 검색·답변 화면을 직접 봐야 한다",
    "검색 콘솔·서치어드바이저 지표 — 계정이 필요하다",
    "직답 문단이 실제로 답인지, 질문이 실수요인지 — 의미 판정이다",
    "수치의 산식이 맞는지(산술 검산) — 원자료를 알아야 한다",
    "의도된 색인 제외인지 — 사용자 확인이 필요하다",
    "리치 결과 테스트와 배포 후 리치 결과 상태 보고서(GSC) — 브라우저와 계정이 필요하다",
    "schema.org 검증기(네이버가 지정한 도구) — 브라우저가 필요하다",
    "타입 선택이 페이지 실체와 맞는지, 평점·가격이 실제 운영과 같은지 — 의미 판정이다",
]


def render(result):
    icon = {"OK": "OK   ", "CHECK": "CHECK", "FAIL": "FAIL "}
    lines = []
    for section, data in result["sections"]:
        lines.append("\n[{}]".format(section))
        for state, label, detail in data.get("checks", []):
            lines.append("  {} {:<16} {}".format(icon[state], label, detail))
    bots = next((d.get("bots") or {} for s, d in result["sections"] if s == "robots.txt"), {})
    if bots:
        lines.append("\n[AI 크롤러 정책] — 루트(/) 접근 기준")
        for bot, verdict in bots.items():
            lines.append("  {:<20} {}".format(bot, verdict))
    lines.append("\n관측 완료: OK {ok} · CHECK {check} · FAIL {fail}".format(**result["summary"]))
    lines.append("CHECK는 판정이 아니라 사람이 확인할 항목이다. 양호로 올리지 않는다.")
    lines.append("자동으로 보지 않는 항목은 --coverage로 확인한다.")
    return "\n".join(lines)


def print_coverage():
    print("자동으로 관측하는 항목")
    for lane, item in COVERAGE:
        print("  {:<5} {}".format(lane, item))
    print("\n사람이 판정해야 하는 항목")
    for item in MANUAL:
        print("  - {}".format(item))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("base", nargs="?", help="진단할 사이트의 루트 URL")
    parser.add_argument("--pages", default="", help="추가로 볼 경로를 쉼표로 구분")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--delay", type=float, default=0.5, help="요청 사이 지연(초)")
    parser.add_argument("--user-agent", default=fetch.DEFAULT_UA)
    parser.add_argument("--no-asset-check", action="store_true", help="og:image 실응답 확인 생략")
    parser.add_argument("--engine", choices=["google", "naver", "both"], default="both",
                        help="구조화 데이터를 어느 엔진 규칙표로 볼지 (기본: both)")
    parser.add_argument("--json", action="store_true", help="관측 결과를 JSON으로 출력")
    parser.add_argument("--coverage", action="store_true", help="자동·수동 항목 목록만 출력")
    args = parser.parse_args(argv)

    if args.coverage:
        print_coverage()
        return 0
    if not args.base:
        parser.error("base URL이 필요하다 (또는 --coverage)")

    base = args.base if "://" in args.base else "https://" + args.base
    ua, timeout = args.user_agent, args.timeout
    assets = not args.no_asset_check
    engines = ("google", "naver") if args.engine == "both" else (args.engine,)

    home = checks_page.audit_page(base, ua, timeout, assets, engines)
    if home.get("error") and home.get("status") is None:
        print("대상에 접속하지 못했다: {}".format(home["error"]), file=sys.stderr)
        return 2

    time.sleep(args.delay)
    robots = checks_site.audit_robots(base, ua, timeout)
    time.sleep(args.delay)
    sitemap = checks_site.audit_sitemap(base, ua, timeout, robots["sitemaps"])
    time.sleep(args.delay)
    llms = checks_site.audit_llms(base, ua, timeout)
    time.sleep(args.delay)
    notfound = checks_site.audit_notfound(base, ua, timeout)

    pages = [home]
    sections = [("robots.txt", robots), ("sitemap", sitemap), ("llms.txt", llms),
                ("404 처리", notfound), ("페이지: {}".format(base), home)]
    for path in [p.strip() for p in args.pages.split(",") if p.strip()]:
        time.sleep(args.delay)
        url = fetch.join(base, path)
        page = checks_page.audit_page(url, ua, timeout, assets, engines)
        pages.append(page)
        sections.append(("페이지: {}".format(url), page))

    page_locs = [] if sitemap.get("is_index") else (sitemap.get("locs") or [])
    cross = checks_cross.audit_cross(pages, page_locs)
    if cross.get("checks"):
        sections.append(("페이지 간 대조", cross))

    summary = {"ok": 0, "check": 0, "fail": 0}
    for _, data in sections:
        for state, _, _ in data.get("checks", []):
            summary[state.lower()] += 1

    result = {"base": base, "user_agent": ua, "engines": list(engines),
              "sections": sections, "summary": summary}
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str) if args.json
          else render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
