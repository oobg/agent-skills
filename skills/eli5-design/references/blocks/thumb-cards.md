# thumb-cards — 그림 카드

## 해부 구조

- 3~5장. 각 장 = 그림(미니 격자 또는 와이어프레임 SVG) → 이름(15px/600) → 필요하면 배지 하나.
- 그림이 카드 면적의 대부분이다. 카드 안에 설명 문단을 넣지 않는다(이름과 배지면 충분).
- 같은 크기·같은 정보량. 카드는 흰 면 + 1px grey-200 테두리(기준 톤의 예외 허용). hover에서 테두리가 블루로 바뀌고 2px 올라온다. reduced-motion이면 올라오지 않는다.
- 그림은 [diagram.md](diagram.md)의 (c) 미니 격자 `d0Grid()`나 (d) 와이어프레임을 작게 쓴다. 장마다 실제 모양이 달라야 한다.
- 배지는 [shell.md](shell.md)의 `.d0-pill` 규칙(높이 22px 고정, 톤별 대비)을 그대로 쓴다.

## 언제 쓰나 / 변형

- "무엇이 몇 개 있고 각각 어떤 모양인가"를 첫 화면에 보여 줄 때(결과물 묶음, 화면 목록, 시안 목록).
- 카드가 섹션 이동 링크면 `<li>` 안을 `<a class="d0-thumb">`로 만든다. 아니면 `<li class="d0-thumb">`만 쓴다.
- 배지는 상태가 서로 다를 때만 단다(`지금 가능`·`준비 중`). 전부 같은 배지면 뺀다.
- 용어 변형(faq): 이름 아래 한 줄 비유(`.d0-thumb__note`, 13px)를 허용한다. 두 줄 이상이면 accordion으로 보낸다.

## 스니펫

```html
<ul class="d0-thumbs">
  <li class="d0-thumb">
    <div data-grid='{"rows":7,"cols":5,"sumCol":true,"seed":2,"label":"팀 행 × 합계 열 표"}'></div>
    <strong>팀별 합계</strong>
    <span class="d0-pill" data-tone="green">지금 가능</span>
  </li>
  <li class="d0-thumb">
    <div data-grid='{"rows":8,"cols":9,"sumRow":true,"blanks":0.18,"seed":5,"label":"상품 행 × 일자 열 표"}'></div>
    <strong>상품 × 일자</strong>
    <span class="d0-pill" data-tone="orange">준비 중</span>
  </li>
  <li class="d0-thumb">
    <div data-grid='{"rows":5,"cols":4,"keyCol":false,"sumRow":true,"seed":4,"label":"월 행 요약 표"}'></div>
    <strong>월별 요약</strong>
    <span class="d0-pill" data-tone="green">지금 가능</span>
  </li>
  <li class="d0-thumb">
    <svg viewBox="0 0 160 96" role="img" aria-labelledby="t4-t">
      <title id="t4-t">받기 화면 골격, 오른쪽 위 버튼 강조</title>
      <rect class="d0-s-frame" x="1" y="1" width="158" height="94" rx="8"/>
      <path class="d0-s-line" d="M1 22 H159"/>
      <rect class="d0-s-fill" x="10" y="9" width="40" height="6" rx="3"/>
      <rect class="d0-s-accent" x="116" y="7" width="34" height="10" rx="3"/>
      <rect class="d0-s-fill" x="10" y="32" width="66" height="26" rx="5"/>
      <rect class="d0-s-fill" x="84" y="32" width="66" height="26" rx="5"/>
      <rect class="d0-s-fill" x="10" y="68" width="140" height="7" rx="3"/>
      <rect class="d0-s-fill" x="10" y="80" width="96" height="7" rx="3"/>
    </svg>
    <strong>받기 화면</strong>
    <span class="d0-pill" data-tone="blue">새 화면</span>
  </li>
</ul>
<!-- data-grid는 diagram.md (c)의 d0Grid() 스크립트가 SVG로 바꾼다. d0-s-* 클래스도 diagram.md 공용 CSS. -->
```

```css
.d0-thumbs { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }
.d0-thumb {
  display: grid; grid-template-rows: auto auto 1fr; gap: 10px; align-content: start;
  padding: 16px; border: 1px solid var(--d0-grey-200); border-radius: var(--d0-radius-card); background: #fff;
  color: inherit; text-decoration: none;
  transition: border-color var(--d0-dur) var(--d0-ease), transform var(--d0-dur) var(--d0-ease);
}
.d0-thumb:hover, a.d0-thumb:focus-visible { border-color: var(--d0-blue); transform: translateY(-2px); }
.d0-thumb svg { width: 100%; height: auto; padding: 8px; border-radius: var(--d0-radius-sm); background: var(--d0-grey-50); }
.d0-thumb strong { font-size: 15px; font-weight: 600; letter-spacing: var(--d0-tracking-title); }
.d0-thumb__note { color: var(--d0-grey-600); font-size: var(--d0-text-compact); }
@media (prefers-reduced-motion: reduce) { .d0-thumb:hover, a.d0-thumb:focus-visible { transform: none; } }
```

- 썸네일 바탕은 grey-50 판(`svg` padding 8px)이다. 머리 행 blue-light가 흰 카드에 묻히지 않게 한다.

## 금지

- 장마다 같은 그림(아이콘만 바꾼 카드), 그림 대신 아이콘·이모지.
- 카드 안 설명 문단, 장마다 다른 높이나 정보량, 그림자 박스, 카드마다 같은 배지.
