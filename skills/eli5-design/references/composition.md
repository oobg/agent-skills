# composition — 구도

구도는 용어 계층의 Layout이다. Pattern은 어떻게 설명할지, Block은 무엇으로 표현할지, Layout은 어디에 놓을지 정한다. 구도는 그 사이에서 한 화면을 **어떻게 놓을지** 정한다.
page의 축과 섹션 뼈대(제목 → 그림 → 해석 한 줄 → 필요할 때 "왜" 한 줄, [shell.md](blocks/shell.md))는 고정이다. 구도는 그 뼈대 안에서 **그림의 종류·크기·강조**로 장면을 바꾼다. 모든 그림이 같은 회색 무대에 같은 모양이면 장면이 바뀌지 않으므로, 이웃한 섹션과 다른 구도를 고른다. 축의 시작선과 2열 분할선은 구도를 바꾸려고 옮기지 않는다.

## 세 축

구도·강조·도식 장르는 서로 다른 축이다. 하나를 바꿔도 나머지는 그대로다.

| 축 | 속성 | 다는 곳 | 정본 |
| --- | --- | --- | --- |
| 구도(배치) | `data-composition="hero\|spotlight\|split\|sequence\|canvas\|evidence\|summary"` | page의 `main > section`, deck의 `.d0-slide` | 이 파일 |
| 강조(음량) | `data-emphasis="quiet\|impact"`, 생략 = normal | 같은 곳 | 이 파일, CSS는 [shell.md](blocks/shell.md) |
| 도식 장르 | `figure.d0-fig[data-genre="structural\|narrative\|editorial"]`, 생략 = structural | 그림 `figure` | [diagram.md](blocks/diagram.md) |

```html
<section class="d0-section" data-composition="sequence" aria-labelledby="sec-b">
  <header class="d0-section-head"><h2 id="sec-b">지금 세 번째 단계예요</h2></header>
  <figure class="d0-fig" data-genre="narrative">…</figure>
</section>
```

**구도 다양화는 섹션을 늘리지 않는다.** 섹션 수는 독자 질문이 정한 그대로 두고(SKILL.md 원칙 4번), Editorial·Impact는 기존 섹션 하나를 **대체**할 때만 쓴다.
기본 타이포·간격(h1 32 / h2 20 / 본문 15, 섹션 사이 64, 블록 사이 24, 본문 축 720)은 바꾸지 않는다. 크게 쓰는 것은 Impact·Spotlight 장면뿐이다.

`data-composition`은 선택 표시다. 스타일을 바꾸지 않고, 리듬 규칙(같은 구도 연속 금지)을 검토하는 이름표다. 배치는 고른 블록과 레이아웃(본문 축, 넓은 구간 `.d0-wide`, 2열 `.d0-cols`)이 만든다.

## 구도 7종

비율은 섹션 콘텐츠 폭(page 본문 축 720px, 2열이면 `.d0-wide` 구간, deck 슬라이드 폭) 기준이다. 그림 = 도식·목업·화면, 글 = 제목 밖 문단·목록.

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
- **블록.** [hero.md](blocks/hero.md), Impact([shell.md](blocks/shell.md)), editorial 도식.
- **page.** header(h1 → 히어로 → 요약 행)가 첫 Hero다. 본문에서는 기존 섹션 하나를 Impact(문장 32px 또는 숫자 64px)로 바꿀 때만 쓴다.
- **deck.** 표지(`cover`)는 주 패턴 대표 도식의 모양에 맞춰 contrast·bottom·side·center·map 배치를 고른다([slide-deck](blocks/slide-deck.md)). 주장(`assertion`)·큰 숫자(`stat`)는 하나를 크게 두며 주장 슬라이드는 Impact가 기본이다.

### Spotlight — 화면 한 곳

- **언제.** 실제 화면에서 "여기를 보세요"가 할 말일 때(어디를 누르나, 무엇이 바뀌었나).
- **비율.** page는 화면이 축 폭을 채우고 번호 주석은 아래에 둔다. 주석을 옆에 두려면 `.d0-wide` 안 화면 7 | 주석 5다. deck은 [slide-deck](blocks/slide-deck.md)의 덱 screenshot 격자를 따른다(화면 열이 몸 높이를 채우고 주석은 오른쪽 레일). 화면 바깥 크롬은 최소.
- **골격.**
  ```
  ┌──────────────────────┬────────┐
  │ 화면 (dim)  ┌──┐     │ ① 주석 │
  │             │①│ spot │ ② 주석 │
  │             └──┘     │        │
  └──────────────────────┴────────┘
  ```
- **블록.** `figure.d0-shot`([mockup-frame.md](blocks/mockup-frame.md) Screenshot spotlight), pins 변형([diagram.md](blocks/diagram.md) (g)).
- **page.** 축에서는 화면 위·주석 아래. `.d0-wide` 안에서만 960px 이상 화면 | 주석 2열이다.
- **deck.** `data-kind="screenshot"`. 슬라이드 하나에 화면 하나, spot 1~3개.

### Split — 그림 | 요점

- **언제.** 둘을 동시에 비교할 때(A안 | B안, 전 | 후), 대등한 두 덩어리(완료 | 남은 것, 문제 | 해결)를 견줄 때. 그림 하나에 요점을 붙이는 것은 Split이 아니라 그림 아래 explanation이다.
- **비율.** 12열 중 6 : 6(비교·대등한 덩어리). 그림 지점과 번호로 대응하는 주석 열이면 7 : 5. 문서 전체에서 분할선은 하나다.
- **골격.**
  ```
  ┌──────────────────┬─────────────┐
  │ 그림              │ 요점 1      │
  │                  │ 요점 2      │
  └──────────────────┴─────────────┘
  ```
- **블록.** `.d0-wide` 안 `.d0-cols`, [side-by-side.md](blocks/side-by-side.md), [before-after.md](blocks/before-after.md).
- **page.** `.d0-wide` 구간에서 960px 이상 2열, 그 아래 1열. 섹션 머리는 축에 두고 2열 다음 블록은 축으로 돌아온다.
- **deck.** `data-kind` 생략(기본 근거 슬라이드).
- **비대칭(deck).** 제목을 한쪽 좁은 열에 작게, 핵심 그림을 반대편 넓은 열에 크게 두는 Split의 덱 변형이다(`.d0-slide[data-layout="asym"]`, 반대형 `data-flip`, [slide-deck](blocks/slide-deck.md)). 그림이 실제로 그 장의 핵심일 때만 쓰고, 덱에 1~3장이다. 모든 장을 좌우 번갈아 놓지 않는다.

### Sequence — 순서와 진행

- **언제.** 단계, 시간, 경위. 왼쪽에서 오른쪽(위에서 아래)으로 읽히는 것이 뜻일 때.
- **비율.** 축 폭을 채우는 가로 띠 그림, 높이는 낮게(폭의 1/4 이하). 점·단계가 3~4개뿐이면 `data-fit="compact"`(75%). 글은 그림 아래 짧게.
- **골격.**
  ```
  ●━━━━●━━━━◉ · · · ○ · · · ○
  지난   지난  지금    남음    남음
  ```
- **블록.** narrative 도식, steps (e), [timeline.md](blocks/timeline.md), [step-columns.md](blocks/step-columns.md), [flow-line.md](blocks/flow-line.md).
- **page.** 5칸 이상 단계 줄이나 점이 많은 긴 타임라인처럼 축 폭에서 칸·라벨이 하한을 못 지키는 띠는 `.d0-wide` 한 블록으로 넓힌다(2열 아님, [shell.md](blocks/shell.md) 넓은 구간 (b)). 375px에서는 세로로 돌리거나 단계를 줄인다.
- **deck.** 기본 근거 슬라이드나 `breakdown`. 슬라이드를 넘길 때마다 현재 위치가 한 칸씩 가도 된다.

### Canvas — 큰 그림 하나

- **언제.** 구조·연결·화면 골격처럼 전체 모양이 할 말일 때.
- **비율.** 그림이 축 폭을 채운다(75~100%). 범례·주석은 그림 아래, 번호로 대응하는 범례 열이면 `.d0-wide` 안 7 : 5.
- **골격.**
  ```
  ┌──────────────────────────────┐
  │ 도식 (축 폭)                   │
  └──────────────────────────────┘
  캡션 한 줄 · 범례
  ```
- **블록.** structural 도식(graph·wireframe·pins).
- **page.** 축 폭 그림 하나가 주인공이다. 옆에 남는 폭은 채우지 않고, 범례는 그림 아래나 `.d0-wide` 안 번호 범례 열에 둔다.
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
- **블록.** bars (b), 비율 막대, [kpi-cards.md](blocks/kpi-cards.md) 막대 변형, 공용 [evidence.md](blocks/evidence.md)(그림형 `figure.d0-evidence`), 해석은 [explanation.md](blocks/explanation.md) `interpretation`.
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
  ━ closing 한 문장 ━━━━━━━━━━━━━━
  담당 · 기한 · 다음
  ```
- **블록.** [diff-rows.md](blocks/diff-rows.md), [checklist.md](blocks/checklist.md), [accordion.md](blocks/accordion.md), [faq.md](blocks/faq.md)(question-answer), [closing.md](blocks/closing.md).
- **page.** 보통 마지막 섹션이고 Quiet와 잘 맞는다. 끝에 남길 일 하나가 있으면 `footer.d0-closing`(공용 closing)으로 맺는다. 기억할 사실 한 문장은 그 앞 `.d0-keep`(선택, 페이지당 1개)에 둔다.
- **deck.** 참고 정리는 `summary`, 마지막 장은 `closing`(`data-closing`: decision·request·action·criteria·takeaway)이다. 마지막 장은 한 문장을 세로 중앙에 크게 두고 구분선 아래 작은 `dl` 메타 행을 붙인다. 목록 3개를 같은 무게로 놓지 않는다.

## 리듬

- **같은 구도를 연속으로 두지 않는다.** page는 header를 Hero로 세고 본문 섹션을 차례로 본다. deck은 슬라이드 순서로 본다.
- **밀도를 교차한다.** 저 → 중 → 고 → 저. 같은 밀도가 셋 이어지지 않는다.
  - 저: 요소 1~2개(숫자 하나, 문장 하나). Hero, Impact, Summary.
  - 중: 그림 하나 + 요점 2~3개. Split, Evidence, Sequence.
  - 고: 그림 + 주석·범례 4~6개, 목업. Canvas, Spotlight.
- 섹션이 3개면 header(저) → 중 → 고 → 저, 2개면 header(저) → 고 → 저가 기본이다.
- **deck의 박자.** 장마다 실루엣(구도)은 달라도 크롬·제목 문법이 같아 한 덱으로 읽힌다. 한 장에 특징(진한 면, 비대칭, 주석, 큰 숫자)을 몰아넣지 않고 한 장에 하나만 쓴다.
  진한 면 장(`data-surface="dark"`)은 표지·섹션·마무리에서 장면을 전환할 때만 쓰는 쉼표다. 섹션 장·목차는 구도 연속·밀도 리듬 계산에서 빼고, 진한 면은 Impact로 세지 않는다.

## 강조

### 강조 순서

크기 → 위치 → 여백 → 무게 → 색. 앞 수단으로 충분하면 뒤 수단을 더하지 않는다.

- **크기.** 가장 중요한 것을 가장 크게. **큰 숫자는 색이 아니라 크기로 중요하게 만든다**(기본 grey-900).
- **위치.** 첫 화면, 왼쪽 위, 섹션 첫 줄.
- **여백.** 주변을 비워 혼자 서게 한다.
- **무게.** 600~700 굵기. 그 밖은 400.
- **색.** 마지막 수단이다. blue 계열 진한 포인트는 장면마다 강조 묶음 하나에만. 파랑 하나가 모든 강조를 맡지 않게 한다.
  **강조 묶음 = 같은 의미 계열이다.** 여러 행에 걸친 같은 뜻의 표식(행마다의 `후` 막대, 같은 추천안의 막대들, 닿는 노드와 그 엣지)은 행이 여럿이어도 묶음 하나로 센다. 뜻이 다른 두 강조(후 막대 + 따로 켠 노드)는 묶음 둘이다.

### 강조 3단계 (`data-emphasis`)

| 단계 | 속성 | 모양 | 언제 |
| --- | --- | --- | --- |
| Quiet | `quiet` | 진한 포인트 채움 없음(완료 체크·의미색 점만), h2 한 단계 작게(18px), 본문·목록 글자 grey-700 | 참고, 부록, 정리 목록, deck 목차 |
| Normal | 생략 | 흰 바탕 + 기존 규칙 | 대부분의 섹션 |
| Impact | `impact` | page: 배경 없이 초대형 글자 + 여백(면·풀블리드 없음). deck: blue-light 면 + 초대형 글자. 글자 grey-900, 강조 숫자 blue-dark | 주장 한 문장, 결론 숫자 하나 |

- **Impact 안에는 하나만** 둔다: page는 문장 하나 또는 숫자 하나(+ 짧은 라벨)이고, editorial 도식을 넣지 않는다. deck은 그림 하나도 된다. 카드·목록·배지·둥근 박스 금지.
- **page**는 Impact를 선택으로 페이지당 0~1개 둔다(기존 본문 섹션 하나가 큰 문장·숫자만 남긴다. 섹션을 더하지 않는다). 배경 면·풀블리드 띠 없이 글자 크기와 여백만 쓰고, 섹션 간격은 일반과 같은 64px(모바일 48px)다. header 히어로와 같은 숫자를 되풀이하지 않는다.
- **deck**은 Impact 슬라이드를 전체의 20~30%로 둔다(10장이면 2~3장). 연속 두 장을 Impact로 두지 않는다.
- 어두운 배경은 쓰지 않는다(Day0 라이트 온리). Impact의 무게는 글자 크기와 여백에서 온다(deck은 면도 쓴다).
  예외는 deck 표지·섹션·마무리 장의 진한 면(`data-surface="dark"`, 덱당 1~3장)뿐이다. Impact가 아니라 장면 전환 면이고, 본문 장·page에는 쓰지 않는다.
- CSS와 대비는 [shell.md](blocks/shell.md) 강조 절이 정본이다.

### 색 비율과 옅은 표면

- 커버·마지막 closing 장을 포함한 색 면적은 [shell.md](blocks/shell.md)의 진한 포인트 lint Warning(<1%·1~15%·>15%)을 따른다. 게이트를 맞추려고 색 면적을 늘리지 않는다.
- **면 단위 옅은 표면**(blue-light 무대, 기억할 한 줄 `.d0-keep`, deck Impact 슬라이드, 썸네일 판)은 비율 계산에서 빼고 **장면 수**로 관리한다: page는 blue 무대 1개와 `.d0-keep` 1개까지(page Impact는 면이 없다), deck은 Impact 20~30%.
- 정본은 [shell.md](blocks/shell.md) 색 절이다.

## 무대와 상자

- **회색 무대는 기본 없음.** 도식은 흰 바탕에 바로 놓고 축의 왼쪽 정렬선을 따른다.
  **무대를 쓰는 때:** 글자 없는 도식이 여백 없이 떠서 그림의 경계가 안 보일 때(흩어진 화면 조각, 테두리 없는 선 그림), 목업·고스트 카드처럼 흰 면 요소에 받침 면이 필요할 때.
- **빈 공간은 채울 공간이 아니다.** 그림은 축 폭의 75~100%를 쓰고, 옆이나 아래에 남는 여백은 덩어리를 묶어 주는 자리로 둔다. 빈자리를 채우려고 설명 문단·목록을 그림 옆에 붙이지 않는다.
  2열은 동시 비교, 번호로 대응하는 주석·범례, 대등한 두 덩어리일 때만 `.d0-wide` 안에 쓰고 분할선은 문서 전체에서 하나다(정본: [shell.md](blocks/shell.md) 2열 절).
- **무대와 글자.** 무대 패딩 때문에 렌더 라벨이 하한 아래로 내려가면 무대를 쓰지 않는다. 글자 있는 도식은 무대 없이 두고, 무대는 글자 없는 그림·목업 받침에 쓴다(정본: [diagram.md](blocks/diagram.md) 라벨 절).
- **카드·둥근 박스를 기본값으로 쓰지 않는다.** 묶음은 여백·정렬·행 구분선으로 만든다. 카드는 하나씩 눌러 보거나 나란히 견주는 독립 대상(썸네일, 시안)일 때만 쓴다.
  예외: 선택지 비교([side-by-side](blocks/side-by-side.md))의 **split-card 변형(`data-layout="card"`)만** 카드 예외다. 각 안이 그림·설명을 가진 선택 단위일 때 외곽선 카드(1px grey-200 테두리, 면·그림자 없음)로 묶고, 카드 묶음은 가운데, 카드 안은 왼쪽 정렬한다. 기본 split-plain은 카드가 없다.

## 패턴별 권장 구도 순서

page 기준 예시다. 그 패턴이 페이지 대부분을 차지할 때의 순서이고, 패턴을 섞으면 섹션마다 그 패턴의 장면을 빌린다. 첫 칸은 header다. 섹션 수는 독자 질문이 정하고, Impact·editorial은 기존 섹션을 대체한다. 섹션은 축을 따라 위아래로 쌓고 나란히 두지 않는다. 독자 질문에 필요 없는 장면은 뺀다.

| 패턴 | 권장 순서 |
| --- | --- |
| compare | Hero(결정 질문) → Split(A \| B, 전/후) → Spotlight(차이 한 곳) → Summary(결정·할 일) |
| flow | Hero → Sequence(narrative 단계) → Canvas(구조) → Summary(막히면) |
| preview | Hero → Canvas(결과물 전체, pins) → Spotlight(핵심 화면 한 곳) → Summary |
| report | Hero(결론 수치) → Evidence(차트 + 해석) → Hero(Impact, 주장 한 문장) → Summary(할 일, Quiet) |
| guide | Hero → Spotlight(어디를 누르나) → Sequence(단계) → Summary(막히면) |
| timeline | Hero → Sequence(narrative: 지난 것·지금·남은 것) → Evidence(변경 규모) → Summary |
| incident | Hero(영향 수치) → Sequence(경위) → Canvas(원인 그래프) → Summary(재발 방지) |
| faq | Hero → Canvas(용어 핀) → Split(비유 그림 \| 풀이) → Summary(질문 목록) |

deck은 같은 순서를 슬라이드로 늘리되 cover → toc 뒤에 시작하고, 리듬·Impact 비율 규칙을 그대로 따른다.

## 금지

- 모든 섹션이 같은 구도(제목 → 무대 → SVG → 캡션), 같은 구도 연속, 같은 밀도 셋 연속.
- 구도를 바꾸려고 섹션 더하기, 구도를 바꾸려고 축 시작선·분할선 옮기기, 세 경우 밖의 2열, 빈 옆자리를 글·목록으로 채우기.
- 색으로만 강조하기, 큰 숫자를 전부 blue로 칠하기, 장면마다 blue 강조 묶음 둘 이상.
- page에 Impact 2개 이상, deck Impact 30% 초과, Impact 안 카드·목록·둘 이상의 숫자, 어두운 Impact 면.
- 진한 면을 본문 장·page에 쓰기, 모든 장을 좌우 번갈아 비대칭으로 두기, 한 장에 진한 면·비대칭·주석·큰 숫자 몰아넣기.
- 기본값으로 두른 회색 무대·카드·둥근 박스.
