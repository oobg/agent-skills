# thumb-cards — 그림 카드

## 해부 구조

- 3~5장. 각 장 = 그림(미니 격자 또는 와이어프레임 SVG) → 이름(15px/600) → 상태 배지 하나(카드마다 1개까지).
- 그림이 카드 면적의 대부분이다. 카드 안에 설명 문단을 넣지 않는다(이름과 배지면 충분).
- 같은 크기·같은 정보량. 카드는 흰 면 + 1px grey-200 테두리(기준 톤의 예외 허용). hover에서 테두리가 블루로 바뀌고 2px 올라온다. reduced-motion이면 올라오지 않는다.
- 그림은 [diagram.md](diagram.md)의 (c) 미니 격자 `d0Grid()`나 (d) 와이어프레임을 작게 쓴다. 장마다 실제 모양이 달라야 한다.
- 배지는 [shell.md](shell.md)의 `.d0-pill` 규칙(높이 22px 고정, 톤별 대비)을 그대로 쓴다.
- 색: 격자는 머리 행 blue-light, 합계 blue, 키 열 grey-400이 기본이다. 와이어프레임은 바뀌는 곳 하나를 blue로. 회색만 있는 썸네일은 금지다.

## 언제 쓰나 / 변형

- "무엇이 몇 개 있고 각각 어떤 모양인가"를 첫 화면에 보여 줄 때(결과물 묶음, 화면 목록, 시안 목록).
- 카드가 섹션 이동 링크면 `<li>` 안을 `<a class="d0-thumb">`로 만든다. 아니면 `<li class="d0-thumb">`만 쓴다.
- 카드끼리 상태가 갈리면 기본 상태에도 배지를 단다(`지금 가능` green / `준비 중` orange / `백엔드 필요` orange 등). 대비가 색의 이유다.
  모든 카드가 같은 상태면 배지를 빼고 섹션 설명 한 줄로 말한다. 톤 종류는 페이지 전체에서 3가지 이하([shell.md](shell.md) 색 절).
- **카드 수와 열.** 기본 격자는 `auto-fit`이라 3·5장은 한 줄을 채운다. 4장이면 `data-count="4"`로 데스크톱 4열·640px 이하 2열에 고정한다
  (`auto-fill`이나 큰 최대 폭에서는 빈 트랙이 남거나 3+1로 접힌다).
- **카드 수와 그림 폭.** 카드 그림 폭은 약 280px 이하다. 3장 이하가 전체 폭(1200px)을 나눠 그림이 그보다 커지면 `data-layout="row"`로 바꾼다:
  카드를 세로로 쌓고, 카드 안에서 그림을 왼쪽 고정폭 168px, 이름·배지를 오른쪽에 가로로 둔다(640px 이하는 다시 위아래).
- 용어 변형(faq): 이름 아래 한 줄 비유(`.d0-thumb__note`, 13px)를 허용한다. 두 줄 이상이면 accordion으로 보낸다.

## 스니펫

```html
<ul class="d0-thumbs" data-count="4">
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
.d0-thumbs { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
.d0-thumbs[data-count="4"] { grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 640px) { .d0-thumbs[data-count="4"] { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.d0-thumb {
  display: grid; grid-template-rows: auto auto 1fr; gap: 10px; align-content: start;
  padding: 16px; border: 1px solid var(--d0-grey-200); border-radius: var(--d0-radius-card); background: #fff;
  color: inherit; text-decoration: none;
  transition: border-color var(--d0-dur) var(--d0-ease), transform var(--d0-dur) var(--d0-ease);
}
.d0-thumb:hover, a.d0-thumb:focus-visible { border-color: var(--d0-blue); transform: translateY(-2px); }
.d0-thumb svg { width: 100%; height: auto; padding: 8px; border-radius: var(--d0-radius-sm); background: var(--d0-blue-light); }
.d0-thumb strong { font-size: 15px; font-weight: 600; letter-spacing: var(--d0-tracking-title); }
.d0-thumbs[data-layout="row"] { grid-template-columns: 1fr; }
.d0-thumbs[data-layout="row"] .d0-thumb { grid-template-columns: 168px 1fr; grid-template-rows: auto 1fr; column-gap: 20px; }
.d0-thumbs[data-layout="row"] .d0-thumb > :first-child { grid-row: span 2; }
@media (max-width: 640px) { .d0-thumbs[data-layout="row"] .d0-thumb { grid-template-columns: 1fr; } .d0-thumbs[data-layout="row"] .d0-thumb > :first-child { grid-row: auto; } }
.d0-thumb__note { color: var(--d0-grey-600); font-size: var(--d0-text-compact); }
@media (prefers-reduced-motion: reduce) { .d0-thumb:hover, a.d0-thumb:focus-visible { transform: none; } }
```

- 썸네일 바탕은 blue-light 판(`svg` padding 8px)이다. 카드마다 옅은 블루 면이 생겨 첫 화면 포인트 면적의 대부분을 맡는다(5장 기준 1280px에서 약 10%).
  머리 행은 blue-light 칸 + 0.75 blue 테두리라 같은 색 판 위에서도 테두리로 보인다. 와이어프레임 썸네일은 흰 `d0-s-frame`이 판 위에 놓인다.

## 금지

- 장마다 같은 그림(아이콘만 바꾼 카드), 그림 대신 아이콘·이모지.
- 카드 안 설명 문단, 장마다 다른 높이나 정보량, 그림자 박스, 카드 하나에 배지 2개 이상.
- 정보 없는 같은 배지를 모든 카드에 달기(상태가 다 같으면 배지를 뺀다), 회색만 있는 썸네일, 4장인데 빈 트랙이 남는 격자.
