# 산출물 템플릿

진단 리포트, 측정 로그, 그리고 실제로 배포하는 파일의 기본형이다. 그대로 붙여넣지 말고
사이트의 사실에 맞게 채운다. **채울 수 없는 칸은 지우거나 `미확인`으로 남기고,
그럴듯한 값으로 메우지 않는다.** 확인되지 않은 값이 들어간 순간 이 스킬이 막으려는
바로 그 실패(사실 아닌 것을 말하는 화면)가 된다.

## 1. 진단 리포트

Phase 0의 산출물이다. 근거 칸에는 관측 결과만 적는다.

```markdown
# 검색 노출 진단 — example.com (2026-08-27)

관측 방법: `python3 scripts/crawl_audit.py https://example.com --pages /pricing,/faq`
관측하지 못한 것: 네이버 서치어드바이저 지표 (계정 필요), AI 인용 여부 (수동 확인 예정)

| 레인 | 상태 | 근거 |
| --- | --- | --- |
| SEO | 주의 | 홈은 SSR이나 /docs 이하 가시 텍스트 120자, 상세 페이지가 사이트맵에 없음 |
| AEO | 미흡 | FAQPage JSON-LD 0건, 질문형 랜딩 없음 |
| GEO | 미흡 | llms.txt 404, AI 크롤러 정책 전부 미지정 |
| LLMO | 확인 불가 | 브라우징 없는 모델 응답을 아직 안 재봄 |
| NEO | 주의 | Yeti 미지정, 모바일 첫 화면에 핵심 수치 없음 |

## 우선순위 제안
1. /docs 이하 SSR 확인 — 이게 안 되면 아래 작업의 효과를 잴 수 없다
2. 사이트맵에 상세 페이지 포함
3. llms.txt + AI 크롤러 정책 결정 (허용 범위는 사용자 결정 필요)

승인받을 것: 3번의 크롤러 허용 범위
```

## 2. 측정 로그

프로젝트에 파일로 남긴다. 대화에만 적으면 다음 세션이 기준선을 처음부터 다시 찍는다.

```markdown
# 검색 노출 측정 로그 — example.com

## 2026-08-27 기준선
- Search Console (7/30~8/26): 노출 12,400 · 클릭 180 · 평균 순위 18.4
- 서치어드바이저 (7/30~8/26): 노출 8,900 · 클릭 240
- 색인: site: 검색 320건 / GSC 색인 411건
- AI 인용: 0/8 (질문 세트는 아래 3절)

## 2026-08-29 변경
- 의도 랜딩 6종 추가, llms.txt 생성, FAQPage JSON-LD 적용
- 재측정 예정: 2026-09-12 (14일), LLMO는 2026-11-27 (분기)

## 2026-09-12 재측정
- (비워 둔다. 예상 수치로 채우지 않는다)
```

## 3. 인용 프로브 시트

AEO·GEO·NEO의 인용 여부는 자동으로 확인되지 않는다. 질문을 고정해 두고 같은 질문으로
반복 측정해야 변화를 읽을 수 있다.

```markdown
| # | 질문 | 출처 | 8/27 | 9/12 |
| --- | --- | --- | --- | --- |
| 1 | 어떤 회사 실적발표 언제 | 고객 문의 | X | |
| 2 | 배당 기준일 확인하는 법 | GSC 검색어 | X | |

측정 대상: Google AI Overviews · Perplexity · ChatGPT 검색 모드 · 네이버 AI 브리핑
기록: 출처 목록에 도메인이 뜨면 O, 아니면 X. 모델과 측정 시각을 함께 남긴다.
```

## 4. 인용 경쟁 판독표

질문 하나에 표 하나다. 축은 인용 여부를 가르는 것만 세우고, 판정 칸에는 관측한 것만 적는다.

```markdown
### 질문: "어떤 회사 실적발표 언제"

| 축 | 점유 A | 점유 B | 점유 C | 점유 D | 우리 |
| --- | --- | --- | --- | --- | --- |
| 직답 위치 | 첫 화면 | 3스크롤 | 첫 화면 | 없음 | 없음 |
| 기준 명시 | 기준일 있음 | 미상 | 미상 | 미상 | — |
| 1차 소스 | 공시 기반 | 2차 요약 | 2차 요약 | 2차 요약 | 공시 기반 |
| 구조 | 표 | 산문 | 표 | 산문 | 표 |
| FAQ | 5개 | 0 | 0 | 0 | 0 |
| 마지막 갱신 | 2026-08-26 | 2025-11 | 2026-03 | 미상 | 매일 |

전수 공백: 기준 명시 (A만 있음 → 개별 선택), FAQ (A만 있음 → 개별 선택)
반례: B는 우리보다 내부 링크 구조가 낫다
판정: 차별화 가능 — 1차 소스와 갱신 주기는 우리가 앞선다. 직답 문단이 없는 것이 유일한 결손
다음에 뒤집힐 조건: A가 갱신 주기를 일 단위로 올리면 재판정
```

## 5. llms.txt

```markdown
# 서비스명

> 한 문장 설명. 무엇의 1차 소스인지 밝힌다.

## 핵심 페이지
- [페이지 이름](https://example.com/path): 이 페이지가 확정해 주는 사실
- [페이지 이름](https://example.com/path): 이 페이지가 확정해 주는 사실

## 데이터 정책
- 출처: 무엇을 근거로 산출하는지
- 갱신 주기: 실제 주기만 적는다
- 인용 표기: example.com
```

## 6. robots.txt의 AI 크롤러 블록

허용 범위는 사용자 결정이다. 아래는 인용 유입을 원할 때의 형태이고, 학습만 막으려면
검색용 봇과 학습용 봇을 갈라 적는다.

```
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Yeti
Allow: /

Sitemap: https://example.com/sitemap.xml
```

## 7. JSON-LD

가시 텍스트에 없는 내용을 넣지 않는다. Organization은 사이트 전역에서 한 번만 선언하고
나머지 페이지는 `@id`로 참조한다.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#org",
  "name": "서비스명",
  "url": "https://example.com",
  "sameAs": [
    "https://github.com/example",
    "https://www.linkedin.com/company/example"
  ]
}
</script>
```

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "화면에 보이는 질문과 글자까지 같게",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "화면에 보이는 답과 글자까지 같게"
    }
  }]
}
</script>
```

`crawl_audit.py`는 아래 타입의 `name`·`headline`이 가시 텍스트에 있는지도 대조한다.
화면에 없는 이름을 선언하면 엔티티 표기가 갈라진다.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "화면의 h1과 같은 제목",
  "datePublished": "2026-08-27",
  "dateModified": "2026-08-27",
  "author": {"@type": "Person", "name": "저자 이름", "sameAs": ["https://..."]},
  "publisher": {"@id": "https://example.com/#org"}
}
</script>
```

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "화면에 쓰는 제품명과 같은 표기",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "description": "화면 설명과 같은 내용",
  "offers": {"@type": "Offer", "category": "B2B"}
}
</script>
```

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "화면에 쓰는 제품명",
  "description": "화면 설명과 같은 내용",
  "brand": {"@id": "https://example.com/#org"},
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW",
             "availability": "https://schema.org/InStock"}
}
</script>
```

다국어 사이트에서 화면은 한글, `name`은 영문으로 쓰면 대조에서 걸린다. 스팸은 아니지만
모델 안에서 엔티티가 갈라지므로 `alternateName`으로 함께 선언한다.

## 8. 의도 랜딩 페이지의 골격

```markdown
# (질문을 그대로 쓴 h1)

(첫 문단: 40자 내외 직답. 주어·수치·기준일을 자체 보유한다.)

| 항목 | 값 | 기준일 |
| --- | --- | --- |
| ... | ... | 2026-08-27 |

## 산출 방식
(어떤 원본에서 어떻게 계산했는지. 숨기면 인용해도 되는 숫자인지 판정할 근거가 없다.)

## 자주 묻는 질문
(실제 검색 질문 3~5개. FAQPage JSON-LD와 글자까지 동일하게.)
```
