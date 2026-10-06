# shell — 페이지 골격

모든 페이지는 이 골격에서 시작한다. 고른 블록의 마크업은 `<main class="d0-page">` 안에,
CSS는 `<style>` 끝에, JS는 `</body>` 앞 `<script>` 하나에 붙인다.

## 해부 구조

- doctype → `lang="ko"` → meta viewport → Pretendard Variable 웹폰트(외부 리소스는 이것 하나).
- `<style>`: tokens.css 전체 인라인 → `color-scheme: light` → 기본 리셋 → `body` 배경 → 컨테이너 → 타이포 스케일 → 섹션 → 공용 배지 → 포커스 → 모션 축소.
- 컨테이너는 day0 폭 규칙을 따른다: 기본 wide `1200px`, `data-width="narrow"`면 `640px`.
- 여백은 넉넉하게: 페이지 패딩 데스크톱 `48px 32px 88px`, 640px 이하 `40px 16px 72px`(좌우 16px 거터).
- 섹션 = 위쪽 1px 구분선 + 세로 패딩 36px, 섹션 안 그룹 간격 24px. 섹션 사이에 카드 상자를 두르지 않는다.
- 섹션 안 행은 위로 붙는다(`align-content: start`). 섹션이 늘어나도 그룹 사이가 벌어지지 않는다.

## 나란히 두 섹션 (`.d0-split`)

짧은 섹션 둘(숫자 카드 + 도식, 그림 + 목록)을 한 줄에 놓을 때 쓴다. `<div class="d0-split">` 안에 `section.d0-section` 두 개.

- 960px 이상에서 2열, 그 아래는 1열. 열 사이 48px.
- `align-items: start`라 짧은 섹션은 제 높이만 차지한다. 옆 섹션 높이에 맞춰 늘어나 아래가 비지 않는다.
- 각 섹션은 자기 `border-top`을 그대로 둔다. 데스크톱에서는 구분선이 열 사이에서 끊겨 보이는데, 의도한 모양이다.
- 세 개 이상 나란히 두지 않는다.
- **높이 기준(정본).** 데스크톱에서 한쪽 섹션 높이가 다른 쪽의 1.5배를 넘으면 나란히 두지 않고 위아래로 쌓는다.
  작은 차(예: 수십 px)는 허용하고, 짧은 쪽 아래에 큰 빈 공간이 생기면 금지다. 균형을 맞추려고 내용을 다른 섹션으로 옮기지 않는다.

## 타이포 스케일

| 역할 | 크기 / 굵기 | 색 |
| --- | --- | --- |
| h1 (페이지 제목) | 26px / 700, display 자간·행간 | grey-900 |
| h2 (섹션 제목) | 18px / 700, title 자간 | grey-900 |
| h3 (그림·열 제목) | 16px / 650 | grey-900 |
| 리드·섹션 설명 | 15px / 400 | grey-600 |
| 본문 | 15px / 400 | grey-900 |
| 주석·보조(그림 옆) | 13–14px / 400~500 | grey-600 |
| 단계 라벨 | 12px / 600 | blue-dark |
| 배지 | 12px / 600, 높이 22px | 아래 배지 표 |

- 글자 최소 크기는 12px(배지·단계 라벨)이고 문장은 13px 이상이다.
- 13px 회색 문장을 페이지의 주 콘텐츠로 쓰지 않는다. 주 콘텐츠는 그림과 15px 이상의 제목·숫자다.

## 배지 (`.d0-pill`)

배지는 상태·분류를 글자로 말하고, 색은 배경과 점으로 거든다. 시맨틱 전경색(`--d0-green`·`--d0-red`·`--d0-orange`)은
글자 대비 4.5:1에 못 미쳐 글자에 쓰지 않는다. 아래 대비는 tokens.css 실제 값으로 계산한 WCAG 2.x 비율이다.

| 톤 | 글자 / 배경 | 글자 대비 | 점 / 배경 |
| --- | --- | --- | --- |
| 기본(회색) | grey-700 / grey-100 | 6.70 | 없음 |
| `blue` | blue-dark / blue-light | 4.94 | 없음(글자 자체가 블루) |
| `green` | grey-900 / green-bg | 15.12 | green / green-bg 3.17 |
| `red` | grey-900 / red-bg | 14.91 | red / red-bg 3.21 |
| `orange` | grey-900 / orange-bg | 15.42 | orange / orange-bg 2.30 (보조 표식) |

점은 글자 배지를 거드는 보조 표식이라 `aria-hidden`이다. 상태 뜻은 글자가 전한다(1.4.11 대상 아님). orange 점은
3:1에 못 미치므로 orange 톤만으로 무언가를 구분하게 만들지 않는다.

**높이 고정.** 배지는 grid·flex 행 안에서 늘어나지 않는다. `height` 고정 + `flex: none` + `align-self: flex-start`
+ `justify-self: start`. 작은 변형(`data-size="sm"`)은 20px. 버튼·탭으로 쓰는 pill은 포인터 대상 24px 하한 때문에
높이 32px이다(`button.d0-pill`, `a.d0-pill`, `[role="tab"].d0-pill`).

## 개행

- 리드·설명 문단은 부모 폭을 그대로 쓴다. `p`에 컨테이너보다 좁은 `max-width`를 걸지 않는다.
- 문장 단위 개행(선택): 리드·설명이 2문장 이상이고 데스크톱 폭에서 2줄을 넘기거나 문장마다 역할이 다르면
  문장마다 `<span class="d0-sentence">`로 감싼다(`display: block`). `<br>`을 늘어놓지 않는다.

## 스니펫

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>주문 내보내기 한눈에 보기</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
/* (아래 css 블록 + 고른 블록 css) */
</style>
</head>
<body>
<main class="d0-page">
  <!-- header → section(2~4개, 기본 3~4개) 순서로 블록 마크업을 붙인다 -->
  <section class="d0-section" aria-labelledby="sec-a">
    <h2 id="sec-a">파일은 이렇게 생겼어요</h2>
    <!-- 그림 하나 + 짧은 주석 -->
  </section>
  <div class="d0-split">
    <section class="d0-section" aria-labelledby="sec-b"><h2 id="sec-b">얼마나 빨라지나</h2><!-- 숫자 카드 --></section>
    <section class="d0-section" aria-labelledby="sec-c"><h2 id="sec-c">어디가 다시 도나</h2><!-- 도식 --></section>
  </div>
</main>
<script>
/* 인터랙션 블록의 JS만 여기 붙인다 */
</script>
</body>
</html>
```

```css
/* ../day0-design/references/tokens.css 파일 전체를 수정 없이 여기(<style> 맨 앞)에 붙인다.
   day0-design 위치는 SKILL.md의 탐색 순서를 따른다. 토큰을 외부 <link>로 걸지 않는다. */
:root { color-scheme: light; }
*, *::before, *::after { box-sizing: border-box; }
body {
  margin: 0;
  background: #fff;
  color: var(--d0-grey-900);
  font-family: var(--d0-font);
  font-size: 15px;
  line-height: var(--d0-leading-body);
  letter-spacing: var(--d0-tracking-body);
  word-break: keep-all;
  overflow-wrap: break-word;
}
.d0-page { max-width: 1200px; margin: 0 auto; padding: 48px 32px 88px; }
.d0-page[data-width="narrow"] { max-width: 640px; }
h1, h2, h3 {
  margin: 0;
  line-height: var(--d0-leading-title);
  letter-spacing: var(--d0-tracking-title);
  text-wrap: balance;
}
h1 { font-size: 26px; font-weight: 700; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
h2 { font-size: 18px; font-weight: 700; }
h3 { font-size: 16px; font-weight: 650; }
p { margin: 0; text-wrap: pretty; }
ul, ol, dl, dd, figure { margin: 0; padding: 0; list-style: none; }
svg { display: block; max-width: 100%; height: auto; }
button { font: inherit; color: inherit; letter-spacing: inherit; cursor: pointer; }
.d0-sentence { display: block; }
.d0-section { display: grid; gap: 24px; align-content: start; padding-block: 36px; border-top: 1px solid var(--d0-grey-200); }
.d0-split { display: grid; gap: 0 48px; }
.d0-split > * { min-width: 0; }
@media (min-width: 960px) {
  .d0-split { grid-template-columns: 1fr 1fr; align-items: start; }
}
.d0-section > p { color: var(--d0-grey-600); }
.d0-note { color: var(--d0-grey-600); font-size: var(--d0-text-compact); }

.d0-pill {
  display: inline-flex; align-items: center; gap: 6px;
  flex: none; align-self: flex-start; justify-self: start;
  height: 22px; padding: 0 9px; border: 0; border-radius: 999px;
  background: var(--d0-grey-100); color: var(--d0-grey-700);
  font-size: var(--d0-meta); font-weight: 600; line-height: 1; white-space: nowrap;
}
.d0-pill[data-size="sm"] { height: 20px; padding: 0 8px; }
button.d0-pill, a.d0-pill, .d0-pill[role="tab"] { height: 32px; padding: 0 14px; font-size: var(--d0-text-compact); }
.d0-pill[data-tone="blue"] { background: var(--d0-blue-light); color: var(--d0-blue-dark); }
.d0-pill[data-tone="green"] { background: var(--d0-green-bg); color: var(--d0-grey-900); }
.d0-pill[data-tone="red"] { background: var(--d0-red-bg); color: var(--d0-grey-900); }
.d0-pill[data-tone="orange"] { background: var(--d0-orange-bg); color: var(--d0-grey-900); }
.d0-pill[data-tone="green"]::before,
.d0-pill[data-tone="red"]::before,
.d0-pill[data-tone="orange"]::before { content: ""; flex: none; width: 8px; height: 8px; border-radius: 999px; }
.d0-pill[data-tone="green"]::before { background: var(--d0-green); }
.d0-pill[data-tone="red"]::before { background: var(--d0-red); }
.d0-pill[data-tone="orange"]::before { background: var(--d0-orange); }

.d0-sr-only {
  position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
:focus-visible { outline: 2px solid var(--d0-blue-dark); outline-offset: 2px; }
@media (max-width: 640px) {
  .d0-page { padding: 40px 16px 72px; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## 금지

- 다크 팔레트·`prefers-color-scheme: dark` 분기 추가, `body` 배경 생략.
- `p`나 리드에 컨테이너보다 좁은 `max-width`·`width`·`ch`. 좁혀야 하면 `data-width="narrow"`.
- Pretendard 외 외부 폰트·CSS·JS 링크, `outline: none` 단독 사용.
- 글자에 `--d0-blue`·`--d0-grey-500` 이하·시맨틱 전경색 사용(흰 배경 대비 4.5:1 미달). 글자는 `--d0-blue-dark`, `--d0-grey-600` 이상.
- tokens.css에 없는 `--d0-*` 변수 만들기(표면 `#fff`만 예외). 반투명 막은 `color-mix(in srgb, var(--d0-grey-900) 32%, transparent)`.
- 배지 높이를 행 높이에 맡기기(늘어난 배지), 섹션마다 카드 상자.
- `.d0-split`에 섹션 3개 이상, `align-items: stretch`로 짧은 섹션을 옆 섹션 높이까지 늘리기.
