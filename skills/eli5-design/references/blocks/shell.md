# shell — 페이지 골격

모든 페이지는 이 골격에서 시작한다. 고른 블록의 마크업은 `<main class="d0-page">` 안에,
CSS는 `<style>` 끝에, JS는 `</body>` 앞 `<script>` 하나에 붙인다.

## 해부 구조

- doctype → `lang="ko"` → meta viewport → 폰트 → 메인 `<style>`.
- **폰트.** 결과물 HTML을 넘길 때는(파일·artifact 모두, 발행 여부와 무관) `scripts/subset_font.py`가 만든 Pretendard 서브셋 `@font-face`(woff2 data URI)를 별도 `<style>`로
  메인 `<style>` **앞**에 둔다. 외부 요청은 0건이다. 아래 스니펫의 jsDelivr `<link>`는 작업 중 초안용이고, 도구를 못 쓸 때만 남긴다(정본: SKILL.md 출력 형식).
- 메인 `<style>`: tokens.css 전체 인라인 → `color-scheme: light` → 기본 리셋 → `body` 배경 → 컨테이너 → 타이포 스케일 → 섹션 → 강조(Impact·Quiet) → 무대 → 열 나누기 → 공용 배지 → 포커스 → 모션.
  폰트 `<style>`은 이 앞의 별도 요소라 "tokens.css는 메인 `<style>` 맨 앞" 규칙과 부딪히지 않는다.
- 컨테이너는 day0 폭 규칙을 따른다: 기본 wide `1200px`, `data-width="narrow"`면 `640px`.
- 페이지 패딩: 데스크톱 `64px 32px 96px`, 640px 이하 `48px 16px 72px`(좌우 16px 거터).
- 모든 블록은 페이지 왼쪽 정렬선 하나를 공유한다. 블록마다 들여쓰기를 따로 두지 않는다.
- **첫 화면 높이 예산(정본).** 판정은 하나다: 1100~1280px 폭에서 **첫 SVG 도식의 아래 끝이 y ≤ 720px**(갤러리 iframe 약 720px, 1280×800 첫 화면 공통).
  머리(작업 라벨 → h1 → 히어로 → 요약 행 끝) 260px + 첫 그림(무대가 있으면 무대) 300px은 **합계 560px 기준**이다(상단 패딩 64 + 머리 260 + 섹션 패딩 32 + h2·간격 약 52 + 그림 300 ≈ 708px).
  머리가 짧으면 그림이 그만큼 길어도 된다. 카드 안에 그림이 든 블록(thumb-cards·side-by-side 와이어 카드 등)은 카드 아래 끝이 아니라 첫 SVG의 아래 끝으로 잰다.
  넘으면 요약 행을 줄이거나 히어로 한 줄 뜻을 빼고, 무대 SVG의 viewBox 높이를 줄인다.

## 여백 리듬

| 자리 | 데스크톱 | 640px 이하 |
| --- | --- | --- |
| 페이지 상단 | 64px | 48px |
| 섹션 사이(구분선 위아래 합) | 64px | 48px |
| 섹션 안 블록 사이 | 24px | 24px |
| 제목 ↔ 설명 | 8px | 8px |
| 카드 안쪽 | 24px | 20px |

- 섹션 = 위쪽 1px `grey-100` 구분선 + 위아래 패딩 32px(모바일 24px). 구분선은 섹션 경계에만 긋는다.
- 블록 안 테두리는 최소로 둔다. 행 목록의 행 구분선(`grey-100`)만 허용한다. 섹션에 카드 상자를 두르지 않는다.
- 섹션 안 행은 위로 붙는다(`align-content: start`). 섹션이 늘어나도 블록 사이가 벌어지지 않는다.

## 나란히 두 섹션 (`.d0-split`)

짧은 섹션 둘(숫자 카드 + 도식, 그림 + 목록)을 한 줄에 놓을 때 쓴다. `<div class="d0-split">` 안에 `section.d0-section` 두 개.

- 960px 이상에서 2열, 그 아래는 1열. 열 사이 48px.
- 기본은 `align-items: start`라 짧은 섹션은 제 높이만 차지한다. 옆 섹션 높이에 맞춰 늘어나 아래가 비지 않는다.
  두 섹션이 모두 무대 위 그림이면 아래 무대 정렬 변형(`data-align="stage"`)이 기본이다.
- 마지막이 아닌 `.d0-split` 안 섹션은 둘 다 아래 패딩 32px(모바일 24px)을 지킨다. 오른쪽 섹션이 `:last-child`라 `padding-bottom: 0`을 받는 것을
  `.d0-split:not(:last-child) > .d0-section`이 되돌린다(이 규칙이 없으면 split 아래 여백이 왼쪽 열만큼만 남는다).
- 페이지 끝 `.d0-split`은 2열(960px 이상)에서 두 섹션 모두, 1열에서는 마지막 섹션만 `padding-bottom: 0`이다. 1열에서 왼쪽(위) 섹션의 아래 패딩까지 없애지 않는다.
- 각 섹션은 자기 `border-top`을 그대로 둔다. 데스크톱에서는 구분선이 열 사이에서 끊겨 보이는데, 의도한 모양이다.
- 세 개 이상 나란히 두지 않는다.
- **높이 기준(정본).** 데스크톱에서 한쪽 섹션 높이가 다른 쪽의 1.5배를 넘으면 나란히 두지 않고 위아래로 쌓는다.
  작은 차(예: 수십 px)는 허용하고, 짧은 쪽 아래에 큰 빈 공간이 생기면 금지다. 균형을 맞추려고 내용을 다른 섹션으로 옮기지 않는다.
  무대 정렬 변형(아래)에서는 두 섹션 높이가 같아지므로, 비는 정렬을 끈 자연 높이(또는 두 무대 안 SVG 높이)로 잰다.

### 무대 정렬 변형 (`.d0-split[data-align="stage"]`)

두 섹션이 모두 [섹션 머리 + 무대 위 그림 `figure` + figcaption]이면 이 변형이 기본이다. 좌우의 h2 줄, 무대 위·아래 끝, figcaption 줄이 같은 높이에 맞는다.
한쪽이라도 그림 없는 섹션(diff-rows·checklist·숫자 카드·explanation 등)이면 쓰지 않고 기본 `align-items: start`를 둔다.

- 960px 이상에서만 건다. `.d0-split`이 행 3개(`auto 1fr auto`)를 만들고, 각 섹션은 `grid-row: span 3` + `grid-template-rows: subgrid`,
  `figure`는 `grid-row: span 2` + `subgrid`로 무대·캡션 행을 이어받는다. 낮은 쪽 무대가 늘어나고 SVG는 무대 세로 가운데에 놓인다.
- 섹션 직계 자식은 섹션 머리 `header` 하나와 `figure` 하나뿐이다. 섹션 설명 `p`는 `header` 안에 둔다(섹션 직계에 두면 행이 어긋난다).
- 섹션의 `border-top`·패딩은 그대로다. 960px 미만(1열)에서는 변형이 풀려 기본 쌓기로 돌아간다.
- subgrid를 못 쓰는 브라우저는 `@supports` 폴백으로 섹션을 늘리고(`align-items: stretch`) 무대가 남는 높이를 채운다. 무대 아래 끝과 캡션 줄은 맞고, 머리 높이가 다르면 무대 위 끝이 그 차만큼 어긋난다.

```html
<div class="d0-split" data-align="stage">
  <section class="d0-section" aria-labelledby="sec-b">
    <header class="d0-section-head"><h2 id="sec-b">전에는 이렇게 돌았어요</h2></header>
    <figure class="d0-fig" data-stage><div class="d0-fig__stage"><svg …>…</svg></div><figcaption>…</figcaption></figure>
  </section>
  <section class="d0-section" aria-labelledby="sec-c">
    <header class="d0-section-head"><h2 id="sec-c">지금은 이렇게 돌아요</h2></header>
    <figure class="d0-fig" data-stage><div class="d0-fig__stage"><svg …>…</svg></div><figcaption>…</figcaption></figure>
  </section>
</div>
```

## 줄 길이 (정본)

본문 텍스트 블록 한 줄은 **공백 포함 실제 글자 수 50자 이하**다(`code`·`pre`·명령어 줄·[code-block](code-block.md) 제외). 판정은 렌더된 줄마다 공백까지 센 글자 수로 하고, 폭에서 글자 수를 추정하는 근사식은 쓰지 않는다.

- **폭 기준은 32em이다.** Pretendard 15px 본문에서 공백 포함 50자 연속 구간의 폭은 실측 482~529px(32.1~35.2em)이다.
  그래서 글 블록 컨테이너가 32em(15px에서 480px) 이하이면 한글 위주 문장은 한 줄 50자를 넘지 못한다. 행간(1.55~1.65)은 이 값에 영향이 없다.
  숫자·라틴 문자·공백이 많은 줄은 글자 폭이 좁아 같은 폭에 더 들어갈 수 있으므로 실제 글자 수로 확인한다.
  같은 측정에서 650px 열은 최대 66자, 1200px 페이지의 반 열(약 552px)은 54자였다. 2열로 나누는 것만으로는 50자를 지키지 못한다.
- **좁히는 곳은 컨테이너다.** `p`·`dd`에 `max-width`를 걸지 않고(개행 규칙), 글 블록 컨테이너(explanation `dl`, evidence `dl`, faq `dl`)에 `max-width: 32em`을 건다. 2열(`.d0-cols`)로 쓴 글 블록은 묶음 대신 열 칸(`.d0-cols > *`)마다 32em이 걸린다. 960px 미만 1열에서도 같다.
  em 단위라 14px 보조문 블록에서도 같은 기준이 된다. 그 안 문단은 컨테이너 폭을 그대로 쓰므로 "옆 영역이 남는데 줄이 바뀐 문단" 게이트의 대상이 아니다(32em 바깥 빈 폭은 남는 영역으로 세지 않는다).
- **한 줄짜리 글**(요약 행 값, 행 설명, checklist 결과 한 줄, checkpoint)은 문장 길이로 지킨다. 50자를 넘는 문장은 줄인다.
- **리드 `p`**(header 리드, 섹션 리드)는 컨테이너를 좁히지 않는다. 리드가 한 줄 50자를 넘으면 문장 단위 개행(`.d0-sentence`)이 **필수**다(아래 개행 절의 "선택" 조건보다 이 규칙이 우선한다). 문장마다 줄을 나누고 문장 하나를 50자 이내로 쓴다.
- **2열(`.d0-cols`).** 960px 이상에서 열 트랙이 각각 `minmax(0, 32em)`인 2열 grid(열 사이 48px), 그 아래는 1열이다. 글 블록의 열 칸은 어느 폭에서나 `max-width: 32em`이다(그림 칸은 그림 폭 상한을 따른다).
  그림 + 짧은 설명, 행 목록 둘(주의 | 할 일), 짝수 개 행 목록에 쓴다. 행 목록 2열 변형은 [diff-rows.md](diff-rows.md).
- 홀수 개 항목을 2열로 나눠 마지막 하나가 외톨이로 남으면 쓰지 않는다. 섹션 둘이면 `.d0-split`을 쓴다.
- 그림 옆 설명 열(`.d0-figtext`, `data-layout="side"`)도 글 열을 `minmax(220px, 32em)`으로 둔다([explanation.md](explanation.md), [diagram.md](diagram.md)).

## 타이포 스케일

| 역할 | 크기 / 굵기 | 색 | 640px 이하 |
| --- | --- | --- | --- |
| h1 (페이지 제목) | 32px / 700, display 자간·행간 | grey-900 | 26px |
| 히어로 숫자 | 44px / 600, display 자간, 단위도 같은 크기 | grey-900(선택: blue-dark) | 36px ([hero.md](hero.md)) |
| Impact 문장 (`.d0-impact__line`) | 32px / 700, display 자간·행간 | grey-900 | 24px (아래 강조 절) |
| Impact 숫자 (`.d0-impact__num`) | 64px / 600, display 자간, 단위도 같은 크기 | blue-dark | 48px (아래 강조 절) |
| h2 (섹션 제목) | 20px / 700, title 자간 | grey-900 | 18px |
| h3 (그림·열 제목) | 16px / 650 | grey-900 | 16px |
| 본문 | 15px / 400, 문단 행간 1.65(아래 행간 예외) | grey-800 | 15px |
| 보조(섹션 설명, 행 설명) | 14px / 400 | grey-600 | 14px |
| 그림 설명(figcaption) | 13px / 400 | grey-600 | 13px |
| 라벨(카드 라벨, 막대 라벨) | 12px / 600, 대문자 변환 없음 | grey-600 | 12px |
| 배지 | 12px / 600, 높이 22px | 아래 배지 표 | 12px |

- 숫자는 전부 `font-variant-numeric: tabular-nums`다. `body`에 한 번 건다.
- **행간 예외(정본).** 행간은 토큰(`--d0-leading-*`)이 기본이다. 단 설명 문단(`p`, explanation `dd`)의 행간 1.65는 긴 설명을 읽기 위한 이 스킬의 타이포 값이고 글(본문) 행간에서 토큰 규칙의 예외다(배지·큰 숫자·핀처럼 한 줄 요소의 `line-height: 1`은 글 행간이 아니다). 다른 글자(본문 `body`, 목록, 슬라이드)는 `--d0-leading-body`(1.55)를 쓴다.
- 12px 라벨 글자는 grey-600(흰 바탕 5.0, grey-50 위 4.71)이다. grey-500은 흰 바탕 3.19라 작은 글자에 쓰지 않는다.
  히어로 전 값도 grey-600이다.
- 회색 보조문은 줄인다. 섹션 설명은 최대 1문장이고 제목과 같은 말이면 뺀다. 주 콘텐츠는 그림과 숫자, 15px 본문이다.

## 강조 면 (`data-emphasis`)

장면의 음량을 정한다. 구도·리듬과 언제 쓰는지는 [composition.md](../composition.md)가 정본이고, 이 절은 모양과 CSS다.
`main > section`(page)이나 `.d0-slide`(deck)에 단다. 생략하면 normal이다.

**Impact (`data-emphasis="impact"`).** 선택이다(페이지당 0~1개). 섹션을 하나 **더하지 않고** 기존 섹션 하나를 큰 글자와 여백만으로 크게 말하는 장면으로 바꾼다. **page만 이 모양이다.** 배경 면·풀블리드 띠·카드 없이 글자 크기와 여백이 무게를 만든다. deck Impact 슬라이드는 이 절이 아니라 [slide-deck.md](slide-deck.md)(blue-light 면)를 따르며 바뀌지 않았다.
Impact·Spotlight 밖의 타이포·간격은 이 파일의 기본값 그대로다.

- 배경색·`margin-inline`·`100vw` 확장·`:has()` 간격 보정이 없다. 섹션 안 위아래 패딩과 위쪽 구분선은 일반 섹션과 같아(32px + 32px) 이웃 섹션과의 간격이 일반과 똑같이 64px(모바일 48px)다. 더 또렷한 경계가 필요하면 위쪽 구분선만 `var(--d0-grey-200)`로 한 단계 진하게 쓸 수 있다.
- 안에는 하나만: 문장 하나(`h2.d0-impact__line`, 32px/700, 모바일 24px) 또는 숫자 하나(`h2` 라벨 + `p.d0-impact__num`, 64px, 모바일 48px). 카드·목록·배지·둥근 박스·editorial 도식·무대 금지.
- 글자는 grey-900, 강조 숫자는 blue-dark다. 바탕이 흰색이라 보조 글자(섹션 설명·figcaption·`.d0-note`)는 일반 섹션 그대로 grey-600이다.
- 큰 숫자 blue-dark는 페이지에 하나다. Impact에 숫자를 두면 header 히어로 숫자는 grey-900으로 두고, 같은 숫자를 되풀이하지 않는다([hero.md](hero.md)).
- page는 페이지당 0~1개다. 어두운 배경으로 바꾸지 않는다(라이트 온리).

```html
<!-- 문장 하나 -->
<section class="d0-section" data-emphasis="impact" data-composition="hero" aria-labelledby="sec-i">
  <h2 id="sec-i" class="d0-impact__line">고친 파일에 닿는 검사만 다시 돌아요</h2>
</section>
<!-- 숫자 하나 -->
<section class="d0-section" data-emphasis="impact" data-composition="hero" aria-labelledby="sec-n">
  <h2 id="sec-n">밤사이 멈춘 내보내기</h2>
  <p class="d0-impact__num"><data value="58">58</data>건</p>
</section>
```

**Quiet (`data-emphasis="quiet"`).** 참고·부록·정리 목록처럼 뒤로 물러날 섹션이다. h2를 18px로 한 단계 낮추고 본문·목록 글자를 grey-700로 둔다(섹션 설명 `p`·figcaption은 원래 grey-600 그대로).
진한 포인트 채움(blue 막대·노드·버튼)을 새로 두지 않는다. 완료 체크·의미색 점처럼 상태를 말하는 표식은 그대로 둔다.

## 그림 무대 (`.d0-fig[data-stage]`) — 기본 없음, 필요할 때만

**기본은 무대 없음이다.** 도식 `figure.d0-fig`는 흰 바탕에 바로 SVG를 두고 페이지 왼쪽 정렬선을 따른다. `figcaption`은 그림 아래 13px grey-600이다.
**무대를 쓰는 때:** 도식이 여백 없이 떠서 그림의 경계가 안 보일 때(흩어진 노드, 테두리 없는 선 그림), 목업·고스트 카드처럼 흰 면 요소에 받침 면이 필요할 때,
나란히 둔 두 그림의 높이를 맞출 때(`.d0-split[data-align="stage"]`).
**그림을 키워 폭을 채우지 않는다.** SVG는 글자가 없어도(와이어프레임·핀 그림 포함) 기본 360px, `data-size="wide"` 400px에서 멈춘다. 옆이 비면 관련 explanation을 그림 옆 열(`.d0-figtext`, [explanation.md](explanation.md))에 두거나 `.d0-split` 2열(우선), `data-layout="side"`, `.d0-cols` 한 열, 그림 옆 짧은 주석·범례 열(900px 이상)로 채운다.
전체 폭 그림은 가로로 긴 타임라인·단계 줄만 쓰고 최대 720px다([diagram.md](diagram.md) 라벨 절).

무대를 쓰면 패널 = `div.d0-fig__stage`(배경 grey-50, `--d0-radius-card`, 패딩 28px,
모바일 20px). `figcaption`은 패널 **밖** 아래에 13px grey-600으로 둔다. 테두리·그림자는 없다.
SVG는 패널 안에서 가운데 놓이고, 패널 자체는 페이지 왼쪽 정렬선을 따른다. 선 굵기·라벨 규칙은 [diagram.md](diagram.md).
페이지의 핵심 도식 하나는 `data-stage="blue"`로 무대를 blue-light로 칠할 수 있다. 그 무대 위 회색 선·글자는 한 단계 진하게 바뀐다([diagram.md](diagram.md) 공용 CSS).
Impact 안에서는 무대를 두지 않는다.

```html
<!-- 기본: 무대 없음 -->
<figure class="d0-fig" data-layout="side">
  <svg viewBox="0 0 360 224" role="img" aria-labelledby="g1-t">…</svg>
  <figcaption>고친 파일에서 선을 따라간 검사만 다시 돌아요.</figcaption>
</figure>
<!-- 필요할 때만: 무대 -->
<figure class="d0-fig" data-stage>
  <div class="d0-fig__stage"><svg viewBox="0 0 360 224" role="img" aria-labelledby="g2-t">…</svg></div>
  <figcaption>흩어진 노드가 어디까지 한 그림인지 무대가 묶어 줘요.</figcaption>
</figure>
```

## 색 (정본)

Day0의 6:3:1(배경 · 텍스트 · 포인트)을 따른다. **회색만 남은 페이지는 실패다.** 이 절이 색 규칙의 정본이고 다른 파일은 여기를 가리킨다.

- **색 면적은 lint Warning이다.** 1280×800과 375×812 첫 화면에서 진한 포인트 채움이 **1% 미만**이면 "강조가 너무 약한지 확인", **1~15%**이면 정상, **15% 초과**이면 "포인트 색이 배경처럼 쓰이는지 확인" 경고를 낸다. 경계값 1%·15%는 정상이다.
  색 면적 때문에 출력을 실패시키지 않고, 게이트를 맞추려고 색 면적을 늘리지 않는다. 색은 상태·강조·구조가 있는 자리에만 둔다.
  - **측정 정의(정본).** 진한 포인트 = `blue`·`blue-dark`·`green`·`orange`·`red` 채움. HTML `background-color`와 SVG 도형 `fill`이 해당 색인 요소의 보이는 bbox 합 ÷ 뷰포트 면적(뷰포트로 자름, 이미 센 요소의 자손은 제외)으로 잰다.
    `stroke`·`border`만 해당 색인 요소는 세지 않는다. 진한 포인트는 옅은 면 안에 있어도 센다.
  - 내용 단위 옅은 채움과 **면 단위 옅은 표면**(blue-light 무대, 덱 Impact 슬라이드, 썸네일 판)은 이 진한 포인트 경고 비율에서 뺀다.
    장면 수는 별도로 유지한다: page는 blue 무대 최대 1개(Impact는 면이 없다), deck은 Impact 슬라이드 20~30%([composition.md](../composition.md)).
  - 회색만으로 된 도식·카드 묶음 금지는 유지한다. 의미 있는 blue 또는 의미색 표식 하나를 두되 경고 비율을 채우려고 뜻 없는 면을 칠하지 않는다.
- **Hard 유지.** 대비와 WCAG 2.2 AA, 의미색 글자 금지는 색 면적 Warning과 별개로 반드시 통과한다.
- **블루 단계.** `blue` = 강조 선·채움(후 막대, 닿는 노드, 진행 막대, 썸네일 합계 칸). `blue-dark` = 글자·번호, 흰 글자 바탕(버튼, 고른 탭, 흐름 줄의 현재 단계).
  `blue-light` = 옅은 면(썸네일 판, 반 열 도식의 무대 `data-stage="blue"`, 덱 Impact 슬라이드, 선택 카드, 표 머리 행·합계 행).
- **강조 순서.** 크기 → 위치 → 여백 → 무게 → 색. 큰 숫자는 색이 아니라 크기로 중요하게 만든다(기본 grey-900, 큰 숫자 blue-dark는 페이지에 하나).
  blue는 장면마다 강조 묶음 하나에만 둔다([composition.md](../composition.md) 강조).
- **의미색.** `green` = 가능·통과·완료, `orange` = 주의·준비 중, `red` = 위험·실패. 도식 채움·막대·체크·배지 배경에 쓴다.
  페이지당 의미색 2가지까지 + blue. **의미색은 글자 색으로 쓰지 않는다**(흰 바탕 4.5:1 미달). 글자는 grey-900·blue-dark, 색은 면·점·선으로 낸다.
- **orange 한계.** 그래픽 3:1을 green(3.17~3.47)·red(3.21~3.57)는 넘고 orange(2.30~2.47)는 못 넘는다. orange는 옅은 배경(`orange-bg`) + 글자 라벨,
  또는 grey-700 테두리를 함께 둘 때만 쓴다. orange 선·점·노드 혼자 뜻을 전하게 하지 않는다.
- **표·격자.** 썸네일 격자와 표 목업은 머리 행 blue-light, 합계 blue, 키 열 grey-400이 기본이다. 글자가 든 표 칸은 blue 위 흰 글자(3.99)가
  안 되므로 합계 행을 blue-light 바탕 + 위 2px blue 선 + grey-900 굵은 글자로 그린다. 순수 blue 채움은 글자 없는 썸네일 칸에만 쓴다.
- **체크·완료**는 green 채움 + 흰 체크선(3.47:1)이다. 진행 막대는 blue다.

### 대비 계산표

tokens.css 실제 값으로 계산한 WCAG 2.x 비율이다. 글자 4.5:1, 큰 글자(18.66px/700 이상)·그래픽 3:1.

| 앞 / 뒤 | 비율 | 판정 |
| --- | --- | --- |
| blue-dark / 흰 · grey-50 · blue-light | 5.50 · 5.18 · 4.94 | 글자 통과 |
| 흰 / blue-dark | 5.50 | 흰 글자·번호 통과 |
| 흰 / blue | 3.99 | 글자 미달, 그래픽만 |
| blue / 흰 · grey-50 · blue-light | 3.99 · 3.75 · 3.58 | 그래픽 통과 |
| grey-900 / blue-light · green-bg · red-bg · orange-bg | 14.87 · 15.12 · 14.91 · 15.42 | 글자 통과 |
| grey-700 / blue-light · grey-100 | 6.87 · 6.70 | 글자 통과 |
| grey-600 / grey-50 · blue-light | 4.71 · **4.49** | blue-light 위 글자 미달 → grey-700 |
| grey-500 / grey-50 · blue-light | 3.01 · **2.87** | blue-light 위 선 미달 → grey-600 |
| green / 흰 · grey-50 · green-bg · blue-light | 3.47 · 3.26 · 3.17 · 3.11 | 그래픽 통과, 글자 미달 |
| 흰 / green | 3.47 | 흰 체크선 통과(그래픽) |
| red / 흰 · grey-50 · red-bg · blue-light | 3.57 · 3.36 · 3.21 · 3.20 | 그래픽 통과, 글자 미달 |
| orange / 흰 · grey-50 · orange-bg | 2.47 · 2.32 · 2.30 | 그래픽 미달 → 라벨·테두리 동반 |

## 배지 (`.d0-pill`)

배지는 상태·분류를 글자로 말하고, 색은 배경과 점으로 거든다.

| 톤 | 글자 / 배경 | 글자 대비 | 점 / 배경 |
| --- | --- | --- | --- |
| 기본(회색) | grey-700 / grey-100 | 6.70 | 없음 |
| `blue` | blue-dark / blue-light | 4.94 | 없음(글자 자체가 블루) |
| `green` | grey-900 / green-bg | 15.12 | green / green-bg 3.17 |
| `red` | grey-900 / red-bg | 14.91 | red / red-bg 3.21 |
| `orange` | grey-900 / orange-bg | 15.42 | orange / orange-bg 2.30 (보조 표식) |

점은 글자 배지를 거드는 보조 표식이라 `aria-hidden`이다. 상태 뜻은 글자가 전한다(1.4.11 대상 아님).

**배지 수.** 정보가 있는 상태 배지는 카드·행마다 1개까지, 페이지 전체 톤 종류(`data-tone` 값, 없으면 회색)는 3가지 이하다.
기본 상태라도 다른 상태와 대비가 필요하면 단다(예: `지금 가능` / `준비 중` / `백엔드 필요`). 모든 항목이 같은 상태면 항목마다 달지 않는다. 그 상태를 알려야 하면 섹션 머리에 한 번만 단다(diff-rows `data-badge="head"`, [diff-rows.md](diff-rows.md)).
탭·버튼으로 쓰는 pill(아래 32px 변형)은 컨트롤이라 배지로 세지 않는다.

**높이 고정.** 배지는 grid·flex 행 안에서 늘어나지 않는다. `height` 고정 + `flex: none` + `align-self: flex-start`
+ `justify-self: start`. 작은 변형(`data-size="sm"`)은 20px. 버튼·탭으로 쓰는 pill은 포인터 대상 24px 하한 때문에
높이 32px이다(`button.d0-pill`, `a.d0-pill`, `[role="tab"].d0-pill`).

## 개행

- 리드·설명 문단은 부모 폭을 그대로 쓴다. `p`에 컨테이너보다 좁은 `max-width`를 걸지 않는다. 줄이 길면 위 줄 길이 절대로 글 블록 컨테이너를 32em으로 두거나 `.d0-cols`로 나눈다.
- 문장 단위 개행(선택, 단 리드가 한 줄 50자를 넘으면 필수 — 위 줄 길이 절): 리드·설명이 2문장 이상이고 데스크톱 폭에서 2줄을 넘기거나 문장마다 역할이 다르면
  문장마다 `<span class="d0-sentence">`로 감싼다(`display: block`). `<br>`을 늘어놓지 않는다.

## 모션 (선택)

- 섹션 진입: 섹션의 직계 블록이 opacity 0 → 1, 8px 아래에서 제자리로. 블록마다 60ms씩 늦게 시작한다.
- SVG 강조 경로: `class="d0-draw"` + `pathLength="1"`인 `path`가 600ms 동안 그려진다(`stroke-dashoffset` 1 → 0, `var(--d0-ease)`).
  여러 갈래를 동시에 그리려면 갈래마다 `path`를 따로 둔다(한 `path`의 서브패스는 이어서 그려진다).
- `IntersectionObserver`가 블록을 한 번만 드러내고 관찰을 끝낸다. 스크롤을 올려도 다시 숨기지 않는다.
- 초기 숨김은 스크립트가 `<html>`에 붙인 `data-motion="on"` 아래에서만 건다. JS가 없거나 꺼져 있으면 모든 것이 처음부터 보인다.
- `prefers-reduced-motion: reduce`이면 스크립트가 `data-motion`을 붙이지 않는다. 숨김도 움직임도 없다.
- 무대 위 경로 그리기는 그 경로를 품은 블록이 드러날 때 함께 시작한다.

## 스니펫

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>주문 내보내기 한눈에 보기</title>
<!-- 넘기기 전(파일·artifact 모두): 이 <link> 대신 scripts/subset_font.py 출력(<style>@font-face…</style>)을 여기 둔다 -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
/* (아래 css 블록 + 고른 블록 css) */
</style>
</head>
<body>
<main class="d0-page">
  <!-- header(h1 → 히어로 → 요약 행) → section(독자 질문마다 하나, data-pattern) -->
  <section class="d0-section" data-pattern="preview" aria-labelledby="sec-a">
    <header class="d0-section-head"><h2 id="sec-a">파일은 이렇게 생겼어요</h2></header>
    <!-- 무대 위 그림 하나 + 그림 설명 한 줄 -->
  </section>
  <div class="d0-split">
    <section class="d0-section" aria-labelledby="sec-b"><header class="d0-section-head"><h2 id="sec-b">어디서 줄었나</h2></header><!-- 숫자 카드 --></section>
    <section class="d0-section" aria-labelledby="sec-c"><header class="d0-section-head"><h2 id="sec-c">어디가 다시 도나</h2></header><!-- 도식 --></section>
  </div>
</main>
<script>
/* 모션 JS + 인터랙션 블록의 JS를 여기 붙인다 */
</script>
</body>
</html>
```

```css
/* ../day0-design/references/tokens.css 파일 전체를 수정 없이 여기(메인 <style> 맨 앞)에 붙인다.
   day0-design 위치는 SKILL.md의 탐색 순서를 따른다. 토큰을 외부 <link>로 걸지 않는다. */
:root { color-scheme: light; }
/* 스크롤바 자리를 항상 비워 둔다: 긴 페이지와 짧은 페이지를 오가거나 탭·토글로 높이가 바뀌어도 가로 폭이 흔들리지 않는다 */
html { scrollbar-gutter: stable; }
*, *::before, *::after { box-sizing: border-box; }
body {
  margin: 0;
  background: #fff;
  color: var(--d0-grey-800);
  font-family: var(--d0-font);
  font-size: 15px;
  line-height: var(--d0-leading-body);
  letter-spacing: var(--d0-tracking-body);
  font-variant-numeric: tabular-nums;
  word-break: keep-all;
  overflow-wrap: break-word;
}
.d0-page { max-width: 1200px; margin: 0 auto; padding: 64px 32px 96px; }
.d0-page[data-width="narrow"] { max-width: 640px; }
h1, h2, h3 {
  margin: 0;
  color: var(--d0-grey-900);
  line-height: var(--d0-leading-title);
  letter-spacing: var(--d0-tracking-title);
  text-wrap: balance;
}
h1 { font-size: 32px; font-weight: 700; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
h2 { font-size: 20px; font-weight: 700; }
h3 { font-size: 16px; font-weight: 650; }
p { margin: 0; line-height: 1.65; text-wrap: pretty; }
ul, ol, dl, dd, figure { margin: 0; padding: 0; list-style: none; }
svg { display: block; max-width: 100%; height: auto; }
button { font: inherit; color: inherit; letter-spacing: inherit; cursor: pointer; }
.d0-sentence { display: block; }

/* 섹션: 구분선 위아래 32px씩 → 섹션 사이 64px */
.d0-section { display: grid; gap: 24px; align-content: start; min-width: 0; padding-block: 32px; border-top: 1px solid var(--d0-grey-100); }
.d0-section:last-child { padding-bottom: 0; } /* 1열 split이면 마지막(아래) 섹션만 0 */
.d0-split:not(:last-child) > .d0-section { padding-bottom: 32px; } /* 오른쪽 섹션도 :last-child라 0이 되는 것을 막는다 */
.d0-split { display: grid; gap: 0 48px; }
.d0-split > * { min-width: 0; }
.d0-cols { display: grid; gap: 24px 48px; align-items: start; }
.d0-cols > * { min-width: 0; }
/* 줄 길이(정본: 줄 길이 절): 글 블록 컨테이너 32em = 15px 본문 공백 포함 50자 이하. p·dd에는 걸지 않는다 */
:is(.d0-explain, .d0-evidence, .d0-faq):not(.d0-cols) { max-width: 32em; }
:is(.d0-explain, .d0-evidence, .d0-faq).d0-cols > * { max-width: 32em; } /* 2열 글 블록: 열 칸마다, 960px 미만 1열에서도 */
@media (min-width: 960px) {
  .d0-split { grid-template-columns: 1fr 1fr; align-items: start; }
  .d0-cols { grid-template-columns: repeat(2, minmax(0, 32em)); }
  .d0-split:last-child > .d0-section { padding-bottom: 0; } /* 2열에서만 두 섹션 모두 0 */
  /* 무대 정렬: 두 그림 섹션의 머리·무대·캡션 줄을 맞춘다 */
  .d0-split[data-align="stage"] { grid-template-rows: auto 1fr auto; align-items: stretch; }
  .d0-split[data-align="stage"] > .d0-section { grid-row: span 3; grid-template-rows: subgrid; align-content: stretch; }
  .d0-split[data-align="stage"] > .d0-section > .d0-fig { grid-row: span 2; grid-template-rows: subgrid; align-content: stretch; }
  .d0-split[data-align="stage"] .d0-fig__stage { align-content: center; }
  .d0-split[data-align="stage"] .d0-section-head { align-content: start; } /* 낮은 쪽 머리의 h2가 행 높이로 늘어나지 않게 */
  @supports not (grid-template-rows: subgrid) {
    .d0-split[data-align="stage"] { grid-template-rows: none; }
    .d0-split[data-align="stage"] > .d0-section { grid-row: auto; grid-template-rows: auto 1fr; }
    .d0-split[data-align="stage"] > .d0-section > .d0-fig { grid-row: auto; grid-template-rows: 1fr auto; }
  }
}
.d0-section > p { color: var(--d0-grey-600); font-size: 14px; }
.d0-note { color: var(--d0-grey-600); font-size: var(--d0-text-compact); }

/* 강조: page Impact = 배경 없이 큰 글자와 여백(섹션 간격 64 그대로), Quiet = 한 단계 물러남. 덱 Impact는 slide-deck.md */
.d0-section[data-emphasis="impact"] .d0-fig__stage { padding: 0; background: transparent; } /* Impact 안에는 무대 없음 */
.d0-impact__line { font-size: 32px; font-weight: 700; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
.d0-impact__num, .d0-section > .d0-impact__num { color: var(--d0-blue-dark); font-size: 64px; font-weight: 600; line-height: 1; letter-spacing: var(--d0-tracking-display); }
.d0-section[data-emphasis="quiet"] { color: var(--d0-grey-700); }
.d0-section[data-emphasis="quiet"] h2 { font-size: 18px; }

/* 그림: 기본은 무대 없음. 무대(.d0-fig__stage)는 경계가 안 보이거나 받침 면이 필요할 때만 쓴다 */
.d0-fig { display: grid; gap: 12px; align-content: start; min-width: 0; }
.d0-fig__stage { display: grid; justify-items: center; padding: 28px; border-radius: var(--d0-radius-card); background: var(--d0-grey-50); }
.d0-fig__stage > :not(svg) { justify-self: stretch; } /* 카드 목록 등 SVG 아닌 내용은 무대 폭을 채운다 */
.d0-fig figcaption { color: var(--d0-grey-600); font-size: var(--d0-text-compact); }
.d0-fig[data-stage="blue"] > .d0-fig__stage { background: var(--d0-blue-light); } /* 핵심 도식 하나만 */

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

/* 모션: data-motion은 JS가 reduced-motion이 아닐 때만 붙인다. 없으면 전부 그대로 보인다. */
html[data-motion="on"] [data-reveal] {
  transition: opacity calc(var(--d0-dur) * 2) var(--d0-ease), transform calc(var(--d0-dur) * 2) var(--d0-ease);
}
html[data-motion="on"] [data-reveal]:not([data-in]) { opacity: 0; transform: translateY(8px); }
html[data-motion="on"] .d0-draw { stroke-dasharray: 1; stroke-dashoffset: 0; transition: stroke-dashoffset 600ms var(--d0-ease) 120ms; }
html[data-motion="on"] [data-reveal]:not([data-in]) .d0-draw { stroke-dashoffset: 1; }

@media (max-width: 640px) {
  .d0-page { padding: 48px 16px 72px; }
  h1 { font-size: 26px; }
  h2 { font-size: 18px; }
  .d0-section { padding-block: 24px; }
  .d0-split:not(:last-child) > .d0-section { padding-bottom: 24px; }
  .d0-fig__stage { padding: 20px; }
  .d0-impact__line { font-size: 24px; }
  .d0-impact__num, .d0-section > .d0-impact__num { font-size: 48px; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

```js
// 모션: 섹션 직계 블록을 한 번 드러내고(60ms 순차), 안의 .d0-draw 경로를 그린다.
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var groups = document.querySelectorAll('.d0-header, .d0-section');
  if (!groups.length) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.setAttribute('data-in', '');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  groups.forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (el, i) {
      el.setAttribute('data-reveal', '');
      el.style.transitionDelay = (i * 60) + 'ms';
      io.observe(el);
    });
  });
  document.documentElement.setAttribute('data-motion', 'on');
})();
```

## 금지

- 다크 팔레트·`prefers-color-scheme: dark` 분기 추가, `body` 배경 생략.
- `p`나 리드에 컨테이너보다 좁은 `max-width`·`width`·`ch`. 줄이 길면 글 블록 컨테이너 32em(줄 길이 절)이나 `.d0-cols`, 페이지 전체를 좁히려면 `data-width="narrow"`.
- Pretendard jsDelivr 링크 외 외부 폰트·CSS·JS 링크, 넘긴 결과물 HTML에 남은 외부 폰트 요청(도구가 없을 때만 예외), `outline: none` 단독 사용.
- 글자에 `--d0-blue`·`--d0-grey-500` 이하·시맨틱 전경색 사용(흰 바탕 대비 4.5:1 미달). 글자는 `--d0-blue-dark`, `--d0-grey-600` 이상.
  예외는 18.66px/700 이상 큰 글자(3:1)뿐이다.
- tokens.css에 없는 `--d0-*` 변수 만들기(표면 `#fff`만 예외). 반투명 막은 `color-mix(in srgb, var(--d0-grey-900) 32%, transparent)`.
- 배지 높이를 행 높이에 맡기기(늘어난 배지), 섹션마다 카드 상자, 섹션 안 블록마다 테두리, 섹션·행 사이 `grey-200` 이상 진한 구분선.
  예외는 블록 안 한 줄 표식인 closing 문장 아래 구분선(page `.d0-closing__meta`, deck `.d0-slide__meta`)과 checkpoint 뒤 선이다. 이 둘은 1px grey-200이고 섹션·행 구분선으로 세지 않는다.
- 회색만 있는 도식·카드, 의미색 글자, 의미색 3가지 이상, 카드·행 하나에 배지 2개 이상, 배지 톤 4종류 이상, 혼자 뜻을 전하는 orange 선·점.
- `.d0-split`에 섹션 3개 이상, `align-items: stretch`로 짧은 섹션을 옆 섹션 높이까지 늘리기(두 그림 섹션의 무대 정렬 변형 `data-align="stage"`만 예외. 늘어난 높이는 무대가 받는다).
- 그라디언트·글래스·두꺼운 그림자·장식 3D, 무대 패널에 테두리나 그림자.
- 기본값으로 두른 무대(경계가 이미 보이는 그림에 회색 패널), 섹션마다 같은 `제목 → 무대 → SVG → 캡션` 모양.
- Impact를 쓰려고 섹션 더하기, 그림을 키워 폭 채우기(360/400px 상한 넘기기, 전체 폭은 타임라인·단계 줄 720px까지만).
- page Impact 2개 이상, Impact 안 카드·목록·배지·무대·editorial·숫자 둘 이상, page Impact에 배경 면·풀블리드 띠 칠하기, 어두운 Impact 면.
- CSS만으로 초기 숨김(`opacity: 0`을 `data-motion` 밖에 걸기), 스크롤마다 반복되는 모션, reduced-motion 무시.
