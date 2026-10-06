# checklist — 따라하기 체크리스트

## 해부 구조

- 맨 위 진행률(완료 수 / 전체 + 막대). 그 아래 행 + 1px `grey-100` 디바이더. 행에 상자·배경을 두지 않는다.
- 행 = 체크박스(실제 `input type="checkbox"`, 24px 원) → 제목 label(15px/600, 사용자가 하는 동작) → 결과 한 줄(14px grey-600, 끝나면 보이는 것) → 행 끝 칸(기본: 소요 시간, owner: 담당·기한, 없으면 생략).
- 결과 한 줄은 한 줄(약 50자 이내)이다. 넘치면 줄이거나 목록을 `.d0-split` 한쪽 섹션에 둬 열 폭을 줄인다.
- 결정 본문이 header 요약 행에 있으면 할 일 행은 짧게 가리킨다(`PR로 올릴지 답하기` + `위 결정 1`). 결정 문장을 다시 쓰지 않는다.
- 행 안 요소는 첫 줄 기준으로 맞춘다(`align-items: start`). 체크박스·시간·배지가 행 높이로 늘어나지 않는다.
- 체크하면 행이 `data-status="done"`이 되고 진행률(네이티브 `<progress>`)이 갱신된다. 소요 시간은 `<time datetime="PT3M">`.
- 색: 진행 막대는 blue, 끝난 체크는 green 원 + 흰 체크선(흰 바탕 위 green 3.47, green 위 흰 선 3.47로 그래픽 3:1 통과). 체크 모양과 취소선이 색 없이도 완료를 말한다.
  green은 글자에 쓰지 않는다(완료 행 글자는 grey-600).

## 언제 쓰나 / 변형

- 기본(guide): 단계(최대 7). 행 끝 칸 = 소요 시간 `<time datetime="PT3M">`. 모든 행에 시간이 있을 때만 이 칸을 둔다.
- `data-variant="owner"`(incident 재발 방지, report 다음 할 일): 행 끝 칸 = 담당·기한 `.d0-check__meta`
  (`팀 A · <time datetime="2026-10-20">10월 20일</time>`). 담당·기한이 없는 행은 메타 요소를 **빼고** 행에 `data-meta="none"`을 둔다.
  빈 `span`으로 자리를 채우지 않는다. 640px 이하에서는 메타가 설명 아래 줄로 내려간다.
  기한이 날짜가 아니라 단계(`머지 후`, `PR 검토 때`)면 `<time>` 없이 텍스트로 쓴다(`팀 A · 머지 후`). `<time>`은 실제 날짜·기간에만 쓴다.
- 목록 전체에 행 끝 칸이 없으면 `.d0-check`에 `data-meta="none"`을 둬 모든 행을 `auto 1fr` 2열로 만든다.
- **시간이 일부 행에만 있으면 시간 열을 만들지 않는다.** 그 행의 결과 한 줄 끝에 넣는다(`… 보여요. 약 20분`). 한 행에만 붙은 오른쪽 끝 숫자는 근거 없이 튀어 보인다.
- 입력 예시가 필요한 행은 `<details>`로 행 안에 접어 둔다.

| 조건 | 열 정의 |
| --- | --- |
| 기본, 모든 행에 시간 | `auto 1fr auto` |
| `owner`, 메타 있는 행 | `auto 1fr auto` |
| 메타 없는 행 `[data-meta="none"]` 또는 목록 전체 `.d0-check[data-meta="none"]` | `auto 1fr` |

## 스니펫

```html
<div class="d0-check">
  <label class="d0-check__progress" for="check-progress"><output data-count>0</output> / 3 완료</label>
  <progress class="d0-check__bar" id="check-progress" max="3" value="0">0 / 3</progress>
  <ol>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-1">
      <div><label for="step-1">설정 열기</label><p>왼쪽 메뉴에 '내보내기'가 보여요.</p></div>
      <time class="d0-check__time" datetime="PT1M">1분</time>
    </li>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-2">
      <div><label for="step-2">받을 팀 고르기</label><p>목록에 팀 A가 체크돼요.</p>
        <details><summary>입력 예시</summary><p>팀 이름 칸에 '팀 A'를 입력해요.</p></details></div>
      <time class="d0-check__time" datetime="PT3M">3분</time>
    </li>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-3">
      <div><label for="step-3">자동 전송 켜기</label><p>스위치 옆에 '매일 아침 9시'가 보여요.</p></div>
      <time class="d0-check__time" datetime="PT1M">1분</time>
    </li>
  </ol>
</div>
```

```css
.d0-check__progress { display: block; color: var(--d0-grey-600); font-size: 14px; font-weight: 600; font-variant-numeric: tabular-nums; }
.d0-check__bar {
  appearance: none; display: block; width: 100%; height: 6px; margin: 8px 0 12px;
  border: 0; border-radius: 999px; background: var(--d0-grey-100); overflow: hidden; color: var(--d0-blue);
}
.d0-check__bar::-webkit-progress-bar { background: var(--d0-grey-100); }
.d0-check__bar::-webkit-progress-value { background: var(--d0-blue); transition: width var(--d0-dur) var(--d0-ease); }
.d0-check__bar::-moz-progress-bar { background: var(--d0-blue); }
.d0-check__row { display: grid; grid-template-columns: auto 1fr auto; align-items: start; gap: 12px; padding: 16px 0; border-top: 1px solid var(--d0-grey-100); }
.d0-check__row label { color: var(--d0-grey-900); font-weight: 600; cursor: pointer; }
.d0-check__row p, .d0-check summary { color: var(--d0-grey-600); font-size: 14px; }
.d0-check__time { color: var(--d0-grey-600); font-size: var(--d0-text-compact); font-variant-numeric: tabular-nums; }
.d0-check__box {
  appearance: none; display: grid; place-content: center;
  width: 24px; height: 24px; margin: 0;
  border: 2px solid var(--d0-grey-500); border-radius: 999px; background: #fff; cursor: pointer;
}
.d0-check__box::after { content: ""; width: 10px; height: 6px; border: solid #fff; border-width: 0 0 2px 2px; transform: rotate(-45deg) translate(1px, -1px); }
.d0-check__row[data-status="done"] .d0-check__box { border-color: var(--d0-green); background: var(--d0-green); }
.d0-check__row[data-status="done"] label { color: var(--d0-grey-600); text-decoration: line-through; }
.d0-check details { margin-top: 6px; }
```

```js
document.querySelectorAll('.d0-check').forEach(function (list) {
  list.addEventListener('change', function (e) {
    if (!e.target.matches('.d0-check__box')) return;
    var row = e.target.closest('.d0-check__row');
    if (e.target.checked) row.dataset.status = 'done'; else delete row.dataset.status;
    var n = list.querySelectorAll('.d0-check__box:checked').length;
    list.querySelector('[data-count]').textContent = n;
    var bar = list.querySelector('progress');
    bar.value = n; bar.textContent = n + ' / ' + bar.max;
  });
});
```

### owner 변형 스니펫

```html
<div class="d0-check" data-variant="owner">
  <label class="d0-check__progress" for="fix-progress"><output data-count>0</output> / 3 완료</label>
  <progress class="d0-check__bar" id="fix-progress" max="3" value="0">0 / 3</progress>
  <ol>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="fix-1">
      <div><label for="fix-1">실패 알림을 채팅으로도 보내기</label><p>밤사이 실패를 아침 전에 알아요.</p></div>
      <span class="d0-check__meta">팀 A · <time datetime="2026-10-20">10월 20일</time></span>
    </li>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="fix-2">
      <div><label for="fix-2">재시도 횟수 3번으로 늘리기</label><p>잠깐 끊긴 연결은 저절로 다시 보내요.</p></div>
      <span class="d0-check__meta">팀 B</span>
    </li>
    <li class="d0-check__row" data-meta="none">
      <input type="checkbox" class="d0-check__box" id="fix-3">
      <div><label for="fix-3">보관 기간 다시 정하기</label><p>담당은 다음 회의에서 정해요.</p></div>
    </li>
  </ol>
</div>
```

```css
.d0-check__meta { color: var(--d0-grey-700); font-size: var(--d0-text-compact); font-weight: 500; white-space: nowrap; font-variant-numeric: tabular-nums; }
.d0-check[data-meta="none"] .d0-check__row,
.d0-check__row[data-meta="none"] { grid-template-columns: auto 1fr; }
@media (max-width: 640px) {
  .d0-check[data-variant="owner"] .d0-check__row { grid-template-columns: auto 1fr; }
  .d0-check__meta { grid-column: 2; white-space: normal; }
}
```

JS는 기본 변형과 같다.

## 금지

- 행마다 카드, 행 배경, `grey-200` 이상 구분선, 완료 판정이 모호한 제목("확인하기", "점검").
- green 글자(완료 행 제목을 초록으로), 체크 모양 없이 색만 바뀌는 완료 표시.
- 요약 행의 결정 문장을 할 일 행에 다시 쓰기, 두 줄로 넘치는 결과 한 줄.
- 사용자가 할 일과 시스템이 하는 일을 한 목록에 섞기(시스템 일은 결과 한 줄로만).
- 일부 행에만 있는 시간 열, 메타 칸을 채우려는 빈 `span`·`-` 표시.
