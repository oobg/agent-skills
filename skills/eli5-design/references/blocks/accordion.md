# accordion — 질문 펼침

## 해부 구조

- 질문 4~6개. 행 = 질문 버튼(`aria-expanded`) → 답(3문장 이내). 행 사이 1px 디바이더.
- 가장 중요한 첫 질문만 `data-open`으로 펼쳐 둔다.
- 펼침 상태는 `data-open`과 `aria-expanded`를 함께 바꾼다.

## 언제 쓰나 / 변형

- faq의 질문, guide의 "막혔을 때".
- `data-variant="terms"`(용어 카드): 펼침 없이 행으로 나열한다. 행 = 용어 → 한 줄 뜻 → 비유.

## 스니펫

```html
<div class="d0-acc">
  <div class="d0-acc__item" data-open>
    <h3><button type="button" aria-expanded="true" aria-controls="acc-1">내보내기는 얼마나 걸려요?</button></h3>
    <div class="d0-acc__panel" id="acc-1"><div><p>보통 2분 안에 끝나요. 주문이 많으면 은행 번호표처럼 차례를 기다려요.</p></div></div>
  </div>
  <div class="d0-acc__item">
    <h3><button type="button" aria-expanded="false" aria-controls="acc-2">파일은 언제까지 받을 수 있어요?</button></h3>
    <div class="d0-acc__panel" id="acc-2"><div><p>만든 날부터 30일 동안 받을 수 있어요.</p></div></div>
  </div>
</div>
<!-- 용어 카드 변형 -->
<dl class="d0-acc" data-variant="terms">
  <div class="d0-acc__item"><dt>대기열</dt><dd>먼저 온 일부터 처리하는 줄이에요. <span>은행 번호표와 같아요.</span></dd></div>
</dl>
```

```css
.d0-acc__item { border-top: 1px solid var(--d0-grey-100); }
.d0-acc h3 { font-size: 15px; font-weight: 600; }
.d0-acc button {
  display: flex; justify-content: space-between; gap: 12px;
  width: 100%; padding: 14px 0; border: 0; background: none; text-align: left;
}
.d0-acc button::after { content: "+" / ""; color: var(--d0-grey-600); transition: transform var(--d0-dur) var(--d0-ease); }
.d0-acc__item[data-open] button::after { transform: rotate(45deg); }
.d0-acc__panel { display: grid; grid-template-rows: 0fr; visibility: hidden; transition: grid-template-rows var(--d0-dur) var(--d0-ease), visibility var(--d0-dur); }
.d0-acc__item[data-open] .d0-acc__panel { grid-template-rows: 1fr; visibility: visible; }
.d0-acc__panel > div { overflow: hidden; }
.d0-acc__panel p { padding-bottom: 14px; color: var(--d0-grey-700); }
.d0-acc[data-variant="terms"] .d0-acc__item { display: grid; gap: 2px; padding: 14px 0; }
.d0-acc[data-variant="terms"] dt { font-weight: 600; }
.d0-acc[data-variant="terms"] dd span { color: var(--d0-grey-600); }
```

```js
document.querySelectorAll('.d0-acc:not([data-variant="terms"])').forEach(function (acc) {
  acc.addEventListener('click', function (e) {
    var btn = e.target.closest('button[aria-expanded]');
    if (!btn) return;
    var open = btn.closest('.d0-acc__item').toggleAttribute('data-open');
    btn.setAttribute('aria-expanded', String(open));
  });
});
```

## 금지

- 핵심 답을 접어서 가리기, 답 3문장 초과.
- 용어를 다른 용어로 설명하기(비유는 일상 사물로).
