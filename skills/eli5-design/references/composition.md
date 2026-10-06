# composition — 구도

프리셋은 **무엇을** 말할지, 블록은 **무엇으로** 그릴지 정한다. 구도는 그 사이에서 한 화면을 **어떻게 놓을지** 정한다.
모든 섹션이 `제목 → 회색 무대 → SVG → 캡션`으로 같은 화면처럼 보이면 장면이 바뀌지 않는다. 섹션마다 구도를 고르고, 이웃한 섹션과 다르게 놓는다.

## 세 축

구도·강조·도식 장르는 서로 다른 축이다. 하나를 바꿔도 나머지는 그대로다.

| 축 | 속성 | 다는 곳 | 정본 |
| --- | --- | --- | --- |
| 구도(배치) | `data-composition="hero\|spotlight\|split\|sequence\|canvas\|evidence\|summary"` | page의 `main > section`(`.d0-split` 안 섹션 포함), deck의 `.d0-slide` | 이 파일 |
| 강조(음량) | `data-emphasis="quiet\|impact"`, 생략 = normal | 같은 곳 | 이 파일, CSS는 [shell.md](blocks/shell.md) |
| 도식 장르 | `figure.d0-fig[data-genre="structural\|narrative\|editorial"]`, 생략 = structural | 그림 `figure` | [diagram.md](blocks/diagram.md) |

```html
<section class="d0-section" data-composition="sequence" aria-labelledby="sec-b">
  <header class="d0-section-head"><h2 id="sec-b">지금 세 번째 단계예요</h2></header>
  <figure class="d0-fig" data-genre="narrative">…</figure>
</section>
```

**구도 다양화는 섹션을 늘리지 않는다.** 섹션 수는 대개 3개, 최대 4개 그대로 두고, Editorial·Impact는 기존 섹션 하나를 **대체**할 때만 쓴다.
기본 타이포·간격(h1 32 / h2 20 / 본문 15, 섹션 사이 64, 블록 사이 24, 컨테이너 1200)은 바꾸지 않는다. 크게 쓰는 것은 Impact·Spotlight 장면뿐이다.

`data-composition`은 선택 표시다. 스타일을 바꾸지 않고, 리듬 규칙(같은 구도 연속 금지)을 검토하는 이름표다. 배치는 고른 블록과 레이아웃(`.d0-split`·`.d0-cols`·`data-layout="side"`)이 만든다.

## 구도 7종

비율은 섹션 콘텐츠 폭(page 1136px, deck 슬라이드 폭) 기준이다. 그림 = 도식·목업·화면, 글 = 제목 밖 문단·목록.

### Hero — 결론 하나

- **언제.** 결론 숫자 하나, 주장 한 문장, 표지. 독자가 이것 하나만 기억하면 되는 장면.
- **비율.** 숫자·문장 하나가 주인공, 나머지는 여백. 그림은 없거나 120px 이하 객체 하나(editorial).
- **골격.**
  ```
  ┌──────────────────────────────┐
  │ 라벨                          │
  │ 58건            ← 아주 크게   │
  │ 한 줄 뜻                      │
  └──────────────────────────────┘
  ```
- **블록.** [hero.md](blocks/hero.md), Impact 띠([shell.md](blocks/shell.md)), editorial 도식.
- **page.** header(h1 → 히어로 → 요약 행)가 첫 Hero다. 본문에서는 기존 섹션 하나를 Impact 띠(문장 32px 또는 숫자 64px)로 바꿀 때만 쓴다.
- **deck.** 표지(`cover`), 주장(`assertion`), 큰 숫자(`stat`). 주장 슬라이드는 Impact가 기본이다.

### Spotlight — 화면 한 곳

- **언제.** 실제 화면에서 "여기를 보세요"가 할 말일 때(어디를 누르나, 무엇이 바뀌었나).
- **비율.** 화면 최대 560px + 바로 옆 주석 열(220~300px). 화면 바깥 크롬은 최소.
- **골격.**
  ```
  ┌──────────────────────┬────────┐
  │ 화면 (dim)  ┌──┐     │ ① 주석 │
  │             │①│ spot │ ② 주석 │
  │             └──┘     │        │
  └──────────────────────┴────────┘
  ```
- **블록.** `figure.d0-shot`([mockup-frame.md](blocks/mockup-frame.md) Screenshot spotlight), pins 변형([diagram.md](blocks/diagram.md) (g)).
- **page.** 900px 이상 화면 | 주석 2열, 그 아래 화면 위·주석 아래.
- **deck.** `data-kind="screenshot"`. 슬라이드 하나에 화면 하나, spot 1~3개.

### Split — 그림 | 요점

- **언제.** 그림 하나에 요점 2~3개를 붙일 때, 둘을 나란히 비교할 때.
- **비율.** 그림 6 : 글 4(또는 7 : 5). 비교면 1 : 1.
- **골격.**
  ```
  ┌──────────────────┬─────────────┐
  │ 그림              │ 요점 1      │
  │                  │ 요점 2      │
  └──────────────────┴─────────────┘
  ```
- **블록.** `data-layout="side"` 도식, `.d0-cols`, `.d0-split`, [side-by-side.md](blocks/side-by-side.md).
- **page.** 960px 이상 2열, 그 아래 1열.
- **deck.** `data-kind` 생략(기본 근거 슬라이드).

### Sequence — 순서와 진행

- **언제.** 단계, 시간, 경위. 왼쪽에서 오른쪽(위에서 아래)으로 읽히는 것이 뜻일 때.
- **비율.** 가로 띠 그림, 높이는 낮게(폭의 1/4 이하). 기본은 360px이고, 가로로 긴 타임라인·단계 줄만 최대 720px까지 넓힌다. 글은 그림 아래 짧게.
- **골격.**
  ```
  ●━━━━●━━━━◉ · · · ○ · · · ○
  지난   지난  지금    남음    남음
  ```
- **블록.** narrative 도식, steps (e), [timeline.md](blocks/timeline.md), [step-columns.md](blocks/step-columns.md), [flow-line.md](blocks/flow-line.md).
- **page.** 375px에서는 세로로 돌리거나 단계를 줄인다.
- **deck.** 기본 근거 슬라이드나 `breakdown`. 슬라이드를 넘길 때마다 현재 위치가 한 칸씩 가도 된다.

### Canvas — 큰 그림 하나

- **언제.** 구조·연결·화면 골격처럼 전체 모양이 할 말일 때.
- **비율.** 그림(360px, wide 400px 상한) + 옆 범례·주석 열. 그림을 키워 폭을 채우지 않는다.
- **골격.**
  ```
  ┌──────────────────────────────┐
  │ 도식 (≤400px)   │ 범례·주석    │
  └──────────────────────────────┘
  캡션 한 줄
  ```
- **블록.** structural 도식(graph·wireframe·pins, `data-size="wide"`).
- **page.** 폭은 pins(글자 없는 SVG + HTML 범례), `data-layout="side"`, `.d0-split` 2열로 채운다. 글자 없는 SVG·와이어프레임도 400px에서 멈춘다.
- **deck.** `data-kind="breakdown"`(전체 → 구성 요소).

### Evidence — 주장 + 근거

- **언제.** 제목이 결론 문장이고, 그 아래 차트 하나가 증거일 때.
- **비율.** 제목(결론 문장) → 차트 60~70% → 해석 한 줄.
- **골격.**
  ```
  결론 문장 (제목)
  ┌──────────────────────────────┐
  │ 차트                          │
  └──────────────────────────────┘
  해석 한 줄
  ```
- **블록.** bars (b), 비율 막대, [kpi-cards.md](blocks/kpi-cards.md) 막대 변형.
- **page.** 섹션 h2를 결론 문장으로 쓴다("어디서 줄었나"가 아니라 "내보내기 대기가 절반 아래로 줄었어요").
- **deck.** `data-kind="evidence"`.

### Summary — 정리와 다음 행동

- **언제.** 마무리. 결정, 할 일, 주의, 남은 질문.
- **비율.** 목록이 주인공, 그림 없음 허용. 행 사이 여백으로 읽힌다.
- **골격.**
  ```
  제목
  ─ 행 1 ─────────────────────────
  ─ 행 2 ─────────────────────────
  마무리 한 줄
  ```
- **블록.** [diff-rows.md](blocks/diff-rows.md), [checklist.md](blocks/checklist.md), [accordion.md](blocks/accordion.md).
- **page.** 보통 마지막 섹션이고 Quiet와 잘 맞는다.
- **deck.** `data-kind="summary"`.

## 리듬

- **같은 구도를 연속으로 두지 않는다.** page는 header를 Hero로 세고 본문 섹션을 차례로 본다(`.d0-split`의 두 섹션은 한 장면으로 센다). deck은 슬라이드 순서로 본다.
- **밀도를 교차한다.** 저 → 중 → 고 → 저. 같은 밀도가 셋 이어지지 않는다.
  - 저: 요소 1~2개(숫자 하나, 문장 하나). Hero, Impact, Summary.
  - 중: 그림 하나 + 요점 2~3개. Split, Evidence, Sequence.
  - 고: 그림 + 주석·범례 4~6개, 목업. Canvas, Spotlight.
- 섹션이 3개면 header(저) → 중 → 고 → 저, 2개면 header(저) → 고 → 저가 기본이다.

## 강조

### 강조 순서

크기 → 위치 → 여백 → 무게 → 색. 앞 수단으로 충분하면 뒤 수단을 더하지 않는다.

- **크기.** 가장 중요한 것을 가장 크게. **큰 숫자는 색이 아니라 크기로 중요하게 만든다**(기본 grey-900).
- **위치.** 첫 화면, 왼쪽 위, 섹션 첫 줄.
- **여백.** 주변을 비워 혼자 서게 한다.
- **무게.** 600~700 굵기. 그 밖은 400.
- **색.** 마지막 수단이다. blue 계열 진한 포인트는 장면마다 강조 묶음 하나에만. 파랑 하나가 모든 강조를 맡지 않게 한다.

### 강조 3단계 (`data-emphasis`)

| 단계 | 속성 | 모양 | 언제 |
| --- | --- | --- | --- |
| Quiet | `quiet` | 진한 포인트 채움 없음(완료 체크·의미색 점만), h2 한 단계 작게(18px), 본문·목록 글자 grey-700 | 참고, 부록, 정리 목록, deck 목차 |
| Normal | 생략 | 흰 바탕 + 기존 규칙 | 대부분의 섹션 |
| Impact | `impact` | blue-light 풀블리드 면 + 초대형 글자. 글자 grey-900, 강조 숫자 blue-dark | 주장 한 문장, 결론 숫자 하나 |

- **Impact 안에는 하나만** 둔다: page는 문장 하나 또는 숫자 하나(+ 짧은 라벨)이고, editorial 도식을 넣지 않는다. deck은 그림 하나도 된다. 카드·목록·배지·둥근 박스 금지.
- **page**는 Impact 띠를 선택으로 페이지당 0~1개 둔다(기존 본문 섹션 하나가 화면 폭 끝까지 칠한 띠가 된다. 섹션을 더하지 않는다). 띠 안 패딩 48px, 이웃 내용까지 합계 64px로 일반 섹션 간격과 같다. header 히어로와 같은 숫자를 띠에서 되풀이하지 않는다.
- **deck**은 Impact 슬라이드를 전체의 20~30%로 둔다(10장이면 2~3장). 연속 두 장을 Impact로 두지 않는다.
- 어두운 배경은 쓰지 않는다(Day0 라이트 온리). Impact의 무게는 면의 넓이와 글자 크기에서 온다.
- CSS와 대비는 [shell.md](blocks/shell.md) 강조 절이 정본이다.

### 색 비율과 옅은 표면

- 색 비율 규칙(진한 포인트 1280 1.2% 이상, 375 0.8% 이상, 전체 3~15%)은 **진한 포인트**(blue·blue-dark·의미색 채움)를 재는 규칙이다.
- **면 단위 옅은 표면**(blue-light 무대, Impact 띠, 썸네일 판)은 비율 계산에서 빼고 **장면 수**로 관리한다: page는 Impact 띠 1개 + blue 무대 1개까지, deck은 Impact 20~30%.
- 정본은 [shell.md](blocks/shell.md) 색 절이다.

## 무대와 상자

- **회색 무대는 기본 없음.** 도식은 흰 바탕에 바로 놓고 페이지 왼쪽 정렬선을 따른다.
  **무대를 쓰는 때:** 도식이 여백 없이 떠서 그림의 경계가 안 보일 때(흩어진 노드, 테두리 없는 선 그림), 목업·고스트 카드처럼 흰 면 요소에 받침 면이 필요할 때, 나란히 둔 두 그림의 높이를 맞출 때(`.d0-split[data-align="stage"]`).
- 무대 없는 그림이 폭의 절반만 쓰고 옆을 비우면 안 된다. **그림을 키워 채우지 않는다.** `.d0-split` 2열(나란히 두던 구성을 우선 유지), `data-layout="side"`, `.d0-cols` 한 열, 그림 옆 짧은 주석·범례 열(900px 이상), pins 중 하나로 채운다.
  SVG는 글자가 없어도 기본 360px, wide 400px에서 멈추고, 전체 폭은 가로로 긴 타임라인·단계 줄만 최대 720px다.
- **카드·둥근 박스를 기본값으로 쓰지 않는다.** 묶음은 여백·정렬·행 구분선으로 만든다. 카드는 하나씩 눌러 보거나 나란히 견주는 독립 대상(썸네일, 시안)일 때만 쓴다.

## 프리셋별 권장 구도 순서

page 기준 예시다. 첫 칸은 header다. 본문 섹션은 3개(최대 4개)를 넘기지 않고, Impact 띠·editorial은 기존 섹션을 대체한다. 나란히 둘 수 있는 두 장면은 `.d0-split` 2열로 묶는다. 독자 질문에 필요 없는 장면은 뺀다.

| 프리셋 | 권장 순서 |
| --- | --- |
| compare | Hero(결정 질문) → Split(A \| B, 전/후) → Spotlight(차이 한 곳) → Summary(결정·할 일) |
| flow | Hero → Sequence(narrative 단계) → Canvas(구조) → Summary(막히면) |
| preview | Hero → Canvas(결과물 전체, pins) → Spotlight(핵심 화면 한 곳) → Summary |
| report | Hero(결론 수치) → Evidence(차트 + 해석) → Hero(Impact 띠, 주장 한 문장) → Summary(할 일, Quiet) |
| guide | Hero → Spotlight(어디를 누르나) → Sequence(단계) → Summary(막히면) |
| timeline | Hero → Sequence(narrative: 지난 것·지금·남은 것) → Evidence(변경 규모) → Summary |
| incident | Hero(영향 수치) → Sequence(경위) → Canvas(원인 그래프) → Summary(재발 방지) |
| faq | Hero → Canvas(용어 핀) → Split(비유 그림 \| 풀이) → Summary(질문 목록) |

deck은 같은 순서를 슬라이드로 늘리되 cover → toc 뒤에 시작하고, 리듬·Impact 비율 규칙을 그대로 따른다.

## 금지

- 모든 섹션이 같은 구도(제목 → 무대 → SVG → 캡션), 같은 구도 연속, 같은 밀도 셋 연속.
- 구도를 바꾸려고 섹션 더하기, 그림을 키워 폭 채우기, 2열로 두던 구성을 1열로 풀어 길게 늘이기.
- 색으로만 강조하기, 큰 숫자를 전부 blue로 칠하기, 장면마다 blue 강조 묶음 둘 이상.
- page에 Impact 띠 2개 이상, deck Impact 30% 초과, Impact 안 카드·목록·둘 이상의 숫자, 어두운 Impact 면.
- 기본값으로 두른 회색 무대·카드·둥근 박스.
