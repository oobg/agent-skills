# shell — 페이지 골격

모든 페이지는 이 골격에서 시작한다. 고른 블록의 마크업은 `<main class="d0-page">` 안에,
CSS는 `<style>` 끝에, JS는 `</body>` 앞 `<script>` 하나에 붙인다.

## 해부 구조

- doctype → `lang="ko"` → meta viewport → Pretendard Variable 웹폰트(외부 리소스는 이것 하나).
- `<style>`: tokens.css 전체 인라인 → `color-scheme: light` → 기본 리셋 → `body` 배경 → 컨테이너 → 타이포 → 공용 pill → 포커스 → 모션 축소.
- 컨테이너는 day0 폭 규칙을 따른다: 기본 wide `1200px`, `data-width="narrow"`면 `640px`.
- 패딩은 데스크톱 `28px 32px`, 640px 이하에서 좌우 16px 거터.

## 언제 쓰나 / 변형

- 항상 쓴다. 읽기 위주의 짧은 페이지(faq, guide)는 `data-width="narrow"`를 고려한다.
- `.d0-pill`은 배지·태그·탭 전용 공용 조각이다. 톤은 `data-tone="blue|green|red|orange"`. 배지는 늘 글자를 함께 써서 색만으로 상태를 말하지 않는다.
- 포커스 링은 `--d0-blue-dark` 2px 실선이다(배경 대비 3:1 이상). `.d0-sr-only`는 표 caption처럼 화면에 안 보여도 되는 이름에 쓴다.

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
  <!-- header → section … 순서로 블록 마크업을 붙인다 -->
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
.d0-page { max-width: 1200px; margin: 0 auto; padding: 28px 32px 64px; }
.d0-page[data-width="narrow"] { max-width: 640px; }
.d0-page > * + * { margin-top: 40px; }
h1, h2, h3 {
  margin: 0;
  line-height: var(--d0-leading-title);
  letter-spacing: var(--d0-tracking-title);
  text-wrap: balance;
}
p { margin: 0; text-wrap: pretty; }
ul, ol, dl, dd { margin: 0; padding: 0; list-style: none; }
svg { display: block; max-width: 100%; height: auto; }
button { font: inherit; color: inherit; letter-spacing: inherit; cursor: pointer; }
.d0-pill {
  display: inline-flex; align-items: center;
  padding: 4px 10px; border-radius: 999px;
  background: var(--d0-grey-100); color: var(--d0-grey-700);
  font-size: var(--d0-meta); font-weight: 600; line-height: 1.4;
}
.d0-pill[data-tone="blue"] { background: var(--d0-blue-light); color: var(--d0-blue-dark); }
/* 시맨틱 전경색은 글자 대비 4.5:1 미달이라 글자는 grey-800, 색은 점으로만 */
.d0-pill[data-tone="green"] { background: var(--d0-green-bg); color: var(--d0-grey-800); }
.d0-pill[data-tone="red"] { background: var(--d0-red-bg); color: var(--d0-grey-800); }
.d0-pill[data-tone="orange"] { background: var(--d0-orange-bg); color: var(--d0-grey-800); }
.d0-pill[data-tone]:not([data-tone="blue"])::before {
  content: ""; width: 6px; height: 6px; margin-right: 6px; border-radius: 999px;
}
.d0-pill[data-tone="green"]::before { background: var(--d0-green); }
.d0-pill[data-tone="red"]::before { background: var(--d0-red); }
.d0-pill[data-tone="orange"]::before { background: var(--d0-orange); }
.d0-sr-only {
  position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
:focus-visible { outline: 2px solid var(--d0-blue-dark); outline-offset: 2px; }
@media (max-width: 640px) {
  .d0-page { padding: 20px 16px 48px; }
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
