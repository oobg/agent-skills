# flow-line — 한 줄 흐름

## 해부 구조

- `A → B → C` 한 줄. 노드는 짧은 명사, 화살표는 노드 사이 텍스트 기호.
- 현재 단계만 `data-current`(+ `aria-current="step"`)로 blue-dark 채움 + 흰 글자(5.50) + 점 표시, 나머지는 회색. 기준 톤의 활성 칩 모양이다(blue 채움은 흰 글자 3.99라 안 쓴다).
- 노드 3~5개. 모바일에서 줄이 바뀌어도 화살표는 앞 노드에 붙어 줄 끝에 남는다.

## 언제 쓰나 / 변형

- 이 블록은 글 한 줄이지 도식이 아니다. 같은 섹션에 SVG 도식이나 그림 카드가 함께 있어야 한다. flow-line만으로 그림 게이트를 채우지 않는다.

- 페이지 위쪽에서 "전체가 어떻게 흘러가는가"를 한눈에 보여 줄 때(flow, preview, compare 전/후).
- 노드가 같은 페이지 섹션으로 이동하는 링크면 `<nav aria-label>` 안 `<ol>`에 `<a>`를 쓴다. 이동이 없으면 `<ol>`만 쓴다.
- 현재 단계가 없으면 `data-current`를 빼고 모두 회색으로 둔다.

## 스니펫

```html
<ol class="d0-flow" aria-label="내보내기 흐름">
  <li class="d0-flow__node"><span>주문 고르기</span></li>
  <li class="d0-flow__node" data-current aria-current="step"><span>파일 만들기</span></li>
  <li class="d0-flow__node"><span>내려받기</span></li>
  <li class="d0-flow__node"><span>팀에 공유</span></li>
</ol>
```

```css
.d0-flow {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 10px;
}
.d0-flow__node { display: flex; align-items: center; gap: 10px; }
.d0-flow__node span {
  padding: 8px 12px;
  border-radius: var(--d0-radius-sm);
  background: var(--d0-grey-50);
  color: var(--d0-grey-600);
  font-weight: 600;
}
.d0-flow__node:not(:last-child)::after {
  content: "→" / "";
  color: var(--d0-grey-600);
}
.d0-flow__node[data-current] span {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--d0-blue-dark);
  color: #fff;
}
/* 색만으로 현재를 말하지 않도록 점 모양을 함께 둔다 */
.d0-flow__node[data-current] span::before {
  content: ""; width: 6px; height: 6px; border-radius: 999px; background: currentColor;
}
```

## 금지

- 모든 노드를 블루로 칠하기, 노드 안에 문장 쓰기.
- 노드 6개 이상(묶어서 5개 이하로).
