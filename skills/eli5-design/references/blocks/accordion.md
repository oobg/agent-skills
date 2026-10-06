# accordion — 질문 답변·선택 펼침

## 해부 구조

- FAQ 기본은 `data-variant="reply"`다. 질문 4~6개를 `<dl>` → `<div>` → `<dt>` 질문 + `<dd>` 답(3문장 이내)으로 묶는다. 답변은 질문에 종속된 reply이며 항상 노출한다.
- 질문은 15px/600, 답은 14px/400 grey-700이다. 질문 아래 답을 16~24px 들여쓰고 질문 사이 24~32px를 둔다. 375px에서도 들여쓰기를 유지한다.
- 왼쪽 1px grey-200 연결선은 질문 아래에서 내려와 답 첫 줄로 꺾인다. CSS pseudo-element로만 그리고 꺾임점의 작은 점만 blue를 쓴다. 질문·답 박스와 Q 배지는 없다.
- 질문 묶음 전체는 `<section>`의 h2 아래 둔다. guide의 선택 보조 정보에만 `<details>` → `<summary>` → 답을 쓰며 JS 없이 동작한다. summary 안에 제목 태그를 넣지 않는다.

## 언제 쓰나 / 변형

- faq의 질문은 reply를 쓴다. guide의 "막혔을 때"처럼 선택적으로 확인하는 보조 정보는 details 펼침을 쓸 수 있다.
- `data-variant="terms"`(용어 목록): 펼침 없이 `<dl>`로 나열한다. 행 = `<dt>` 용어(약어면 `<abbr title>`) → `<dd>` 한 줄 뜻 → 비유.

## 스니펫

```html
<!-- FAQ: 답을 항상 노출하는 reply -->
<dl class="d0-acc" data-variant="reply">
  <div><dt>내보내기는 얼마나 걸려요?</dt><dd>보통 2분 안에 끝나요. 주문이 많으면 은행 번호표처럼 차례를 기다려요.</dd></div>
  <div><dt>파일은 언제까지 받을 수 있어요?</dt><dd>만든 날부터 <time datetime="P30D">30일</time> 동안 받을 수 있어요.</dd></div>
</dl>
<!-- guide의 선택 보조 정보: 펼침 -->
<div class="d0-acc">
  <details open>
    <summary>내보내기는 얼마나 걸려요?</summary>
    <p>보통 2분 안에 끝나요. 주문이 많으면 은행 번호표처럼 차례를 기다려요.</p>
  </details>
  <details>
    <summary>파일은 언제까지 받을 수 있어요?</summary>
    <p>만든 날부터 <time datetime="P30D">30일</time> 동안 받을 수 있어요.</p>
  </details>
</div>
<!-- 용어 목록 변형 -->
<dl class="d0-acc" data-variant="terms">
  <div><dt>대기열</dt><dd>먼저 온 일부터 처리하는 줄이에요. <span>은행 번호표와 같아요.</span></dd></div>
  <div><dt><abbr title="쉼표로 값을 나눈 표 파일">CSV</abbr></dt><dd>엑셀로 열 수 있는 가벼운 표 파일이에요.</dd></div>
</dl>
```

```css
.d0-acc[data-variant="reply"] { display: grid; gap: 28px; margin: 0; }
.d0-acc[data-variant="reply"] > div { min-width: 0; }
.d0-acc[data-variant="reply"] dt { font-size: 15px; font-weight: 600; }
.d0-acc[data-variant="reply"] dd {
  position: relative; margin: 8px 0 0 24px;
  font-size: 14px; font-weight: 400; color: var(--d0-grey-700);
  line-height: var(--d0-leading-body); overflow-wrap: anywhere;
}
.d0-acc[data-variant="reply"] dd::before {
  content: ""; position: absolute; left: -16px; top: -8px;
  width: 10px; height: 19px;
  border-left: 1px solid var(--d0-grey-200); border-bottom: 1px solid var(--d0-grey-200);
}
.d0-acc[data-variant="reply"] dd::after {
  content: ""; position: absolute; left: -18px; top: 9px;
  width: 4px; height: 4px; border-radius: 50%; background: var(--d0-blue);
}
.d0-acc details { border-top: 1px solid var(--d0-grey-100); }
.d0-acc summary {
  display: flex; justify-content: space-between; align-items: center; gap: 12px;
  min-height: 24px; padding: 14px 0; list-style: none; cursor: pointer;
  font-weight: 600;
}
.d0-acc summary::-webkit-details-marker { display: none; }
.d0-acc summary::after { content: "+" / ""; flex: none; color: var(--d0-grey-600); transition: transform var(--d0-dur) var(--d0-ease); }
.d0-acc details[open] summary::after { transform: rotate(45deg); }
.d0-acc details > p { padding-bottom: 14px; color: var(--d0-grey-700); }
.d0-acc[data-variant="terms"] > div { display: grid; gap: 2px; padding: 14px 0; border-top: 1px solid var(--d0-grey-100); }
.d0-acc[data-variant="terms"] dt { font-weight: 600; }
.d0-acc[data-variant="terms"] dd span { color: var(--d0-grey-600); }
.d0-acc abbr { text-decoration: none; }
```

## 금지

- FAQ 답을 details로 접기, 질문·답 박스나 Q 배지, 연결선을 문자(`ㄴ`, `>`)로 만들기.
- `div`+`button`+`aria-expanded`로 펼침을 다시 만들기(`details`로 충분하다), 핵심 답을 접어서 가리기, 답 3문장 초과.
- 용어를 다른 용어로 설명하기(비유는 일상 사물로).
