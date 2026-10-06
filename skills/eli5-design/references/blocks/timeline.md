# timeline — 시간 축

## 해부 구조

- 점마다 날짜 → 제목 → 상태 배지. 점은 선 위에 놓인다.
- 상태는 `data-status="planned|active|done"`(예정·진행·완료). 진행만 블루 점, 완료는 채운 회색, 예정은 빈 점. 상태 배지 글자를 늘 함께 둔다.
- 오늘 표식은 블루 세로선 + `오늘` 라벨(`.d0-timeline__today`).

## 언제 쓰나 / 변형

- 기본(가로): 로드맵 마일스톤 3~5개. 640px 이하에서는 자동으로 세로가 된다.
- `data-variant="vertical"`: 변경 내역·사건 기록. 항목 아래 "달라지는 점" 한 줄을 둔다.

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
- 내부 작업 번호·파일명만 나열하고 독자에게 달라지는 점이 없는 항목.
