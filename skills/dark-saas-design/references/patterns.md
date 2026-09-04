# 패턴 레시피

수치는 전부 `tokens.css` 변수로 쓴다. 아래 표의 px는 실측 원본 값이다.

## 1. 타입 스케일

Pretendard Variable **한 벌**로 전부 처리한다. 굵기는 `font-variation-settings`.

| 역할 | 데스크톱 | ≤809px | wght | line-height | letter-spacing |
| --- | --- | --- | --- | --- | --- |
| 히어로 h1 | 60px | 44px | 750 | 1.3em | -0.02em |
| FAQ 대제목 h2 | 48px | 34px | 400 | 1.2em | -0.02em |
| 섹션 제목 h3 | 42px | 28px | 600 | **1.0em** / 모바일 1.4em | -0.02em |
| 카드·아코디언 제목 | 24px | 24px | 500 | 1.4em | 0 |
| 본문 | 16px | 16px | 500 | 1.7em | -0.02em |
| 히어로 서브 | 16px | 16px | **700** | 1.7em | -0.01em |
| 버튼 | 18px | 18px | 500 | 1.2em | -0.02em |
| 내비·소형 버튼 | 14~16px | 14~16px | 500~600 | 1.2em | 0 |
| 법적 고지 | 15px | 15px | 400 | 1.6em | 0 |
| 스크롤 리빌 | 48px | 34px | 400 | 1.21em | -0.04em |
| 라틴 라벨(푸터 h5) | 20px | 20px | Poppins 500 | 1.4em | -0.04em |

```css
h1 {
  font-family: var(--ds-font);
  font-size: 60px;
  font-weight: 400;                          /* 축을 쓰므로 400 고정 */
  font-variation-settings: "wght" var(--ds-wght-display);
  line-height: var(--ds-leading-display);
  letter-spacing: var(--ds-tracking);
  color: var(--ds-text);
}
```

읽는 규칙 두 가지.

- **데스크톱 섹션 제목은 행간 1.0em.** 두 줄 제목이 한 덩어리로 붙어 보이는 게
  이 디자인의 얼굴이다. 모바일에서만 1.4em으로 푼다.
- **히어로 서브는 본문보다 굵다(700).** 크기는 그대로 16px. 크기 대신 굵기로
  위계를 만든다.

## 2. 레이아웃 격자

```css
.ds-section {
  padding: var(--ds-section-y) var(--ds-gutter);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ds-section-gap);
}
.ds-container { width: 100%; max-width: var(--ds-container); }
```

- 컨테이너 1224px 고정. 세로 리듬 120px, 모바일 60px.
- 섹션 안쪽 gap은 64px 하나로 통일. 카드 내부 좌우 컬럼만 54px.
- 실측 gap 값: 6·8·10·12·14·16·18·20·24·32·40·48·54·56·62·64·80·88.
  새 값을 만들지 말고 이 중에서 고른다.

**2단을 세로 1단으로 접을 때의 함정.** 가로 2단에서 `flex: 1`을 쓴 컬럼을
`flex-direction: column`으로 바꾸면 주축이 세로가 되어 `flex-basis: 0`이 높이를
먹는다. `height`를 줘도 무시되고 높이가 0이 되어 비주얼이 통째로 사라진다.
접히는 컬럼에는 `flex: none`과 명시 높이를 함께 준다.

```css
@media (max-width: 809px) {
  .card { flex-direction: column; }
  .card > .vis { flex: none; height: 300px; }  /* flex:1 이면 높이 0 */
}
```

## 3. 내비게이션

```css
.ds-nav {
  position: sticky; top: 0; z-index: 10;
  height: var(--ds-nav-h);           /* 72px */
  padding: 16px 0;
  background: rgba(0, 0, 0, 0.85);   /* backdrop-filter 쓰지 않는다 */
}
```

- 링크 16px/500, `--ds-text-2`. 활성 표시 없음.
- 우측 CTA 2개: 둘 다 고스트(`--ds-chip`), 152×40, radius 8, padding 10px 20px,
  텍스트 14px/600. **랜딩 최상단에 채운 버튼을 두지 않는다.**

## 4. 버튼

| 종류 | 배경 | 크기 | 텍스트 |
| --- | --- | --- | --- |
| primary | `--ds-accent` | h48, padding `14px 22px 14px 28px`, gap 8 | 18px/500 흰색 + 우측 화살표 |
| ghost | `--ds-chip` | h40, padding `10px 20px` | 14px/600 흰색 |
| inverse | `#000` | h48, padding `14px 22px` | 18px/500 흰색 (보라 배너 위) |

- radius는 전부 8px. 알약(`border-radius: 999px`) 없음.
- hover는 색 전환만. `transition: color .4s var(--ds-ease)` — 이동·확대 없음.
- 모바일에서 primary는 `width: 100%`.

## 5. 아이브로 칩

섹션 제목 위에 붙는 라벨.

```css
.ds-eyebrow {
  background: var(--ds-chip);
  border-radius: var(--ds-radius-control);
  padding: 10px 20px;
  font-size: 18px;
  font-variation-settings: "wght" 500;
  color: var(--ds-text);
}
```

대문자 변환·자간 확대를 하지 않는다. 한국어 그대로 쓴다.

## 6. 스택 카드 (핵심 섹션)

랜딩 본문의 주력. 카드가 스크롤에 따라 쌓인다.

```css
.ds-feature-card {
  position: sticky;
  top: var(--ds-sticky-top);        /* 40px */
  height: 468px;
  background: var(--ds-bg);          /* 검정 위 검정 */
  border: 1px solid var(--ds-border);/* 면 분리는 이 1px이 전부 */
  border-radius: var(--ds-radius-card);
  display: flex;
  align-items: center;
  overflow: hidden;
}
/* 카피 컬럼 — 넓은 쪽 */
.ds-feature-card > .copy {
  width: 704px;
  padding: 64px 60px 64px 48px;
  display: flex; flex-direction: column; align-items: flex-start;
  gap: 48px;                         /* 칩과 제목, 제목과 본문 사이 */
}
/* 비주얼 컬럼 — 좁은 쪽. 배경도 패딩도 주지 않는다 */
.ds-feature-card > .vis {
  width: 520px; height: 100%;
  background: none;                  /* 카드와 같은 검정을 그대로 */
  padding: 0;
  overflow: clip;
}
.ds-feature-card > .vis > * { width: 100%; height: 100%; object-fit: cover; }
```

실측 비율은 **카피 704 : 비주얼 520**(58:42)이다. 반반으로 나누면 제목이 세 줄로
꺾이고 비주얼은 헐거워진다.

**비주얼 컬럼에 배경색을 깔지 않는다.** 카드와 다른 색을 주면 카드 한가운데
세로 분할선이 생겨 카드가 두 조각으로 읽힌다. 이게 "싸 보이는" 가장 흔한 원인이다.

**비주얼에 패딩을 주지 않는다.** 여백에 둘러싸인 그림은 액자 속 카탈로그로 보인다.
원본은 520×468 이미지가 컬럼을 한 픽셀도 남기지 않고 채운다. 다만 **컬럼 밖으로
넘치게 하지는 않는다.** 넘치면 잘림선이 값을 통과한다. §11-1을 본다.

- 카피 컬럼 순서: 아이브로 칩 → h3(2줄) → 본문 2줄. 그 이상 넣지 않는다.
- h3는 **반드시 두 줄에 맞춘다.** 세 줄로 꺾이면 행간 1.0em이 뭉쳐 읽힌다.
  줄당 13~14자가 상한이다. 넘으면 카피를 줄이지 레이아웃을 늘리지 않는다.
- 좌우는 카드마다 번갈아도 된다. 다만 한 페이지 안에서 규칙을 지킨다.
- 모바일은 세로 1단, 카피 먼저, 비주얼 아래.

## 7. 아코디언 (FAQ)

```css
.ds-accordion-item {
  width: 704px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-accordion); /* 12px, 카드보다 2px 큼 */
  padding: 24px;
  gap: 10px;
}
```

- 좌측에 제목 + 설명 컬럼(438px), 우측에 아코디언 리스트. 2단 고정.
- 질문에 번호를 붙인다(`1.` `2.`). 24px/500.
- 답변 16px/500 `--ds-text-3`.
- 토글 아이콘은 `+` / `−` 선 아이콘. 회전 애니메이션 없음.

**라이트 변형.** 가격 페이지처럼 라이트 본문에 놓을 때는 색만 바꾸고 치수는 그대로
쓴다. 보더 `--ds-light-hairline`, 아이콘과 답변 `--ds-light-muted`, 질문은 기본 검정.
좌측 제목 컬럼(438px)과 우측 리스트 2단 구조도 다크와 같다.

## 8. 로고 스트립

```css
.ds-logo-strip {
  width: 100%;                       /* 컨테이너를 벗어나 풀블리드 */
  background: var(--ds-surface-veil); /* #ffffff0d */
  border: 1px solid var(--ds-border-soft);
  padding: 40px 0;
  overflow: hidden;
}
.ds-logo-track { width: 2560px; border-radius: var(--ds-radius-marquee); }
.ds-logo-track img { filter: grayscale(1) invert(1); opacity: 0.6; }
```

두 줄을 반대 방향으로 흘린다. 로고 원본 색을 쓰지 않고 흑백 반전으로 통일한다.

## 9. CTA 배너 + 푸터

- 배너: 1224×168, radius 10, 보라 그라디언트 **이미지**(CSS 그라디언트 아님),
  우측에 검정 inverse 버튼 하나.
- 푸터 컬럼 제목은 Poppins 20px/500 `--ds-text-2` — 여기만 라틴 폰트를 쓴다.
- 링크 16px/500, 저작권 15px/400 `--ds-text-5`, 위에 1px 디바이더.

## 10. 라이트 면 컴포넌트

제품 소개와 가격 페이지 본문에서 쓴다. 어느 페이지에 무엇을 얹을지는
`pages.md`가 정한다. 여기는 개별 블록의 규격만 둔다.

### 10-1. 스테이트먼트 밴드

히어로 바로 아래에서 다크에서 라이트로 넘어가는 이음매 역할을 한다.

```css
.ds-band {
  background: var(--ds-light-band);        /* #f5f5f5 */
  padding: var(--ds-section-y) var(--ds-gutter);
  text-align: center;
}
.ds-band p {
  font-size: 36px; font-weight: 400;
  font-variation-settings: "wght" 700;
  line-height: 1.5;                         /* 54px */
  letter-spacing: var(--ds-tracking);
  color: var(--ds-light-text);
}
```

두 줄 고정. 제품이 무엇인지 한 문장, 그래서 무엇이 되는지 한 문장.
한 페이지에 **하나만** 쓴다. 두 개 이상이면 밴드가 구획이 아니라 벽지가 된다.

### 10-2. 기능 그룹

라이트 본문의 주력. 동사 헤딩 하나에 항목 1~3개를 매단다.

```css
.ds-group { padding: var(--ds-section-y) var(--ds-gutter) 0; }  /* 아래 0 — 그룹끼리 붙인다 */
.ds-group > h2 {
  font-size: 36px; font-weight: 400;
  font-variation-settings: "wght" 700;
  line-height: 1.5; letter-spacing: var(--ds-tracking);
  color: var(--ds-light-text);
}
.ds-group-items {
  display: grid; grid-template-columns: repeat(2, 582px);
  gap: var(--ds-col-gap);                   /* 60px */
}
```

- 헤딩은 **동사 종결**로 쓴다. `연결합니다` `정리합니다` `분석합니다`
  `확인합니다` `받아봅니다`. 명사 라벨(`주요 기능`)을 쓰지 않는다.
- 헤딩 오른쪽에 보라 점 하나를 붙인다. 6px 원, `--ds-accent`.
- 항목 수는 유동이다. 1개면 한 칸만 채우고 나머지는 비워 둔다. 억지로
  2의 배수를 맞추려고 내용을 만들지 않는다.
- 그룹은 페이지당 2~3개. 그룹 사이는 1px `--ds-light-border` 디바이더.

### 10-3. 기능 항목

```css
.ds-item { width: 582px; }
.ds-item .shot {                            /* 스크린샷 패널 */
  height: 505px;
  background: var(--ds-light-panel);        /* #f7f7f7 */
  border: 1px solid var(--ds-light-border); /* #e8e8e8 */
  border-radius: var(--ds-radius-shot);     /* 5px — 여기만 예외 */
  overflow: hidden;
}
.ds-item h3 {
  margin-top: 24px;
  font-size: 30px; font-weight: 400;
  font-variation-settings: "wght" 600;
  line-height: 1.4; letter-spacing: var(--ds-tracking);
}
.ds-item p { margin-top: 8px; font-size: 16px; color: #666; line-height: 1.7; }
```

스크린샷은 패널 안에서 **위와 옆이 잘리도록** 크게 넣는다. §11과 같은 원리다.
설명은 두 줄. 첫 줄은 무엇을 하는지, 둘째 줄은 그래서 무엇이 없어지는지.

### 10-4. 요금제 카드 (3-up)

```css
.ds-plan {
  width: 392px; min-height: 550px;
  border: 1px solid var(--ds-light-hairline); /* 실측 0.7px */
  border-radius: var(--ds-radius-control);    /* 8px */
  padding: 50px 32px;
  background: none;
}
```

순서: 제품명(36/700) → 한 줄 설명(16) → 1px 디바이더 → 가격(30/600) + 단위 →
기능 리스트. 리스트 불릿은 점이 아니라 **작은 화살표**를 쓴다.
카드에 배경색을 깔지 않는다. 흰 바탕 위 1px 선만으로 세운다.

### 10-5. 후기 카드 (3-up × n)

```css
.ds-quote {
  width: 392px;
  background: var(--ds-light-panel);
  border-radius: var(--ds-radius-card);   /* 10px */
  padding: 30px;
}
```

인용문 먼저, 로고와 이름·직함은 카드 바닥에 붙인다. 얼굴 사진을 쓰지 않는다.
행 수는 유동. 넘치면 `더 보기`로 접는다.

### 10-6. 다크 반전 섹션

라이트 본문 한가운데에서 한 번만 검정으로 뒤집는다. 보안·신뢰처럼
"무게를 줘야 하는" 내용에만 쓴다.

```css
.ds-invert { background: var(--ds-bg); padding: var(--ds-section-y) var(--ds-gutter); }
.ds-invert .card {
  background: rgba(0, 0, 0, 0.12);
  border: 1px solid var(--ds-border-hair);   /* #ffffff1f */
  border-radius: var(--ds-radius-control);
  padding: 24px;
}
```

### 10-7. 틴트 밴드

전환을 유도하는 자리에만 쓰는 연보라 면.

```css
.ds-tint { background: var(--ds-light-tint); padding: var(--ds-section-y) var(--ds-gutter);
  text-align: center; }
```

가운데 정렬, 제목 한 줄 + 설명 한 줄 + 버튼 하나. 그 이상 넣지 않는다.

### 10-8. 짧은 히어로

목록형 페이지(뉴스룸, 자료실)는 히어로에 목업도 글로우도 두지 않는다.
제목과 한 줄 설명만으로 **359px**에서 끝낸다.

```css
.ds-hero[data-variant="short"]{
  background: var(--ds-bg); color: var(--ds-text);
  padding: var(--ds-section-y) var(--ds-gutter);   /* 120px 30px */
  height: auto;
}
.ds-hero[data-variant="short"] .inner{
  max-width: var(--ds-container); margin: 0 auto;
  display: flex; flex-direction: column; gap: 64px;
}
.ds-hero[data-variant="short"] p{
  font-size: 18px; font-variation-settings: "wght" 500;
  line-height: 1.7; color: var(--ds-text-3);
}
```

h1은 다른 페이지와 같은 60px/750을 쓴다. 목록 페이지라고 제목을 줄이지 않는다.

### 10-9. 목록 행 (뉴스룸)

**카드를 쓰지 않는다.** 행과 1px 디바이더로만 나눈다. 카드로 만들면 항목마다
박스가 생겨 목록이 무거워지고, 개수가 늘수록 더 나빠진다.

```css
.ds-list{max-width:var(--ds-container);margin:0 auto}
.ds-list a{
  display:flex; flex-direction:column; gap:12px;
  padding:0 0 24px; margin-bottom:24px;
  border-bottom:1px solid var(--ds-light-divider);
}
.ds-list h3{
  font-size:23px; font-weight:400; font-variation-settings:"wght" 600;
  line-height:1.5; letter-spacing:0; color:var(--ds-light-title);
}
.ds-list p{
  font-size:16px; font-variation-settings:"wght" 400;
  line-height:1.4; color:var(--ds-light-muted);
}
.ds-list .meta{
  display:flex; gap:16px; align-items:baseline;
  font-size:16px; font-variation-settings:"wght" 400; color:var(--ds-light-muted);
}
.ds-list .meta .src{font-size:14px}
```

- 행 순서: 제목 → 요약 1~2줄 → 메타(출처, 날짜). 썸네일을 넣지 않는다.
- 제목 자간은 **0**이다. 여기만 예외로 -0.02em을 쓰지 않는다.
- 요약은 굵기 400. 제목 600과 대비를 만든다.
- 페이지네이션 없이 전부 나열한다. 12~15개까지는 그대로 읽힌다.

## 11. 비주얼 에셋

카드 오른쪽과 기능 항목 안에 무엇을 넣느냐가 완성도를 가른다. 토큰과 격자를 다
맞춰도 여기가 비면 화면이 싸 보인다.

**정본은 미리 렌더링한 에셋이다.** 원본의 비주얼 컨테이너 안에는 `<img>` 하나가
들어 있고, 폰 베젤과 헤더 그라디언트, 그림자, 잘린 구도가 전부 이미지 안에 구워져
있다. 실제 제품을 캡처해 프레임까지 포함한 PNG나 루프 mp4로 굽는 것이 가장 빠르고
결과도 가장 좋다.

### 11-1. 잘라내지 않는다

이 스킬은 한때 "컨테이너보다 크게 만들어 잘리게 하라"고 적었다. **틀렸다.**
원본을 다시 재 보면 이미지가 컨테이너를 정확히 채우고 넘침이 사방 0이다.
잘린 것처럼 보이는 구도는 이미지 안에서 디자이너가 만든 것이지, DOM이 자른 게
아니다.

CSS로 목업을 그릴 때 넘치게 두면 잘림선이 값과 컨트롤을 통과한다. 실제로 그렇게
만들었더니 `−31.5%`, `연결됨` 다섯 개, 비교군 칩 세 개가 반쯤 잘려 나갔다.
"뭔가 투박하다"는 인상은 대부분 여기서 나온다.

| | 규칙 |
| --- | --- |
| 가로 | **절대 자르지 않는다.** 모든 값이 컨테이너 안에 들어온다 |
| 세로 | 자르지 않는다. 내용을 컨테이너에 맞춘다 |
| "더 있다" 신호 | 잘림이 아니라 `+ 전체보기` 행으로 만든다 |

### 11-2. 액자를 만들지 않는다

회색 프레임 안에 흰 카드를 띄우지 않는다. **프레임이 곧 패널이다.**
원본은 582x505 이미지가 프레임을 그대로 채운다. 안쪽에 여백을 주면
"스크린샷을 붙여 넣은 상자"로 보인다.

```css
.ds-item .shot{                     /* 프레임 = 패널 */
  height:460px; background:#fff;
  border:1px solid var(--ds-light-border);
  border-radius:var(--ds-radius-shot);
  overflow:hidden; position:relative;
}
.ds-item .app{                      /* 내용이 프레임을 꽉 채운다 */
  position:absolute; inset:0;
  padding:28px; border-radius:0;
  display:flex; flex-direction:column;
}
```

### 11-3. 바닥은 액션 행으로 채운다

내용이 프레임보다 짧으면 아래가 비어 허전하다. 원본 제품 화면이 쓰는
`+ 전체보기` 행을 바닥에 붙인다. 공간도 채우고 실제 제품처럼 보인다.

```css
.app-more{
  margin-top:auto;                  /* 바닥에 붙인다 */
  padding-top:14px; border-top:1px solid #f0f0f0;
  text-align:center; font-size:13px;
  font-variation-settings:"wght" 600; color:var(--ds-app-text-muted);
}
```

### 11-4. 좁아지면 행을 줄인다

패널 높이는 고정인데 폭이 줄면 내용이 길어져 넘친다. 폭이 아니라 **행 수**를
줄인다.

```css
@media (max-width:1179px){ .app .rows .row:nth-child(n+5){display:none} }
@media (max-width:809px){
  .app .rows .row:nth-child(n+4){display:none}
  .app .grade{height:96px}
  .app .chips{display:none}          /* 컨트롤 행은 통째로 뺀다 */
}
```

컨트롤 행(칩, 탭)은 **반쯤 잘리느니 통째로 감춘다.** 반쯤 보이는 컨트롤이
가장 나빠 보인다.

### 11-5. 여러 페이지를 한 파일로 합칠 때

CSS를 라우트별로 스코프해 합치면 페이지 사이 셀렉터 충돌은 막을 수 있지만,
합치는 과정 자체가 새 결함을 만든다. 실제로 두 번 겪었다.

**중괄호 균형을 먼저 검사한다.** CSS를 줄 단위로 잘라 붙이면 여러 줄 규칙이
쪼개져 중괄호가 깨진다. 그러면 그 뒤 규칙이 통째로 하나의 선언 블록으로 삼켜져
사라진다. 한 라우트의 스타일이 전부 증발했는데 콘솔에는 아무 오류도 안 뜬다.

```js
// 합치기 전 각 조각을 검사한다. 규칙은 줄이 아니라 중괄호 단위로 자른다.
if ((css.match(/{/g)||[]).length !== (css.match(/}/g)||[]).length)
  throw new Error("중괄호 불균형 — 뒤쪽 규칙이 삼켜진다");
```

**정의하지 않은 변수를 검사한다.** `var(--ds-leading-title)`을 쓰는데 토큰 블록에
그 줄을 빠뜨리면 행간이 브라우저 기본값으로 풀린다. 값이 아니라 이름 하나가 빠져서
타이포 리듬이 통째로 무너지는데, 화면만 봐서는 원인을 못 찾는다.

**라우트마다 스타일이 실제로 먹었는지 확인한다.** 그림자와 넘침만 세면 스타일이
아예 안 붙은 라우트도 전부 0으로 나와 통과한다. 라우트별로 h1 크기, 폰트 패밀리,
컨테이너 폭 같은 기준값을 직접 대조한다. h1이 32px이면 CSS가 안 붙은 것이다.

| 검사 | 통과 기준 |
| --- | --- |
| 중괄호 | 조각마다 열림 = 닫힘 |
| 미정의 `--ds-*` | 0개 |
| h1 폰트 크기 | 라우트마다 60px |
| h1 폰트 패밀리 | `Pretendard Variable` |
| 컨테이너 폭 | 1224px |

**직접 진입으로 검증한다.** 내비 클릭만 눌러 보면 초기 로드 경로를 놓친다.
`#/price` 같은 해시를 주소창에 직접 넣어 새로고침한 상태로 확인한다.

### 11-6. 검수 방법

눈으로는 놓친다. 실제 글자 상자와 잘라내는 조상을 비교해 기계로 잡는다.

```js
// 모든 텍스트 노드의 실제 글자 상자가 overflow:hidden 조상을 넘는지
for (const el of document.querySelectorAll(".app")) {
  if (el.scrollHeight > el.clientHeight) console.warn("넘침", el, el.scrollHeight - el.clientHeight);
}
```

`scrollHeight > clientHeight`인 패널이 하나라도 있으면 통과가 아니다.
1440, 1180, 1024, 860, 390, 360 여섯 폭에서 전부 0이어야 한다.

### 11-7. 에셋을 만들 때

- 실제 데이터를 넣는다. `999,999,999,999`처럼 자리를 채운 더미는 티가 난다.
- 기기 프레임(폰 베젤, 브라우저 크롬)으로 감싸면 평면 스크린샷보다 깊이가 산다.
- 목업 안 글자는 12px 아래로 내리지 않는다.
- 요소 수 하한: 헤더 한 줄 + 주요 수치 + 보조 문장 + 데이터 영역 + 액션 행.

## 12. 제품 UI (라이트 앱)

랜딩 목업에서 관측한 값이라 정밀도가 낮다. 라이트 면으로 뒤집되 뼈대는 같다.

- 배경 `--ds-app-bg`, 사이드바·표 헤더 `--ds-app-surface`.
- 숫자가 주인공이다. 금액은 32~40px 굵게, 통화·단위는 같은 줄에 작게.
- 변화량은 **문장으로** 쓴다: `지난달보다 1,920,893,058원 (212.8%) 증가했어요`.
  증가 `--ds-app-green`, 초과·감소 `--ds-app-rose`, 차트 라인 `--ds-app-teal`.
- 강조 카드만 보라 계열 테두리로 띄운다. 나머지는 1px 회색 보더.
- 버튼은 검정 채움 + 흰 글씨. 라이트 면에서도 보라는 포인트로만 아낀다.
- radius 랜딩과 동일(카드 12, 컨트롤 8).
