# hero — 결론 수치

페이지의 결론 숫자 하나를 크게 보여 준다. 문장 속에 묻힌 숫자를 꺼내 첫 화면의 주인공으로 둔다.

## 해부 구조

- `p.d0-hero` 하나 = 숫자 줄(`.d0-hero__nums`) → 한 줄 뜻(`.d0-hero__note`).
- 숫자 줄 = 전 값(20px/600, grey-600, 취소선 없음) → 화살표(장식 SVG, `aria-hidden`) → 후 값(44px/600, display 자간).
  단위는 숫자와 같은 크기·굵기로 붙여 쓴다. 숫자 열은 `tabular-nums`. 640px 이하에서 후 값은 36px.
- 값은 `<data value>`로 감싼다(기계가 읽는 값). 기간이면 `<data>` 대신 `<time datetime="PT26M">`도 된다.
- 한 줄 뜻(15px grey-600, 한 문장): 이 숫자가 무엇을 잰 것인지, 예상치인지. 같은 말을 요약 행·섹션 제목에서 되풀이하지 않는다.
- **읽는 순서.** 화살표는 `aria-hidden`이다. 뜻은 화살표 앞뒤에 숨긴 조사(`.d0-sr-only`)로 전한다.
  스크린 리더는 "26분에서 약 10분으로"로 읽는다. 숫자를 `aria-label`에 한 번 더 적지 않는다(같은 숫자 문자열이 늘어난다).
- 색: 후 값은 grey-900이 기본이다. 강조가 필요하면 숫자에만 blue-dark(5.5:1)를 쓴다. 배경·배지·밑줄은 두지 않는다.

## 언제 쓰나 / 변형

- 위치는 header 안 **h1 바로 아래, 요약 행 위**다(h1 → 히어로 → 요약 행). 페이지당 하나.
- report, compare 전/후, incident에서 결론 수치가 있을 때 쓴다. **수치가 없으면 쓰지 않는다.** 문장으로 바꿔 채우지 않는다.
- 히어로가 있으면 그 숫자는 히어로가 정본이다. 요약 행·섹션 제목·callout에 같은 숫자를 다시 쓰지 않는다.
  숫자 카드에 같은 비교가 다시 나오면 전 값만 막대 라벨로 두고, 히어로와 같은 문장을 반복하지 않는다.
- 적용 전 제안이면 후 값에 `약`을 붙이고 한 줄 뜻에 `예상치`를 한 번 쓴다.

| 변형 | 숫자 줄 | 언제 |
| --- | --- | --- |
| 전 → 후(기본) | `26분 → 약 10분` | 바뀐 결과가 결론일 때 |
| 단일 값 `data-variant="single"` | `58건` | 전 값이 없는 결론(건수, 영향 범위) |

## 스니펫

```html
<!-- 전 → 후 -->
<p class="d0-hero">
  <span class="d0-hero__nums">
    <span class="d0-hero__before"><data value="26">26</data>분</span><span class="d0-sr-only">에서</span>
    <svg class="d0-hero__arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 12h15M13 6l6 6-6 6"/></svg>
    <span class="d0-hero__after">약 <data value="10">10</data>분</span><span class="d0-sr-only">으로</span>
  </span>
  <span class="d0-hero__note">PR 하나를 검사하는 시간이에요. 지난 실행 기록으로 낸 예상치예요.</span>
</p>

<!-- 단일 값 -->
<p class="d0-hero" data-variant="single">
  <span class="d0-hero__nums"><span class="d0-hero__after"><data value="58">58</data>건</span></span>
  <span class="d0-hero__note">밤사이 멈춘 내보내기 수예요.</span>
</p>
```

```css
.d0-hero { display: grid; gap: 6px; margin: 8px 0 4px; }
.d0-hero__nums { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; font-variant-numeric: tabular-nums; }
.d0-hero__before { color: var(--d0-grey-600); font-size: 20px; font-weight: 600; letter-spacing: var(--d0-tracking-title); }
.d0-hero__arrow { align-self: center; flex: none; width: 24px; height: 24px; fill: none; stroke: var(--d0-grey-500); stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
.d0-hero__after { color: var(--d0-grey-900); font-size: 44px; font-weight: 600; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
.d0-hero[data-tone="blue"] .d0-hero__after { color: var(--d0-blue-dark); }
.d0-hero__note { display: block; color: var(--d0-grey-600); font-size: 15px; }
@media (max-width: 640px) {
  .d0-hero__after { font-size: 36px; }
}
```

- 후 값 앞 `약`·단위는 같은 크기로 둔다. 단위만 작게 줄이지 않는다.
- 전 값은 정보라서 grey-600(5.0:1)이다. 화살표는 장식이라 대비 기준 밖이지만 grey-500 1.5px 선으로 보이게 둔다.

## 금지

- 수치 없이 히어로 두기, 페이지에 히어로 2개, h1 위나 요약 행 아래에 두기.
- 전 값 취소선, 화살표 글자(`→`)를 읽히게 두기, 같은 숫자를 `aria-label`로 한 번 더 적기.
- 그라디언트 배경, 카드 상자, 배지·증감 기호 덧붙이기, 700 이상 굵기, 단위만 작게 줄이기.
- 히어로 숫자를 요약 행·섹션 제목·callout·KPI 배지에 되풀이하기.
