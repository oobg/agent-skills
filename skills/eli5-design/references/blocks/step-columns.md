# step-columns — 단계 열

## 해부 구조

- 2~5열. 열마다 블루 단계 라벨(`1단계`, 12px/600 blue-dark) → 소제목 h3(16px) → 굵은 항목명 + 설명 한 줄 쌍(14px).
- 단계 열은 그림을 거드는 주석이다. 같은 섹션의 그림(도식·격자 카드) 바로 아래에 둔다. 열마다 설명은 두 줄 이내.
- 순서가 있으므로 `<ol>`, 열마다 `<li>`, 라벨-값 쌍은 `<dl>`.
- 열 너비는 같게, 모든 열이 같은 구조를 갖는다.
- 열 사이는 1px 디바이더로 나눈다. 카드 박스로 감싸지 않는다.

## 언제 쓰나 / 변형

- flow에서 단계마다 "누가 무엇을 하고 무엇이 나오는가"를 나란히 보여 줄 때.
- 640px 이하에서는 세로로 쌓이고, 디바이더가 위쪽 가로선으로 바뀐다.
- **자리(page).** 2~4열은 읽기 축(기본 720px, report 960px)에 둔다. 5열은 축 720px에서 칸이 144px라 열 그림과 `dd` 한 문장이 들어가지 않으므로 `<div class="d0-wide">` 바로 안에 `ol.d0-steps` 하나로 두고 오른쪽만 프레임 끝까지 넓힌다(2열 `.d0-cols`로 감싸지 않는다, [shell.md](shell.md) 넓은 구간 (c)). report 축 960px에서는 5열도 칸이 192px라 축에 둘 수 있다.
- `data-variant="figure"`(그림+설명 단계 열): 열마다 작은 SVG 한 장 + `하는 일`·`나오는 것` dl. 위에 따로 도식이 없을 때 이 블록이 그림 블록이 된다.
- **사실 단계가 5를 넘으면 의미 단위로 묶어 2~5열로 줄인다.** 열 라벨은 묶은 범위(`1~3단계`)로 쓰고, h3는 묶음 이름이다.
  예: 내보내기 8단계(기간·팀·형식 고르기 / 모으기·계산·파일 만들기 / 알림·받기) → `고르기`(1~3) · `만들기`(4~6) · `받기`(7~8) 3열.
  묶음 안의 세부 단계는 `하는 일` 한 문장에 나열한다. 열을 6개 이상 두거나 글자를 줄여 다 넣지 않는다.

## 그림+설명 단계 열 (`data-variant="figure"`)

```html
<ol class="d0-steps" data-variant="figure">
  <li class="d0-step">
    <span class="d0-step__label">1~3단계</span>
    <div class="d0-step__fig">
      <svg viewBox="0 0 160 96" role="img" aria-labelledby="sf1-t">
        <title id="sf1-t">세 가지 중 하나를 고른 목록</title>
        <rect class="d0-s-frame" x="1" y="1" width="158" height="94" rx="10"/>
        <rect class="d0-s-fill" x="16" y="16" width="128" height="16" rx="5"/>
        <rect class="d0-s-zone" x="16" y="40" width="128" height="16" rx="5"/>
        <rect class="d0-s-fill" x="16" y="64" width="128" height="16" rx="5"/>
      </svg>
    </div>
    <h3>고르기</h3>
    <dl><dt>하는 일</dt><dd>기간, 팀, 형식을 차례로 골라요.</dd><dt>나오는 것</dt><dd>내보낼 주문 목록이에요.</dd></dl>
  </li>
  <li class="d0-step">
    <span class="d0-step__label">4~6단계</span>
    <div class="d0-step__fig">
      <svg viewBox="0 0 160 96" role="img" aria-labelledby="sf2-t">
        <title id="sf2-t">합계 열이 붙은 표</title>
        <rect class="d0-s-cell" x="16" y="16" width="36" height="16" rx="3"/><rect class="d0-s-cell" x="58" y="16" width="36" height="16" rx="3"/><rect class="d0-s-sum" x="100" y="16" width="44" height="16" rx="3"/>
        <rect class="d0-s-cell" x="16" y="40" width="36" height="16" rx="3"/><rect class="d0-s-cell" x="58" y="40" width="36" height="16" rx="3"/><rect class="d0-s-sum" x="100" y="40" width="44" height="16" rx="3"/>
        <rect class="d0-s-cell" x="16" y="64" width="36" height="16" rx="3"/><rect class="d0-s-cell" x="58" y="64" width="36" height="16" rx="3"/><rect class="d0-s-sum" x="100" y="64" width="44" height="16" rx="3"/>
      </svg>
    </div>
    <h3>만들기</h3>
    <dl><dt>하는 일</dt><dd>주문을 모아 팀별로 더해 파일을 만들어요.</dd><dt>나오는 것</dt><dd>합계 열이 붙은 표예요.</dd></dl>
  </li>
  <li class="d0-step">
    <span class="d0-step__label">7~8단계</span>
    <div class="d0-step__fig">
      <svg viewBox="0 0 160 96" role="img" aria-labelledby="sf3-t">
        <title id="sf3-t">받기가 끝난 파일</title>
        <path class="d0-s-frame" d="M52 12 H96 L112 28 V84 H52 Z"/>
        <path class="d0-s-line" d="M64 44 H100 M64 56 H100 M64 68 H88"/>
        <circle class="d0-s-node" data-tone="green" cx="112" cy="76" r="12"/>
        <path class="d0-s-tick" d="M106 76 L110 80 L118 71"/>
      </svg>
    </div>
    <h3>받기</h3>
    <dl><dt>하는 일</dt><dd>알림을 눌러 파일을 내려받아요.</dd><dt>나오는 것</dt><dd>내 컴퓨터에 저장된 파일이에요.</dd></dl>
  </li>
</ol>
```

```css
/* diagram.md 공용 CSS(.d0-s-*)를 함께 쓴다 */
.d0-steps[data-variant="figure"] .d0-step__fig { display: grid; place-items: center; padding: 16px; border-radius: var(--d0-radius-card); background: var(--d0-grey-50); }
.d0-step__fig svg { display: block; width: 100%; max-width: 200px; height: auto; }
```

- 열 SVG는 글자 없음(라벨 크기 게이트 밖). 이름은 h3, 접근 이름은 `<title>`이 맡는다. 모든 열이 같은 viewBox(160×96)다.
- 열마다 blue나 의미색 표식은 하나다. 끝난 결과는 green 원 + 흰 체크. 회색만인 열 그림은 금지다.
- dl 짝은 `하는 일`·`나오는 것` 두 개로 고정한다. 각 dd는 한 문장이다.

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
.d0-step__label { color: var(--d0-blue-dark); font-size: var(--d0-meta); font-weight: 600; }
.d0-step dt { margin-top: 4px; font-size: 14px; font-weight: 600; }
.d0-step dd { color: var(--d0-grey-600); font-size: 14px; }
@media (max-width: 640px) {
  .d0-steps { grid-auto-flow: row; }
  .d0-step { padding: 16px 0; }
  .d0-step + .d0-step { border-left: 0; border-top: 1px solid var(--d0-grey-100); }
}
```

## 금지

- 열마다 다른 구조, 설명 3문장 초과, 6열 이상(사실 단계가 많으면 의미 단위로 묶는다).
- 그림 변형에서 열마다 다른 viewBox, SVG 안 글자, 회색뿐인 열 그림.
- 열마다 보더 카드.
