# tab-preview — 파일 미리보기

## 해부 구조

- 이 블록 자체가 결과물 목업(그림)이다. 실물처럼 보이게 하고 설명은 열 주석 한 줄씩으로 끝낸다.
- pill 탭(시트·파일 단위, 버튼이라 높이 32px) → 파일명 바 + `예시 데이터` 배지 → 표 목업 → 열 의미 주석.
- 전체를 `<figure>`로 감싸고 열 주석은 `<figcaption>` 안 `<dl>`(열 문자 → 뜻)로 둔다.
- 표 목업 = 행 번호 열 + 열 문자 머리(A, B, C…) + 합계 행(`<tfoot>`, 숫자는 `<data value>`) + 하단 시트 탭.
- 데이터 열은 6개 이하(행 번호 열을 더해 7, SKILL 표 열 상한). 칸 폭을 고정해 페이지 가로 스크롤을 만들지 않는다. 확대 시에는 표만 자체 스크롤된다(`.d0-sheet__wrap`).

## 언제 쓰나 / 변형

- preview에서 받게 될 파일·시트의 모양을 보여 줄 때. 탭은 `aria-selected`와 `data-selected`를 함께 바꾼다.
- 시트가 하나면 pill 탭을 빼고 파일명 바부터 시작한다.
- 엑셀처럼 보이게 하려면 파일명 바·표·하단 시트 탭을 테두리 상자 `.d0-tabprev__panel`(tabpanel)로 묶는다. 완성 예는 [preview-compare.html](../examples/preview-compare.html) ②.
- 클래스 이름은 `.d0-tabprev*`·`.d0-sheet*`만 쓴다. `.d0-sheet`는 이 블록의 표 전용이다(mockup-frame의 오른쪽 패널은 `.d0-panel`).

## 스니펫

```html
<figure class="d0-tabprev">
  <div class="d0-tabprev__tabs" role="tablist" aria-label="시트">
    <button type="button" role="tab" class="d0-pill" id="tab-sum" aria-controls="panel-sum" aria-selected="true" data-selected>요약</button>
    <button type="button" role="tab" class="d0-pill" id="tab-det" aria-controls="panel-det" aria-selected="false" tabindex="-1">상세</button>
  </div>
  <div class="d0-tabprev__bar"><span>주문 내보내기 (예시).xlsx</span><span class="d0-pill" data-tone="orange">예시 데이터</span></div>
  <div role="tabpanel" id="panel-sum" aria-labelledby="tab-sum">
    <div class="d0-sheet__wrap" role="region" aria-label="요약 시트 표" tabindex="0"><table class="d0-sheet">
      <caption class="d0-sr-only">요약 시트 예시: 팀별 주문 수와 금액</caption>
      <thead><tr><td></td><th scope="col">A</th><th scope="col">B</th><th scope="col">C</th></tr></thead>
      <tbody>
        <tr><th scope="row">1</th><td>팀</td><td>주문 수</td><td>금액</td></tr>
        <tr><th scope="row">2</th><td>팀 A</td><td>37</td><td>412,300</td></tr>
        <tr><th scope="row">3</th><td>팀 B</td><td>21</td><td>238,750</td></tr>
      </tbody>
      <tfoot><tr data-total><th scope="row">4</th><td>합계</td><td><data value="58">58</data></td><td><data value="651050">651,050</data></td></tr></tfoot>
    </table></div>
    <p class="d0-sheet__tabs"><span data-selected>요약</span><span>상세</span></p>
  </div>
  <div role="tabpanel" id="panel-det" aria-labelledby="tab-det" hidden><!-- 상세 시트 표 --></div>
  <figcaption><dl class="d0-tabprev__notes"><div><dt>B</dt><dd>기간 안에 들어온 주문 건수예요.</dd></div><div><dt>C</dt><dd>할인을 뺀 금액이에요.</dd></div></dl></figcaption>
</figure>
```

```css
.d0-tabprev { display: grid; gap: 12px; }
.d0-tabprev__tabs { display: flex; gap: 6px; }
.d0-tabprev__tabs [role="tab"] { border: 0; }
.d0-tabprev__tabs [data-selected] { background: var(--d0-blue-light); color: var(--d0-blue-dark); }
.d0-tabprev__bar { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px; padding: 10px 12px; border-radius: var(--d0-radius-sm); background: var(--d0-grey-50); font-size: var(--d0-text-compact); }
.d0-tabprev__bar .d0-pill { align-self: center; }
.d0-sheet { width: 100%; table-layout: fixed; border-collapse: collapse; font-size: var(--d0-text-compact); font-variant-numeric: tabular-nums; }
.d0-sheet th, .d0-sheet td { padding: 8px; border: 1px solid var(--d0-grey-100); text-align: left; overflow-wrap: anywhere; }
.d0-sheet__wrap { overflow-x: auto; }
.d0-sheet thead th, .d0-sheet tbody th { background: var(--d0-grey-50); color: var(--d0-grey-600); font-weight: 500; }
.d0-sheet thead td { background: var(--d0-grey-50); }
.d0-sheet tr > :first-child { width: 36px; text-align: center; }
.d0-sheet tfoot td { font-weight: 700; }
.d0-sheet__tabs { display: flex; gap: 2px; margin-top: 4px; font-size: var(--d0-meta); color: var(--d0-grey-600); }
.d0-sheet__tabs span { padding: 4px 10px; }
.d0-sheet__tabs [data-selected] { background: var(--d0-grey-100); color: var(--d0-grey-800); border-radius: 0 0 var(--d0-radius-sm) var(--d0-radius-sm); }
.d0-tabprev__notes { display: grid; gap: 4px; color: var(--d0-grey-600); font-size: var(--d0-text-compact); }
.d0-tabprev__notes div { display: flex; gap: 6px; }
.d0-tabprev__notes dt { font-weight: 700; color: var(--d0-grey-900); }
```

```js
document.querySelectorAll('.d0-tabprev__tabs').forEach(function (list) {
  var tabs = Array.from(list.querySelectorAll('[role="tab"]'));
  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.toggleAttribute('data-selected', on);
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }
  list.addEventListener('click', function (e) { var t = e.target.closest('[role="tab"]'); if (t) select(t); });
  list.addEventListener('keydown', function (e) {
    var i = tabs.indexOf(document.activeElement), d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
    if (i < 0 || !d) return;
    var next = tabs[(i + d + tabs.length) % tabs.length]; select(next); next.focus();
  });
});
```

## 금지

- 데이터 열 7개 이상으로 가로 스크롤, 실제 개인 데이터·상호·연락처처럼 보이는 값.
- `예시 데이터` 표시 없이 실제 결과물처럼 보이게 두기.
