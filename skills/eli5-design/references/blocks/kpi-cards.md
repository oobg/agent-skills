# kpi-cards — 숫자 카드

## 해부 구조

- `dl.d0-kpis > div.d0-kpi` 2~4개. 카드 하나 = `dt` 짧은 라벨(명사, 12px/600 grey-600) → `dd` 큰 숫자(28px/600, 단위도 같은 크기, `tabular-nums`)
  → (선택) `dd` 전/후 막대. 라벨-값 짝이라 `dl`로 쓴다. `div`로 `dt`·`dd` 묶음을 감싸는 것은 HTML 표준이다.
  카드 라벨을 `h3`로 올리지 않는다(숫자 카드마다 제목이 생겨 제목 탐색이 시끄러워진다).
- **숫자 + 막대만.** 증감 배지·▲▼ 기호·설명 문단을 두지 않는다. 숫자와 막대가 같은 말을 세 번 하지 않게 한다.
- 숫자는 `<data value>`로 감싼다(기계가 읽는 값). 목표 대비 비율이면 `<meter>`를 쓴다. 기간이면 `<time datetime="PT6M">`.
- 카드 = 배경 grey-50, `--d0-radius-card`, 안쪽 24px(모바일 20px). 테두리·그림자 없음. 숫자는 카드 왼쪽 정렬선에 맞춘다.
- 히어로([hero.md](hero.md))와 같은 비교를 카드로 다시 둘 때는 히어로 문장을 되풀이하지 않는다. 카드는 막대 하나로 크기만 보여 준다.

## 막대 변형 (`data-variant="bar"`)

- 숫자 아래 전/후 막대 두 줄. 줄 = 라벨(12px/600 grey-600, `tabular-nums`) → 막대.
- 전 줄 라벨 = `전` + 값(`전 26분`). 후 줄 라벨 = `후`. 후 값은 바로 위 큰 숫자가 맡는다(같은 카드 안에서 숫자를 두 번 쓰지 않는다).
- 막대 폭 = 값 ÷ 큰 값 × 100%. 전 막대는 grey-400(값이 글자로 적혀 있다), 후 막대는 blue(grey-50 위 3.75:1). 높이 6px, 끝 둥글게.
- 막대는 글자 없는 `span`이라 `aria-hidden`이다. 뜻은 라벨 글자와 큰 숫자가 전한다.
- **상태 막대.** 숫자가 전/후가 아니라 상태 건수(실패·통과)면 막대 하나로 전체 중 몫을 보인다. 줄 라벨 = `전체 58건 중`, 막대 = 전체 트랙
  (`data-whole`, grey-200) 위 몫 채움 `data-tone="red|green"`(grey-50 위 3.36 · 3.26). orange는 그래픽 3:1 미달이라 상태 막대에 쓰지 않는다.
  의미색은 막대에만 쓰고 큰 숫자·라벨 글자는 grey-900·grey-600 그대로다.
- 비교가 핵심이면 [diagram.md](diagram.md)의 (b) 전/후 막대를 쓴다. diagram 전/후 막대는 비교 쌍 2개까지다.
  3쌍 이상이면 이 막대 변형(카드 하나에 쌍 하나)을 쓴다.

## 언제 쓰나 / 변형

- report·incident에서 근거 숫자를 보여 줄 때. 결론 숫자 하나뿐이면 카드 대신 [hero.md](hero.md)를 쓴다.
- 막대 없이 같은 단위 지표 4~6개를 훑으면 kpi-cards가 아니라 [evidence](evidence.md) tiles 변형이다. 비율·구성을 가로 막대 목록으로 견주면 evidence bar-list다. 한 섹션·장에 kpi-cards와 tiles를 함께 두지 않는다.
- **전 값이 0인 비교(0 → 5개)는 막대 변형에 넣지 않는다.** 전 막대가 0%라 비율이 아무 말도 하지 않는다. [hero.md](hero.md) 전 → 후(`0개 → 5개`)로 보낸다.
- 적용 전 예상치면 값 앞에 `약`을 붙인다. `예상치`라는 말은 페이지에 한 번(히어로 한 줄 뜻 등)만 쓴다.

## 스니펫

```html
<dl class="d0-kpis">
  <div class="d0-kpi" data-variant="bar">
    <dt class="d0-kpi__label">내보내기 대기</dt>
    <dd class="d0-kpi__value"><data value="6">6</data>분</dd>
    <dd class="d0-kpi__bars">
      <span class="d0-kpi__tag">전 <data value="14">14</data>분</span>
      <span class="d0-kpi__track" aria-hidden="true"><span class="d0-kpi__fill" style="width: 100%"></span></span>
      <span class="d0-kpi__tag">후</span>
      <span class="d0-kpi__track" aria-hidden="true"><span class="d0-kpi__fill" data-on style="width: 42.9%"></span></span>
    </dd>
  </div>
  <div class="d0-kpi" data-variant="bar">
    <dt class="d0-kpi__label">실패한 내보내기</dt>
    <dd class="d0-kpi__value"><data value="4">4</data>건</dd>
    <dd class="d0-kpi__bars">
      <span class="d0-kpi__tag">전체 <data value="58">58</data>건 중</span>
      <span class="d0-kpi__track" data-whole aria-hidden="true"><span class="d0-kpi__fill" data-tone="red" style="width: 6.9%"></span></span>
    </dd>
  </div>
  <div class="d0-kpi">
    <dt class="d0-kpi__label">받은 팀</dt>
    <dd class="d0-kpi__value"><data value="12">12</data>팀</dd>
  </div>
</dl>
```

```css
.d0-kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
.d0-kpi { display: grid; gap: 8px; align-content: start; padding: 24px; border-radius: var(--d0-radius-card); background: var(--d0-grey-50); }
.d0-kpi__label { color: var(--d0-grey-600); font-size: var(--d0-meta); font-weight: 600; }
.d0-kpi dd { margin: 0; min-width: 0; }
.d0-kpi__value { color: var(--d0-grey-900); font-size: 28px; font-weight: 600; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); font-variant-numeric: tabular-nums; }
.d0-kpi__bars { display: grid; grid-template-columns: max-content 1fr; align-items: center; gap: 6px 10px; margin-top: 8px; }
.d0-kpi__tag { color: var(--d0-grey-600); font-size: var(--d0-meta); font-weight: 600; font-variant-numeric: tabular-nums; white-space: nowrap; }
.d0-kpi__track { display: block; height: 6px; border-radius: 999px; overflow: hidden; }
.d0-kpi__fill { display: block; height: 100%; border-radius: 999px; background: var(--d0-grey-400); }
.d0-kpi__fill[data-on] { background: var(--d0-blue); }
.d0-kpi__track[data-whole] { background: var(--d0-grey-200); } /* 상태 막대의 전체 트랙(라벨 글자가 전체를 말한다) */
.d0-kpi__fill[data-tone="green"] { background: var(--d0-green); }
.d0-kpi__fill[data-tone="red"] { background: var(--d0-red); }
@media (max-width: 640px) { .d0-kpi { padding: 20px; } }
/* 3장은 좁은 폭에서 2+1로 접히지 않게 1열로 쌓는다 */
@media (max-width: 520px) {
  .d0-kpis:has(> .d0-kpi:nth-child(3):last-child) { grid-template-columns: 1fr; }
}
/* 축 안 2열 열(336px, report 456px)은 3장 한 줄에 필요한 474px보다 좁다. 2+1로 접히지 않게 쌓는다 */
.d0-section > .d0-cols:not(.d0-wide) .d0-kpis:has(> .d0-kpi:nth-child(3):last-child) { grid-template-columns: 1fr; }
```

카드 최소 폭은 150px다(안쪽 24px씩 빼면 내용 약 120px). 3장이 한 줄에 놓이려면 474px(150 × 3 + 간격 12 × 2)가 필요하다.
축(기본 720px 각 232px, narrow 640px 각 약 205px, report 960px 각 312px)과 넓은 구간 6/6 열(544px 각 약 173px, report 616px 각 약 197px)에서는 한 줄에 놓인다.
축 안 2열 열(기본 336px, report 456px)은 474px보다 좁아 2+1로 접히므로 3장이면 1열로 쌓는다(위 CSS). 2장·4장은 그 열에서 2열로 놓인다.
숫자 28px은 `약 10분`까지 들어간다. 더 길면 그 블록에서만 `.d0-kpi__value`를 24px로 낮춘다.
375px(343px)에서 2장·4장은 2열로 접힌다. 3장은 2+1(외톨이 카드)이 되지 않게 520px 이하에서 1열로 쌓는다.
막대 폭은 숫자에서 계산한다(6 ÷ 14 = 42.9%, 4 ÷ 58 = 6.9%). 숫자를 지어 맞추지 않는다.

## 금지

- 증감 배지·▲▼ 기호, 카드마다 설명 문단, 해석 없는 거대 숫자 장식, 근거 없는 숫자, 둥글게 맞춘 가짜 수치.
- 라벨 없는 막대(어느 쪽이 전인지 모르는 막대), 같은 카드 안에서 후 값을 숫자와 막대 라벨에 두 번 쓰기.
- 단위만 작게 줄이기, 카드 테두리·그림자, 카드 5개 이상, 좁은 폭에서 2+1로 남는 외톨이 카드.
- 의미색 숫자·라벨 글자, orange 상태 막대, 막대가 하나도 없어 회색뿐인 KPI 줄(최소 한 장은 막대 변형).
- 히어로와 같은 문장·배지를 카드에 되풀이하기.
