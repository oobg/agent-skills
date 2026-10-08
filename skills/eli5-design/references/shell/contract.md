# shell/contract — 골격과 배치 계약

page 골격이 무엇을 보장하고 생성자가 무엇을 고르는지 적는다. 폭·간격·글자 크기·문턱 같은 구현 수치는 `assets/page.css`(page)와 `assets/deck*.css`(deck) 한 곳이 갖는다. 이 문서에는 언제 무엇을 쓰는지만 있다. CSS를 고칠 때는 [implementation.md](implementation.md)를 연다.

## CSS가 보장하는 것

- **가운데 읽기 축.** 머리와 섹션의 직계 자식(글·그림·표·지표·2열)은 화면 가운데 놓인 같은 폭의 축을 쓰고, 왼쪽 끝과 오른쪽 끝이 각각 하나다. 블록마다 폭 상한이나 들여쓰기를 따로 두지 않는다.
- **글 폭.** 문단·설명은 부모 폭을 그대로 쓴다. `p`·`dd`에 `max-width`를 걸지 않는다. 줄을 더 짧게 읽혀야 하면 문서 전체에 `data-width="narrow"`를 단다.
- **섹션 리듬.** 섹션은 축을 따라 위아래로 쌓이고 사이에 가는 구분선 하나가 생긴다. 섹션에 카드 상자를 두르지 않는다.
- **그림 폭.** 도식은 놓인 자리 폭을 채운다. 좁은 화면에서는 SVG 글자가 커져 읽힌다(viewBox 폭 규칙은 [diagrams/index.md](../diagrams/index.md)).
- **라이트 온리.** `color-scheme: light`와 `body` 배경이 들어 있어 다크 호스트에서도 깨지지 않는다.
- **블록 CSS.** 머리·요약 행·히어로·라벨 설명·주장과 근거·지표 목록·가로 막대 목록·몫 막대·타일·비교 표·마무리·요청 상자·지표 카드·옵션 나란히·단계 열·도식 클래스·번호 핀·번호 주석이 모두 들어 있다. 결과물에 따로 붙이지 않는다. `references/blocks/`의 특수 블록(목업, 체크리스트, 코드, 탭 미리보기, 타임라인, 행 목록, 썸네일 카드, 질문-답, 접기 목록, 전과 후, 확인 지점, 흐름 줄)은 그 파일의 CSS를 메인 `<style>` 끝에 붙인다.

## 생성자가 고르는 것

| 고를 것 | 쓰는 것 | 언제 |
| --- | --- | --- |
| 문서 폭 | `main.d0-page`(기본), `data-width="narrow"` | 읽고 따라 하는 글이 주인공이면 narrow. 한 문서에 섞지 않는다 |
| 결정·보고 표시 | `data-width="report"` | 결정·보고 문서임을 표시한다. 폭은 기본과 같다 |
| 넓은 구간 | `.d0-wide` | 기본 축에서 필수 정보가 넘치거나 라벨이 부딪히는 넓은 표·5칸 이상 가로 띠·화면 A/B 실제 크기 비교만. 같은 중심선에서 양쪽으로 넓어지고 다음 블록은 축으로 돌아온다 |
| 표 가로 스크롤 | `div.d0-scroll > table`(`style="--min-w: 640px"`처럼 읽히는 최소 폭) | 좁은 화면에서도 열 비교가 핵심인 표. 표 글자를 줄여 맞추지 않는다 |
| 3선택지 표 | `table.d0-table[data-stack]` + 칸마다 `data-label` | 선택지 3개까지. 좁은 화면에서 기준 아래 선택지 칸이 나란히 놓여 가로 스크롤 없이 다 보인다 |
| 좁은 화면 그림 | `figure.d0-fig > svg[data-view="wide"]` + `svg[data-view="narrow"]` | 다시 배치할 수 있는 그림. 좁은 화면에서 세로형만 보인다 |
| 그림 안 가로 스크롤 | `div.d0-fig__scroll[style="--min-w: 560px"] > svg` | 좌표·관계를 지켜야 해 다시 배치할 수 없는 넓은 그림 |
| 2열 | `div.d0-cols` | 동시 비교(전 \| 후, A \| B), 대등한 두 덩어리(완료 \| 남은 것)만. "그림 \| 설명 문단"은 2열이 아니다. 좁으면 저절로 쌓인다 |
| 넓은 2열 | `div.d0-wide > div.d0-cols`(그림/목록이면 `data-split="7-5"`) | 화면 둘을 실제 크기로 견줄 때, 그림과 번호 목록이 함께 본문일 때 |
| 작게 | `figure.d0-fig[data-fit="compact"]` | 축 폭에서 너무 커 보이는 단순 도식 |
| 외곽선 틀 끄기 | `figure.d0-fig[data-frame="none"]` | SVG만 든 그림(compact 제외)은 기본으로 외곽선 카드에 담긴다. 그림 안에 이미 바깥 틀을 그렸을 때만 끈다 |
| 그림 곁 노트·범례 | `div.d0-margined > figure + aside.d0-margin`, 핀 범례, 주석 목록 | 넓은 화면에서는 대상 오른쪽 바깥, 좁은 화면과 인쇄에서는 대상 아래에 놓인다. 본문 위치는 바뀌지 않는다 |
| 접기 | `details.d0-more > summary` | 흐름을 끊는 세부. 섹션의 핵심 답·결정은 접지 않는다 |
| 기억할 한 줄 | `aside.d0-keep > span.d0-keep__label + p` | 페이지 끝에 기억할 사실 한 문장(선택). 행동 요청은 closing |
| 장면 음량 | 섹션 `data-emphasis="quiet"` | 참고·부록처럼 뒤로 물러날 섹션 |
| 문장 줄 나눔 | `span.d0-sentence` | 역할이 다른 문장을 줄마다 |
| 배지 | `span.d0-pill[data-tone="blue|green|orange|red"]` | 상태를 글자로 말할 때. 카드·행마다 하나 |

## 마크업 계약

- 루트는 `main.d0-page` 하나, 그 안에 `header.d0-header` 하나와 `section.d0-section[aria-labelledby]` 여럿이다. 섹션 머리는 `header.d0-section-head > h2`다.
- 그림은 `figure.d0-fig`, 표는 `table` + `caption` + `th scope`, 수치는 `data value`, 날짜·기간은 `time datetime`이다.
- 인터랙션은 실제 `button`·`input`·`details`와 짧은 바닐라 JS로 짓는다. 상태는 `data-*` 속성(`data-on`, `data-selected`, `data-active-pin`)으로 나타낸다.
- 색·radius·모션은 `var(--d0-*)` 토큰만 쓴다. 토큰에 없는 이름을 만들지 않는다(흰 표면 `#fff`만 예외).
- 한 artifact 안에서 여러 페이지를 iframe으로 보여 주면 `src`로 같은 artifact를 부르지 않고 `srcdoc` + `sandbox="allow-scripts"`를 쓴다(자세한 내용은 [publishing.md](../publishing.md)).

## 인쇄

- page는 `.d0-scroll` 표와 그림 스크롤이 인쇄 영역 안으로 접히고, 표 머리 행이 쪽마다 되풀이되며, 노트·범례는 대상 아래로 간다.
- deck은 한 장이 가로 한 쪽이 되고 네비가 숨는다.
- 인쇄 규칙도 정본 CSS 안에 있다. 결과물에 따로 붙이지 않는다.

## 모션

- 콘텐츠를 숨겼다 보여 주는 모션(등장, 선 그리기, 장 전환 페이드)은 쓰지 않는다. 처음부터 최종 상태로 보이고, deck 장 전환은 즉시 바뀐다.
- 움직임은 사용자 조작에 대한 짧은 강조(hover·focus, 버튼 상태)에만 쓰고, `prefers-reduced-motion`이면 그마저 끈다.
