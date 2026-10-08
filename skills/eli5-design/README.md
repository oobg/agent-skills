# ELI5 Design

처음 보는 사람도 그림으로 구조를 먼저 이해하고, 짧은 글로 이유와 맥락까지 이해하는 HTML 문서를
Day0 시각 언어로 만드는 에이전트 스킬입니다. 기능 소개, 절차 설명, 결정 문서, 상태 보고, 장애 회고처럼
누군가에게 무언가를 쉽게 보여 줘야 하는 문서에 씁니다. 기본은 혼자 읽는 한 장짜리 페이지이고,
발표나 화면 공유용으로 한 장씩 넘기는 덱으로도 만듭니다.

## 사용 조건

- 구조, 흐름, 결과물의 모양, 사용법을 처음 보는 사람에게 설명할 때
- 선택지를 견주어 결정을 받거나, 상태·결과·사건을 보고할 때
- 위 내용을 발표나 화면 공유로 한 장씩 넘기며 보여 줄 때
- `/eli5-design`으로 명시 호출할 때

설명 문서가 아닌 Day0 제품 화면은 `day0-design`, 문구만 다듬는 작업은 `ux-writing`을 사용합니다.
설명 목적이 없는 일반 화면과 랜딩 디자인에는 쓰지 않습니다.

## 핵심 동작

### 규칙은 다섯 개입니다

1. 그림·표·글은 서로 다른 정보를 맡습니다. 이미 보여 준 내용을 카드·캡션·요약으로 반복하지 않습니다.
2. 비교는 같은 틀로 그리고 실제 차이만 바꿉니다. 역할이 모호한 요소와 없음·미확정은 그림 안에 직접 적습니다.
3. 주어진 사실을 바꾸거나 없는 사실·수치를 만들지 않습니다.
4. 라벨 아래 설명은 최대 3문장이고, 그림만으로 충분하면 쓰지 않습니다.
5. 내부 식별자와 제작 과정을 화면에 드러내지 않고, 완성 후 실제 렌더를 보며 다시 편집합니다.

"큰 그림과 적은 글"을 글을 적게 쓰라는 뜻이 아니라 같은 말을 그림과 글로 두 번 하지 말라는 뜻으로 읽습니다.
무엇을 얼마나 보여 줄지는 문서의 목적과 독자 질문이 정하고, 스킬은 섹션 수·숫자 반복 횟수·장 구성을 정해 두지 않습니다.

### 레시피 하나를 고릅니다

| 레시피 | 쓰는 때 |
| --- | --- |
| 설명 page | 구조·흐름·결과물·사용법·일정·용어를 혼자 읽고 이해시킬 때(기본) |
| 결정·보고 page | 결정을 받거나 상태·결과·사건을 보고할 때. 제목과 첫 화면에 결론과 그 결론을 가르는 값을 둡니다 |
| deck | 발표·화면 공유. 사용자가 정한 장 수를 따르고, 장마다 주장 하나와 그 근거 하나를 둡니다. 목차·영향 요약·되짚기 장은 요청이 있을 때만 만듭니다 |

### 필요한 문서만 읽습니다

일반 작업은 라우터(`SKILL.md`), 규칙(`core.md`), 레시피 하나, 최종 검토(`final-review.md`) 네 파일만 읽습니다.
도식·점 그래프·특수 블록·배치 세부는 실제로 고른 뒤에만 해당 문서 하나를 엽니다.
폭·간격·글자 크기 같은 구현 수치는 정본 CSS 한 곳이 갖고, 블록 CSS도 모두 정본 CSS에 들어 있어 결과물에 따로 붙이지 않습니다.

### 마지막에 렌더를 보고 고칩니다

완성한 결과를 넓은 화면과 좁은 화면에서 렌더하고 네 질문으로 다시 편집합니다.

1. 그림·표만 훑어도 각 섹션이나 장의 핵심이 보이는가
2. 글·카드·캡션이 그림에서 이미 보인 내용을 다시 말하지 않는가
3. 겹치거나 잘리거나 넘친 곳이 없고, 그림 속 역할·대상이 원문의 실제 이름으로 식별되는가
4. 주장·결정의 근거(값·상태·없음)가 화면에 보이고, 제목이 그 근거보다 강하게 말하지 않는가

콘솔 오류, 가로 넘침, SVG 잘림, 내부 식별자 노출, report 표지 회귀처럼 기계가 확실히 아는 것은 검사 스크립트가 잽니다.
렌더할 수 없는 환경에서는 검토를 통과한 것으로 기록하지 않고 안전 모드로 만들며, 자동으로 게시하지 않습니다.

## 도구와 요구 사항

- 형제 스킬 `day0-design`의 `references/tokens.css`가 필요합니다. 로컬에 없으면 공개 저장소 원본을 읽고, 찾지 못하면 멈춥니다.
- `scripts/inline_assets.py`는 Python 표준 라이브러리만 씁니다.
- `scripts/check_render.cjs`는 Node.js와 `playwright-core`(Chromium 포함)가 필요합니다. 경로는 `--playwright` 인자나 `ELI5_PLAYWRIGHT` 환경 변수로 줄 수 있습니다.
- `scripts/subset_font.py`는 `fonttools`와 `brotli`가 필요합니다. 없으면 폰트 링크 하나를 남기고 알립니다.

## 파일 구성

| 경로 | 설명 |
| --- | --- |
| `SKILL.md` | 라우터: 규칙 다섯, 항상 읽는 네 파일, 레시피 고르기, 고른 뒤에만 읽는 문서, 작업 순서, 도구 |
| `references/core.md` | 다섯 규칙의 세부, 말투와 직역투 점검, 보이는 모양의 기본 |
| `references/recipes/explainer-page.md` | 설명 page: 질문 → 그림 고르기 표, page 뼈대, 자주 쓰는 부품과 비교 표 마크업 |
| `references/recipes/decision-report.md` | 결정·보고 page: 결론을 앞에 두는 첫 화면, 문서 종류별 출발점, 근거를 놓는 법, 비교의 모양, 뼈대 |
| `references/recipes/deck.md` | deck: 장 수와 장 구성, 장 종류, 차트 글자와 모양, 덱 뼈대 |
| `references/final-review.md` | 최종 렌더 검토 네 질문, 렌더하는 법, 기계 검사 기준, 넘기기 |
| `references/diagrams/index.md` | SVG 도식 공통 규칙과 도형 클래스, 상세 파일 고르기 |
| `references/diagrams/flow.md` | 갈래가 있는 흐름 정본 예시(역할 이름, 비율, 건너뜀, 되돌림·종료, 좁은 화면), 연결 그래프, 단계, 주고받기, 진행선, 모으기 |
| `references/diagrams/comparison.md` | 같은 틀 비교와 없음 자리, 전/후·선택지 막대, 비율 막대, 숫자 하나 크게 |
| `references/diagrams/annotation.md` | 화면 골격, 표 썸네일, 번호 핀, 번호 주석, 파일 트리, 그림 곁 노트 |
| `references/charts-points.md` | 점 그래프: 주장에 맞는 형태, 작은 집단, 겹침과 결정적 배치, 계산값·축·이름표 |
| `references/shell/contract.md` | 골격이 보장하는 것과 생성자가 고르는 것(폭, 넓은 구간, 2열, 노트, 접기), 마크업 계약, 인쇄, 움직임 범위 |
| `references/shell/implementation.md` | 정본 CSS·JS를 고칠 때의 수치: 인라인 순서, page 레이아웃·타이포·그림 글자, 대비표, deck 수치와 동작, 검사 스크립트 |
| `references/render-unavailable.md` | 렌더할 수 없을 때의 기록 방식과 안전 모드 |
| `references/publishing.md` | 단일 파일·폰트·여러 페이지 artifact, 게시 조건과 민감도, 같은 링크 갱신 |
| `references/day0.md` | `day0-design` 탐색 순서와 토큰 인라인 |
| `references/blocks/` | 특수 블록. 고른 블록 하나만 엽니다: `mockup-frame.md`(목업·기기 프레임·화면 캡처), `checklist.md`(체크리스트), `code-block.md`(코드), `tab-preview.md`(탭 미리보기), `timeline.md`(타임라인), `diff-rows.md`(행 목록), `thumb-cards.md`(썸네일 카드), `faq.md`(질문-답), `accordion.md`(접기 목록), `before-after.md`(전과 후), `checkpoint.md`(확인 지점), `flow-line.md`(흐름 줄), `side-by-side.md`(옵션 나란히), `kpi-cards.md`(지표 카드), `step-columns.md`(단계 열), `callout.md`(요청 상자) |
| `references/examples/preview-compare.html` | 합성 데이터로 만든 완성 예시(현행 정본 CSS로 인라인) |
| `assets/page.css` | 정본 CSS: 골격·읽기 축·2열·노트, 타이포, 섹션, 배지, 공용 블록(머리·히어로·설명·근거·가로 막대 목록·몫 막대·비교 표와 좁은 화면 3선택지 배치·마무리 등), 좁은 화면 그림 전환, 그림 외곽선 틀, 도식 클래스, 번호 핀·주석, 인쇄 |
| `assets/page.js` | 표 썸네일 생성, 번호 핀 연동 |
| `assets/deck.css`, `assets/deck-shapes.css`, `assets/deck-enhance.css` | 덱 CSS: 16:9 한 장, 장 종류, 표지 배치, 덱 차트, 진한 면, 좁은 화면, 인쇄 |
| `assets/deck.js` | 한 장 모드, 네비, 키보드·스와이프, 해시와 쪽수 |
| `scripts/inline_assets.py` | 자리표시자를 tokens.css와 `assets/` 내용으로 채웁니다(`page`·`deck` 모드) |
| `scripts/check_render.cjs` | 1440·390px 렌더 기계 검사 |
| `scripts/subset_font.py` | 페이지 글자만 담은 Pretendard 서브셋 `@font-face`를 인라인합니다 |

설치와 검증 방법은 저장소의 [루트 README](../../README.md)에서 확인할 수 있습니다.
