# section-head — 섹션 머리

## 해부 구조

- 섹션(`.d0-section`) = 위쪽 1px 구분선 + 세로 패딩 36px + 그룹 간격 24px. shell에 정의돼 있다.
- 섹션은 `<section aria-labelledby="h2 id">`, 머리는 섹션 안 `<header>`. 머리 = h2(18px/700) → 필요하면 설명 한 줄(15px grey-600).
- **태그 pill은 기본 없음.** 제목만으로 알 수 없는 정보(예: `눌러 볼 수 있어요`, `예시 데이터`, `예상치`)가 있을 때만 하나 붙인다.
  정보가 있는 태그도 같은 태그는 페이지당 1회만 쓴다.
- 섹션마다 한 가지 일. 앞쪽 핵심 섹션은 그림 하나, 목록 섹션(위험·한계·할 일)은 그림 없이 둘 수 있다. 섹션은 페이지당 2~4개(기본 3~4개).

## 언제 쓰나 / 변형

- header 다음의 모든 구획 앞에 둔다.
- 설명이 그림 주석으로 충분하면 설명 줄을 뺀다. 제목이 결론을 말하게 쓴다("PR 검사가 26분에서 10분으로").

## 스니펫

```html
<section class="d0-section" aria-labelledby="sec-sheets">
  <header class="d0-section-head">
    <h2 id="sec-sheets">파일 안에는 시트가 두 장 있어요</h2>
    <p>요약 시트는 팀별 합계, 상세 시트는 주문 한 건이 한 줄이에요.</p>
  </header>
  <!-- 앞쪽 핵심 섹션은 그림 하나, 목록 섹션은 그림 없이 둘 수 있다 -->
</section>
<!-- 정보가 있는 태그가 필요할 때만 -->
<header class="d0-section-head">
  <div class="d0-section-head__title"><h2 id="sec-demo">두 가지 시안</h2><span class="d0-pill" data-tone="blue">눌러 볼 수 있어요</span></div>
</header>
```

```css
.d0-section-head { display: grid; gap: 6px; }
.d0-section-head__title { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.d0-section-head p { color: var(--d0-grey-600); }
```

## 금지

- 모든 h2에 태그 붙이기(`그림`, `위험` 같은 반복 태그는 소음이다), 정보가 있는 태그를 섹션마다 반복하기.
- 설명 두 줄 이상, 섹션 5개 이상, 섹션마다 다른 머리 모양.
