# checklist — 따라하기 체크리스트

## 해부 구조

- 맨 위 진행률(완료 수 / 전체 + 막대). 그 아래 행 + 1px 디바이더.
- 행 = 체크박스(실제 `input type="checkbox"`, 24px 원) → 제목 label(사용자가 하는 동작) → 결과 한 줄(끝나면 보이는 것) → 소요 시간.
- 체크하면 행이 `data-status="done"`이 되고 진행률(`role="progressbar"` + `aria-valuenow`)이 갱신된다.

## 언제 쓰나 / 변형

- guide의 단계(최대 7), incident의 재발 방지 항목(결과 한 줄 자리에 담당·기한).
- 입력 예시가 필요한 행은 `<details>`로 행 안에 접어 둔다.

## 스니펫

```html
<div class="d0-check">
  <p class="d0-check__progress" aria-live="polite"><span data-count>0</span> / 3 완료</p>
  <div class="d0-check__bar" role="progressbar" aria-label="진행률" aria-valuemin="0" aria-valuemax="3" aria-valuenow="0"><span></span></div>
  <ol>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-1">
      <div><label for="step-1">설정 열기</label><p>왼쪽 메뉴에 '내보내기'가 보여요.</p></div>
      <span class="d0-check__time">1분</span>
    </li>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-2">
      <div><label for="step-2">받을 팀 고르기</label><p>목록에 팀 A가 체크돼요.</p>
        <details><summary>입력 예시</summary><p>팀 이름 칸에 '팀 A'를 입력해요.</p></details></div>
      <span class="d0-check__time">3분</span>
    </li>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-3">
      <div><label for="step-3">자동 전송 켜기</label><p>스위치 옆에 '매일 아침 9시'가 보여요.</p></div>
      <span class="d0-check__time">1분</span>
    </li>
  </ol>
</div>
```

```css
.d0-check__progress { font-weight: 600; font-variant-numeric: tabular-nums; }
.d0-check__bar { height: 6px; margin: 8px 0 12px; border-radius: 999px; background: var(--d0-grey-100); overflow: hidden; }
.d0-check__bar span { display: block; width: 0; height: 100%; background: var(--d0-blue); transition: width var(--d0-dur) var(--d0-ease); }
.d0-check__row { display: grid; grid-template-columns: auto 1fr auto; gap: 12px; padding: 14px 0; border-top: 1px solid var(--d0-grey-100); }
.d0-check__row label { font-weight: 600; cursor: pointer; }
.d0-check__row p, .d0-check__time, .d0-check summary { color: var(--d0-grey-600); font-size: var(--d0-text-compact); }
.d0-check__box {
  appearance: none; display: grid; place-content: center;
  width: 24px; height: 24px; margin: 0;
  border: 2px solid var(--d0-grey-500); border-radius: 999px; background: #fff; cursor: pointer;
}
.d0-check__box::after { content: ""; width: 10px; height: 6px; border: solid #fff; border-width: 0 0 2px 2px; transform: rotate(-45deg) translate(1px, -1px); }
.d0-check__row[data-status="done"] .d0-check__box { border-color: var(--d0-blue-dark); background: var(--d0-blue-dark); }
.d0-check__row[data-status="done"] label { color: var(--d0-grey-600); text-decoration: line-through; }
.d0-check details { margin-top: 6px; }
```

```js
document.querySelectorAll('.d0-check').forEach(function (list) {
  var boxes = list.querySelectorAll('.d0-check__box');
  list.addEventListener('change', function (e) {
    if (!e.target.matches('.d0-check__box')) return;
    var row = e.target.closest('.d0-check__row');
    if (e.target.checked) row.dataset.status = 'done'; else delete row.dataset.status;
    var n = list.querySelectorAll('.d0-check__box:checked').length;
    list.querySelector('[data-count]').textContent = n;
    list.querySelector('[role="progressbar"]').setAttribute('aria-valuenow', n);
    list.querySelector('.d0-check__bar span').style.width = (n / boxes.length * 100) + '%';
  });
});
```

## 금지

- 행마다 카드, 완료 판정이 모호한 제목("확인하기", "점검").
- 사용자가 할 일과 시스템이 하는 일을 한 목록에 섞기(시스템 일은 결과 한 줄로만).
