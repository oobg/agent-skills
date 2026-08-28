# Search Visibility

사이트가 검색엔진, 답변엔진, 생성 AI, 네이버 AI 브리핑에 인용되도록 진단하고 고치는
에이전트 스킬입니다. 작업했다가 아니라 크롤러 눈으로 확인했다와 언제 다시 재는지까지를
작업 완료 조건으로 봅니다. 효과는 재측정 결과가 나온 뒤에야 주장합니다.

## 언제 사용하나요?

- 검색 노출이나 색인 상태를 점검하고 싶을 때
- 생성 AI가 우리 사이트를 출처로 인용하게 만들고 싶을 때
- `llms.txt`, 구조화 데이터, 사이트맵처럼 기계가 읽는 표면을 정비할 때
- 네이버 검색과 AI 브리핑 노출을 다룰 때
- 작업 후 효과를 숫자로 확인하는 측정 루프를 세팅할 때

- 어떤 질문의 답 자리를 누가 점유했는지 판독하고 우선순위를 정할 때

광고 집행이나 SNS 운영, 문구만 다듬는 작업은 다루지 않습니다. 문구는
[UX Writing](../ux-writing/README.md) 스킬을 사용합니다. 경쟁 판독도 **인용 경쟁만**
다루며 제품 비교, 가격 포지셔닝, 시장 규모 분석은 이 스킬 밖입니다.

유료 SEO 도구는 필요 없습니다. 공개 응답, 검색 결과 화면, 사용자의 검색 콘솔, 무료 관측
소스만으로 진단과 구현이 끝납니다.

## 다섯 레인

| 레인 | 상대 | 대표 작업 |
| --- | --- | --- |
| SEO | 검색 크롤러와 색인 | SSR 노출, 사이트맵, 메타, JSON-LD |
| AEO | 검색 결과 상단 AI 답변 박스 | 질문별 랜딩, 직답 문단, FAQ |
| GEO | 웹을 읽는 생성 AI | `llms.txt`, 크롤러 정책, 1차 소스 |
| LLMO | 브라우징 없는 모델 지식 | 엔티티 일관성, 학습 표면, 퍼머링크 |
| NEO | 네이버 검색과 AI 브리핑 | 서치어드바이저, 구조화된 사실, 투트랙 |

## 하지 않는 것

백링크 구매, 링크 품앗이, 자동화된 서로이웃과 댓글, 클로킹, 숨긴 텍스트, 문서 대량 복제는
요청받아도 수행하지 않습니다. 단기 순위가 아니라 도메인 전체를 거는 선택이기 때문입니다.
거절할 때는 이유와 함께 대신 할 수 있는 정공법을 제시합니다.

## 판정 기준

```text
코드에 있다  →  판정 근거가 아닙니다
자바스크립트 없이 받은 HTML에 있다  →  판정 근거입니다
```

진단 상태는 `양호 / 주의 / 미흡 / 확인 불가` 넷으로 적고, 확인하지 못한 항목을 양호로
올리지 않습니다.

## 사용 예

```text
example.com 검색 노출 상태 진단해줘. 한국 시장 서비스야.
```

```text
생성 AI가 우리 데이터 페이지를 인용하게 만들고 싶어. llms.txt부터 봐줘.
```

## 진단 도구

Python 3.8 이상에서 실행합니다. 표준 라이브러리만 사용하므로 설치할 것이 없습니다.

```bash
python3 <search-visibility 스킬 폴더>/scripts/crawl_audit.py https://example.com
python3 <search-visibility 스킬 폴더>/scripts/crawl_audit.py https://example.com --pages /pricing,/faq
python3 <search-visibility 스킬 폴더>/scripts/crawl_audit.py https://example.com --json > audit.json
python3 <search-visibility 스킬 폴더>/scripts/crawl_audit.py --coverage
python3 <search-visibility 스킬 폴더>/scripts/crawl_audit.py https://example.com --engine naver
```

robots.txt, 사이트맵, `llms.txt`, 404 처리, AI 크롤러 정책, 페이지별 메타와 구조화 데이터를
자바스크립트 없이 관측합니다. 결과는 `OK / CHECK / FAIL` 셋으로 나오는데, **CHECK는 판정이
아니라 사람이 확인할 항목입니다.** 스크립트는 관측만 하고 레인 점수를 매기지 않습니다.

가장 값이 큰 검사는 **구조화 데이터 대조**입니다. JSON-LD가 선언한 문답이 가시 텍스트에
실제로 있는지 확인합니다 — 화면에 없는 답변을 구조화 데이터가 말하고 있으면 렌더링하지
않는 소비자에게 그 답변은 존재하지 않습니다.

무엇이 자동이고 무엇이 사람 몫인지는 `--coverage`가 알려줍니다. 이 목록은 스크립트가
정본이며 문서에 복제하지 않습니다.

자기 사이트와 판독 대상의 공개 페이지에만 사용합니다. 로그인이나 결제 뒤의 콘텐츠는 대상이
아니며, 요청 수를 제한하고 요청 사이에 지연을 두고, 크롤러 UA를 사칭하지 않습니다.

## 구성

```text
search-visibility/
├── SKILL.md
├── README.md
├── agents/
│   └── visibility-auditor.md
├── references/
│   ├── seo.md
│   ├── aeo.md
│   ├── geo.md
│   ├── llmo.md
│   ├── neo-naver.md
│   ├── citation-competition.md
│   ├── measure.md
│   ├── templates.md
│   └── ontology-boost.md
└── scripts/
    ├── crawl_audit.py
    ├── fetch.py
    ├── parse.py
    ├── checks_site.py
    ├── checks_page.py
    ├── checks_passage.py
    ├── checks_cross.py
    ├── checks_schema.py
    └── schema_rules.py
```

- [`SKILL.md`](SKILL.md): 진단 절차, 불변 원칙, 승인 게이트, 보고 형식
- [`references/seo.md`](references/seo.md): 크롤러 노출, 사이트맵, 메타, 구조화 데이터, 응답 위생
- [`references/aeo.md`](references/aeo.md): 질문별 랜딩과 추출되는 문장의 형태
- [`references/geo.md`](references/geo.md): `llms.txt`, AI 크롤러 정책, 1차 소스 되기
- [`references/llmo.md`](references/llmo.md): 엔티티 일관성과 학습 표면 관리
- [`references/neo-naver.md`](references/neo-naver.md): 서치어드바이저, AI 브리핑 인용 요건, 투트랙
- [`references/citation-competition.md`](references/citation-competition.md): 인용 경쟁 판독 —
  대상 3분류, 표본 규칙, 판독 축, 산술 검산, FAQ 역산, 재관측, 판정
- [`references/measure.md`](references/measure.md): 기준선, 재측정 일정, 지표 읽는 법
- [`references/templates.md`](references/templates.md): 진단 리포트, 측정 로그, 인용 프로브 시트,
  `llms.txt`, robots.txt, JSON-LD, 의도 랜딩 골격
- [`agents/visibility-auditor.md`](agents/visibility-auditor.md): 결과만 보고 채점하는
  fresh-eyes 검증 패스
- [`scripts/crawl_audit.py`](scripts/crawl_audit.py): CLI 진입점, 관측 순서와 출력, `--coverage`
- [`scripts/fetch.py`](scripts/fetch.py): HTTP 회수. 자바스크립트를 실행하지 않습니다
- [`scripts/parse.py`](scripts/parse.py): HTML·JSON-LD 파싱 유틸
- [`scripts/checks_site.py`](scripts/checks_site.py): robots.txt, 사이트맵, `llms.txt`, 404 처리
- [`scripts/checks_page.py`](scripts/checks_page.py): 페이지 단위 관측과 구조화 데이터 대조
- [`scripts/checks_passage.py`](scripts/checks_passage.py): 문단 단위 관측. 인용은 페이지가 아니라
  문단째로 잘려 나가므로 자체 완결 여부를 문단마다 봅니다
- [`scripts/checks_cross.py`](scripts/checks_cross.py): 페이지 간 대조(메타 중복, 엔티티 표기, 사이트맵 포함)
- [`scripts/checks_schema.py`](scripts/checks_schema.py): 구조화 데이터를 구글·네이버 규칙표에
  각각 대조. 두 엔진은 필수 속성이 다르므로 판정이 엔진별로 따로 나옵니다
- [`scripts/schema_rules.py`](scripts/schema_rules.py): 엔진별 규칙표. 데이터만 있고 판정
  로직은 없습니다. 엔진이 정책을 바꾸면 해당 항목만 고칩니다
- [`references/ontology-boost.md`](references/ontology-boost.md): 온톨로지가 있을 때만 여는
  선택 모듈. 질문 목록, 1차 소스 정의, 서비스명 표기, 과거 결정을 회수합니다.

설치 방법은 저장소의 [루트 README](../../README.md)를 참고하세요.
