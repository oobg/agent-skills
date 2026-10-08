# accordion — 선택 펼침·용어 목록

## 해부 구조

- 선택 보조 정보에만 `<details>` → `<summary>` → 답을 쓰며 JS 없이 동작한다. summary 안에 제목 태그를 넣지 않는다. 핵심 답은 접어서 가리지 않는다.
- 질문·답(faq, guide "막혔을 때")은 접지 않고 항상 노출하는 [faq](faq.md)(답글형)를 쓴다.
- 섹션 본 흐름에서 빼낸 세부 한 덩어리(계산 과정, 전체 표)는 이 블록이 아니라 [shell/contract.md](../shell/contract.md)의 `.d0-more` 접기 하나다. accordion은 여러 선택 보조 항목의 목록이다.

## 언제 쓰나 / 변형

- 별도의 선택 보조 정보(추가 설명, 옵션 상세)에만 details 펼침을 쓴다.
- `data-variant="terms"`(용어 목록): 펼침 없이 `<dl>`로 나열한다. 행 = `<dt>` 용어(약어면 `<abbr title>`) → `<dd>` 한 줄 뜻 → 비유.

## 스니펫

```html
<!-- 선택 보조 정보: 펼침 -->
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

- 질문·답(FAQ)을 details로 접기. 질문·답은 faq.md를 쓴다.
- `div`+`button`+`aria-expanded`로 펼침을 다시 만들기(`details`로 충분하다), 핵심 답을 접어서 가리기, 답 3문장 초과.
- 용어를 다른 용어로 설명하기(비유는 일상 사물로).
