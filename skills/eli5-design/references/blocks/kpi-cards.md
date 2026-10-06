# kpi-cards — 숫자 카드

## 해부 구조

- `dl.d0-kpis > div.d0-kpi` 2~4개. 카드 하나 = `dt` 짧은 라벨(명사, 13px) → `dd` 큰 숫자(28px/700, 단위 포함, `tabular-nums`)
  → `dd` 증감 배지(`▼ 14분 → 6분`) → (선택) `dd` 미니 막대. 라벨-값 짝이라 `dl`로 쓴다. `div`로 `dt`·`dd` 묶음을 감싸는 것은 HTML 표준이다.
  카드 라벨을 `h3`로 올리지 않는다(숫자 카드마다 제목이 생겨 제목 탐색이 시끄러워진다).
- 숫자는 `<data value>`로 감싼다(기계가 읽는 값). 목표 대비 비율이면 `<meter>`를 쓴다. 기간이면 `<time datetime="PT6M">`.
- **문단을 넣지 않는다.** "그래서 좋은가"는 섹션 제목이나 그림 주석이 한 번만 말한다.
- 증감 배지는 [shell.md](shell.md)의 `.d0-pill`을 쓴다. 좋으면 `green`, 나쁘면 `red`, 변화 없음은 기본 회색.
  이 배지에는 색 점을 두지 않는다. 점 대신 ▲▼ 기호(`aria-hidden`)를 의미색으로 칠하고, 뜻은 글자(`14분 → 6분`)가 전한다.
  기호 대비: green / green-bg 3.17, red / red-bg 3.21(그래픽 3:1 통과). 상태 배지의 점 규칙은 shell.md 그대로다.
- 비교가 핵심이면 [diagram.md](diagram.md)의 (b) 전/후 막대를 쓰거나 카드 아래 미니 막대를 붙인다.
  diagram 전/후 막대는 비교 쌍 2개까지다. 3쌍 이상이면 이 블록의 막대 변형(카드 하나에 쌍 하나)을 쓴다.

## 언제 쓰나 / 변형

- report·incident에서 근거 숫자를 보여 줄 때. 숫자가 하나뿐이면 카드 대신 섹션 제목에 쓴다.
- `data-variant="bar"`: 숫자 아래 전/후 미니 막대 SVG(위 grey-400 = 전, 아래 blue = 후). 막대 폭 = 값 / 큰 값 × 200.

## 스니펫

```html
<dl class="d0-kpis">
  <div class="d0-kpi" data-variant="bar">
    <dt class="d0-kpi__label">내보내기 대기</dt>
    <dd class="d0-kpi__value"><data value="6">6</data><small>분</small></dd>
    <dd><span class="d0-pill" data-tone="green"><span class="d0-kpi__sym" aria-hidden="true">▼</span> 14분 → 6분</span></dd>
    <dd><svg viewBox="0 0 200 28" role="img" aria-labelledby="k1-t">
      <title id="k1-t">전 14분, 후 6분</title>
      <rect class="d0-s-bar" x="0" y="2" width="200" height="10" rx="5"/>
      <rect class="d0-s-bar" data-on x="0" y="16" width="86" height="10" rx="5"/>
    </svg></dd>
  </div>
  <div class="d0-kpi">
    <dt class="d0-kpi__label">실패한 내보내기</dt>
    <dd class="d0-kpi__value"><data value="4">4</data><small>건</small></dd>
    <dd><span class="d0-pill" data-tone="red"><span class="d0-kpi__sym" aria-hidden="true">▲</span> 3건 → 4건</span></dd>
  </div>
  <div class="d0-kpi">
    <dt class="d0-kpi__label">받은 팀</dt>
    <dd class="d0-kpi__value"><data value="12">12</data><small>팀</small></dd>
    <dd><span class="d0-pill">변화 없음</span></dd>
  </div>
</dl>
```

```css
.d0-kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
.d0-kpi { display: grid; gap: 6px; align-content: start; padding: 20px; border-radius: var(--d0-radius-card); background: var(--d0-grey-50); }
.d0-kpi__label { color: var(--d0-grey-700); font-size: var(--d0-text-compact); font-weight: 600; }
.d0-kpi__value { margin: 0; font-size: 28px; font-weight: 700; letter-spacing: var(--d0-tracking-display); line-height: var(--d0-leading-display); font-variant-numeric: tabular-nums; }
.d0-split .d0-kpi__value { font-size: 24px; }
.d0-kpi__value small { margin-left: 2px; font-size: 15px; font-weight: 600; }
.d0-kpi dd { margin: 0; min-width: 0; }
.d0-kpi .d0-pill { gap: 4px; font-variant-numeric: tabular-nums; }
.d0-kpi .d0-pill[data-tone]::before { content: none; }
.d0-kpi__sym { font-size: 10px; }
.d0-pill[data-tone="green"] .d0-kpi__sym { color: var(--d0-green); }
.d0-pill[data-tone="red"] .d0-kpi__sym { color: var(--d0-red); }
.d0-kpi svg { margin-top: 6px; width: 100%; max-width: none; height: auto; }
/* 3장은 좁은 폭에서 2+1로 접히지 않게 1열로 쌓는다 */
@media (max-width: 520px) {
  .d0-kpis:has(> .d0-kpi:nth-child(3):last-child) { grid-template-columns: 1fr; }
}
```

반 열(`.d0-split` 안, 약 544px)에서도 카드 3장이 한 줄에 놓이도록 최소 폭을 150px로 둔다(카드 안 여백 20px씩 빼면 내용 110px).
숫자 28px은 네 글자(`1,234`)까지 들어간다. 더 길면 `.d0-split .d0-kpi__value { font-size: 24px; }`로 낮춘다.
375px(343px)에서 2장·4장은 2열로 접힌다. 3장은 2+1(외톨이 카드)이 되지 않게 520px 이하에서 1열로 쌓는다.

막대 클래스(`d0-s-bar`)는 diagram.md 공용 CSS를 쓴다. 미니 막대는 숫자가 배지 글자로 함께 적혀 있어
grey-400(2.19:1) 전 막대를 써도 된다. 뜻을 전하는 후 막대는 blue(grey-50 위 3.75:1)다.

## 금지

- 카드마다 설명 문단, 해석 없는 거대 숫자 장식, 근거 없는 숫자, 둥글게 맞춘 가짜 수치.
- 증감을 색으로만 표시(기호와 전 값을 배지 글자에 함께 쓴다), 증감 배지에 색 점과 기호를 함께 두기, 배지 글자(기호 제외)에 시맨틱 전경색, 카드 5개 이상, 좁은 폭에서 2+1로 남는 외톨이 카드.
