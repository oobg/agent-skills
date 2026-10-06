# section-head — 섹션 머리

## 해부 구조

- 섹션(`.d0-section`) = 위쪽 1px grey-100 구분선 + 섹션 사이 64px(모바일 48) + 블록 간 24px. 값의 CSS는 shell에 있다.
- 섹션은 `<section aria-labelledby="h2 id">`, 머리는 섹션 안 `<header>`. 머리 = h2(20px/700, title 자간, 모바일 18px) → 8px → 필요하면 설명(14px grey-600).
- **설명은 최대 1문장.** 제목과 같은 말이면 생략한다. 예외는 아래 섹션 리드 변형 하나다. 결론 수치는 히어로에 있으므로 제목·설명에 되풀이하지 않는다.
- **태그 pill은 기본 없음.** 제목만으로 알 수 없는 정보(예: `눌러 볼 수 있어요`, `예시 데이터`, `예상치`)가 있을 때만 하나 붙인다.
  정보가 있는 태그도 같은 태그는 페이지당 1회만 쓴다.
- 섹션마다 독자 질문 하나. 첫 화면 섹션은 그림 하나, 그 아래는 핵심 구조가 있으면 그림을 권장하고, 그림 없는 섹션은 구조 블록(explanation·evidence·checklist 등)으로 짓는다. 섹션 수는 독자 질문이 정한다(SKILL.md 원칙 4번).
- 섹션 머리 설명은 섹션의 한 줄 요지다. 본문 설명은 라벨을 단 [explanation](explanation.md)으로 쓴다.

## 언제 쓰나 / 변형

- header 다음의 모든 구획 앞에 둔다.
- **섹션 리드 `p.d0-section-lead`.** compare의 "핵심 차이 2~3문장"처럼 표·그림 앞에 결론 방향이 필요할 때만, 머리 `header` 바로 다음에 15px grey-800 문단 하나(최대 3문장). 페이지당 1개.
- 설명이 그림 주석으로 충분하면 설명 줄을 뺀다. 제목이 결론을 말하게 쓰되, 히어로가 있으면 그 숫자 없이 쓴다
  (히어로 `26분 → 10분`이면 제목은 `어디서 줄었나`).

## 스니펫

```html
<section class="d0-section" aria-labelledby="sec-sheets">
  <header class="d0-section-head">
    <h2 id="sec-sheets">파일 안에는 시트가 두 장 있어요</h2>
    <p>요약 시트는 팀별 합계, 상세 시트는 주문 한 건이 한 줄이에요.</p>
  </header>
  <!-- 첫 화면 섹션은 그림 하나, 그림 없는 섹션은 구조 블록으로 -->
</section>
<!-- 정보가 있는 태그가 필요할 때만 -->
<header class="d0-section-head">
  <div class="d0-section-head__title"><h2 id="sec-demo">두 가지 시안</h2><span class="d0-pill" data-tone="blue">눌러 볼 수 있어요</span></div>
</header>
```

```css
.d0-section-head { display: grid; gap: 8px; }
.d0-section-head h2 { font-size: 20px; font-weight: 700; letter-spacing: var(--d0-tracking-title); line-height: var(--d0-leading-title); }
.d0-section-head__title { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.d0-section-head p { font-size: 14px; color: var(--d0-grey-600); }
.d0-section > p.d0-section-lead { color: var(--d0-grey-800); font-size: 15px; } /* shell의 .d0-section > p(14px grey-600)를 이긴다 */
@media (max-width: 640px) { .d0-section-head h2 { font-size: 18px; } }
```

## 금지

- 모든 h2에 태그 붙이기(`그림`, `위험` 같은 반복 태그는 소음이다), 정보가 있는 태그를 섹션마다 반복하기.
- 설명 2문장 이상(섹션 리드 변형 제외), 섹션 리드 4문장 이상·페이지당 2개 이상, 제목을 되풀이한 설명, 섹션마다 다른 머리 모양.
- 히어로·요약 행에 있는 숫자를 제목이나 설명에 다시 쓰기.
