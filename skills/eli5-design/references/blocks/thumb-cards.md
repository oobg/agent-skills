# thumb-cards — 썸네일 카드

## 해부 구조

- 3~5장. 각 장 = 단순 SVG 도식(선·상자 수준) → 이름 → 상태 배지(`data-status`).
- 도식은 이름을 거드는 그림이라 `aria-hidden`이다. 도식만으로 뜻을 전하면 `role="img"`와 `aria-label`을 단다.
- 같은 크기·같은 정보량. 카드는 plain이고 도식 영역만 soft 배경을 쓴다.
- 누르면 해당 섹션으로 이동해도 된다(앵커 링크).

## 언제 쓰나 / 변형

- 첫 화면에 "무엇이 몇 개 있는가"를 그림으로 보여 줄 때(시안 목록, 결과물 목록).
- 상태는 `data-status="planned|active|done"`. 배지 색은 `data-tone`으로 맞춘다.

## 스니펫

```html
<ul class="d0-thumbs">
  <li class="d0-thumb" data-status="done">
    <a href="#sec-summary">
      <svg viewBox="0 0 160 90" aria-hidden="true">
        <rect x="16" y="16" width="128" height="58" rx="6" fill="none" stroke="currentColor" stroke-width="2"/>
        <path d="M16 34h128M60 16v58" stroke="currentColor" stroke-width="2"/>
      </svg>
      <span class="d0-thumb__name">요약 시트</span>
      <span class="d0-pill" data-tone="green">완료</span>
    </a>
  </li>
  <li class="d0-thumb" data-status="active">
    <a href="#sec-detail">
      <svg viewBox="0 0 160 90" aria-hidden="true">
        <path d="M24 24h112M24 42h112M24 60h72" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <span class="d0-thumb__name">상세 시트</span>
      <span class="d0-pill" data-tone="blue">진행</span>
    </a>
  </li>
  <li class="d0-thumb" data-status="planned">
    <a href="#sec-share">
      <svg viewBox="0 0 160 90" aria-hidden="true">
        <circle cx="52" cy="45" r="16" fill="none" stroke="currentColor" stroke-width="2"/>
        <circle cx="108" cy="45" r="16" fill="none" stroke="currentColor" stroke-width="2"/>
        <path d="M68 45h24" stroke="currentColor" stroke-width="2"/>
      </svg>
      <span class="d0-thumb__name">팀 공유</span>
      <span class="d0-pill">예정</span>
    </a>
  </li>
</ul>
```

```css
.d0-thumbs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}
.d0-thumb a {
  display: grid;
  gap: 8px;
  justify-items: start;
  color: inherit;
  text-decoration: none;
}
.d0-thumb svg {
  width: 100%;
  padding: 12px;
  border-radius: var(--d0-radius-control);
  background: var(--d0-grey-50);
  color: var(--d0-grey-500);
  transition: color var(--d0-dur) var(--d0-ease);
}
.d0-thumb a:hover svg, .d0-thumb[data-status="active"] svg { color: var(--d0-blue-dark); }
.d0-thumb__name { font-weight: 600; }
```

## 금지

- 추상 3D·홀로그램·스톡 이미지, 장마다 다른 높이나 정보량.
- 카드마다 보더·그림자 박스.
