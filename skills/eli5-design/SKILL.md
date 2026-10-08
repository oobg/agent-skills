---
name: eli5-design
description: "아무것도 모르는 사람도 그림으로 구조를 먼저 이해하고 짧은 글로 이유와 맥락까지 이해하는 HTML 설명 문서를 Day0 시각 언어로 만든다. 그림과 글이 같은 말을 반복하지 않게 하고, 비교는 같은 틀로 그리며 없음·미확정을 그림 안에 밝히고, 라벨 아래 설명은 3문장 이내(그림만으로 충분하면 생략)로 쓰고, 용어는 그림 속 사물 비유로 먼저 보여 준다. 설명 page, 결정·보고 page, 발표 deck 세 레시피 중 하나로 만들고 마지막에 실제 렌더를 보고 다시 편집한다. 토큰은 형제 스킬 day0-design의 tokens.css 전체를 인라인하며, day0-design이 로컬에 없으면 공개 저장소 원본을 읽는다. '/eli5-design', '쉽게 설명하는 시안', '설명 페이지', '설명서 페이지', 'eli5 디자인', '그림으로 쉽게 보여줘', '쉽게 보는 발표 슬라이드' 요청에 사용한다. 설명 페이지가 아닌 Day0 제품 화면은 day0-design, 문구만이면 ux-writing으로 넘긴다. 설명 목적이 없는 일반 화면·랜딩 디자인에는 사용하지 않는다."
---

# ELI5 Design

처음 보는 사람이 **그림으로 구조를 먼저 잡고, 짧은 글로 이유와 맥락까지 이해하는 HTML 문서**를 Day0 시각 언어로 만든다. 기본은 한 장짜리 page, 발표용은 한 장씩 넘기는 deck이다.

> Explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words.

"few words"는 글을 적게 쓰라는 뜻이 아니라 같은 말을 그림과 글로 두 번 하지 말라는 뜻이다.

## 규칙 다섯

1. 그림·표·글은 서로 다른 정보를 맡는다. 이미 보여 준 내용을 반복하지 않고, 추가 정보가 없으면 제거한다.
2. 비교는 같은 시각 문법으로 그리고 실제 차이만 바꾼다. 역할이 모호한 요소와 없음·미확정은 그림 안에서 직접 밝힌다.
3. 주어진 사실을 바꾸거나 없는 사실·수치를 만들지 않는다.
4. 라벨 아래 설명은 최대 3문장이다. 그림만으로 충분하면 쓰지 않는다.
5. 내부 식별자와 제작·판정 과정을 화면에 드러내지 않고, 완성 후 실제 렌더를 보며 다시 편집한다.

세부는 [references/core.md](references/core.md)에 있다.

## 항상 읽는 것 (4개)

1. 이 파일
2. [references/core.md](references/core.md)
3. 레시피 하나(아래 표에서 고른다)
4. [references/final-review.md](references/final-review.md) — 완성 직후

| 요청 | 레시피 |
| --- | --- |
| 구조·흐름·결과물·사용법·일정·용어를 혼자 읽고 이해시킨다(신호가 없으면 이것) | [recipes/explainer-page.md](references/recipes/explainer-page.md) |
| 결정을 받거나 상태·결과·사건을 보고한다(결정 문서, 상태 보고, 장애 회고, 출시 보고, 적용 전 제안) | [recipes/decision-report.md](references/recipes/decision-report.md) |
| 발표·화면 공유·슬라이드·장표·덱 | [recipes/deck.md](references/recipes/deck.md) |

레시피는 한 작업에 하나만 연다. 결정을 발표로 받으면 deck이다.

## 고른 뒤에만 읽는 것

후보를 견주는 동안에는 레시피의 표만 본다. 표현·기능을 실제로 고른 뒤 그 상세 문서 하나를 연다. "혹시 필요할지 몰라" 미리 읽지 않고, 문서 안 링크를 따라 연달아 열지 않는다.

| 고른 것 | 읽을 것 |
| --- | --- |
| SVG 도식을 그린다 | [diagrams/index.md](references/diagrams/index.md) → 그중 하나: [flow](references/diagrams/flow.md) · [comparison](references/diagrams/comparison.md) · [annotation](references/diagrams/annotation.md) |
| 점·산점·스트립 그래프 | [charts-points.md](references/charts-points.md) |
| 목업·체크리스트·명령·타임라인 같은 특수 블록 | 레시피 표가 가리킨 `references/blocks/` 파일 하나 |
| 배치(넓은 구간·2열·사이드 노트·인쇄)를 더 알아야 한다 | [shell/contract.md](references/shell/contract.md) |
| 정본 CSS·JS를 고친다 | [shell/implementation.md](references/shell/implementation.md) |
| 렌더할 수 없는 환경이다 | [render-unavailable.md](references/render-unavailable.md) |
| 게시를 요청받았거나 호스트가 게시를 기본으로 요구한다 | [publishing.md](references/publishing.md) |
| 인라인 스크립트가 토큰을 못 찾는다 | [day0.md](references/day0.md) |
| 시각 톤 예시가 꼭 필요하다 | `references/examples/preview-compare.html` |

`assets/`의 CSS·JS는 읽지 않고 스크립트로 인라인한다. 고칠 때만 읽는다.

## 작업 순서

1. **독자와 질문.** 독자가 다 읽고 할 수 있어야 할 것 한 줄과 질문 목록을 적는다. 답할 수 없는 질문은 사용자에게 확인한다.
2. **레시피.** 위 표에서 하나를 고르고 연다.
3. **그림 고르기.** 질문마다 레시피 표에서 그림을 고르고, 고른 것의 상세 문서만 연다.
4. **작성.** 레시피의 뼈대에 마크업을 쓴다. 레시피의 부품과 도식 CSS는 `assets/page.css`에 있어 붙이지 않는다. `references/blocks/`의 특수 블록만 그 파일의 CSS를 메인 `<style>` 끝에 붙인다.
5. **인라인.** `python3 scripts/inline_assets.py page|deck out.html`이 토큰과 정본 CSS·JS를 자리표시자에 채운다(`--tokens`로 경로를 줄 수 있다). 토큰을 찾지 못하면 멈추고 알린다.
6. **최종 검토.** [final-review.md](references/final-review.md)대로 렌더를 보고 네 질문에 답하며, `node scripts/check_render.cjs out.html`로 기계 검사를 돌린다. 고친 뒤 다시 본다.
7. **폰트와 넘기기.** `scripts/subset_font.py`로 폰트 서브셋을 인라인하고 HTML 파일을 남긴다. 게시는 publishing 조건을 따른다.

## 도구

| 스크립트 | 하는 일 |
| --- | --- |
| `scripts/inline_assets.py` | `page`·`deck` 모드로 tokens.css와 `assets/` CSS·JS를 자리표시자에 채운다. 표준 라이브러리만 쓴다 |
| `scripts/check_render.cjs` | playwright-core로 1440·390px 렌더를 열어 콘솔 오류·가로 넘침·SVG 잘림·내부 식별자·report 표지 회귀를 검사한다 |
| `scripts/subset_font.py` | 페이지 글자만 담은 Pretendard 서브셋 `@font-face`를 인라인한다(fontTools 필요) |
