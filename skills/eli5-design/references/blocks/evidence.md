# evidence — 주장과 근거

공용 정보 블록이다. **Claim(주장 한 줄) + Proof(근거)**를 한 짝으로 묶는다. 어느 패턴에서나 "그래서 왜 그렇게 말할 수 있나"를 보일 때 쓴다.
예: `B안이 더 잘 맞아요` / `새 요청 10건 중 10건 수용`.

## 해부 구조

- **Claim.** 결론 한 줄(15px/600 grey-900). 주제명이 아니라 주장이다(`처리 시간` ✕ → `처리 시간이 절반으로 줄었어요` ○). 말투는 출력의 말투를 따른다(page 해요체, SKILL.md 말투).
- **Proof.** 주장을 받치는 근거 하나. 표현 방식(`data-proof`)은 넷 중 하나다.

  | `data-proof` | 근거 모양 | 마크업 |
  | --- | --- | --- |
  | `number` | 숫자 + 단위 + 기준 한 줄 | `data value` 20px/600 grey-900 `tabular-nums` + 14px grey-600 기준 |
  | `source` | 어디서 확인했나 | 14px grey-700 한 줄 + `small` 출처(12px grey-600) |
  | `before-after` | 바뀌기 전과 후 | [before-after](before-after.md)를 Proof 안에 넣는다 |
  | `example` | 실제 한 건 | 14px grey-700 한 줄, 값은 합성 |

- 형태는 `dl.d0-evidence > div[data-proof]`(짝이 여럿) 또는 `figure.d0-evidence`(근거가 그림 하나: Claim은 `figcaption`을 그림 위에, Proof는 SVG·kpi-cards 막대 변형).
- 짝은 섹션당 1~3개. 여럿이면 세로로 쌓는다(짝수라서 2열로 나누지 않는다). 짝 사이 24px. 묶음은 축 폭을 그대로 쓴다.
- 카드·배경·테두리 상자 금지. 묶음은 여백과 글자 굵기로만 만든다.
- **한 사실은 한 번.** 히어로·요약 행에 있는 숫자를 Proof에 다시 쓰지 않는다. 그 숫자가 정본이면 Proof는 출처나 예시로 받친다.
- 숫자 Proof에는 단위·기간·기준을 붙인다. 예상치는 글자 라벨 `(예상치)`를 단다. 측정값과 섞지 않는다.

## 근거 변형 (`figure.d0-evidence[data-variant]`)

Proof가 숫자 여럿일 때 쓰는 모양 셋이다. 새 블록이 아니라 그림형 `figure.d0-evidence`의 변형이고, Claim은 그대로 `figcaption`(page는 그림 위, deck은 슬라이드 제목)이다.
deck에서는 evidence 장의 `figure.d0-slide__fig`에 같은 `data-variant`를 달고 근거 요소만 옮긴다(자리·크기는 [slide-deck](slide-deck.md) 근거 변형과 주석).

| `data-variant` | 근거 요소 | 언제 | 그림으로 세나 |
| --- | --- | --- | --- |
| `metric-list` | `div.d0-mlist` = `dl.d0-mlist__rows`(큰 숫자 + 짧은 라벨 세로 목록 2~4행) + 옆 작은 차트 `svg.d0-mlist__chart` | 한 변화가 지표 여럿에 함께 나타날 때. 차트는 강조 행 하나의 추이 | 예(작은 차트가 그림) |
| `bar-list` | `ol.d0-barlist` = 행마다 라벨 + 값 + 가로 막대 | 같은 단위의 비율·구성(예산 40/30/20/10%), 같은 단위 값 3~6개를 견줄 때 | 예 |
| `tiles` | `dl.d0-tiles` = 옅은 면 타일 4개(2×2) 또는 6개(2×3) | 같은 단위·성격의 현황 지표를 훑을 때. 값끼리 크기를 견주는 게 주장이면 bar-list | 아니오(막대 없는 kpi-cards와 같다) |

- **표식은 단순하게.** 아이콘을 붙이지 않는다. metric-list 강조 행은 왼쪽 2px blue 선, tiles 강조 타일은 라벨 앞 6px blue 점 + 라벨 blue-dark다. 강조는 장면에 하나다(`data-on`).
- **큰 숫자는 grey-900.** 색이 아니라 크기로 중요하게 만든다. 값 `dd` 안의 숫자는 `<data value>`로 감싼다.
- **bar-list 막대 폭.** 구성비면 폭 = 비율 그대로(합 100%), 같은 단위 값 비교면 가장 큰 값 = 100%다. 숫자에서 계산하고 지어 맞추지 않는다. 막대는 `aria-hidden`이고 값 글자가 뜻을 전한다. 강조 행만 blue, 나머지 grey-400(값이 글자로 적혀 있다).
- **tiles는 같은 단위·성격만.** 건수와 비율, 시간과 금액을 한 묶음에 섞지 않는다. 5개는 두지 않는다(외톨이 타일). 테두리·그림자 없이 grey-50 면과 radius card만 쓴다.
- **kpi-cards와의 관계.** 전/후 막대·상태 막대가 있는 2~4장은 [kpi-cards](kpi-cards.md), 막대 없이 같은 단위 지표 4~6개를 훑으면 tiles다. 한 섹션·장에 둘을 함께 두지 않는다.

```html
<figure class="d0-evidence" data-variant="metric-list">
  <figcaption>대기열을 나눈 뒤 세 지표가 함께 좋아졌어요</figcaption>
  <div class="d0-mlist">
    <dl class="d0-mlist__rows">
      <div data-on><dt>10분 넘게 늦은 알림</dt><dd><data value="18">18</data>%</dd></div>
      <div><dt>하루 재시도</dt><dd><data value="90">90</data>건</dd></div>
      <div><dt>평균 도착 시간</dt><dd><data value="4">4</data>분</dd></div>
    </dl>
    <svg class="d0-mlist__chart" viewBox="0 0 240 160" role="img" aria-labelledby="ml1-t">
      <title id="ml1-t">10분 넘게 늦은 알림 비율의 주별 변화. 1주 47%, 2주 35%, 3주 24%, 4주 18%.</title>
      <line class="d0-s-line" x1="8" y1="148" x2="232" y2="148"/>
      <rect class="d0-s-bar" x="20" y="20" width="36" height="128" rx="4"/>
      <rect class="d0-s-bar" x="76" y="52.7" width="36" height="95.3" rx="4"/>
      <rect class="d0-s-bar" x="132" y="82.6" width="36" height="65.4" rx="4"/>
      <rect class="d0-s-bar" data-on x="188" y="99" width="36" height="49" rx="4"/>
    </svg>
  </div>
</figure>

<figure class="d0-evidence" data-variant="bar-list">
  <figcaption>예산의 40%가 인건비예요</figcaption>
  <ol class="d0-barlist">
    <li data-on><span class="d0-barlist__label">인건비</span><data class="d0-barlist__value" value="40">40%</data><span class="d0-barlist__track" aria-hidden="true"><span class="d0-barlist__fill" style="width: 40%"></span></span></li>
    <li><span class="d0-barlist__label">서버</span><data class="d0-barlist__value" value="30">30%</data><span class="d0-barlist__track" aria-hidden="true"><span class="d0-barlist__fill" style="width: 30%"></span></span></li>
    <li><span class="d0-barlist__label">도구</span><data class="d0-barlist__value" value="20">20%</data><span class="d0-barlist__track" aria-hidden="true"><span class="d0-barlist__fill" style="width: 20%"></span></span></li>
    <li><span class="d0-barlist__label">기타</span><data class="d0-barlist__value" value="10">10%</data><span class="d0-barlist__track" aria-hidden="true"><span class="d0-barlist__fill" style="width: 10%"></span></span></li>
  </ol>
</figure>

<figure class="d0-evidence" data-variant="tiles">
  <figcaption>여섯 지역 모두 목표 응답률을 넘었어요</figcaption>
  <dl class="d0-tiles">
    <div><dt>지역 A</dt><dd><data value="96">96</data>%</dd></div>
    <div><dt>지역 B</dt><dd><data value="94">94</data>%</dd></div>
    <div data-on><dt>지역 C</dt><dd><data value="91">91</data>%</dd></div>
    <div><dt>지역 D</dt><dd><data value="97">97</data>%</dd></div>
    <div><dt>지역 E</dt><dd><data value="95">95</data>%</dd></div>
    <div><dt>지역 F</dt><dd><data value="93">93</data>%</dd></div>
  </dl>
</figure>
```

```css
/* metric-list: 큰 숫자 + 짧은 라벨 세로 목록 | 작은 차트(글자 없는 SVG) */
.d0-mlist { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 24px; align-items: center; }
.d0-mlist__rows { margin: 0; display: grid; gap: 16px; }
.d0-mlist__rows > div { display: flex; flex-direction: column-reverse; gap: 2px; padding-left: 12px; border-left: 2px solid transparent; }
.d0-mlist__rows > div[data-on] { border-left-color: var(--d0-blue); }
.d0-mlist__rows dt { color: var(--d0-grey-600); font-size: 14px; }
.d0-mlist__rows dd { margin: 0; color: var(--d0-grey-900); font-size: 28px; font-weight: 600; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); font-variant-numeric: tabular-nums; }
svg.d0-mlist__chart { display: block; width: 100%; height: auto; } /* 지표 목록 옆 열 폭을 채운다(블록 부품 2열) */
/* bar-list: 라벨 + 값 한 줄, 그 아래 막대 */
.d0-barlist { margin: 0; padding: 0; list-style: none; display: grid; gap: 14px; }
.d0-barlist li { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 6px 12px; align-items: baseline; }
.d0-barlist .d0-barlist__label { color: var(--d0-grey-800); font-size: 15px; }
.d0-barlist .d0-barlist__value { color: var(--d0-grey-900); font-size: 15px; font-weight: 600; font-variant-numeric: tabular-nums; }
.d0-barlist__track { grid-column: 1 / -1; display: block; height: 8px; border-radius: 999px; background: var(--d0-grey-100); overflow: hidden; }
.d0-barlist__fill { display: block; height: 100%; border-radius: 999px; background: var(--d0-grey-400); }
.d0-barlist li[data-on] .d0-barlist__fill { background: var(--d0-blue); }
.d0-barlist li[data-on] .d0-barlist__label { color: var(--d0-grey-900); font-weight: 600; }
/* tiles: grey-50 면 타일, 테두리·그림자 없음. 3열(6개) 또는 2열(4개) */
.d0-tiles { margin: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.d0-tiles:has(> div:nth-child(4):last-child) { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.d0-tiles > div { display: grid; gap: 6px; align-content: start; min-width: 0; padding: 20px; border-radius: var(--d0-radius-card); background: var(--d0-grey-50); }
.d0-tiles dt { color: var(--d0-grey-600); font-size: var(--d0-meta); font-weight: 600; }       /* grey-50 위 4.71 */
.d0-tiles dd { margin: 0; color: var(--d0-grey-900); font-size: 28px; font-weight: 600; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); font-variant-numeric: tabular-nums; }
.d0-tiles > div[data-on] dt { color: var(--d0-blue-dark); }                                     /* grey-50 위 5.18 */
.d0-tiles > div[data-on] dt::before { content: ""; display: inline-block; width: 6px; height: 6px; margin-right: 6px; border-radius: 50%; background: var(--d0-blue); vertical-align: middle; }
@media (max-width: 640px) {
  .d0-mlist { grid-template-columns: minmax(0, 1fr); }
  .d0-tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .d0-tiles > div { padding: 16px; }
}
```

## explanation과의 경계

evidence는 "무엇을 근거로"(측정·출처·사례), [explanation](explanation.md)은 "왜·그래서·어떤 조건에서"(이유·뜻·조건)다. 근거 아래 해석이 필요하면 evidence 다음에 explanation `interpretation`을 붙인다. 하나의 블록에 둘을 섞지 않는다.

## 스니펫

```html
<dl class="d0-evidence">
  <div data-proof="number">
    <dt>B안은 새 요청을 다 받아요</dt>
    <dd><data value="10">10건 중 10건</data><span>지난 4주 새 요청 기준</span></dd>
  </div>
  <div data-proof="source">
    <dt>A안은 월말에 느려져요</dt>
    <dd>월말 사흘 동안 대기열이 평소의 세 배였어요.<small>출처: 내부 집계(합성)</small></dd>
  </div>
</dl>

<!-- Proof가 전/후일 때: before-after를 Proof 안에 넣는다 -->
<dl class="d0-evidence">
  <div data-proof="before-after">
    <dt>받을 묶음을 먼저 고르면 다시 받는 일이 줄어요</dt>
    <dd>
      <div class="d0-ba" data-kind="improve">
        <div data-side="before"><span class="d0-ba__label">기존</span><p>전체를 받은 뒤 엑셀에서 지워요.</p></div>
        <span class="d0-ba__arrow" aria-hidden="true"></span>
        <div data-side="after"><span class="d0-ba__label">개선</span><p>필요한 묶음만 받아요.</p></div>
      </div>
    </dd>
  </div>
</dl>
```

```css
.d0-evidence { display: grid; gap: 24px; margin: 0; }
dl.d0-evidence > div { display: grid; gap: 6px; min-width: 0; }               /* 짝 목록 규칙은 dl에만: 근거 변형(figure)과 섞이지 않게 */
dl.d0-evidence dt { color: var(--d0-grey-900); font-size: 15px; font-weight: 600; line-height: var(--d0-leading-title); }
dl.d0-evidence dd { display: grid; gap: 2px; margin: 0; color: var(--d0-grey-700); font-size: 14px; }
dl.d0-evidence data { color: var(--d0-grey-900); font-size: 20px; font-weight: 600; font-variant-numeric: tabular-nums; letter-spacing: var(--d0-tracking-title); }
dl.d0-evidence dd > span, dl.d0-evidence small { color: var(--d0-grey-600); }
dl.d0-evidence small { font-size: var(--d0-meta); }
figure.d0-evidence > figcaption:first-child { color: var(--d0-grey-900); font-size: 15px; font-weight: 600; } /* 그림형: 주장이 그림 위 */
```

## 금지

- 주장 없는 숫자 나열, 근거 없는 주장, 한 짝에 근거 둘 이상.
- 큰 숫자를 blue로 칠하거나 증감 배지 달기(원칙 9번), 히어로 숫자 되풀이.
- 카드·배경 상자, 짝마다 다른 모양.
- 근거 변형에 아이콘 붙이기, 큰 원 안 숫자로 크기 견주기, 단위·성격이 다른 지표를 한 tiles에 섞기, 5개 타일, 합이 100%가 아닌 구성비 bar-list.
