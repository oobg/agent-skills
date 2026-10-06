# step-columns — 단계 열

## 해부 구조

- 2~4열. 열마다 블루 단계 라벨(`1단계`) → 소제목 h3 → 굵은 항목명 + 설명 한 줄 쌍.
- 열 너비는 같게, 모든 열이 같은 구조를 갖는다.
- 열 사이는 1px 디바이더로 나눈다. 카드 박스로 감싸지 않는다.

## 언제 쓰나 / 변형

- flow에서 단계마다 "누가 무엇을 하고 무엇이 나오는가"를 나란히 보여 줄 때.
- 640px 이하에서는 세로로 쌓이고, 디바이더가 위쪽 가로선으로 바뀐다.

## 스니펫

```html
<ol class="d0-steps">
  <li class="d0-step">
    <span class="d0-step__label">1단계</span>
    <h3>고르기</h3>
    <dl>
      <dt>누가</dt><dd>팀 A 담당자가 기간과 팀을 골라요.</dd>
      <dt>나오는 것</dt><dd>내보낼 주문 목록이에요.</dd>
    </dl>
  </li>
  <li class="d0-step">
    <span class="d0-step__label">2단계</span>
    <h3>만들기</h3>
    <dl>
      <dt>누가</dt><dd>시스템이 차례대로 파일을 만들어요.</dd>
      <dt>나오는 것</dt><dd>시트 두 장짜리 파일이에요.</dd>
    </dl>
  </li>
  <li class="d0-step">
    <span class="d0-step__label">3단계</span>
    <h3>받기</h3>
    <dl>
      <dt>누가</dt><dd>담당자가 알림을 눌러 내려받아요.</dd>
      <dt>나오는 것</dt><dd>내 컴퓨터에 저장된 파일이에요.</dd>
    </dl>
  </li>
</ol>
```

```css
.d0-steps { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); }
.d0-step { display: grid; gap: 8px; align-content: start; padding: 4px 20px; }
.d0-step + .d0-step { border-left: 1px solid var(--d0-grey-100); }
.d0-step:first-child { padding-left: 0; }
.d0-step__label { color: var(--d0-blue-dark); font-size: var(--d0-text-compact); font-weight: 600; }
.d0-step h3 { font-size: 15px; font-weight: 650; }
.d0-step dt { margin-top: 4px; font-weight: 600; }
.d0-step dd { color: var(--d0-grey-600); }
@media (max-width: 640px) {
  .d0-steps { grid-auto-flow: row; }
  .d0-step { padding: 16px 0; }
  .d0-step + .d0-step { border-left: 0; border-top: 1px solid var(--d0-grey-100); }
}
```

## 금지

- 열마다 다른 구조, 설명 3문장 초과, 5열 이상.
- 열마다 보더 카드.
