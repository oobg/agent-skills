# side-by-side — 나란히 비교

## 해부 구조

- 같은 크기 2~3열. 열마다 독립 카드라 `<article>`(제목 h3). 열 = 안 이름 → 본문(미니 프로토타입 또는 비교 행) → 고르기 버튼(`aria-pressed`).
- 흰 글자 버튼 배경은 `--d0-blue-dark`(`--d0-blue`는 흰 글자 대비 4.5:1 미달).
- 후보 간 높이·정보량을 맞춘다. 고른 열만 `data-selected`로 soft 블루 배경을 받는다.
- 640px 이하에서는 세로로 쌓인다.

## 언제 쓰나 / 변형

- 화면 시안을 실제처럼 눌러 보게 하려면 이 블록 대신 [mockup-frame.md](mockup-frame.md)을 쓴다. 이 블록의 mock 변형은 버튼 하나 수준의 작은 차이에만 쓴다.

- `data-variant="mock"`(시안): 각 열이 직접 눌러 보는 미니 프로토타입이다. 안의 버튼이 실제로 반응한다.
- `data-variant="decision"`(결정): 같은 순서의 `장점·비용·위험` 행. 추천 열에만 추천 이유 한 줄(`.d0-option__why`)을 붙인다.

## 스니펫

```html
<div class="d0-sbs" data-variant="mock">
  <article class="d0-option">
    <h3>A안: 버튼을 위에</h3>
    <figure class="d0-mock"><span>주문 <data value="24">24</data>건</span><button type="button" class="d0-mock__btn">내보내기</button>
      <output class="d0-mock__msg"></output></figure>
    <button type="button" class="d0-option__pick" aria-pressed="false">A안 고르기</button>
  </article>
  <article class="d0-option">
    <h3>B안: 버튼을 아래에</h3>
    <figure class="d0-mock" data-layout="bottom"><span>주문 <data value="24">24</data>건</span><button type="button" class="d0-mock__btn">내보내기</button>
      <output class="d0-mock__msg"></output></figure>
    <button type="button" class="d0-option__pick" aria-pressed="false">B안 고르기</button>
  </article>
</div>
<!-- 결정 변형: 열 본문을 아래 행으로 바꾼다 -->
<!-- <dl class="d0-option__rows"><dt>장점</dt><dd>한 번에 끝나요</dd><dt>비용</dt><dd>하루 반</dd><dt>위험</dt><dd>알림이 늘어요</dd></dl>
     <p class="d0-option__why">추천: 팀 A가 가장 자주 쓰는 순서와 같아요.</p> -->
```

```css
.d0-sbs { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); gap: 16px; }
.d0-option {
  display: grid; gap: 12px; align-content: start;
  padding: 20px; border-radius: var(--d0-radius-card);
  background: var(--d0-grey-50);
  transition: background var(--d0-dur) var(--d0-ease);
}
.d0-option[data-selected] { background: var(--d0-blue-light); }
.d0-option h3 { font-size: 15px; font-weight: 650; }
.d0-mock { margin: 0; display: flex; flex-direction: column; gap: 8px; padding: 16px; border-radius: var(--d0-radius-control); background: #fff; }
.d0-mock__btn { order: -1; }
.d0-mock[data-layout="bottom"] .d0-mock__btn { order: 2; }
.d0-mock__btn, .d0-option__pick { border: 0; border-radius: var(--d0-radius-sm); padding: 8px 14px; font-weight: 600; }
.d0-mock__btn { background: var(--d0-blue-dark); color: #fff; }
.d0-mock[data-done] .d0-mock__btn { background: var(--d0-grey-200); color: var(--d0-grey-700); }
.d0-mock__msg { order: 3; color: var(--d0-grey-600); font-size: var(--d0-text-compact); }
.d0-option__pick { background: #fff; color: var(--d0-grey-800); }
.d0-option[data-selected] .d0-option__pick { color: var(--d0-blue-dark); }
.d0-option[data-selected] .d0-option__pick::before { content: "✓ " / ""; }
.d0-option__rows { display: grid; grid-template-columns: auto 1fr; gap: 8px 12px; }
.d0-option__rows dt { color: var(--d0-grey-700); }
.d0-option__why { color: var(--d0-blue-dark); font-weight: 600; }
@media (max-width: 640px) { .d0-sbs { grid-auto-flow: row; } }
```

```js
document.querySelectorAll('.d0-sbs').forEach(function (group) {
  group.addEventListener('click', function (e) {
    var btn = e.target.closest('.d0-mock__btn');
    if (btn) {
      var mock = btn.closest('.d0-mock');
      var done = mock.toggleAttribute('data-done');
      mock.querySelector('.d0-mock__msg').textContent = done ? '파일을 만들고 있어요' : '';
    }
    var pick = e.target.closest('.d0-option__pick');
    if (pick) group.querySelectorAll('.d0-option').forEach(function (opt) {
      var on = opt.contains(pick);
      opt.toggleAttribute('data-selected', on);
      opt.querySelector('.d0-option__pick').setAttribute('aria-pressed', String(on));
    });
  });
});
```

## 금지

- 이유 없는 추천 배지, 추천안만 크고 자세한 열, 4열 이상.
- 차이를 문단으로만 설명, 눌러도 반응하지 않는 가짜 프로토타입.
