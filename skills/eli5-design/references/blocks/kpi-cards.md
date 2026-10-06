# kpi-cards — 지표 카드

## 해부 구조

- 3~5개. 이름 → 큰 숫자(단위 포함, `tabular-nums`) → 증감(전 기간 대비, 화살표 기호) → 한 줄 뜻.
- 한 줄 뜻은 "그래서 좋은가 나쁜가"를 말한다.
- 증감은 글자("줄었어요")로 말하고, 좋고 나쁨(`data-tone="good|bad"`)은 화살표 기호 색으로만 거든다.
  시맨틱 색은 글자 대비가 모자라 글자 자체에는 쓰지 않는다.

## 언제 쓰나 / 변형

- report의 결론 바로 아래, 근거 숫자를 보여 줄 때.
- 증감이 없으면 증감 줄을 빼고 "비교 기간 없음"으로 적는다.

## 스니펫

```html
<ul class="d0-kpis">
  <li class="d0-kpi">
    <span class="d0-kpi__label">평균 처리 시간</span>
    <strong class="d0-kpi__value">17<small>분</small></strong>
    <span class="d0-kpi__delta" data-tone="good"><i aria-hidden="true">▼</i> 3분 줄었어요 (전주 대비)</span>
    <p>줄었어요. 주문을 고르고 파일을 받기까지 덜 기다려요.</p>
  </li>
  <li class="d0-kpi">
    <span class="d0-kpi__label">실패한 내보내기</span>
    <strong class="d0-kpi__value">4<small>건</small></strong>
    <span class="d0-kpi__delta" data-tone="bad"><i aria-hidden="true">▲</i> 1건 늘었어요 (전주 대비)</span>
    <p>조금 늘었어요. 모두 기간을 너무 길게 고른 경우예요.</p>
  </li>
  <li class="d0-kpi">
    <span class="d0-kpi__label">내보낸 파일</span>
    <strong class="d0-kpi__value">213<small>개</small></strong>
    <span class="d0-kpi__delta" data-tone="good"><i aria-hidden="true">▲</i> 18개 늘었어요 (전주 대비)</span>
    <p>늘었어요. 팀 A가 매일 받기 시작했어요.</p>
  </li>
</ul>
```

```css
.d0-kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}
.d0-kpi {
  display: grid;
  gap: 4px;
  align-content: start;
  padding: 20px;
  border-radius: var(--d0-radius-control);
  background: var(--d0-grey-50);
}
.d0-kpi__label { font-size: var(--d0-text-compact); color: var(--d0-grey-600); }
.d0-kpi__value {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: var(--d0-tracking-display);
  font-variant-numeric: tabular-nums;
}
.d0-kpi__value small { margin-left: 2px; font-size: 15px; font-weight: 600; }
.d0-kpi__delta { color: var(--d0-grey-800); font-size: var(--d0-text-compact); font-weight: 600; font-variant-numeric: tabular-nums; }
.d0-kpi__delta i { font-style: normal; }
.d0-kpi__delta[data-tone="good"] i { color: var(--d0-green); }
.d0-kpi__delta[data-tone="bad"] i { color: var(--d0-red); }
.d0-kpi p { margin-top: 4px; color: var(--d0-grey-700); }
```

## 금지

- 해석 없는 거대 숫자 장식, 0이거나 근거 없는 숫자, 둥글게 맞춘 가짜 수치.
- 증감을 색으로만 표시(기호와 비교 기간을 함께 쓴다).
