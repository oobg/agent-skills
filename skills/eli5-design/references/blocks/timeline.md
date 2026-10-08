# timeline — 시간 축

## 해부 구조

- 순서가 있으므로 `<ol>`, 날짜는 늘 `<time datetime>`.
- 점마다 날짜 → 제목 → 상태 배지. 점은 선 위에 놓인다. 배지는 높이 고정(22px)이라 행 높이로 늘어나지 않는다.
- **CSS 타임라인(아래 기본·세로)은 그림 블록으로 치지 않는다.** 첫 화면 섹션의 그림은 아래 SVG 시간 막대(`data-variant="timebar"`)로 채우고,
  CSS 목록은 그 아래 항목별 설명이 필요할 때만 붙인다.
- 상태는 `data-status="planned|active|done"`(예정·진행·완료). 진행만 블루 점, 완료는 채운 회색, 예정은 빈 점. 상태 배지 글자를 늘 함께 둔다.
- 오늘 표식은 블루 세로선 + `오늘` 라벨(`.d0-timeline__today`).

## 언제 쓰나 / 변형

- 기본(가로): 로드맵 마일스톤 3~5개. 640px 이하에서는 자동으로 세로가 된다.
- `data-variant="vertical"`: 변경 내역·사건 기록. 항목 아래 "달라지는 점" 한 줄을 둔다.
- `data-variant="timebar"`(SVG 시간 막대): 가로 축 위 점 3~5개와 구간 채움. 그림 블록이다. 일정·사건 경과의 대표 도식으로 쓴다.
- `ol.d0-rail`(status rail, 공용): 완료·진행·예정 구간 이름을 잇는 작은 가로 진행선. 아래 status rail 절이 유일한 정의다.

## SVG 시간 막대 (`data-variant="timebar"`)

```html
<figure class="d0-fig" data-variant="timebar">
  <svg viewBox="0 0 560 140" role="img" aria-labelledby="t1-t t1-d">
    <title id="t1-t">알림 기능 일정</title>
    <desc id="t1-d">1월 12일 설정 화면과 2월 9일 매일 알림은 초록 체크로 끝났어요. 3월 2일 팀 알림이 블루로 진행 중이고, 3월 23일 정리는 예정이에요.</desc>
    <rect class="d0-s-axis" x="40" y="65" width="480" height="10" rx="5"/>
    <rect class="d0-s-bar" data-tone="green" x="40" y="65" width="192" height="10" rx="5"/>
    <rect class="d0-s-bar" data-on x="232" y="65" width="144" height="10" rx="5"/>
    <circle class="d0-s-node" data-tone="green" cx="40" cy="70" r="13"/>
    <path class="d0-s-tick" d="M34 70 L39 75 L47 65"/>
    <circle class="d0-s-node" data-tone="green" cx="232" cy="70" r="13"/>
    <path class="d0-s-tick" d="M226 70 L231 75 L239 65"/>
    <circle class="d0-s-ring" cx="376" cy="70" r="19"/>
    <circle class="d0-s-node" data-on cx="376" cy="70" r="13"/>
    <circle class="d0-s-node" cx="520" cy="70" r="12"/>
    <text class="d0-s-text d0-s-muted" x="27" y="30" text-anchor="start">1월 12일</text>
    <text class="d0-s-text d0-s-muted" x="232" y="30" text-anchor="middle">2월 9일</text>
    <text class="d0-s-text" data-on x="376" y="30" text-anchor="middle">3월 2일</text>
    <text class="d0-s-text d0-s-muted" x="532" y="30" text-anchor="end">3월 23일</text>
    <text class="d0-s-text" x="27" y="124" text-anchor="start">설정 화면</text>
    <text class="d0-s-text" x="232" y="124" text-anchor="middle">매일 알림</text>
    <text class="d0-s-text" data-on x="376" y="124" text-anchor="middle">팀 알림</text>
    <text class="d0-s-text d0-s-muted" x="532" y="124" text-anchor="end">정리</text>
  </svg>
  <figcaption>두 가지는 끝났고, 팀 알림을 만드는 중이에요.</figcaption>
</figure>
```

```css
/* 도식 공용 클래스(.d0-s-*)는 page.css에 있다 */
.d0-s-axis { fill: var(--d0-grey-300); } /* 예정 구간: 점과 날짜 라벨이 뜻을 전한다 */
```

- 크기는 page 도식 기준(viewBox 폭 560, 축 폭을 채움, [diagrams/index.md](../diagrams/index.md))이다. 글자가 있는 그림이라 무대를 두지 않는다.
- 점 x = 40 + (날짜 − 첫 날짜) ÷ 전체 기간 × 480(위 예: 2월 9일은 28일 ÷ 70일 × 480 + 40 = 232). 간격을 지어 맞추지 않는다.
  - **예외: 같은 간격 배치.** 시각이 몰려 비례 배치로는 라벨이 겹치고, 길이보다 순서가 핵심인 변경 내역(하루 안 커밋 몇 번 등)이면 점을 같은 간격으로 둬도 된다.
    이때는 간격이 시간을 말하지 않으므로 **모든 점에 시각 라벨을 단다**(생략 금지). 일정·로드맵처럼 기간 길이가 뜻인 경우에는 쓰지 않는다.
- **좁은 간격.** 두 점 간격이 라벨 폭(viewBox 단위로 데스크톱 14px 라벨 약 80, 모바일 20px 라벨 약 115)보다 좁으면 둘 중 하나를 쓴다.
  ① 한 점으로 묶는다: 가운데 점 하나 + 기간 라벨(`3월 2~5일`) + 이름 하나(`팀 알림 2건`). ② 라벨을 엇갈린다: 겹치는 점의 날짜를 아래, 이름을 위로 바꿔 단다
  (예: x 376·412 두 점이면 412는 날짜 `y="124"`·이름 `y="30"`). 점이 셋 이상 몰리면 ①만 쓴다.
- 상태는 점 색 + 모양 + 라벨로 말한다. 완료 = green 원 + 흰 체크, 진행(현재) = blue 원 + 바깥 고리 + blue-dark 라벨, 예정 = 흰 원 + grey-500 테두리.
  구간 채움도 같다: 완료 구간 green, 진행 구간 blue, 예정 구간 grey-300 축.
- **계획만 있는 경우(아직 시작 전).** 완료·진행 점이 없으면 회색만 남는다(금지). 다음 이정표(또는 결정 지점) 하나를 현재 점 모양(blue 원 + 바깥 고리 + blue-dark 라벨)으로 켜고, 위 줄은 `지금` 대신 날짜 + `예상`(`5월 예상`)으로 쓴다.
  목표일만 있는 다른 점도 날짜에 `예상`을 붙인다. 오늘이 축 범위 안에 있으면 오늘 표식을 두고, 첫 점보다 앞이면 두지 않는다. figcaption에 "아직 시작 전"을 한 번 쓴다.
- **점마다 배지를 달지 않는다.** 상태 배지는 페이지 배지 예산(카드·행당 1개, 톤 3가지)을 먹는다. 점 색과 라벨로 충분하다.
- **라벨 두 줄.** 모든 점에 위(시각·날짜)와 아래(이름) 두 줄을 같은 기준선(`y`)에 달고 `text-anchor="middle"`로 점 중심 `cx`에 맞춘다.
  끝 점은 아래 "끝 점" 규칙만 예외다. 현재 점도 빼지 않는다: 위 줄은 `지금`, 아래 줄은 항목 이름. 그래야 위·아래 줄이 모든 점에서 같은 리듬이 된다. 위는 날짜(흐린 라벨), 아래는 항목 이름(명사 1~2단어).
- **간격 검증.** 같은 줄에서 인접 라벨 bbox 사이는 8px 이상이다. `getBBox()`로 각 `<text>`의 x·width를 재어 `다음.x − (이전.x + 이전.width)`가 8 이상(viewBox 단위, 렌더 px는 × 스케일)인지,
  라벨 중심과 점 `cx` 차가 1px 이내인지 확인한다. 합친 구간 라벨이 가장 넓으니 그 점 양옆 간격을 먼저 본다.
  간격이 모자라면 점 위치를 지어 옮기지 말고 위 "좁은 간격"의 합치기·엇갈리기를 쓴다.
- **합친 구간.** 시각은 en dash로 잇는다(`13:04–13:09`). 가운뎃점(`·`)이나 하이픈은 쓰지 않는다.
- **끝 점.** 오른쪽 끝(또는 왼쪽 끝) 점의 라벨이 트랙·viewBox 밖으로 나가면 그 점만 `text-anchor="end"`(왼쪽은 `start`)로 바꾸고 x를 점 가장자리에 맞춘다. 나머지 점은 middle을 유지한다.
  트랙 좌우에는 가장 넓은 라벨 절반만큼 여백을 둔다. 커밋 번호처럼 긴 값은 SVG 밖 목록이나 figcaption으로 보낸다.

## status rail (`ol.d0-rail`) — 지금 어디에 있는가

공용 정보 블록이다. 구간·단계 이름 3~6개를 잇는 작은 가로 진행선으로 **지금 어디에 있는가**만 말한다. 일정의 현재 단계, 사건 경위의 지금 상태, 절차의 현재 단계에서 같은 요소를 다시 쓴다. 다른 파일에 따로 정의하지 않는다. [checklist](checklist.md) 구간에서는 구간 머리 행이 지도를 맡으므로 rail을 함께 두지 않는다.

- 역할 구분: rail은 위치(완료·진행·예정), [checkpoint](checkpoint.md)는 그 지점에서 완성되는 결과다. rail 이름은 짧은 구간 이름(`준비`, `초안`, `발행`), checkpoint는 결과 문장(`여기까지 하면 초안이 완성돼요`).
- 마크업: `ol.d0-rail > li[data-state="done|current|planned"]`, 현재 항목은 `aria-current="step"`. 각 항목 앞 `span.d0-rail__mark`에 완료면 `✓`를 쓴다(색만으로 구분하지 않는다).
- 점 10px(완료 green 채움, 현재 blue-dark 채움 + 굵은 이름, 예정 빈 원 grey-500 테두리), 잇는 선 2px grey-200, 이름 12px grey-600(현재 grey-900/600). 375px에서 이름이 감겨도 점·선은 한 줄이다.
- 그림 블록이 아니다(첫 화면 그림은 시간 막대·도식이 맡는다). 전체 진행 수(`전체 n / N`)를 함께 쓸 때는 rail 바로 위 진행률 줄에 둔다.

```html
<ol class="d0-rail" aria-label="전체 구간">
  <li data-state="done"><span class="d0-rail__mark" aria-hidden="true">✓</span>준비</li>
  <li data-state="current" aria-current="step"><span class="d0-rail__mark" aria-hidden="true"></span>초안</li>
  <li data-state="planned"><span class="d0-rail__mark" aria-hidden="true"></span>발행</li>
</ol>
```

```css
.d0-rail { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); margin: 0 0 12px; }
.d0-rail li { position: relative; padding: 16px 8px 0 0; color: var(--d0-grey-600); font-size: var(--d0-meta); line-height: var(--d0-leading-title); }
.d0-rail li::before { content: ""; position: absolute; top: 0; left: 0; z-index: 1; box-sizing: border-box; width: 10px; height: 10px; border: 2px solid var(--d0-grey-500); border-radius: 999px; background: #fff; }
.d0-rail li:not(:last-child)::after { content: ""; position: absolute; top: 4px; left: 10px; right: 0; height: 2px; background: var(--d0-grey-200); }
.d0-rail li[data-state="done"]::before { border-color: var(--d0-green); background: var(--d0-green); }
.d0-rail li[aria-current="step"] { color: var(--d0-grey-900); font-weight: 600; }
.d0-rail li[aria-current="step"]::before { border-color: var(--d0-blue-dark); background: var(--d0-blue-dark); }
.d0-rail__mark:not(:empty) { margin-right: 4px; color: var(--d0-grey-900); }
```

## 스니펫

```html
<ol class="d0-timeline">
  <li data-status="done"><time datetime="2026-01-12">1월 12일</time><strong>알림 설정 화면</strong><span class="d0-pill">완료</span></li>
  <li data-status="active"><time datetime="2026-02-09">2월 9일</time><strong>매일 알림</strong><span class="d0-pill" data-tone="blue">진행</span></li>
  <li class="d0-timeline__today" aria-label="오늘"><span>오늘</span></li>
  <li data-status="planned"><time datetime="2026-03-23">3월 23일</time><strong>팀별 알림</strong><span class="d0-pill">예정</span></li>
</ol>
```

```css
.d0-timeline { display: flex; }
.d0-timeline > li {
  position: relative; flex: 1 1 0; min-width: 0;
  display: grid; gap: 4px; justify-items: start; align-content: start;
  padding: 20px 12px 0 0;
  border-top: 2px solid var(--d0-grey-200);
}
.d0-timeline > li::before {
  content: ""; position: absolute; top: -7px; left: 0;
  width: 12px; height: 12px; border-radius: 999px;
  background: #fff; border: 2px solid var(--d0-grey-500);
}
.d0-timeline > li[data-status="done"]::before { background: var(--d0-grey-500); border-color: var(--d0-grey-500); }
.d0-timeline > li[data-status="active"]::before { background: var(--d0-blue); border-color: var(--d0-blue); }
.d0-timeline time { color: var(--d0-grey-600); font-size: var(--d0-text-compact); font-variant-numeric: tabular-nums; }
.d0-timeline > li[data-status="done"] strong { color: var(--d0-grey-600); }
.d0-timeline > .d0-timeline__today { flex: none; width: auto; padding: 0 12px 0 0; border-top: 0; }
.d0-timeline__today::before { display: none; }
.d0-timeline__today span {
  display: block; height: 100%; min-height: 48px; padding: 0 0 0 8px; margin-top: -12px;
  border-left: 2px solid var(--d0-blue);
  color: var(--d0-blue-dark); font-size: var(--d0-meta); font-weight: 600;
}
.d0-timeline[data-variant="vertical"] { flex-direction: column; }
@media (max-width: 640px) { .d0-timeline { flex-direction: column; } }
.d0-timeline[data-variant="vertical"] > li { border-top: 0; border-left: 2px solid var(--d0-grey-200); padding: 0 0 20px 20px; }
.d0-timeline[data-variant="vertical"] > li::before { top: 2px; left: -7px; }
.d0-timeline[data-variant="vertical"] .d0-timeline__today span { min-height: 0; margin: 0 0 12px -2px; padding: 0 0 0 8px; border-left: 0; border-top: 2px solid var(--d0-blue); }
@media (max-width: 640px) {
  .d0-timeline > li { border-top: 0; border-left: 2px solid var(--d0-grey-200); padding: 0 0 20px 20px; }
  .d0-timeline > li::before { top: 2px; left: -7px; }
  .d0-timeline .d0-timeline__today span { min-height: 0; margin: 0 0 12px -2px; padding: 0 0 0 8px; border-left: 0; border-top: 2px solid var(--d0-blue); }
}
```

## 금지

- 점 수십 개(마일스톤 5개 이내, 더 있으면 기간으로 묶는다), 날짜 없는 점.
- CSS 타임라인·status rail만으로 첫 화면 섹션의 그림을 대신하기, SVG 시간 막대의 점마다 상태 배지.
- 내부 작업 번호·파일명만 나열하고 독자에게 달라지는 점이 없는 항목.
