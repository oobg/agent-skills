# faq — 질문 답변 reply

## 해부 구조

- 질문 4~6개를 `<dl class="d0-faq">` → `<div class="d0-faq__item">` → `<dt class="d0-faq__q">` 질문 + `<dd class="d0-faq__answer">` 답(3문장 이내)으로 묶는다. 답변은 질문에 종속된 reply이며 항상 노출한다.
- 질문은 15px/600, 답은 14px/400 grey-700이다. 질문 아래 답을 16~24px 들여쓰고 질문 사이 24~32px를 둔다. 375px에서도 들여쓰기를 유지한다.
- 왼쪽 1px grey-300 연결선은 질문 아래에서 내려와 답 첫 줄로 꺾인다. CSS pseudo-element로만 그리며 점은 두지 않는다. 질문·답 박스와 Q 배지는 없다.
- 질문 묶음 전체는 `<section>`의 h2 아래 둔다. "답을 못 찾았나요" 한 줄은 묶음 바로 아래 `p.d0-faq__more`로 둔다.

## 언제 쓰나

- faq의 질문과 guide의 "막혔을 때"는 이 블록을 쓴다. 접어서 보는 선택 보조 정보와 용어 목록은 [accordion](accordion.md)이다.
- 답을 접어서 가리지 않는다. 핵심 답이 길어지면 문장을 줄이거나 질문을 나눈다.

## 스니펫

```html
<dl class="d0-faq">
  <div class="d0-faq__item"><dt class="d0-faq__q">내보내기는 얼마나 걸려요?</dt><dd class="d0-faq__answer">보통 2분 안에 끝나요. 주문이 많으면 은행 번호표처럼 차례를 기다려요.</dd></div>
  <div class="d0-faq__item"><dt class="d0-faq__q">파일은 언제까지 받을 수 있어요?</dt><dd class="d0-faq__answer">만든 날부터 <time datetime="P30D">30일</time> 동안 받을 수 있어요.</dd></div>
</dl>
<p class="d0-faq__more">답을 못 찾았나요? 도움말 센터에서 찾아보세요.</p>
```

```css
.d0-faq { display: grid; gap: 28px; margin: 0; }
.d0-faq__item { min-width: 0; }
.d0-faq__q { font-size: 15px; font-weight: 600; }
.d0-faq__answer {
  position: relative; margin: 8px 0 0 24px;
  font-size: 14px; font-weight: 400; color: var(--d0-grey-700);
  line-height: var(--d0-leading-body); overflow-wrap: anywhere;
}
.d0-faq__answer::before {
  content: ""; position: absolute; left: -16px; top: -8px;
  width: 14px; height: calc(8px + 0.5em * var(--d0-leading-body));
  border-left: 1px solid var(--d0-grey-300); border-bottom: 1px solid var(--d0-grey-300);
}
.d0-faq abbr { text-decoration: none; }
.d0-faq__more { color: var(--d0-grey-600); font-size: 14px; }
```

## 금지

- 답을 `details`로 접기, 질문·답 박스나 Q 배지, 연결선을 문자(`ㄴ`, `>`)로 만들기.
- 답 3문장 초과, 용어를 다른 용어로 설명하기(비유는 일상 사물로).
