# Search Visibility

사이트가 검색엔진, 답변엔진, 생성 AI, 네이버 AI 브리핑에 인용되도록 진단하고 고치는
에이전트 스킬입니다. 작업했다가 아니라 크롤러 눈으로 확인했다와 언제 다시 재는지까지를
완료 조건으로 봅니다.

## 언제 사용하나요?

- 검색 노출이나 색인 상태를 점검하고 싶을 때
- 생성 AI가 우리 사이트를 출처로 인용하게 만들고 싶을 때
- `llms.txt`, 구조화 데이터, 사이트맵처럼 기계가 읽는 표면을 정비할 때
- 네이버 검색과 AI 브리핑 노출을 다룰 때
- 작업 후 효과를 숫자로 확인하는 측정 루프를 세팅할 때

광고 집행이나 SNS 운영, 문구만 다듬는 작업은 다루지 않습니다. 문구는
[UX Writing](../ux-writing/README.md) 스킬을 사용합니다.

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
```

robots.txt, 사이트맵, `llms.txt`, 404 처리, AI 크롤러 정책, 페이지별 메타와 구조화 데이터를
자바스크립트 없이 관측합니다. 결과는 `OK / CHECK / FAIL` 셋으로 나오는데, **CHECK는 판정이
아니라 사람이 확인할 항목입니다.** 스크립트는 관측만 하고 레인 점수를 매기지 않습니다.

허가받은 사이트에만 사용합니다. 요청 수를 제한하고 요청 사이에 지연을 두며, 크롤러 UA를
사칭하지 않습니다.

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
│   ├── measure.md
│   ├── templates.md
│   └── ontology-boost.md
└── scripts/
    └── crawl_audit.py
```

- [`SKILL.md`](SKILL.md): 진단 절차, 불변 원칙, 승인 게이트, 보고 형식
- [`references/seo.md`](references/seo.md): 크롤러 노출, 사이트맵, 메타, 구조화 데이터, 응답 위생
- [`references/aeo.md`](references/aeo.md): 질문별 랜딩과 추출되는 문장의 형태
- [`references/geo.md`](references/geo.md): `llms.txt`, AI 크롤러 정책, 1차 소스 되기
- [`references/llmo.md`](references/llmo.md): 엔티티 일관성과 학습 표면 관리
- [`references/neo-naver.md`](references/neo-naver.md): 서치어드바이저, AI 브리핑 인용 요건, 투트랙
- [`references/measure.md`](references/measure.md): 기준선, 재측정 일정, 지표 읽는 법
- [`references/templates.md`](references/templates.md): 진단 리포트, 측정 로그, 인용 프로브 시트,
  `llms.txt`, robots.txt, JSON-LD, 의도 랜딩 골격
- [`agents/visibility-auditor.md`](agents/visibility-auditor.md): 결과만 보고 채점하는
  fresh-eyes 검증 패스
- [`scripts/crawl_audit.py`](scripts/crawl_audit.py): 크롤러의 눈으로 표면을 관측
- [`references/ontology-boost.md`](references/ontology-boost.md): 온톨로지가 있을 때만 여는
  선택 모듈. 질문 목록, 1차 소스 정의, 서비스명 표기, 과거 결정을 회수합니다.

설치 방법은 저장소의 [루트 README](../../README.md)를 참고하세요.
