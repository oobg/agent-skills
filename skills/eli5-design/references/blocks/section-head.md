# section-head — 섹션 머리

## 해부 구조

- 제목 h2 + 회색 pill 태그(예: `미리보기`, `결정 필요`) → 설명 한 줄.
- 섹션마다 같은 모양으로 반복해 독자가 구획을 바로 알아보게 한다.
- 섹션 안 블록은 머리 아래에 같은 간격으로 쌓인다.

## 언제 쓰나 / 변형

- header 다음의 모든 구획 앞에 둔다. 블록 하나짜리 섹션도 머리를 둔다.
- 태그는 회색이 기본이다. 결정이 필요한 섹션만 `data-tone="orange"`를 쓸 수 있다.

## 스니펫

```html
<section class="d0-section" aria-labelledby="sec-sheets">
  <div class="d0-section-head">
    <div class="d0-section-head__title">
      <h2 id="sec-sheets">파일 안에는 시트가 두 장 있어요</h2>
      <span class="d0-pill">미리보기</span>
    </div>
    <p>요약 시트는 팀별 합계만, 상세 시트는 주문 한 건을 한 줄로 보여 줘요.</p>
  </div>
  <!-- 이 섹션의 블록 -->
</section>
```

```css
.d0-section > * + * { margin-top: 20px; }
.d0-section-head { display: grid; gap: 6px; }
.d0-section-head__title {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
.d0-section-head h2 { font-size: 17px; font-weight: 650; }
.d0-section-head p { color: var(--d0-grey-600); }
```

## 금지

- 설명 두 줄 이상, 태그를 블루로 칠하기(블루는 현재·강조 전용).
- 섹션마다 다른 머리 모양.
