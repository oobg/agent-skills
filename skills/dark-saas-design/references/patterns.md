# 패턴 레시피

수치는 전부 `tokens.css` 변수로 쓴다. 값이 왜 그 값인지는 `derive.md`에 있고,
여기서는 그 값으로 무엇을 조립하는지만 다룬다.

## 1. 타입 스케일

Pretendard Variable **한 벌**로 전부 처리한다. 굵기는 `font-variation-settings`.

| 역할 | 데스크톱 | ≤767px | wght | line-height | letter-spacing |
| --- | --- | --- | --- | --- | --- |
| 히어로 h1 | 64px | 40px | 700 | 72 / 48px | -0.03em |
| 섹션 h2 | 48px | 32px | 600 | 56 / 40px | -0.03em |
| 블록 h3 | 36px | 28px | 600 | 44 / 36px | -0.02em |
| 카드 제목 h4 | 24px | 24px | 600 | 32px | -0.02em |
| 리드 문장 | 20px | 18px | 450 | 32 / 28px | -0.02em |
| 본문 | 16px | 16px | 450 | 28px | -0.01em |
| 버튼 | 16px | 16px | 450 | 24px | 0 |
| 메타·캡션 | 14px | 14px | 400 | 20px | 0 |
| 스크롤 리빌 | 48px | 32px | 400 | 56 / 40px | -0.03em |

```css
h1 {
  font-family: var(--ds-font);
  font-size: var(--ds-size-display);
  font-weight: 400;                          /* 축을 쓰므로 400 고정 */
  font-variation-settings: "wght" var(--ds-wght-display);
  line-height: var(--ds-lh-display);
  letter-spacing: var(--ds-track-xl);
  color: var(--ds-ink);
}
```

읽는 규칙 셋.

- **행간은 px다.** `1.3em`이 아니라 `72px`. 배수로 주면 크기가 바뀔 때마다
  행간이 8의 배수에서 벗어나 두 컬럼의 줄이 어긋난다.
- **자간은 크기를 따라간다.** 48px 이상은 -0.03em, 20~36px은 -0.02em,
  16px은 -0.01em, 14px 이하와 모든 컨트롤은 0.
- **위계는 크기로만 만들지 않는다.** 리드 문장은 본문보다 4px 크고 굵기는
  같다. 히어로 서브 한 줄을 강조하려면 크기를 올리는 대신 굵기를 600으로 준다.

## 2. 레이아웃 격자

```css
.ds-section {
  padding: var(--ds-section-y) var(--ds-gutter);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ds-block-gap);
}
.ds-container { width: 100%; max-width: var(--ds-container); }
```

- 컨테이너 1200px. 12칼럼 분할이 전부 정수로 떨어진다.
- 세로 리듬 128px (모바일 64), 섹션 안쪽 gap 48px.
- **8pt 사다리 밖 값을 만들지 않는다.** 54px이 필요해 보이면 48이나 64가
  맞는 값이고, 둘 다 틀려 보이면 문제는 간격이 아니라 그 자리에 든 내용의 양이다.

2열은 칼럼 수로 표현한다. 픽셀을 직접 쓰면 컨테이너를 바꾸는 순간 어긋난다.

```css
.ds-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--ds-col-gap); }
.ds-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--ds-col-gap); }
.ds-grid-7-5 { display: grid; grid-template-columns: 7fr 5fr; }
```

**2단을 세로 1단으로 접을 때의 함정.** 가로 2단에서 `flex: 1`을 쓴 컬럼을
`flex-direction: column`으로 바꾸면 주축이 세로가 되어 `flex-basis: 0`이 높이를
먹는다. `height`를 줘도 무시되고 높이가 0이 되어 비주얼이 통째로 사라진다.
접히는 컬럼에는 `flex: none`과 명시 높이를 함께 준다. `grid`로 짜면 이 함정이
아예 없다 — 2열 이상은 grid를 기본으로 쓴다.

```css
@media (max-width: 767px) {
  .card { flex-direction: column; }
  .card > .vis { flex: none; height: 280px; }  /* flex:1 이면 높이 0 */
}
```

## 3. 내비게이션

```css
.ds-nav {
  position: sticky; top: 0; z-index: 20;
  height: var(--ds-nav-h);              /* 64px */
  background: var(--ds-void);           /* 불투명. backdrop-filter 쓰지 않는다 */
  border-bottom: 1px solid var(--ds-line);
}
```

- 링크 16px/450, `--ds-ink-2`. hover에서 `--ds-ink`로. 활성 표시 없음.
- 우측 CTA 2개: 둘 다 고스트(`--ds-chip`), 높이 40, radius 6, 텍스트 14px/450.
  **랜딩 최상단에 채운 버튼을 두지 않는다.** 히어로 안의 CTA와 경쟁한다.
- 내비 항목은 **실제로 그 내용이 있는 곳으로 간다.** `요금`이 CTA 밴드로
  가면 안 된다.

## 4. 버튼

| 종류 | 배경 | 높이 | 텍스트 |
| --- | --- | --- | --- |
| primary | `--ds-accent` | 48 | 16px/450 흰색 + 우측 화살표 |
| ghost | `--ds-chip` | 40 | 14px/450 흰색 |
| inverse | `--ds-void` | 48 | 16px/450 흰색 (포인트 면 위) |

- radius는 전부 `--ds-radius-control`(6px). 알약 없음.
- 안쪽 여백은 8pt 사다리에서 — 높이 48은 `padding: 0 24px`, 높이 40은 `0 16px`.
- hover는 색 전환만. `transition: background var(--ds-dur-state) var(--ds-ease)`.
  이동·확대·그림자 없음.
- 모바일에서 primary는 `width: 100%`.

## 5. 아이브로 칩

섹션 제목 위에 붙는 라벨.

```css
.ds-eyebrow {
  display: inline-flex; align-items: center; height: 32px;
  padding: 0 var(--ds-space-2);
  background: var(--ds-chip);
  border-radius: var(--ds-radius-control);
  font-size: var(--ds-size-meta);
  font-variation-settings: "wght" var(--ds-wght-body);
  letter-spacing: var(--ds-track-s);
  color: var(--ds-ink);
}
```

대문자 변환·자간 확대를 하지 않는다. 한국어 원문 그대로 쓴다. 영문 라벨을
`FEATURES`처럼 늘려 쓰는 순간 이 화면은 다른 계보의 디자인이 된다.

## 6. 스택 카드 (핵심 섹션)

랜딩 본문의 주력. 카드가 스크롤에 따라 쌓인다.

```css
.ds-stack-card {
  position: sticky;
  top: var(--ds-sticky-top);           /* 88px = 내비 64 + 24 */
  display: grid;
  grid-template-columns: 7fr 5fr;      /* 카피 : 비주얼 */
  align-items: center;
  min-height: 440px;
  background: var(--ds-void);          /* 검정 위 검정 */
  border: 1px solid var(--ds-line);    /* 면 분리는 이 1px이 전부 */
  border-radius: var(--ds-radius-card);
  overflow: hidden;
}
.ds-stack-card > .copy {
  display: flex; flex-direction: column; align-items: flex-start;
  gap: var(--ds-space-3);
  padding: var(--ds-space-5);          /* 48 */
}
/* 비주얼 컬럼 — 배경도 패딩도 주지 않는다 */
.ds-stack-card > .vis {
  align-self: stretch;
  background: none;
  padding: 0;
  overflow: clip;
}
.ds-stack-card > .vis > * { width: 100%; height: 100%; object-fit: cover; }
```

**7:5로 나눈다.** 반반으로 나누면 제목이 세 줄로 꺾이고 비주얼은 헐거워진다.
카피가 넓은 쪽이어야 하는 이유는 한글 제목이 라틴보다 같은 글자 수에서 넓기
때문이다.

**비주얼 컬럼에 배경색을 깔지 않는다.** 카드와 다른 색을 주면 카드 한가운데
세로 분할선이 생겨 카드가 두 조각으로 읽힌다. 이게 "싸 보이는" 가장 흔한 원인이다.

**비주얼에 패딩을 주지 않는다.** 여백에 둘러싸인 그림은 액자 속 카탈로그로 보인다.
이미지가 컬럼을 한 픽셀도 남기지 않고 채우되 **밖으로 넘치게 하지는 않는다.**
넘치면 잘림선이 값을 통과한다. §11-1을 본다.

- 카피 컬럼 순서: 아이브로 칩 → h4 또는 h3(2줄) → 본문 2줄. 그 이상 넣지 않는다.
- 제목은 **반드시 두 줄에 맞춘다.** 세 줄로 꺾이면 덩어리가 무너진다.
  줄당 13~14자가 상한이다. 넘으면 카피를 줄이지 레이아웃을 늘리지 않는다.
- 좌우는 카드마다 번갈아도 된다. 다만 한 페이지 안에서 규칙을 지킨다.
- 3~4장까지. 그 이상은 스크롤이 길어져 이탈한다.
- 모바일은 세로 1단, 카피 먼저, 비주얼 아래.

## 7. 아코디언 (FAQ)

```css
.ds-faq { display: grid; grid-template-columns: 4fr 8fr; gap: var(--ds-col-gap); }
.ds-accordion-item {
  border: 1px solid var(--ds-line);
  border-radius: var(--ds-radius-card);
  padding: var(--ds-space-3);
}
```

- 좌측에 제목 + 설명 컬럼(4칼럼), 우측에 아코디언 리스트(8칼럼). 2단 고정.
- 질문에 번호를 붙인다(`1.` `2.`). 24px/600.
- 답변 16px/450 `--ds-ink-2`.
- 토글 아이콘은 `+` / `−` 선 아이콘. 회전 애니메이션 없음.
- 열림 상태는 `data-open`으로 표현한다. 클래스 토글을 쓰지 않는다.

**라이트 변형.** 결정 페이지처럼 라이트 본문에 놓을 때는 색만 바꾸고 치수는
그대로 쓴다. 보더 `--ds-rule`, 아이콘과 답변 `--ds-slate`, 질문은 `--ds-graphite`.

## 8. 로고·출처 스트립

```css
.ds-strip {
  width: 100%;                          /* 컨테이너를 벗어나 풀블리드 */
  background: var(--ds-veil);
  border-block: 1px solid var(--ds-line-soft);
  padding: var(--ds-space-4) 0;
  overflow: hidden;
}
.ds-strip-track { display: flex; gap: var(--ds-space-6); width: max-content; }
.ds-strip-track img { filter: grayscale(1) invert(1); opacity: 0.6; }
```

트랙은 **콘텐츠를 두 벌 복제**해 넣고 `translateX(-50%)`까지 이동시킨 뒤 되감는다.
폭을 픽셀로 박으면 항목이 하나 늘 때마다 이음매가 튄다.

로고 원본 색을 쓰지 않고 흑백 반전으로 통일한다. 색이 살아 있으면 스트립이
아니라 광고판이 된다.

## 9. CTA 배너 + 푸터

```css
.ds-cta {
  display: flex; align-items: center; justify-content: space-between;
  gap: var(--ds-space-4);
  min-height: 160px;
  padding: var(--ds-space-5);
  background: var(--ds-accent);
  border-radius: var(--ds-radius-card);
}
```

- 배너 위 텍스트는 흰색이다. 포인트가 대비 창 안에 있으므로 4.5:1을 넘는다
  (`derive.md` §1). 포인트를 바꿨다면 이 대비부터 다시 잰다.
- 우측에 inverse 버튼 하나. 두 개 두지 않는다 — 결정 직전에 선택지를 늘리면
  결정이 미뤄진다.
- CSS 그라디언트로 배너를 칠하지 않는다. 단색이거나, 글로우 레이어를 얹는다.
- 푸터 컬럼 제목은 16px/600 `--ds-ink-2`. 라틴 전용 서체를 여기에 들이지 않는다.
- 링크 16px/450, 저작권 14px/400 `--ds-ink-3`, 위에 1px `--ds-line` 디바이더.

## 10. 라이트 면 컴포넌트

개요·심층·결정 페이지 본문에서 쓴다. 어느 페이지에 무엇을 얹을지는 `pages.md`가
정한다. 여기는 개별 블록의 규격만 둔다.

### 10-1. 스테이트먼트 밴드

히어로 바로 아래에서 다크에서 라이트로 넘어가는 이음매 역할을 한다.

```css
.ds-band {
  background: var(--ds-paper-3);
  padding: var(--ds-section-y) var(--ds-gutter);
  text-align: center;
}
.ds-band p {
  font-size: var(--ds-size-h3);
  font-weight: 400;
  font-variation-settings: "wght" var(--ds-wght-heading);
  line-height: var(--ds-lh-h3);
  letter-spacing: var(--ds-track-l);
  color: var(--ds-graphite);
}
```

두 줄 고정. 제품이 무엇인지 한 문장, 그래서 무엇이 되는지 한 문장.
한 페이지에 **하나만** 쓴다. 두 개 이상이면 밴드가 구획이 아니라 벽지가 된다.

### 10-2. 기능 그룹

라이트 본문의 주력. 동사 헤딩 하나에 항목 1~3개를 매단다.

```css
.ds-group { padding: var(--ds-section-y) var(--ds-gutter) 0; } /* 아래 0 — 그룹끼리 붙인다 */
.ds-group > h2 {
  font-size: var(--ds-size-h3);
  font-variation-settings: "wght" var(--ds-wght-heading);
  line-height: var(--ds-lh-h3);
  letter-spacing: var(--ds-track-l);
  color: var(--ds-graphite);
}
.ds-group-items { display: grid; grid-template-columns: 1fr 1fr; gap: var(--ds-col-gap); }
```

- 헤딩은 **동사 종결**로 쓴다. `연결합니다` `정리합니다` `분석합니다`
  `확인합니다` `받아봅니다`. 명사 라벨(`주요 기능`)을 쓰지 않는다 — 명사는
  기능 목록이 되고 동사는 사용자가 하는 일이 된다.
- 헤딩 왼쪽에 포인트 점 하나를 붙인다. 8px 사각, `--ds-accent-ink`, radius 2.
- 항목 수는 유동이다. 1개면 한 칸만 채우고 나머지는 비워 둔다. 억지로 2의
  배수를 맞추려고 내용을 만들지 않는다.
- 그룹은 페이지당 2~3개. 그룹 사이는 1px `--ds-rule` 디바이더.

### 10-3. 기능 항목

```css
.ds-item .shot {                              /* 스크린샷 패널 */
  aspect-ratio: 4 / 3;
  background: var(--ds-paper-2);
  border: 1px solid var(--ds-rule);
  border-radius: var(--ds-radius-panel);
  overflow: hidden;
}
.ds-item h3 {
  margin-top: var(--ds-space-3);
  font-size: var(--ds-size-h4);
  font-variation-settings: "wght" var(--ds-wght-heading);
  line-height: var(--ds-lh-h4);
  letter-spacing: var(--ds-track-l);
  color: var(--ds-graphite);
}
.ds-item p {
  margin-top: var(--ds-space-1);
  font-size: var(--ds-size-body);
  line-height: var(--ds-lh-body);
  color: var(--ds-slate);
}
```

패널 높이를 픽셀로 박지 않고 `aspect-ratio`로 잡는다. 컬럼이 좁아져도 비율이
유지되어 넘침이 구조적으로 생기지 않는다. 설명은 두 줄 — 첫 줄은 무엇을 하는지,
둘째 줄은 그래서 무엇이 없어지는지.

### 10-4. 요금 카드 (3-up)

```css
.ds-plan {
  display: flex; flex-direction: column; gap: var(--ds-space-3);
  padding: var(--ds-space-5) var(--ds-space-4);
  background: none;
  border: 1px solid var(--ds-rule);
  border-radius: var(--ds-radius-card);
}
```

순서: 제품명(24/600) → 한 줄 설명(16) → 1px 디바이더 → 가격(36/600) + 단위 →
기능 리스트. 리스트 불릿은 점이 아니라 **작은 화살표**를 쓴다. 점은 나열이고
화살표는 방향이다.

카드에 배경색을 깔지 않는다. 흰 바탕 위 1px 선만으로 세운다. 추천 요금제만
보더를 `--ds-accent-ink`로 바꾼다 — 배경을 칠하거나 크기를 키우지 않는다.

### 10-5. 후기 카드 (3-up × n)

```css
.ds-quote {
  background: var(--ds-paper-2);
  border-radius: var(--ds-radius-card);
  padding: var(--ds-space-4);
}
```

인용문 먼저, 로고와 이름·직함은 카드 바닥에 붙인다. 얼굴 사진을 쓰지 않는다.
행 수는 유동. 넘치면 `더 보기`로 접는다.

### 10-6. 다크 반전 섹션

라이트 본문 한가운데에서 한 번만 검정으로 뒤집는다. 보안·근거처럼 "무게를
줘야 하는" 내용에만 쓴다.

```css
.ds-invert { background: var(--ds-void); padding: var(--ds-section-y) var(--ds-gutter); }
.ds-invert .card {
  background: none;
  border: 1px solid var(--ds-line);
  border-radius: var(--ds-radius-panel);
  padding: var(--ds-space-3);
}
```

### 10-7. 틴트 밴드

전환을 유도하는 자리에만 쓰는 옅은 포인트 면.

```css
.ds-tint {
  background: var(--ds-tint);
  padding: var(--ds-section-y) var(--ds-gutter);
  text-align: center;
}
```

가운데 정렬, 제목 한 줄 + 설명 한 줄 + 버튼 하나. 그 이상 넣지 않는다.
버튼은 primary 하나다.

### 10-8. 짧은 히어로

색인 페이지는 히어로에 목업도 글로우도 두지 않는다. 제목과 한 줄 설명만.

```css
.ds-hero[data-variant="short"] {
  background: var(--ds-void); color: var(--ds-ink);
  padding: calc(var(--ds-section-y) / 2) var(--ds-gutter);
}
.ds-hero[data-variant="short"] .inner {
  max-width: var(--ds-container); margin: 0 auto;
  display: flex; flex-direction: column; gap: var(--ds-space-3);
}
```

h1은 다른 페이지와 같은 64px/700을 쓴다. 색인이라고 제목을 줄이지 않는다.

### 10-9. 목록 행

**카드를 쓰지 않는다.** 행과 1px 디바이더로만 나눈다. 카드로 만들면 항목마다
박스가 생겨 목록이 무거워지고, 개수가 늘수록 더 나빠진다.

```css
.ds-list a {
  display: flex; flex-direction: column; gap: var(--ds-space-1);
  padding-bottom: var(--ds-space-3);
  margin-bottom: var(--ds-space-3);
  border-bottom: 1px solid var(--ds-rule);
}
.ds-list h3 {
  font-size: var(--ds-size-h4);
  font-variation-settings: "wght" var(--ds-wght-heading);
  line-height: var(--ds-lh-h4);
  letter-spacing: var(--ds-track-l);
  color: var(--ds-graphite);
}
.ds-list p { font-size: var(--ds-size-body); line-height: var(--ds-lh-body); color: var(--ds-slate); }
.ds-list .meta {
  display: flex; gap: var(--ds-space-2);
  font-size: var(--ds-size-meta); line-height: var(--ds-lh-meta);
  letter-spacing: var(--ds-track-s); color: var(--ds-slate-2);
}
```

- 행 순서: 제목 → 요약 1~2줄 → 메타(출처, 날짜). 썸네일을 넣지 않는다.
- 요약은 굵기 450. 제목 600과 대비를 만든다.
- 페이지네이션 없이 전부 나열한다. 12~15개까지는 그대로 읽힌다.

## 11. 비주얼 에셋

카드 오른쪽과 기능 항목 안에 무엇을 넣느냐가 완성도를 가른다. 토큰과 격자를 다
맞춰도 여기가 비면 화면이 싸 보인다.

**가장 빠른 정답은 미리 렌더링한 에셋이다.** 실제 제품을 캡처해 프레임까지
포함한 PNG나 루프 mp4로 굽는다. 기기 베젤, 헤더, 잘린 구도가 전부 이미지 안에
있으면 DOM은 그걸 담기만 하면 된다. 아래는 CSS로 목업을 그려야 할 때의 규칙이다.

### 11-1. 잘라내지 않는다

CSS로 목업을 그릴 때 넘치게 두면 잘림선이 값과 컨트롤을 통과한다. 실제로 그렇게
만들었더니 `−31.5%`, `연결됨` 다섯 개, 비교군 칩 세 개가 반쯤 잘려 나갔다.
"뭔가 투박하다"는 인상은 대부분 여기서 나온다.

| | 규칙 |
| --- | --- |
| 가로 | **절대 자르지 않는다.** 모든 값이 컨테이너 안에 들어온다 |
| 세로 | 자르지 않는다. 내용을 컨테이너에 맞춘다 |
| "더 있다" 신호 | 잘림이 아니라 `+ 전체보기` 행으로 만든다 |

### 11-2. 액자를 만들지 않는다

회색 프레임 안에 흰 카드를 띄우지 않는다. **프레임이 곧 패널이다.** 안쪽에
여백을 주면 "스크린샷을 붙여 넣은 상자"로 보인다.

```css
.ds-item .shot {                    /* 프레임 = 패널 */
  position: relative; aspect-ratio: 4 / 3;
  background: var(--ds-paper);
  border: 1px solid var(--ds-rule);
  border-radius: var(--ds-radius-panel);
  overflow: hidden;
}
.ds-item .app {                     /* 내용이 프레임을 꽉 채운다 */
  position: absolute; inset: 0;
  padding: var(--ds-space-3); border-radius: 0;
  display: flex; flex-direction: column;
}
```

### 11-3. 바닥은 액션 행으로 채운다

내용이 프레임보다 짧으면 아래가 비어 허전하다. 실제 제품 화면이 쓰는
`+ 전체보기` 행을 바닥에 붙인다. 공간도 채우고 실제 제품처럼 보인다.

```css
.app-more {
  margin-top: auto;                 /* 바닥에 붙인다 */
  padding-top: var(--ds-space-2);
  border-top: 1px solid var(--ds-rule);
  text-align: center; font-size: 12px;
  font-variation-settings: "wght" var(--ds-wght-heading);
  color: var(--ds-app-text-muted);
}
```

### 11-4. 치수를 컨테이너에 묶는다

패널 폭이 줄어도 비율이 유지되게 하려면 목업 안쪽 치수를 `em`으로 쓰고 기준
글자 크기를 컨테이너 폭에 묶는다(`cqw`). 그러면 넘침이 구조적으로 생기지 않는다.

```css
.ds-item .shot { container-type: inline-size; }
.ds-item .app { font-size: clamp(9px, 2.4cqw, 14px); }
.ds-item .app .row { padding: 0.6em 0.8em; border-bottom: 0.07em solid var(--ds-rule); }
```

**스케일되지 않는 1px 보더가 섞이면 좁은 폭에서 예산이 깨진다.** 목업 안쪽
보더도 `em`으로 쓴다.

`height`와 `aspect-ratio`를 한 요소에 함께 걸지 않는다. 폭이 비율로 역산되어
그리드 트랙을 무시하고, 트랙보다 넓은 요소가 문서 가로 넘침을 만든다.

### 11-5. 좁아지면 행을 줄인다

폭이 아니라 **행 수**를 줄인다.

```css
@media (max-width: 1023px) { .app .rows .row:nth-child(n+5) { display: none } }
@media (max-width: 767px) {
  .app .rows .row:nth-child(n+4) { display: none }
  .app .chips { display: none }      /* 컨트롤 행은 통째로 뺀다 */
}
```

컨트롤 행(칩, 탭)은 **반쯤 잘리느니 통째로 감춘다.** 반쯤 보이는 컨트롤이
가장 나빠 보인다.

### 11-6. 여러 페이지를 한 파일로 합칠 때

CSS를 라우트별로 스코프해 합치면 셀렉터 충돌은 막을 수 있지만, 합치는 과정
자체가 새 결함을 만든다. 실제로 두 번 겪었다.

**중괄호 균형을 먼저 검사한다.** CSS를 줄 단위로 잘라 붙이면 여러 줄 규칙이
쪼개져 중괄호가 깨진다. 그러면 그 뒤 규칙이 통째로 하나의 선언 블록으로 삼켜져
사라진다. 한 라우트의 스타일이 전부 증발했는데 콘솔에는 아무 오류도 안 뜬다.

```js
// 합치기 전 각 조각을 검사한다. 규칙은 줄이 아니라 중괄호 단위로 자른다.
if ((css.match(/{/g) || []).length !== (css.match(/}/g) || []).length)
  throw new Error("중괄호 불균형 — 뒤쪽 규칙이 삼켜진다");
```

**정의하지 않은 변수를 검사한다.** `var(--ds-lh-h3)`을 쓰는데 토큰 블록에 그
줄을 빠뜨리면 행간이 브라우저 기본값으로 풀린다. 값이 아니라 이름 하나가 빠져서
타이포 리듬이 통째로 무너지는데, 화면만 봐서는 원인을 못 찾는다.

**라우트마다 스타일이 실제로 먹었는지 확인한다.** 그림자와 넘침만 세면 스타일이
아예 안 붙은 라우트도 전부 0으로 나와 통과한다. 라우트별로 기준값을 직접 대조한다.

| 검사 | 통과 기준 |
| --- | --- |
| 중괄호 | 조각마다 열림 = 닫힘 |
| 미정의 `--ds-*` | 0개 |
| h1 폰트 크기 | 라우트마다 64px |
| h1 폰트 패밀리 | `Pretendard Variable` |
| 컨테이너 폭 | 1200px |

**직접 진입으로 검증한다.** 내비 클릭만 눌러 보면 초기 로드 경로를 놓친다.
`#/price` 같은 해시를 주소창에 직접 넣어 새로고침한 상태로 확인한다.

### 11-7. 검수 방법

눈으로는 놓친다. 실제 글자 상자와 잘라내는 조상을 비교해 기계로 잡는다.

```js
for (const el of document.querySelectorAll(".app")) {
  if (el.scrollHeight > el.clientHeight)
    console.warn("넘침", el, el.scrollHeight - el.clientHeight);
}
```

`scrollHeight > clientHeight`인 패널이 하나라도 있으면 통과가 아니다.
1440, 1280, 1024, 860, 768, 390 여섯 폭에서 전부 0이어야 한다.

### 11-8. 목록을 도식으로 바꿀지는 내용이 정한다

취향이 아니다. **시스템 사이의 관계를 말하는 자리는 도식, 제품 화면을 말하는
자리는 화면으로 둔다.**

- 같은 정보를 목록으로 적으면 무엇이 있는지는 남지만 어디로 모이는지는 안 보인다.
  데이터 소스 다섯 개를 상태 배지가 붙은 목록에서 하나의 기반으로 잇는 연결
  도식으로 바꾸면 같은 정보에서 관계가 드러난다.
- 두 축으로 갈리는 분류는 목록보다 매트릭스가 낫다. 우선순위 목록은 순위만
  남기지만 두 축을 놓으면 왜 그렇게 갈렸는지가 함께 읽힌다.
- 여러 도구가 따로 논다는 것을 보여주는 도식은 아이콘과 라벨만으로는 인식이
  생기지 않는다. 창 크롬(점과 라벨, 우측 문서명)이 붙은 미니 UI로 그려야 읽는
  사람이 자기 회사에서 쓰는 화면을 알아본다.
- 미니 창 도식은 창 하나가 약 265px 아래로 줄면 안쪽 글자가 11px 밑으로 내려가
  읽히지 않는다. 다섯 개를 넣으려면 6칼럼짜리 자리가 아니라 **12칼럼 풀폭
  블록**이 필요하다.

### 11-9. 에셋을 만들 때

- 실제 데이터를 넣는다. `999,999,999,999`처럼 자리를 채운 더미는 티가 난다.
- 기기 프레임(폰 베젤, 브라우저 크롬)으로 감싸면 평면 스크린샷보다 깊이가 산다.
- 목업 안 글자는 11px 아래로 내리지 않는다.
- 요소 수 하한: 헤더 한 줄 + 주요 수치 + 보조 문장 + 데이터 영역 + 액션 행.

## 12. 제품 UI (라이트 앱)

마케팅 화면과 계보는 같고 면만 뒤집는다. 공유하는 것은 포인트 hue와 격자다.

- 배경 `--ds-app-bg`, 사이드바·표 헤더 `--ds-app-surface`.
- 숫자가 주인공이다. 금액은 36~48px 굵게, 통화·단위는 같은 줄에 작게.
- 변화량은 **문장으로** 쓴다: `지난달보다 1,920,893,058원 (212.8%) 증가했어요`.
  증가 `--ds-app-up`, 감소·초과 `--ds-app-down`, 차트 라인 `--ds-app-line`.
  **색만으로 방향을 말하지 않는다.** 부호나 화살표를 함께 둔다.
- 강조 카드만 포인트 보더로 띄운다. 나머지는 1px `--ds-rule`.
- 버튼은 검정 채움 + 흰 글씨. 라이트 면에서도 포인트는 아낀다.
- radius는 마케팅과 동일(카드 12, 패널 8, 컨트롤 6).
- 컴포넌트를 쓰라는 규칙이 면 계조를 지우지 않게 한다. 표준 컴포넌트로
  치환하면 소비처가 갖고 있던 "이 자리는 한 단 낮은 면"이라는 정보가 함께
  사라진다. 치환 뒤에는 면 종류 수와 `background` 선언 수를 세어 확인한다.
