# shell — 페이지 골격

모든 페이지는 이 골격에서 시작한다. 고른 블록의 마크업은 `<main class="d0-page">` 안에,
CSS는 `<style>` 끝에, JS는 `</body>` 앞 `<script>` 하나에 붙인다.

## 해부 구조

- doctype → `lang="ko"` → meta viewport → 폰트 → 메인 `<style>`.
- **폰트.** 결과물 HTML을 넘길 때는(파일·artifact 모두, 발행 여부와 무관) `scripts/subset_font.py`가 만든 Pretendard 서브셋 `@font-face`(woff2 data URI)를 별도 `<style>`로
  메인 `<style>` **앞**에 둔다. 외부 요청은 0건이다. 아래 스니펫의 jsDelivr `<link>`는 작업 중 초안용이고, 도구를 못 쓸 때만 남긴다(정본: SKILL.md 출력 형식).
- 메인 `<style>`: tokens.css 전체 인라인 → `color-scheme: light` → 기본 리셋 → `body` 배경 → 프레임과 읽기 축·폭 단계·넓은 구간·그림 폭·2열·여백 주석·접기·기억할 한 줄(정본 CSS) → 타이포 스케일 → 섹션 → 강조(Impact·Quiet) → 무대 → 공용 배지 → 포커스 → 모션.
  폰트 `<style>`은 이 앞의 별도 요소라 "tokens.css는 메인 `<style>` 맨 앞" 규칙과 부딪히지 않는다.
- **프레임과 읽기 축.** `.d0-page` 안쪽 폭이 가운데 프레임(기본 1136px)이고, 읽기 축(기본 720px)은 프레임 왼쪽에 붙는다. 폭 단계 `data-width`가 narrow(축 640px)·기본(720px)·report(축 960px·프레임 1280px·글 720px)를 정한다. 모든 섹션이 프레임 왼쪽 같은 시작선에서 시작한다(아래 프레임과 왼쪽 읽기 축 절).
- 페이지 패딩: 데스크톱 `64px 32px 96px`, 640px 이하 `48px 16px 72px`(좌우 16px 거터).
- 모든 블록은 프레임 왼쪽 정렬선 하나를 공유한다. 블록마다 들여쓰기를 따로 두지 않는다. 축 오른쪽으로 나가는 것은 `.d0-wide` 구간과 여백 주석 `.d0-margin`뿐이다.
- **첫 화면 높이 예산(정본).** 판정은 둘이다: 1280×800에서 **첫 SVG 도식의 아래 끝이 y ≤ 800px**(전부 보인다, SKILL.md 원칙 2번), 높이 약 720px 프레임(갤러리 iframe, 1280×720)에서는 **첫 SVG 도식의 위쪽 절반 이상이 y ≤ 720px 안**에 든다.
  머리(작업 라벨 → h1 → 히어로 → 요약 행 끝) 260px + 첫 그림(무대가 있으면 무대) 렌더 높이 390px이 **합계 650px 기준**이다(상단 패딩 64 + 머리 260 + 섹션 패딩 32 + h2·간격 약 52 + 그림 390 ≈ 798px).
  그림은 축 폭을 채우므로 렌더 높이 = 렌더 폭 × viewBox 높이 ÷ viewBox 폭이다. 축 720px에서 viewBox 폭 560이면 viewBox 높이 300 이하(렌더 약 386px)가 기준이다. report 축 960px에서 viewBox 폭 750이면 같은 배율(약 1.28)이라 viewBox 높이 300 이하가 같은 기준이다.
  머리가 짧으면 그림이 그만큼 길어도 된다. 카드 안에 그림이 든 블록(thumb-cards·side-by-side 와이어 카드 등)은 카드 아래 끝이 아니라 첫 SVG의 아래 끝으로 잰다.
  넘으면 요약 행을 줄이거나 히어로 한 줄 뜻을 빼고, 첫 그림의 viewBox 높이를 줄이거나 `data-fit="compact"`로 둔다.

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

## 프레임과 왼쪽 읽기 축

page는 넓은 캔버스를 채우지 않는다. **가운데 프레임 안에서 왼쪽에 붙은 읽기 축**을 따라 그림을 크게 보여 준다.

- **프레임.** `.d0-page` 안쪽 폭이 프레임이다(기본 1136px, 12열 기준). 프레임은 화면 가운데에 놓인다.
- **읽기 축.** 축은 프레임 **왼쪽**에 붙는다(기본 720px, 8열 상당). 섹션 제목과 모든 블록의 왼쪽 시작선은 항상 프레임 왼쪽이다. 1366·1440·1920px에서 h2·축 안 블록·`.d0-wide`·축 안 2열 첫 열의 왼쪽 x가 하나다.
  헤더·섹션의 직계 자식이 폭 상한을 받는다(정본 CSS). 블록마다 들여쓰기를 따로 두지 않는다.
- **오른쪽 여백.** 축 오른쪽(약 4열)은 기본 비어 있다. 빈 공간은 채울 공간이 아니다. 여백이 덩어리를 묶어 준다. 빈자리를 채우려고 그림 옆에 설명 문단·목록을 붙이지 않는다. 이 자리에 둘 수 있는 것은 선택 블록인 여백 주석(`.d0-margin`, 아래)뿐이다.

### 폭 단계 (`data-width`)

| 단계 | 축 | 글 폭 | 프레임 | 쓰는 문서(패턴 기본값) |
| --- | --- | --- | --- | --- |
| `narrow` | 640px | 640px | 1136px | 읽고 따라 하는 문서: guide·install-guide·faq |
| 기본(속성 없음) | 720px | 720px | 1136px | 일반 설명 문서: compare·flow·preview |
| `report` | 960px | 720px | 1280px | 표·차트·지표가 많은 문서: report·incident(장애 회고)·postmortem·launch-report·timeline |

- **고르는 법.** `<main class="d0-page" data-width="…">`에 주된 패턴의 기본값을 쓴다. 패턴이 섞이면 섹션 수와 첫 화면으로 주된 패턴 하나를 정한다. 한 문서 안에서 폭 단계를 섞지 않는다.
- **report의 두 폭.** 문단 글(리드 `p`, 요약 행, explanation·evidence·faq `dl`, 행 목록, checklist, 접기, closing)은 줄 길이 때문에 글 폭 720px(`--d0-measure`)에서 끊고,
  그림·표·차트·지표(`figure`, `table`, kpi-cards, step-columns, timeline, before-after, side-by-side, thumb-cards, 목업 데모)와 축 안 2열은 축 960px(`--d0-axis`)을 채운다. 둘 다 같은 왼쪽 시작선이다.
  축 960px에 놓는 글자 있는 SVG는 viewBox 폭 750으로 그린다(14 × 960 ÷ 750 = 17.9px, [diagram](diagram.md) 라벨 절).
- 폭 단계가 바꾸는 것은 프레임·축·글 폭뿐이다. 타이포·간격·첫 화면 예산은 같다.

### 넓은 구간 (`.d0-wide`)

넓은 구간은 축의 **오른쪽 끝만** 프레임 끝까지 늘린 블록이다. 왼쪽 시작선은 그대로이고 대칭으로 넓히지 않는다. 다음 블록은 다시 축으로 돌아온다. 넓은 구간은 섹션 안 블록이고 섹션 머리(h2)는 축에 둔다.
넓이가 실제로 필요할 때만 쓴다. **두 열이 필요하다고 넓은 구간이 필요한 것은 아니다.**

- **(a) 화면 A/B를 실제 크기로 나란히 비교.** 목업·데모 화면처럼 축 안 6/6 열(기본 336px)에서는 실제보다 작아 비교가 안 되는 화면 두 개.
- **(b) 그림 + 번호 주석 열.** 그림 지점과 번호로 직접 대응하는 주석·범례 열(pins·annotate·`d0-shot`·linked checklist).
- **(c) 5칸 이상 가로 순서 띠·긴 타임라인.** 축 폭에서는 칸·라벨이 하한을 못 지키는 가로 띠 하나. 예: 축 720px에 5열이면 칸이 144px라 열 그림과 `dd` 한 문장이 들어가지 않는다. 띠는 `.d0-wide` 바로 안에 한 블록으로 두고 `.d0-cols`로 나누지 않는다.
  글자 있는 SVG를 넓은 구간에 두면 라벨 게이트를 렌더 폭(기본 1136px, report 1280px)으로 다시 계산하고 viewBox 폭을 렌더 폭에 맞춰 다시 그린다([diagram](diagram.md) 라벨 절). 좁은 화면에서는 띠를 세로로 쌓거나(step-columns는 자동) 단계를 줄인다.
- **(d) 넓은 비교표·매트릭스.** 열이 많아 축 폭에서는 칸이 좁아지는 표.

한 열짜리 그림을 크게 보이려고 넓히지 않는다(그림은 축 폭으로 충분하다). 대등한 두 덩어리(완료 | 남은 것, 문제 | 해결)와 작은 썸네일·와이어 비교는 축 안 `.d0-cols`다. 가로 띠·표는 2열이 아니므로 분할선 수에 들지 않는다.

### 여백 주석 (`.d0-margin`) — 선택

축 오른쪽 여백에 놓는 짧은 보조 한 줄이다. **없어도 본문을 이해할 수 있는 정보만** 둔다.

- **쓰는 것.** 용어 풀이, 짧은 주의사항, 출처, 그림 번호와 연결된 보조 주석, 조건·예외 한 줄.
- **쓰지 않는 것.** 핵심 근거, 결론, 긴 설명, 카드 여러 개, "비어 있으니까" 넣은 정보. 섹션마다 만들 필요가 없다. 옆 빈자리를 채우려고 만들지 않는다.
- **마크업.** 본문 블록 하나와 주석 하나를 `div.d0-margined`로 묶는다. 묶음은 섹션의 직계 자식이다.
- **자리.** 1200px 이상(report는 1344px 이상)에서만 축 오른쪽 열(기본 368px, report 272px)에 본문 블록과 위 끝을 맞춰 놓이고, 그 아래에서는 본문 블록 바로 아래로 내려간다.
- 글자 14px grey-600(흰 바탕 대비 4.5:1 이상), 상자·배경·테두리 없음.
- 이름이 status rail `ol.d0-rail`([timeline](timeline.md))과 겹치지 않게 여백 주석은 `.d0-margin`이다.

```html
<div class="d0-margined">
  <figure class="d0-fig">…</figure>
  <aside class="d0-margin">대기열: 차례를 기다리는 요청이 쌓이는 줄이에요.</aside>
</div>
```

### 반응형

| 화면 | 프레임 | 축 | 넓은 구간 | 여백 주석 | 2열 |
| --- | --- | --- | --- | --- | --- |
| 1200px 이상 | 1136px(report 1280px), 가운데 | 프레임 왼쪽 | 오른쪽만 프레임 끝까지 | 축 오른쪽 열(report는 1344px부터) | 축 안 6/6, 넓은 구간 안 6/6·7/5 |
| 768~1199px | 가용 폭 | min(축, 가용 폭), 왼쪽 정렬 | 가용 프레임 전체 폭 | 본문 아래 | 축 안은 열마다 300px 이상일 때만, 넓은 구간 안은 960px 이상에서만 |
| 767px 이하 | 가용 폭 | 가용 폭 | 100% | 본문 아래 | 쌓기 |

- **2열 최소 폭.** 2열은 각 열이 300px 이상일 때만 유지하고 아니면 세로로 쌓는다. 축 안 2열은 `auto-fit`이 이를 맡는다(기본 720px 각 336px, report 960px 각 456px, narrow 640px은 각 296px이라 쌓인다).
- 페이지 패딩(640px 이하 `48px 16px 72px`), 모바일 라벨 규칙(`.d0-page` 한정 560px 이하 20 / 340px 이하 22, report는 760px 이하 18 / 560px 이하 27 / 340px 이하 30, [diagram](diagram.md)), 첫 화면 예산, 타이포·간격은 그대로다.

## 2열 (`.d0-cols`)

2열은 세 경우에만 쓴다. 그 밖은 1열이다.

| 경우 | 예 | 자리 | 분할 |
| --- | --- | --- | --- |
| (a) 동시 비교가 핵심 | A안 \| B안, 전 \| 후 | 축 안. 화면을 실제 크기로 견줄 때만 넓은 구간 | 6/6 |
| (b) 그림 지점과 번호로 직접 대응하는 주석·범례 열 | 그림 \| ①②③ 주석, 화면 \| 번호 범례 | 넓은 구간 | 7/5(그림/주석) 또는 6/6 |
| (c) 대등한 두 덩어리 | 완료 \| 남은 것, 문제 \| 해결, 주의 \| 할 일 | 축 안 | 6/6 |

- **1열로 두는 것.** "그림 | 그냥 설명 문단", "작은 그림 | 빈자리 채우는 목록", 짝수라서 반으로 나눈 한 목록. 설명(explanation)은 그림 아래에 둔다.
- **자리.** 기본은 축 안이다: 섹션의 직계 자식 `div.d0-cols`. 넓은 구간이 필요한 경우만 `<div class="d0-wide"><div class="d0-cols">…</div></div>`(또는 블록 자체에 `d0-wide d0-cols`)로 둔다.
- **분할선은 종류마다 문서에서 하나.** 축 안 2열은 6/6 하나다(`data-split`을 쓰지 않는다). 넓은 구간 안 2열은 12열 중 6/6(기본) 또는 7/5(`data-split="7-5"`, 그림/주석) 중 하나로 문서 전체를 맞춘다. 축 안 2열과 넓은 구간 2열은 따로 센다.
  넓은 구간 안 2열은 960px 이상에서만 2열이고 그 아래는 1열로 쌓인다. 축 안 2열은 열마다 300px 이상일 때만 2열이다. 열 사이는 48px이다.
- **글 열은 트랙 끝까지 쓴다.** 열 칸에 따로 폭 상한(em·px)을 두지 않는다. 트랙 자체가 좁다(축 안 6/6 열 336px, report 456px. 넓은 구간 6/6 열 544px, report 616px. 7/5의 5열 약 445px).
- 두 열에 그림을 하나씩 둘 때(전 | 후)는 같은 viewBox 크기로 그린다. 그러면 무대 위 끝·아래 끝과 figcaption 줄이 저절로 맞는다. 글자 있는 SVG는 열 폭으로 라벨을 다시 계산한다([diagram](diagram.md) 라벨 절).
- 블록 안 같은 크기 칸(side-by-side 옵션, kpi-cards 카드, thumb-cards, step-columns)은 블록 부품이다. 축 폭을 같은 몫으로 나누고 이 2열 규칙을 따르지 않는다.

```html
<section class="d0-section" data-pattern="report" aria-labelledby="sec-b">
  <header class="d0-section-head"><h2 id="sec-b">된 것과 남은 것</h2></header>
  <div class="d0-cols"> <!-- 대등한 두 덩어리: 축 안 6/6 -->
    <ul class="d0-rows">…</ul>
    <ul class="d0-rows">…</ul>
  </div>
  <dl class="d0-explain">…</dl>
</section>
```

## 섹션 뼈대

원칙이다(게이트가 아니다). 섹션은 **제목(h2) → 그림 → 해석 한 줄 → 필요할 때만 "왜" 한 줄** 순서로 읽힌다.

- 해석 한 줄은 figcaption이나 explanation `interpretation` 한 항목, "왜" 한 줄은 explanation `reason` 한 항목이다.
- 라벨 글 블록·표·목록은 이해에 필요한 만큼만 본 흐름에 둔다. 흐름을 끊는 세부(계산 과정, 전체 표, 긴 예외 목록)는 섹션 끝 `.d0-more` 접기로 보낸다.
- 페이지 끝에 "기억할 한 줄" 상자(`.d0-keep`)를 하나 둘 수 있다(선택).

## 접기 (`.d0-more`)와 기억할 한 줄 (`.d0-keep`)

- **`.d0-more`.** `details.d0-more > summary` + 내용. grey-50 면, radius 12, 패딩 16·20. summary는 14px/600 blue-dark로 무엇이 접혀 있는지 말한다(`단계별 시간 전체 보기`).
  섹션마다 최대 1개이고 섹션 끝에 둔다. 섹션의 핵심 답·결정·정본 숫자는 접지 않는다. 여러 선택 보조 항목을 목록으로 접는 것은 [accordion](accordion.md)이고, `.d0-more`는 본 흐름에서 빼낸 세부 한 덩어리다.
- **`.d0-keep`.** `aside.d0-keep` = 라벨(`.d0-keep__label`, 13px/600 blue-dark, 예 `기억할 한 줄`) + 문장 `p` 하나(18px/700 grey-900). blue-light 면, radius 16, 패딩 20·24.
  페이지당 0~1개, 마지막 섹션 안 끝(closing이 있으면 그 앞)에 둔다. 기억할 사실 한 문장이다. 독자에게 행동·결정을 요구하면 [closing](closing.md)이 맡고, 같은 문장을 둘에 쓰지 않는다. 같은 숫자 반복 셈(SKILL.md 원칙 8번)에 들어간다.
  면 단위 옅은 표면이라 진한 포인트 비율에서 빼고 장면 수로 센다(아래 색 절).

```html
<details class="d0-more">
  <summary>단계별 시간 전체 보기</summary>
  <table>…</table>
</details>

<aside class="d0-keep" aria-labelledby="keep-l">
  <span class="d0-keep__label" id="keep-l">기억할 한 줄</span>
  <p>큰 요청을 따로 세우면 작은 요청은 기다리지 않아요.</p>
</aside>
```

## 줄 길이 (정본)

본문 한 줄의 길이는 **폭 단계의 글 폭(`--d0-measure`)이 정한다**. 기본·narrow는 축 폭, report는 720px이다. 글 블록(리드 `p`, explanation·evidence·faq `dl`, 행 목록)은 글 폭이나 놓인 2열 열 폭을 그대로 쓰고, 그 안에서 따로 폭 상한을 두지 않는다. 글 블록마다 다른 상한을 두면 오른쪽 끝이 섹션마다 들쭉날쭉해진다.

- **폭 기준.** Pretendard 15px 본문에서 공백 포함 50자 연속 구간의 폭은 실측 482~529px다. 그래서 글 폭 720px(기본·report)은 한 줄 약 68~75자, narrow 640px은 약 60~66자, 넓은 구간 6/6 열(약 544px)은 약 51~56자, 축 안 6/6 열(336px)은 약 32~35자다.
- **좁히는 곳은 축이다.** `p`·`dd`나 글 블록에 `max-width`를 걸지 않는다(개행 규칙). 글이 주인공이라 줄을 더 짧게 읽혀야 하면 페이지 전체를 `data-width="narrow"`로 둔다.
- **한 줄짜리 글**(요약 행 값, 행 설명, checklist 결과 한 줄, checkpoint)은 축 한 줄 안에서 끝나게 쓴다. 넘치면 문장을 줄인다.
- **리드 `p`**(header 리드, 섹션 리드)는 컨테이너를 좁히지 않는다. 2문장 이상이고 데스크톱에서 2줄을 넘으면 문장 단위 개행(`.d0-sentence`)을 쓴다(아래 개행 절).
- `code`·`pre`·명령어 줄·[code-block](code-block.md)은 줄 길이 규칙 밖이다.

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
- page는 페이지당 0~1개다. 어두운 배경으로 바꾸지 않는다(라이트 온리). 덱 표지·섹션·마무리 장의 진한 면(`data-surface="dark"`)만 예외이고 Impact와는 다른 축이다([slide-deck.md](slide-deck.md) 진한 면 절).

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

**기본은 무대 없음이다.** 도식 `figure.d0-fig`는 흰 바탕에 바로 SVG를 두고 축의 왼쪽 정렬선을 따른다. `figcaption`은 그림 아래 13px grey-600이다.
**그림은 축 폭을 채운다.** SVG 렌더 폭은 놓인 자리(축, 무대 안쪽, 2열 열, `.d0-wide`) 폭의 100%가 기본이고, 축 폭에서 너무 커 보이는 단순 도식만 `data-fit="compact"`(75%, 가운데)로 둔다. 75% 아래로 줄이지 않는다.
글자 크기 하한은 viewBox 대비 렌더 배율로 검사한다([diagram.md](diagram.md) 라벨 절).
**무대를 쓰는 때:** 글자 없는 도식이 여백 없이 떠서 그림의 경계가 안 보일 때(흩어진 노드, 테두리 없는 선 그림), 목업·고스트 카드처럼 흰 면 요소에 받침 면이 필요할 때.
**무대 패딩 때문에 렌더 라벨이 하한(1280px 13px, 375·320px 11px) 아래로 내려가면 무대를 쓰지 않는다.** 글자 있는 도식(viewBox 560)은 375px에서 무대 안쪽 303px이라 라벨이 11px 아래로 줄므로 무대 없이 두고, 경계는 그림 안 선·면으로 만든다.

무대를 쓰면 패널 = `div.d0-fig__stage`(배경 grey-50, `--d0-radius-card`, 패딩 28px,
모바일 20px). `figcaption`은 패널 **밖** 아래에 13px grey-600으로 둔다. 테두리·그림자는 없다.
SVG는 패널 안에서 가운데 놓이고, 패널 자체는 축의 왼쪽 정렬선을 따른다. 선 굵기·라벨 규칙은 [diagram.md](diagram.md).
페이지의 핵심 도식 하나는 `data-stage="blue"`로 무대를 blue-light로 칠할 수 있다. 그 무대 위 회색 선·글자는 한 단계 진하게 바뀐다([diagram.md](diagram.md) 공용 CSS).
Impact 안에서는 무대를 두지 않는다.

```html
<!-- 기본: 무대 없음, 축 폭을 채운다 -->
<figure class="d0-fig">
  <svg viewBox="0 0 560 280" role="img" aria-labelledby="g1-t">…</svg>
  <figcaption>고친 파일에서 선을 따라간 검사만 다시 돌아요.</figcaption>
</figure>
<!-- 필요할 때만: 무대(글자 없는 그림) -->
<figure class="d0-fig" data-stage>
  <div class="d0-fig__stage"><svg viewBox="0 0 560 300" role="img" aria-labelledby="g2-t">…</svg></div>
  <figcaption>흩어진 화면 조각이 어디까지 한 그림인지 무대가 묶어 줘요.</figcaption>
</figure>
```

## 색 (정본)

Day0의 6:3:1(배경 · 텍스트 · 포인트)을 따른다. **회색만 남은 페이지는 실패다.** 이 절이 색 규칙의 정본이고 다른 파일은 여기를 가리킨다.

- **색 면적은 lint Warning이다.** 1280×800과 375×812 첫 화면에서 진한 포인트 채움이 **1% 미만**이면 "강조가 너무 약한지 확인", **1~15%**이면 정상, **15% 초과**이면 "포인트 색이 배경처럼 쓰이는지 확인" 경고를 낸다. 경계값 1%·15%는 정상이다.
  색 면적 때문에 출력을 실패시키지 않고, 게이트를 맞추려고 색 면적을 늘리지 않는다. 색은 상태·강조·구조가 있는 자리에만 둔다.
  - **측정 정의(정본).** 진한 포인트 = `blue`·`blue-dark`·`green`·`orange`·`red` 채움. HTML `background-color`와 SVG 도형 `fill`이 해당 색인 요소의 보이는 bbox 합 ÷ 뷰포트 면적(뷰포트로 자름, 이미 센 요소의 자손은 제외)으로 잰다.
    `stroke`·`border`만 해당 색인 요소는 세지 않는다. 진한 포인트는 옅은 면 안에 있어도 센다.
  - 내용 단위 옅은 채움과 **면 단위 옅은 표면**(blue-light 무대, `.d0-keep`, 덱 Impact 슬라이드, 썸네일 판)은 이 진한 포인트 경고 비율에서 뺀다.
    장면 수는 별도로 유지한다: page는 blue 무대 최대 1개와 기억할 한 줄 상자(`.d0-keep`) 최대 1개(Impact는 면이 없다), deck은 Impact 슬라이드 20~30%([composition.md](../composition.md)).
  - 덱의 **진한 면 장**(`data-surface="dark"`, 표지·섹션·마무리)도 면 단위 표면이라 진한 포인트 비율에서 빼고 장면 수(덱당 1~3장)로 관리한다. 대비표는 [slide-deck.md](slide-deck.md) 진한 면 절.
  - 회색만으로 된 도식·카드 묶음 금지는 유지한다. 의미 있는 blue 또는 의미색 표식 하나를 두되 경고 비율을 채우려고 뜻 없는 면을 칠하지 않는다.
- **Hard 유지.** 대비와 WCAG 2.2 AA, 의미색 글자 금지는 색 면적 Warning과 별개로 반드시 통과한다.
- **블루 단계.** `blue` = 강조 선·채움(후 막대, 닿는 노드, 진행 막대, 썸네일 합계 칸). `blue-dark` = 글자·번호, 흰 글자 바탕(버튼, 고른 탭, 흐름 줄의 현재 단계).
  `blue-light` = 옅은 면(썸네일 판, 핵심 도식 하나의 무대 `data-stage="blue"`, 기억할 한 줄 `.d0-keep`, 덱 Impact 슬라이드, 선택 카드, 표 머리 행·합계 행).
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

- 리드·설명 문단은 부모 폭을 그대로 쓴다. `p`에 컨테이너보다 좁은 `max-width`를 걸지 않는다. 줄이 길면 위 줄 길이 절대로 페이지 전체를 `data-width="narrow"`로 둔다.
- 문장 단위 개행(선택): 리드·설명이 2문장 이상이고 데스크톱 폭에서 2줄을 넘기거나 문장마다 역할이 다르면
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
<main class="d0-page"> <!-- 폭 단계: data-width="narrow" | 없음(기본) | "report", 주된 패턴의 기본값 -->
  <!-- header(h1 → 히어로 → 요약 행) → section(독자 질문마다 하나, data-pattern) -->
  <section class="d0-section" data-pattern="preview" aria-labelledby="sec-a">
    <header class="d0-section-head"><h2 id="sec-a">파일은 이렇게 생겼어요</h2></header>
    <!-- 무대 위 그림 하나 + 그림 설명 한 줄 -->
  </section>
  <section class="d0-section" aria-labelledby="sec-b">
    <header class="d0-section-head"><h2 id="sec-b">전과 후는 이렇게 달라요</h2></header>
    <div class="d0-cols"><!-- 전 그림 --><!-- 후 그림 --></div> <!-- 2열은 축 안 6/6. 넓이가 필요할 때만 .d0-wide -->
    <!-- 해석 한 줄 → 다시 축 -->
  </section>
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

/* 본문 축: 가운데 프레임 안에서 왼쪽에 붙은 읽기 축. 폭 단계(data-width) 기본 축 720/프레임 1136, narrow 640/1136, report 960/1280(글은 720) */
.d0-page { --d0-frame: 1136px; --d0-axis: 720px; --d0-measure: 720px; max-width: calc(var(--d0-frame) + 64px); margin: 0 auto; padding: 64px 32px 96px; }
.d0-page[data-width="narrow"] { --d0-axis: 640px; --d0-measure: 640px; }
.d0-page[data-width="report"] { --d0-frame: 1280px; --d0-axis: 960px; }
/* 블록은 모두 프레임 왼쪽에서 시작한다. 글은 --d0-measure, 그림·표·지표·축 안 2열은 --d0-axis까지. 넓은 구간과 여백 주석 묶음만 예외 */
.d0-page :is(.d0-header, .d0-section, .d0-margined) > :not(.d0-wide, .d0-margined, .d0-margin) { max-width: var(--d0-measure); }
.d0-page :is(.d0-header, .d0-section, .d0-margined) > :is(figure, table, .d0-cols, .d0-kpis, .d0-steps, .d0-timeline, .d0-ba, .d0-sbs, .d0-thumbs, .d0-demos):not(.d0-wide) { max-width: var(--d0-axis); }
/* 넓은 구간: 왼쪽 시작선은 그대로 두고 오른쪽만 프레임 끝까지 */
.d0-wide { width: 100%; max-width: none; }
/* 그림은 축 폭을 채운다(75~100%). 글자 하한은 렌더 배율로 검사 */
.d0-fig svg { width: 100%; height: auto; }
.d0-fig[data-fit="compact"] svg { width: 75%; margin-inline: auto; }
/* 2열: 축 안은 6/6(각 열 300px 이상일 때만, 아니면 쌓는다). 넓은 구간 안은 12열 6/6 또는 7/5. 축 안과 넓은 구간이 각각 분할선 하나 */
.d0-cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 24px 48px; align-items: start; }
.d0-cols > * { min-width: 0; }
:where(.d0-wide) .d0-cols, .d0-cols:where(.d0-wide) { grid-template-columns: minmax(0, 1fr); }
@media (min-width: 960px) {
  :where(.d0-wide) .d0-cols, .d0-cols:where(.d0-wide) { grid-template-columns: repeat(12, minmax(0, 1fr)); }
  :where(.d0-wide) .d0-cols > *, .d0-cols:where(.d0-wide) > * { grid-column: span 6; }
  :where(.d0-wide) .d0-cols[data-split="7-5"] > :first-child, .d0-cols:where(.d0-wide)[data-split="7-5"] > :first-child { grid-column: span 7; }
  :where(.d0-wide) .d0-cols[data-split="7-5"] > :last-child, .d0-cols:where(.d0-wide)[data-split="7-5"] > :last-child { grid-column: span 5; }
}
/* 여백 주석(선택): 본문 블록 하나 + aside.d0-margin. 1200px 이상(report는 1344px 이상)에서만 축 오른쪽 열, 그 아래는 본문 바로 아래 */
.d0-margined { display: grid; gap: 12px 48px; align-items: start; }
.d0-margined > * { min-width: 0; }
.d0-margin { max-width: var(--d0-measure); color: var(--d0-grey-600); font-size: 14px; line-height: 1.6; }
@media (min-width: 1200px) {
  .d0-page:not([data-width="report"]) .d0-margined { grid-template-columns: minmax(0, var(--d0-axis)) minmax(0, 1fr); }
}
@media (min-width: 1344px) {
  .d0-page[data-width="report"] .d0-margined { grid-template-columns: minmax(0, var(--d0-axis)) minmax(0, 1fr); }
}
/* 접기와 기억할 한 줄 */
.d0-more { border-radius: 12px; background: var(--d0-grey-50); padding: 16px 20px; }
.d0-more > summary { cursor: pointer; font-size: 14px; font-weight: 600; color: var(--d0-blue-dark); }
.d0-more[open] > summary { margin-bottom: 12px; }
.d0-keep { border-radius: 16px; background: var(--d0-blue-light); padding: 20px 24px; display: grid; gap: 6px; }
.d0-keep > .d0-keep__label { font-size: 13px; font-weight: 600; color: var(--d0-blue-dark); }
.d0-keep > p { font-size: 18px; font-weight: 700; color: var(--d0-grey-900); }

/* 섹션: 구분선 위아래 32px씩 → 섹션 사이 64px */
.d0-section { display: grid; gap: 24px; align-content: start; min-width: 0; padding-block: 32px; border-top: 1px solid var(--d0-grey-100); }
.d0-section:last-child { padding-bottom: 0; }
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
  .d0-fig[data-fit="compact"] svg { width: 100%; } /* 모바일: compact도 축 폭을 채워 라벨 11px 이상 */
  h1 { font-size: 26px; }
  h2 { font-size: 18px; }
  .d0-section { padding-block: 24px; }
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

- 다크 팔레트·`prefers-color-scheme: dark` 분기 추가, `body` 배경 생략. 덱 표지·섹션·마무리의 `data-surface="dark"`는 다크 테마가 아니라 장면 전환 면이라 예외다.
- `p`나 리드, 글 블록(explanation·evidence·faq `dl`, 열 칸)에 축보다 좁은 `max-width`·`width`·`ch`. 줄이 길면 페이지 전체를 `data-width="narrow"`로 둔다.
- Pretendard jsDelivr 링크 외 외부 폰트·CSS·JS 링크, 넘긴 결과물 HTML에 남은 외부 폰트 요청(도구가 없을 때만 예외), `outline: none` 단독 사용.
- 글자에 `--d0-blue`·`--d0-grey-500` 이하·시맨틱 전경색 사용(흰 바탕 대비 4.5:1 미달). 글자는 `--d0-blue-dark`, `--d0-grey-600` 이상.
  예외는 18.66px/700 이상 큰 글자(3:1)뿐이다.
- tokens.css에 없는 `--d0-*` 변수 만들기(표면 `#fff`와 정본 CSS의 레이아웃 변수 `--d0-frame`·`--d0-axis`·`--d0-measure`만 예외). 반투명 막은 `color-mix(in srgb, var(--d0-grey-900) 32%, transparent)`.
- 배지 높이를 행 높이에 맡기기(늘어난 배지), 섹션마다 카드 상자, 섹션 안 블록마다 테두리, 섹션·행 사이 `grey-200` 이상 진한 구분선.
  예외는 블록 안 한 줄 표식인 closing 문장 아래 구분선(page `.d0-closing__meta`, deck `.d0-slide__meta`)과 checkpoint 뒤 선이다. 이 둘은 1px grey-200이고 섹션·행 구분선으로 세지 않는다.
- 회색만 있는 도식·카드, 의미색 글자, 의미색 3가지 이상, 카드·행 하나에 배지 2개 이상, 배지 톤 4종류 이상, 혼자 뜻을 전하는 orange 선·점.
- 섹션을 나란히 두기(섹션은 축을 따라 위아래로 쌓는다), 세 경우(동시 비교·번호 주석·대등한 두 덩어리) 밖의 2열, 대등한 두 덩어리를 `.d0-wide`에 두기, 축 안 2열에 `data-split`, 넓은 구간 2열에 6/6과 7/5 섞기, 섹션마다 다른 분할선, 2열 열 칸에 따로 건 폭 상한, 열이 300px 아래인데 나란히 두기.
- 블록을 프레임 가운데에 두기, `.d0-wide`를 왼쪽으로(대칭으로) 넓히기, 한 문서에 폭 단계 섞기, report에서 문단 글을 720px 넘게 늘리기.
- 여백 주석에 핵심 근거·결론·긴 설명·카드 여러 개 두기, 빈자리를 채우려고 여백 주석 만들기, 섹션마다 여백 주석, 묶음 하나에 주석 둘 이상.
- 빈자리를 채우려고 그림 옆에 설명 문단·목록 붙이기, 그림을 축 폭의 75% 아래로 줄이기, 한 열짜리 그림을 `.d0-wide`로 넓히기(넓은 구간 절의 네 경우만 예외).
- 그라디언트·글래스·두꺼운 그림자·장식 3D, 무대 패널에 테두리나 그림자.
- 기본값으로 두른 무대(경계가 이미 보이는 그림에 회색 패널), 섹션마다 회색 무대를 둘러 모든 그림을 같은 모양으로 만들기, 무대 패딩 때문에 라벨이 하한 아래로 내려가는 글자 있는 도식에 무대 두기.
- Impact를 쓰려고 섹션 더하기.
- `.d0-keep` 2개 이상, 행동·결정 요청을 `.d0-keep`에 쓰기(closing이 맡는다), 섹션의 핵심 답·결정·정본 숫자를 `.d0-more`에 접기.
- page Impact 2개 이상, Impact 안 카드·목록·배지·무대·editorial·숫자 둘 이상, page Impact에 배경 면·풀블리드 띠 칠하기, 어두운 Impact 면.
- CSS만으로 초기 숨김(`opacity: 0`을 `data-motion` 밖에 걸기), 스크롤마다 반복되는 모션, reduced-motion 무시.
