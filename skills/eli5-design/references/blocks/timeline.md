# timeline — 시간 축

## 해부 구조

- 순서가 있으므로 `<ol>`, 날짜는 늘 `<time datetime>`.
- 점마다 날짜 → 제목 → 상태 배지. 점은 선 위에 놓인다. 배지는 높이 고정(22px)이라 행 높이로 늘어나지 않는다.
- **CSS 타임라인(아래 기본·세로)은 그림 블록으로 치지 않는다.** 앞쪽 핵심 섹션의 그림은 아래 SVG 시간 막대(`data-variant="timebar"`)로 채우고,
  CSS 목록은 그 아래 항목별 설명이 필요할 때만 붙인다.
- 상태는 `data-status="planned|active|done"`(예정·진행·완료). 진행만 블루 점, 완료는 채운 회색, 예정은 빈 점. 상태 배지 글자를 늘 함께 둔다.
- 오늘 표식은 블루 세로선 + `오늘` 라벨(`.d0-timeline__today`).

## 언제 쓰나 / 변형

- 기본(가로): 로드맵 마일스톤 3~5개. 640px 이하에서는 자동으로 세로가 된다.
- `data-variant="vertical"`: 변경 내역·사건 기록. 항목 아래 "달라지는 점" 한 줄을 둔다.
- `data-variant="timebar"`(SVG 시간 막대): 가로 축 위 점 3~5개와 구간 채움. 그림 블록이다. timeline 프리셋·incident 경과의 대표 도식으로 쓴다.

## SVG 시간 막대 (`data-variant="timebar"`)

```html
<figure class="d0-fig" data-stage data-size="wide" data-variant="timebar">
  <div class="d0-fig__stage">
  <svg viewBox="0 0 480 120" role="img" aria-labelledby="t1-t t1-d">
    <title id="t1-t">알림 기능 일정</title>
    <desc id="t1-d">1월 12일 설정 화면과 2월 9일 매일 알림은 초록 체크로 끝났어요. 3월 2일 팀 알림이 블루로 진행 중이고, 3월 23일 정리는 예정이에요.</desc>
    <rect class="d0-s-axis" x="40" y="56" width="400" height="8" rx="4"/>
    <rect class="d0-s-bar" data-tone="green" x="40" y="56" width="160" height="8" rx="4"/>
    <rect class="d0-s-bar" data-on x="200" y="56" width="120" height="8" rx="4"/>
    <circle class="d0-s-node" data-tone="green" cx="40" cy="60" r="11"/>
    <path class="d0-s-tick" d="M35 60 L39 64 L46 56"/>
    <circle class="d0-s-node" data-tone="green" cx="200" cy="60" r="11"/>
    <path class="d0-s-tick" d="M195 60 L199 64 L206 56"/>
    <circle class="d0-s-ring" cx="320" cy="60" r="16"/>
    <circle class="d0-s-node" data-on cx="320" cy="60" r="11"/>
    <circle class="d0-s-node" cx="440" cy="60" r="10"/>
    <text class="d0-s-text d0-s-muted" x="40" y="26" text-anchor="middle">1월 12일</text>
    <text class="d0-s-text d0-s-muted" x="200" y="26" text-anchor="middle">2월 9일</text>
    <text class="d0-s-text" data-on x="320" y="26" text-anchor="middle">3월 2일</text>
    <text class="d0-s-text d0-s-muted" x="440" y="26" text-anchor="middle">3월 23일</text>
    <text class="d0-s-text" x="40" y="106" text-anchor="middle">설정 화면</text>
    <text class="d0-s-text" x="200" y="106" text-anchor="middle">매일 알림</text>
    <text class="d0-s-text" data-on x="320" y="106" text-anchor="middle">팀 알림</text>
    <text class="d0-s-text d0-s-muted" x="440" y="106" text-anchor="middle">정리</text>
  </svg>
  </div>
  <figcaption>두 가지는 끝났고, 팀 알림을 만드는 중이에요.</figcaption>
</figure>
```

```css
/* diagram.md 공용 CSS(.d0-s-*)를 함께 쓴다 */
.d0-s-axis { fill: var(--d0-grey-300); } /* 예정 구간: 점과 날짜 라벨이 뜻을 전한다 */
```

- 크기는 diagram.md `data-size="wide"`(W 480, 글자 18, max-width 400px)다. 라벨 게이트도 같다.
- 점 x = 40 + (날짜 − 첫 날짜) ÷ 전체 기간 × 400(위 예: 2월 9일은 28일 ÷ 70일 × 400 + 40 = 200). 간격을 지어 맞추지 않는다.
  두 점 중심이 100보다 가까우면 라벨이 겹치므로 기간으로 묶거나 날짜 라벨을 한 칸 걸러 둔다.
- 상태는 점 색 + 모양 + 라벨로 말한다. 완료 = green 원 + 흰 체크, 진행(현재) = blue 원 + 바깥 고리 + blue-dark 라벨, 예정 = 흰 원 + grey-500 테두리.
  구간 채움도 같다: 완료 구간 green, 진행 구간 blue, 예정 구간 grey-300 축.
- **점마다 배지를 달지 않는다.** 상태 배지는 페이지 배지 예산(카드·행당 1개, 톤 3가지)을 먹는다. 점 색과 라벨로 충분하다.
- 위는 날짜(흐린 라벨), 아래는 항목 이름(명사 1~2단어). 커밋 번호처럼 긴 값은 SVG 밖 목록이나 figcaption으로 보낸다.
- 1280px 첫 화면에 넣을 때는 `.d0-split` 한쪽 열이나 diagram.md `data-layout="side"`에 둔다(무대 양옆이 비지 않게).

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
- CSS 타임라인만으로 앞쪽 핵심 섹션의 그림을 대신하기, SVG 시간 막대의 점마다 상태 배지.
- 내부 작업 번호·파일명만 나열하고 독자에게 달라지는 점이 없는 항목.
