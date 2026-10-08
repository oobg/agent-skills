# shell/implementation — 정본 CSS·JS를 고칠 때

`assets/`를 수정할 때만 읽는다. 일반 생성은 [contract.md](contract.md)와 레시피로 충분하다. 값을 바꾸면 이 문서의 수치도 함께 고친다.

## 파일과 인라인 순서

| 모드 | 메인 `<style>` 순서 | 스크립트 |
| --- | --- | --- |
| page | tokens.css → `page.css` → (특수 블록 CSS) | `page.js`(표 썸네일, 번호 핀 연동) |
| deck | tokens.css → `page.css` → `deck.css` → `deck-shapes.css`(HTML에 `d0-s-*`가 있을 때만 채움) → `deck-enhance.css` | `deck.js`(한 장 모드, 네비, 키보드, 스와이프, 해시) |

- `scripts/inline_assets.py`가 자리표시자 주석(`/* eli5:page.css */` 등)을 파일 내용으로 바꾼다. 모드에 필요한 자리표시자가 빠지거나 겹치면 멈춘다. 자산 파일을 더하거나 이름을 바꾸면 스크립트의 `MODES`와 세 레시피의 뼈대를 함께 고친다.
- tokens.css는 형제 스킬 day0-design에서 찾는다(탐색 순서는 [day0.md](../day0.md)). 폰트 `@font-face`는 메인 `<style>` 앞 별도 `<style>`이다.
- `examples/preview-compare.html`은 `page.css` 인라인 사본을 담고 있다. CSS를 바꾸면 자리표시자 원본으로 다시 만든다.

## page 레이아웃 수치

| 항목 | 값 |
| --- | --- |
| 축 폭(`--d0-axis`) | 기본·`report` 720px, `narrow` 640px |
| 프레임·넓은 구간 | min(960px, 가용 폭 − 64px). 640px 이하는 좌우 16px 거터 |
| 페이지 패딩 | 위아래 64/96px(640px 이하 48/72px), 좌우 0(컨테이너 폭 = `main` 폭) |
| 섹션 | 위 1px grey-100 구분선(축 폭, 가운데) + 위아래 32px(모바일 24px), 블록 사이 24px |
| 2열 | 축 안 `auto-fit` 열마다 300px 이상, 간격 48px. 넓은 구간 안은 960px 이상에서 12열 6/6 또는 7/5 |
| compact 그림 | 75%(640px 이하는 100%) |
| 사이드 패널 | 대상 열 \| 24px \| 192px. 문턱 = 대상 폭 + 2 × (24 + 192 + 32): 640 → 1136, 720 → 1216, 960 → 1456px. `main`의 이름 붙은 컨테이너 쿼리 `@container d0-page`로 잰다(스크롤바 거터 제외) |

- `report`는 폭이 아니라 결정·보고 표시다. report 선택자에 폭 규칙을 두지 않는다. 표지(머리)도 같은 720px 축이고, `.d0-wide`만 960px로 넓어진 뒤 다음 블록은 다시 720px 축이다. `scripts/check_render.cjs`가 1440px에서 이 회귀를 잰다.
- 사이드 패널은 호스트의 폭·여백을 바꾸지 않고 격자 열만 바꾼다(폭을 바꾸면 화면 ↔ 인쇄 전환 때 옛 값이 남는다). 패널 유무로 축 위치가 바뀌지 않는다.
- `html { scrollbar-gutter: stable }`이라 레이아웃 폭은 뷰포트보다 스크롤바만큼 좁을 수 있다. 측정은 뷰포트 숫자가 아니라 `main`이나 SVG의 실제 박스로 한다.

## page 타이포

| 역할 | 크기 / 굵기 | 640px 이하 |
| --- | --- | --- |
| h1 | 32 / 700 | 26 |
| 히어로 후 값 | 44 / 600(전 값 20 / 600 grey-600) | 36 |
| h2 | 20 / 700 | 18 |
| h3 | 16 / 650 | 16 |
| 본문 | 15 / 400, 설명 문단 행간 1.65 | 15 |
| 보조(섹션 설명) | 14 grey-600 | 14 |
| 캡션 | 13 grey-600 | 13 |
| 라벨·배지 | 12 / 600, 배지 높이 22px(작은 변형 20, 버튼형 32) | 12 |
| editorial 숫자 | 56 / 600 | 40 |

- 숫자는 `tabular-nums`, 한글은 `word-break: keep-all`, 본문은 `text-wrap: pretty`, `balance`는 제목만이다. 12px 글자는 grey-600 이상이다.

## 그림 글자 (page)

렌더 글자 = font-size × (SVG 렌더 폭 ÷ viewBox 폭). 1280px에서 13~20px, 375·320px에서 11px 이상을 목표로 CSS가 좁은 화면에서 글자를 키운다.

| 놓는 곳 | viewBox 폭 | 글자(기본 / 760px 이하 / 560px 이하 / 340px 이하) |
| --- | --- | --- |
| 축 | 560 | 14 / 14 / 20 / 22 |
| `.d0-wide` 바로 안 | 750 | 14 / 18 / 27 / 30 |
| 2열 칸 | 360(넓은 구간 칸 480) | 나란하면 18, 쌓이면 칸이 축(넓은 구간) 폭이라 축 그림과 같은 렌더 크기로 줄인다(값은 page.css) |

- 예: 축 720px → 14 × 720 ÷ 560 = 18px, 390px 화면 → 20 × 358 ÷ 560 = 12.8px.
- 무대(`.d0-fig__stage`) 패딩은 렌더 폭을 줄여 375px에서 글자가 11px 아래로 내려가므로 글자 있는 도식에는 두지 않는다.

## 색과 대비

tokens.css 실제 값으로 계산한 WCAG 2.x 비율(글자 4.5:1, 큰 글자·그래픽 3:1).

| 앞 / 뒤 | 비율 | 판정 |
| --- | --- | --- |
| blue-dark / 흰 · grey-50 · blue-light | 5.50 · 5.18 · 4.94 | 글자 통과 |
| 흰 / blue | 3.99 | 글자 미달, 그래픽만 |
| blue / 흰 · grey-50 · blue-light | 3.99 · 3.75 · 3.58 | 그래픽 통과 |
| grey-700 / blue-light · grey-100 | 6.87 · 6.70 | 글자 통과 |
| grey-600 / grey-50 · blue-light | 4.71 · 4.49 | blue-light 위 글자 미달 → grey-700 |
| grey-500 / 흰 · blue-light | 3.19 · 2.87 | blue-light 위 선 미달 → grey-600 |
| green / 흰 | 3.47 | 그래픽 통과, 글자 미달 |
| red / 흰 | 3.57 | 그래픽 통과, 글자 미달 |
| orange / 흰 | 2.47 | 그래픽 미달 → 옅은 면 + 진한 테두리·라벨 |
| 보조 색 진한 / 흰 · 자기 옅은 면 · blue-light | 5.25~5.42 · 4.61~4.68 · 4.71~4.86 | 글자 통과(값은 `page.css`) |

- 의미색은 글자 색으로 쓰지 않는다. 흰 숫자는 blue-dark 원 위에만 둔다. 표 합계 행은 blue-light 바탕 + 위 2px blue 선 + grey-900 굵은 글자다.
- 비교 표의 없음 표식은 grey-500 점선 원(3.19), 미확정 표식은 orange-bg 면 + grey-700 테두리다. 뜻은 칸의 글자가 전한다.

## deck 수치

| 항목 | 값 |
| --- | --- |
| 한 장 모드 | 16:9, 슬라이드 폭 = min(100vw − 2 × 거터, max((100dvh − 크롬 88px) × 16/9, 730px)). JS가 `data-mode="single"`을 붙일 때만 |
| 좁은 장 | 슬라이드 폭 730px 미만이면 16:9를 풀고 px 글자, 1열 |
| 글자(cqi, 1280 한 장 기준) | 제목 3.6(약 39px), 표지 h1 5.6, 비대칭 제목 3.2, assertion·순수 Impact 6, closing 5, 본문 2(좁은 장 15px), 큰 숫자 10 |
| 그림 글자 | `--sl-font`(기본 17, 가로형·evidence 20, 좁은 장 30, 320px 36). 렌더 = `--sl-font` × SVG 렌더 폭 ÷ viewBox 폭, 1280에서 28px 이하, 좁은 화면 11px 이상 |
| split | 그림 3 : 요점 2 |
| 비대칭 | 제목 열 2 : 그림 열 3, `data-flip`이면 좌우 반전 |
| 진한 면 | 바탕 blue-dark, 제목·강조 #fff(5.50), 보조·선 blue-light(4.94), blue·의미색 칠 금지(blue 1.38). `deck-enhance.css`가 도형 색을 바꾼다 |

- 표지 배치: `side`(기본, 3fr 2fr), `bottom`·`contrast`·`center`는 1열, `map`은 2fr 1fr. report·preview 덱의 side 표지만 5fr 4fr이고, 이 규칙은 `:where()`로 side에만 걸려 다른 표지를 덮지 않는다. 좁은 장의 1열 규칙이 가장 뒤에서 이긴다.
- 덱 SVG 글자의 가운데 정렬은 `text-anchor` 속성이 없는 `text`에만 건다. 속성에 적은 `start`·`end`를 CSS가 덮지 않게 하려는 것이다.
- `deck-shapes.css`는 슬라이드 SVG 도형에 `vector-effect: non-scaling-stroke`를 걸고 번호 글자를 `--sl-font`에 맞춘다.

## deck 동작 (`deck.js`)

- →·Space·PageDown 다음, ←·Shift+Space·PageUp 이전, Home·End 처음·끝, F 전체 화면. 입력 칸 안의 키와 버튼 위 Space는 가로채지 않는다.
- 넘길 때 주소가 `#s-NN`으로 바뀌고(`replaceState`, 실패해도 무시), 해시로 열면 그 장부터 보인다. 터치 스와이프 48px 이상이면 넘긴다.
- 네비의 `data-deck="toc"` 버튼은 목차 장이 있을 때만 둔다(없으면 첫 장으로 간다).
- JS가 실패하면 세로 나열로 남는다. 인쇄는 한 장 = 가로 한 쪽이다.

## 검사 스크립트

`scripts/check_render.cjs`는 기계로 확실히 아는 것만 잰다: 콘솔 오류, 문서 가로 넘침(`scrollWidth` vs `clientWidth`, 1px 허용), SVG 잘림(도형 합집합 vs SVG 박스, 1px 허용), page 그림 글자 크기(경고, SVG 실제 렌더 폭 기준), 내부 식별자 slug, report 회귀, 자리표시자·토큰·외부 요청. slug 목록은 스크립트 맨 위 `SLUGS` 한 곳에 있다. 블록·레시피 이름을 더하면 함께 더한다.
