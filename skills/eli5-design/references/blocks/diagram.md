# diagram — SVG 도식

페이지의 주인공이다. 대상의 **모양**을 선과 면으로 그린다. 글은 그림 아래 주석 한 줄로 줄인다.

## 해부 구조

- `figure.d0-fig[data-stage]` = 무대 패널 `div.d0-fig__stage`(grey-50, `--d0-radius-card`, 패딩 28px / 모바일 20px) 안에 인라인 SVG 하나
  → 패널 **밖** `figcaption` 한 줄(13px grey-600, "그래서 무엇이 보이는가"). 무대 CSS는 [shell.md](shell.md)에 있다.
- 모든 도식은 무대 위에 놓는다. 예외는 폭을 꽉 채우는 비율 막대(무대 없이 섹션 폭)와 카드 안 미니 격자(카드가 무대다)다.
- SVG는 `role="img"` + `<title>`(그림 이름) + `<desc>`(무엇이 강조됐는지 한두 문장). 장식 SVG만 `aria-hidden="true"`.
- 색은 SVG 안에 직접 쓰지 않는다. 아래 `d0-s-*` 클래스가 `var(--d0-*)`를 쓴다. 강조 묶음은 블루 하나, 상태가 있는 표식은
  의미색 `data-tone="green|orange|red"`(완료·통과 / 주의·준비 / 실패·위험)를 단다. **회색만으로 된 도식은 금지**다. 색 규칙 정본은 [shell.md](shell.md) 색 절.
- 페이지의 핵심 도식 하나는 무대를 blue-light로 칠할 수 있다(`figure.d0-fig[data-stage="blue"]`). 그 위 회색 선은 grey-600, 흐린 라벨은 grey-700로
  자동으로 한 단계 진해진다(blue-light 위 grey-500 선 2.87, grey-600 글자 4.49라 미달). 무대 면도 포인트 면적에 들어가므로
  전체 폭 무대(1280px에서 약 25~30%)는 12% 상한을 넘는다. blue 무대는 반 열(`.d0-split`·`.d0-cols`) 도식이나 작은 무대에만 쓴다.
- 강조는 색만으로 말하지 않는다. 채움/빈 모양, 굵기, 라벨 중 하나를 함께 바꾼다.
- **선.** 굵기는 기본 1.5, 강조 2.5 두 가지뿐이다. 모든 선은 `stroke-linecap: round`, `stroke-linejoin: round`. 노드에 그림자·그라디언트 없음.
- **그리기 모션.** 강조 경로(`data-on` 엣지·화살표)에 `class="… d0-draw"`와 `pathLength="1"`을 붙이면 섹션이 드러날 때 600ms 동안 그려진다.
  갈래마다 `path`를 따로 둔다(한 `path`의 서브패스는 순서대로 이어 그려진다). 동작·reduced-motion 처리는 [shell.md](shell.md) 모션.
- 반응형: `viewBox`만 두고 `width`·`height` 속성은 쓰지 않는다. CSS가 폭 100%, 높이 auto로 맞춘다.
- **텍스트 상자를 화살표로 이은 것은 도식이 아니다.** 상자 안에 문장이 들어가는 순간 글이다. Mermaid 등 자동 배치 도구는 쓰지 않고 손으로 그린다.

## 라벨

- 설명 문장은 SVG 밖 `figcaption`·HTML에 둔다. 확대·번역·복사가 되기 때문이다.
- SVG `<text>`는 짧은 노드·값 라벨(명사 1~3단어, `고친 파일`, `6분`)에만 쓴다.
- **권장 크기는 렌더 13~14px**, 게이트는 375px에서 11px 이상·데스크톱 16px 이하다(h2보다 작게).
- **측정 기준(정본).** 렌더 글자 크기 = font-size f × (SVG 렌더 폭 ÷ viewBox 폭 W). SVG는 폭 100%로 커지므로 렌더 폭은
  `min(무대 안쪽 폭, max-width)`다. 글자 박스 높이(`getBBox`·`getBoundingClientRect`의 height)는 쓰지 않는다. 줄 높이와 글꼴 여백이 섞여 크게 나온다.
  - 375px 화면: 컨테이너 343px − 무대 패딩 40px = 안쪽 **303px**. 11px 이상이려면 `f × 303 ÷ W ≥ 11` → `W ≤ 27.5 × f`.
  - 데스크톱 16px 이하: `f × max-width ÷ W ≤ 16` → `max-width ≤ W × 16 ÷ f`. 권장 14px이면 `max-width = W × 14 ÷ f`.
- 아래 두 크기 중 하나를 고른다. 다른 W를 쓰면 위 두 식으로 max-width를 다시 계산해 해당 SVG에 둔다.

| 크기 | viewBox 폭 W | 글자 f | SVG max-width | 375px 라벨 | 데스크톱 라벨 | 노드 r 9→렌더 |
| --- | --- | --- | --- | --- | --- | --- |
| 기본 | 360 | 14 | 360px | 11.8px | 14.0px | 18px 지름 |
| `data-size="wide"` | 480 | 18 | 400px | 11.4px | 15.0px | 15px 지름 |

- 번호 글자(`.d0-s-num`)도 같은 식을 따른다. 기본 14px(375px 11.8px), wide 18px(375px 11.4px·데스크톱 15px). wide에서 13~14px로 두면 375px에서 8~9px로 줄어 실패다.

- 노드·원은 viewBox 단위로 그린다. 기본 크기에서 노드 r 9~11(렌더 지름 18~22px), 바깥 고리 r 17을 넘기지 않는다.
- **결론: 글자가 든 SVG는 렌더 폭 약 440px에서 멈춘다.** 데스크톱 16px 상한에서 기본은 360 × 16 ÷ 14 ≈ 411px, wide는 480 × 16 ÷ 18 ≈ 427px이다.
  그래서 전체 폭(1136px) 섹션에 글자 든 SVG를 혼자 두면 무대 양옆이 빈다. 전체 폭 흐름은 `.d0-split`·`.d0-cols` 2열 한쪽에 넣거나,
  `data-layout="side"`(무대 왼쪽 최대 440px + 오른쪽 설명)로 옆을 채우거나, `data-size="wide"`로 키운다. 폭을 꽉 채우는 그림은 글자를 HTML로 뺀다(비율 막대).
- 이 조건을 못 맞추는 넓은 그림(W > 27.5 × f)은 `.d0-fig__scroll` 상자에 넣는다. 페이지 가로 스크롤은 금지다.
- 폭을 꽉 채워야 하는 그림(비율 막대)은 글자를 SVG 밖 HTML에 두고 SVG는 도형만 그린다. 아래 (b) 비율 변형 참고.

## 변형

| 변형 | 그리는 것 | 언제 |
| --- | --- | --- |
| (a) graph 연결 그래프 | 노드 원 + 엣지 곡선, 닿는 것만 블루 | 무엇이 무엇에 닿나(의존, 영향 범위) |
| (b) bars 전/후 막대 | 시간·양을 막대 길이로 | 얼마나 줄었나·늘었나 |
| (b) bars `data-variant="ratio"` 비율 막대 | 전체 한 줄 안의 부분 | 전체 중 얼마인가(234건 중 58건) |
| (c) grid 미니 격자 | 표의 행·열 모양 썸네일(JS 생성) | 결과물이 어떤 모양의 표인가 |
| (d) wireframe 화면 골격 | 상단 바·카드·버튼을 상자로 | 어떤 화면의 어디가 바뀌나 |
| (e) steps 단계 | 번호 원을 1.5px 선으로 잇고 라벨은 아래 | 몇 단계 중 어디인가, 핵심 단계 하나 |
| (f) sequence 주고받기 | 참여자 세로선 3~4개 + 가로 화살표와 짧은 라벨 | 누가 누구에게 무엇을 넘기나 |
| (g) pins 번호 핀 `data-variant="pins"` | 글자 없는 넓은 SVG 위 HTML 번호 핀 + 옆 범례 | 화면 어디가 무엇인가(preview 해부도, faq 용어 핀) |

## 공용 CSS

```css
/* .d0-fig, .d0-fig__stage, figcaption은 shell.md에 있다 */
.d0-fig svg { width: 100%; max-width: 360px; height: auto; }
.d0-fig[data-size="wide"] svg { max-width: 400px; }
.d0-fig[data-size="wide"] .d0-s-text, .d0-fig[data-size="wide"] .d0-s-num { font-size: 18px; }
.d0-fig__scroll { overflow-x: auto; }
.d0-s-text { fill: var(--d0-grey-700); font-family: var(--d0-font); font-size: 14px; font-weight: 600; letter-spacing: var(--d0-tracking-body); font-variant-numeric: tabular-nums; }
.d0-s-text[data-on] { fill: var(--d0-blue-dark); }
.d0-s-muted { fill: var(--d0-grey-600); font-weight: 500; }
.d0-s-edge, .d0-s-node, .d0-s-ring, .d0-s-frame, .d0-s-line, .d0-s-zone, .d0-s-step, .d0-s-life {
  stroke-linecap: round; stroke-linejoin: round;
}
.d0-s-edge { fill: none; stroke: var(--d0-grey-500); stroke-width: 1.5; }
.d0-s-edge[data-on] { stroke: var(--d0-blue); stroke-width: 2.5; }
.d0-s-edge[data-back] { stroke-dasharray: 4 4; }
.d0-s-node { fill: #fff; stroke: var(--d0-grey-500); stroke-width: 1.5; }
.d0-s-node[data-on] { fill: var(--d0-blue); stroke: var(--d0-blue); }
.d0-s-ring { fill: none; stroke: var(--d0-blue); stroke-width: 1.5; }
.d0-s-track { fill: var(--d0-grey-100); }
.d0-s-bar { fill: var(--d0-grey-400); }
.d0-s-bar[data-on] { fill: var(--d0-blue); }
.d0-s-cell { fill: var(--d0-grey-200); }
.d0-s-head { fill: var(--d0-blue-light); stroke: var(--d0-blue); stroke-width: 0.75; } /* 썸네일 격자만 예외(축소 그림) */
.d0-s-key { fill: var(--d0-grey-400); }
.d0-s-sum { fill: var(--d0-blue); }
.d0-s-frame { fill: #fff; stroke: var(--d0-grey-500); stroke-width: 1.5; }
.d0-s-fill { fill: var(--d0-grey-100); }
.d0-s-line { fill: none; stroke: var(--d0-grey-300); stroke-width: 1.5; }
.d0-s-accent { fill: var(--d0-blue); }
.d0-s-zone { fill: var(--d0-blue-light); stroke: var(--d0-blue); stroke-width: 1.5; stroke-dasharray: 4 3; }
.d0-s-step { fill: #fff; stroke: var(--d0-grey-500); stroke-width: 1.5; }
.d0-s-step[data-on] { fill: var(--d0-blue-dark); stroke: var(--d0-blue-dark); }
.d0-s-num { fill: var(--d0-grey-700); font-family: var(--d0-font); font-size: 14px; font-weight: 600; font-variant-numeric: tabular-nums; text-anchor: middle; dominant-baseline: central; }
.d0-s-num[data-on] { fill: #fff; }
.d0-s-life { fill: none; stroke: var(--d0-grey-300); stroke-width: 1.5; }
.d0-s-tick { fill: none; stroke: #fff; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; } /* green·blue-dark 원 위 흰 체크 */
/* 의미색: 상태가 있는 표식에만. 글자 색으로는 쓰지 않는다 */
.d0-s-node[data-tone="green"], .d0-s-step[data-tone="green"] { fill: var(--d0-green); stroke: var(--d0-green); }
.d0-s-node[data-tone="red"], .d0-s-step[data-tone="red"] { fill: var(--d0-red); stroke: var(--d0-red); }
.d0-s-node[data-tone="orange"], .d0-s-step[data-tone="orange"] { fill: var(--d0-orange-bg); stroke: var(--d0-grey-700); } /* orange는 그래픽 3:1 미달 → 옅은 면 + 진한 테두리 */
.d0-s-bar[data-tone="green"] { fill: var(--d0-green); }
.d0-s-bar[data-tone="red"] { fill: var(--d0-red); }
.d0-s-bar[data-tone="orange"] { fill: var(--d0-orange); } /* 값 라벨이 막대 옆에 있을 때만 */
.d0-s-zone[data-tone="red"] { fill: var(--d0-red-bg); stroke: var(--d0-red); }
/* 핵심 무대 blue-light: 회색 선·흐린 글자를 한 단계 진하게 */
.d0-fig[data-stage="blue"] :is(.d0-s-edge, .d0-s-node, .d0-s-step, .d0-s-frame):not([data-on]):not([data-tone]) { stroke: var(--d0-grey-600); }
.d0-fig[data-stage="blue"] .d0-s-muted, .d0-fig[data-stage="blue"] .d0-s-num:not([data-on]) { fill: var(--d0-grey-700); }
```

대비(무대 grey-50 기준, tokens.css 값으로 계산): blue 3.75, blue-dark 5.18, green 3.26, red 3.36, orange 2.32(미달), grey-500 3.01, grey-400 2.06, grey-300 1.49.
blue-light 무대 위: blue 3.58, green 3.11, red 3.20, grey-600 4.49, grey-500 2.87(미달). 전체 표는 [shell.md](shell.md) 색 절.
뜻을 혼자 전하는 선·면(노드 테두리, 엣지, 화살표, 프레임, 강조)은 blue나 grey-500 이상이다. grey-400 이하 면·선은
값이 라벨 글자로 함께 적힌 막대, 이름이 카드 제목으로 적힌 격자 칸, 자리만 잡는 와이어프레임 면, 참여자 이름이 적힌 세로선에만 쓴다.
흰 숫자는 blue-dark 원 위에만 둔다(5.5:1). blue 원 위 흰 글자는 3.99:1이라 쓰지 않는다. green 원에는 숫자 대신 흰 체크선(`.d0-s-tick`, 그래픽 3.47:1)을 둔다.
**의미색 표식은 혼자 뜻을 전하지 않는다.** 완료 단계는 체크 모양, 실패 노드는 라벨, orange 면은 진한 테두리나 값 라벨을 함께 둔다.

## (a) graph — 연결 그래프

```html
<figure class="d0-fig" data-stage>
  <div class="d0-fig__stage">
  <svg viewBox="0 0 360 224" role="img" aria-labelledby="g1-t g1-d">
    <title id="g1-t">고친 파일과 연결된 검사</title>
    <desc id="g1-d">파일 두 개 중 고친 파일 하나에서 선이 검사 세 개로 이어져 블루로 칠해져 있어요. 다른 파일에 붙은 검사 두 개는 비어 있어요.</desc>
    <text class="d0-s-text d0-s-muted" x="290" y="16" text-anchor="middle">검사</text>
    <path class="d0-s-edge" d="M60 168 C175 168 175 160 290 160 M60 168 C175 168 175 200 290 200"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M60 80 C175 80 175 40 290 40"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M60 80 C175 80 175 80 290 80"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M60 80 C175 80 175 120 290 120"/>
    <circle class="d0-s-ring" cx="60" cy="80" r="17"/>
    <circle class="d0-s-node" data-on cx="60" cy="80" r="11"/>
    <circle class="d0-s-node" cx="60" cy="168" r="11"/>
    <circle class="d0-s-node" data-on cx="290" cy="40" r="9"/>
    <circle class="d0-s-node" data-on cx="290" cy="80" r="9"/>
    <circle class="d0-s-node" data-on cx="290" cy="120" r="9"/>
    <circle class="d0-s-node" cx="290" cy="160" r="9"/>
    <circle class="d0-s-node" cx="290" cy="200" r="9"/>
    <text class="d0-s-text" data-on x="60" y="116" text-anchor="middle">고친 파일</text>
    <text class="d0-s-text d0-s-muted" x="60" y="200" text-anchor="middle">다른 파일</text>
    <text class="d0-s-text" data-on x="306" y="85">3개</text>
  </svg>
  </div>
  <figcaption>고친 파일에서 선을 따라간 검사 세 개만 다시 돌아요.</figcaption>
</figure>
```

- 노드는 7개까지. 열은 2~3개(원인 → 중간 → 결과). 더 많으면 묶어서 `+12` 같은 노드 하나로 줄인다.
- 시작 노드(고친 것)는 블루 채움 + 바깥 고리. 닿는 노드·선만 `data-on`. 닿지 않는 것은 흰 채움 + grey-500 테두리.
- 상태가 있으면 노드에 의미색을 단다: 고장 난 곳 `data-tone="red"`, 통과한 곳 `green`(incident 영향 그래프 등). 의미색 노드에도 라벨을 붙인다.
- 강조 엣지는 갈래마다 `path` 하나 + `d0-draw`라 세 갈래가 함께 그려진다. 회색 엣지는 그리지 않고 처음부터 보인다.
- 노드는 원 또는 둥근 상자(`rect rx="8"`, 글자 없음). 상자 안에 문장을 넣지 않는다.

## (b) bars — 전/후 막대

```html
<figure class="d0-fig" data-stage>
  <div class="d0-fig__stage">
  <svg viewBox="0 0 360 112" role="img" aria-labelledby="b1-t b1-d">
    <title id="b1-t">내보내기 대기 시간 전과 후</title>
    <desc id="b1-d">전에는 14분, 지금은 6분이에요.</desc>
    <text class="d0-s-text d0-s-muted" x="0" y="34">전</text>
    <rect class="d0-s-bar" x="32" y="16" width="260" height="26" rx="6"/>
    <text class="d0-s-text" x="300" y="34">14분</text>
    <text class="d0-s-text" data-on x="0" y="86">후</text>
    <rect class="d0-s-track" x="32" y="68" width="260" height="26" rx="6"/>
    <rect class="d0-s-bar" data-on x="32" y="68" width="111" height="26" rx="6"/>
    <text class="d0-s-text" data-on x="151" y="86">6분</text>
  </svg>
  </div>
  <figcaption>기다리는 시간이 절반 아래로 줄었어요.</figcaption>
</figure>
```

- **배치.** 막대 SVG는 360px(`wide`는 400px)에서 멈추고 무대가 그 둘레를 채운다. 전체 폭 섹션에 혼자 두면 무대가 넓게 비므로
  `.d0-split` 한 열에 넣거나, 2열 figure(무대 왼쪽, figcaption 오른쪽 열)로 옆에 짧은 설명을 붙인다.

```html
<figure class="d0-fig" data-stage data-layout="side">
  <div class="d0-fig__stage"><svg>…</svg></div>
  <figcaption>기다리는 시간이 절반 아래로 줄었어요.</figcaption>
</figure>
```

```css
@media (min-width: 640px) {
  .d0-fig[data-layout="side"] { grid-template-columns: minmax(0, 440px) 1fr; align-items: center; gap: 24px; }
}
```

- 막대 폭 = 값 / 최댓값 × 트랙 폭(위 예: 6 / 14 × 260 = 111). 숫자를 지어 맞추지 않는다.
- **막대 수.** 전/후 비교 쌍은 2개까지(막대 4개). 비교 쌍이 3개 이상이면 [kpi-cards.md](kpi-cards.md)의 막대 변형(카드 하나에 쌍 하나)을 쓴다.
- 값 라벨은 막대 끝 바로 뒤(+8)에 둔다. 범례를 따로 두지 않는다. 후(지금) 막대만 블루.
- 막대가 전/후가 아니라 상태(통과·실패 건수)를 말하면 `data-tone="green|red"`로 칠한다. 값 라벨은 그대로 둔다.
- 막대가 3개 이상이면 행 간격 52를 유지하고 viewBox 높이를 `행 수 × 52 + 8`로 늘린다.

### 비율 막대 (`data-variant="ratio"`)

전체 한 줄 중 부분이 얼마인지 보여 준다. 막대는 **컨테이너 폭을 꽉 채운다**. 그래서 숫자 라벨은 SVG 밖 HTML에 두고
(SVG 글자는 폭을 따라 커지기 때문이다) 무대 없이 섹션 폭에 둔다. SVG는 `preserveAspectRatio="none"`으로 가로만 늘고, 높이는 CSS가 12px로 고정한다.

```html
<figure class="d0-fig" data-variant="ratio">
  <div class="d0-ratio__labels" aria-hidden="true">
    <span class="d0-ratio__part">58건 전부 검사</span>
    <span>전체 234건</span>
  </div>
  <svg class="d0-ratio__bar" viewBox="0 0 100 10" preserveAspectRatio="none" role="img" aria-labelledby="r1-t">
    <title id="r1-t">지난 주문 234건 중 58건(25%)을 전부 검사</title>
    <rect class="d0-s-bar" width="100" height="10"/>
    <rect class="d0-s-bar" data-on width="24.8" height="10"/>
  </svg>
  <figcaption>네 번에 한 번은 지금처럼 전부 검사해요.</figcaption>
</figure>
```

```css
.d0-fig[data-variant="ratio"] { gap: 8px; }
.d0-fig[data-variant="ratio"] svg { max-width: none; height: 12px; border-radius: 999px; overflow: hidden; }
.d0-ratio__labels { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px 16px; color: var(--d0-grey-600); font-size: 14px; font-variant-numeric: tabular-nums; }
.d0-ratio__part { color: var(--d0-blue-dark); font-weight: 600; }
```

- 부분 폭 = 부분 ÷ 전체 × 100(위 예: 58 ÷ 234 × 100 = 24.8). viewBox 폭이 100이라 그 값이 곧 퍼센트다.
- 부분은 blue, 나머지는 grey-400(값이 라벨로 적혀 있다). 모서리는 CSS `border-radius`로 둥글린다(`rx`는 늘어나며 찌그러진다).
- 라벨은 `aria-hidden`이고 접근 이름은 SVG `<title>`이 전체 문장으로 말한다. 부분이 둘 이상이면 rect를 이어 붙이고 블루는 하나만 쓴다.
- 섹션 폭의 절반만 쓰고 옆을 비우는 비율 막대는 금지다. 좁게 두고 싶으면 `.d0-split` 한쪽 열에 넣어 그 열을 채운다.

## (c) grid — 미니 격자 (JS 생성)

결과물이 표일 때 "어떤 모양의 표인가"를 썸네일로 그린다. 같은 함수로 카드 여러 장을 만든다.

```html
<figure class="d0-fig" data-stage>
  <div class="d0-fig__stage"><div data-grid='{"rows":8,"cols":6,"sumCol":true,"sumRow":true,"blanks":0.15,"seed":3,"label":"팀 행 × 일자 열 표"}'></div></div>
  <figcaption>팀마다 한 줄, 날짜마다 한 칸이에요.</figcaption>
</figure>
```

```js
function d0Grid(spec) {
  var NS = 'http://www.w3.org/2000/svg', W = 160, H = 96, P = 3;
  var head = spec.headRow !== false, key = spec.keyCol !== false;
  var svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svg.setAttribute('role', 'img');
  var t = document.createElementNS(NS, 'title');
  t.textContent = spec.label || '표 모양';
  svg.appendChild(t);
  var s = spec.seed || 1;
  var rnd = function () { s = (s * 9301 + 49297) % 233280; return s / 233280; };
  var cw = (W - P * 2) / spec.cols, rh = (H - P * 2) / spec.rows;
  for (var r = 0; r < spec.rows; r++) {
    for (var c = 0; c < spec.cols; c++) {
      var cls = 'd0-s-cell';
      if (head && r === 0) cls = 'd0-s-head';
      else if (key && c === 0) cls = 'd0-s-key';
      else if ((spec.sumCol && c === spec.cols - 1) || (spec.sumRow && r === spec.rows - 1)) cls = 'd0-s-sum';
      else if (rnd() < (spec.blanks || 0)) continue; // 빈칸은 그리지 않는다
      var e = document.createElementNS(NS, 'rect');
      e.setAttribute('x', P + c * cw + 1);
      e.setAttribute('y', P + r * rh + 1);
      e.setAttribute('width', Math.max(cw - 2, 1));
      e.setAttribute('height', Math.max(rh - 2, 1));
      e.setAttribute('rx', 2);
      e.setAttribute('class', cls);
      svg.appendChild(e);
    }
  }
  return svg;
}
document.querySelectorAll('[data-grid]').forEach(function (el) {
  el.replaceWith(d0Grid(JSON.parse(el.dataset.grid)));
});
```

- 스펙: `rows`·`cols`(머리 행·키 열 포함), `headRow`·`keyCol`(기본 true), `sumRow`·`sumCol`(기본 false),
  `blanks`(빈칸 비율 0~1), `seed`(같은 값이면 같은 모양), `label`(접근 이름, 필수).
- 색: 머리 행 blue-light(+ 얇은 blue 테두리), 키 열 grey-400, 합계 행·열 blue, 값 칸 grey-200, 빈칸은 생략.
- 글자 없는 그림이라 라벨 규칙의 예외다. 이름은 카드 제목이 말한다. 실제 결과물의 행·열 수에 맞춘다.

## (d) wireframe — 화면 골격

```html
<figure class="d0-fig" data-stage>
  <div class="d0-fig__stage">
  <svg viewBox="0 0 360 220" role="img" aria-labelledby="w1-t w1-d">
    <title id="w1-t">주문 관리 화면 골격</title>
    <desc id="w1-d">위쪽 바 오른쪽 버튼과 그 아래 필터 영역이 블루로 강조돼 있어요. 아래는 카드 두 장과 표 영역이에요.</desc>
    <rect class="d0-s-frame" x="1" y="1" width="358" height="218" rx="12"/>
    <path class="d0-s-line" d="M1 42 H359"/>
    <rect class="d0-s-fill" x="16" y="16" width="84" height="10" rx="5"/>
    <rect class="d0-s-accent" x="270" y="11" width="74" height="20" rx="6"/>
    <rect class="d0-s-zone" x="16" y="56" width="328" height="28" rx="6"/>
    <rect class="d0-s-fill" x="16" y="98" width="158" height="44" rx="8"/>
    <rect class="d0-s-fill" x="186" y="98" width="158" height="44" rx="8"/>
    <rect class="d0-s-fill" x="16" y="156" width="328" height="12" rx="4"/>
    <rect class="d0-s-fill" x="16" y="176" width="328" height="12" rx="4"/>
    <rect class="d0-s-fill" x="16" y="196" width="220" height="12" rx="4"/>
  </svg>
  </div>
  <figcaption>새 필터는 버튼 바로 아래, 표 위에 생겨요.</figcaption>
</figure>
```

- 회색 면은 자리만 잡는다(글자 없는 막대). 바뀌는 곳은 블루 하나(버튼은 채움, 영역은 점선 테두리 `d0-s-zone`).
- 라벨이 필요하면 SVG 밖 figcaption에 쓴다. 넣는다면 바뀌는 곳 하나에만 짧은 명사로.
- 눌러 봐야 이해되는 화면이면 와이어프레임 대신 [mockup-frame.md](mockup-frame.md)을 쓴다.
- 부분마다 이름을 붙여야 하면(해부도) SVG 안에 글자를 넣지 말고 (g) 번호 핀을 얹는다.

## (e) steps — 단계

번호 원을 한 줄로 잇고, 현재(또는 핵심) 단계 하나만 blue-dark로 채운다. 라벨은 원 아래 짧은 명사다.
글 상자를 화살표로 잇는 흐름 줄 대신 이 그림을 쓴다.

```html
<figure class="d0-fig" data-stage>
  <div class="d0-fig__stage">
  <svg viewBox="0 0 360 104" role="img" aria-labelledby="s1-t s1-d">
    <title id="s1-t">내보내기 네 단계</title>
    <desc id="s1-d">첫 단계 '누르기'는 초록 체크로 지금과 같다는 표시예요. 두 번째 '묶음 고르기'가 블루로 채워져 있어요. 이번에 새로 생기는 단계예요.</desc>
    <path class="d0-s-edge" d="M60 36 H124 M156 36 H204 M236 36 H292"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M60 36 H124"/>
    <circle class="d0-s-step" data-tone="green" cx="44" cy="36" r="16"/>
    <circle class="d0-s-step" data-on cx="140" cy="36" r="16"/>
    <circle class="d0-s-step" cx="220" cy="36" r="16"/>
    <circle class="d0-s-step" cx="308" cy="36" r="16"/>
    <path class="d0-s-tick" d="M37 36 L42 41 L51 31"/>
    <text class="d0-s-num" data-on x="140" y="36">2</text>
    <text class="d0-s-num" x="220" y="36">3</text>
    <text class="d0-s-num" x="308" y="36">4</text>
    <text class="d0-s-text d0-s-muted" x="44" y="80" text-anchor="middle">누르기</text>
    <text class="d0-s-text" data-on x="140" y="80" text-anchor="middle">묶음 고르기</text>
    <text class="d0-s-text d0-s-muted" x="220" y="80" text-anchor="middle">미리보기</text>
    <text class="d0-s-text d0-s-muted" x="308" y="80" text-anchor="middle">받기</text>
  </svg>
  </div>
  <figcaption>두 번째 단계가 새로 생겨요. 나머지는 지금과 같아요.</figcaption>
</figure>
```

- 단계는 3~5개. 원 r 16(기본 크기에서 렌더 지름 32px), 원 사이는 1.5px grey-500 선. 원 중심 간격은 라벨 폭에 맞춰 80~100.
- 강조는 단계 하나만: 원 채움 blue-dark + 흰 번호 + 라벨 blue-dark + 그 단계로 들어오는 선(`data-on`, `d0-draw`). 색과 채움이 함께 바뀐다.
- 끝난 단계는 `data-tone="green"` 원 + 흰 체크선(`.d0-s-tick`, 번호 대신). 막힌 단계는 `red` 원 + 라벨. 체크 모양이 색 없이도 완료를 말한다.
- 라벨은 1~2단어(렌더 14px 기준 한 라벨 약 80px 이내). 더 길면 figcaption이나 아래 목록으로 보낸다.
- 단계마다 설명이 필요하면 그림 아래 [step-columns.md](step-columns.md)를 붙이고, 그림의 번호와 같은 번호를 쓴다.

## (f) sequence — 주고받기

참여자 3~4명이 무엇을 주고받는지 그린다. 참여자 이름은 위, 세로선은 아래로, 메시지는 가로 화살표 위 짧은 라벨이다.

```html
<figure class="d0-fig" data-stage>
  <div class="d0-fig__stage">
  <svg viewBox="0 0 360 200" role="img" aria-labelledby="q1-t q1-d">
    <title id="q1-t">내보내기 요청이 오가는 순서</title>
    <desc id="q1-d">사용자가 서버에 내보내기를 누르면 서버가 저장소에 파일을 저장해요. 이 화살표가 블루예요. 그다음 서버가 사용자에게 받기 링크를 돌려줘요.</desc>
    <text class="d0-s-text" x="60" y="18" text-anchor="middle">사용자</text>
    <text class="d0-s-text" x="180" y="18" text-anchor="middle">서버</text>
    <text class="d0-s-text" x="300" y="18" text-anchor="middle">저장소</text>
    <path class="d0-s-life" d="M60 32 V188 M180 32 V188 M300 32 V188"/>
    <path class="d0-s-edge" d="M60 72 H178 M170 66 L178 72 L170 78"/>
    <text class="d0-s-text d0-s-muted" x="120" y="62" text-anchor="middle">누르기</text>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M180 116 H298 M290 110 L298 116 L290 122"/>
    <text class="d0-s-text" data-on x="240" y="106" text-anchor="middle">파일 저장</text>
    <path class="d0-s-edge" data-back d="M180 160 H62 M70 154 L62 160 L70 166"/>
    <text class="d0-s-text d0-s-muted" x="120" y="150" text-anchor="middle">받기 링크</text>
  </svg>
  </div>
  <figcaption>파일은 서버가 저장소에 둔 뒤 링크로 돌려줘요.</figcaption>
</figure>
```

- 참여자는 3~4명, 메시지는 5개까지. 참여자 간격 120(4명이면 viewBox 480 + `data-size="wide"`).
- 세로선은 grey-300 1.5px(이름이 위에 적혀 있어 자리만 잡는다). 메시지 화살표는 grey-500 1.5px, 돌아오는 응답은 점선(`data-back`).
- 핵심 메시지 하나만 `data-on`(blue 2.5px + `d0-draw`) + 라벨 blue-dark. 화살촉은 같은 `path`의 서브패스로 그린다(`marker` 금지, 색이 CSS를 안 따른다).
- 라벨은 화살표 위 10px, 두 세로선 가운데. 한 메시지 라벨은 1~2단어다. 조건·반복은 figcaption으로 보낸다.

## (g) pins — 번호 핀 오버레이

글자 없는 넓은 SVG(와이어프레임, 파일 구성 등) 위에 HTML 번호 핀(①②③)을 얹고, 이름과 뜻은 옆 범례 `dl`에 쓴다.
SVG에 글자가 없으므로 위 라벨 크기 게이트(렌더 11~16px 계산)를 받지 않고 **SVG를 640px까지 키운다**. 핀 숫자와 범례는 HTML 텍스트 규칙을 따른다.

```html
<figure class="d0-fig" data-stage data-variant="pins">
  <div class="d0-fig__stage">
    <div class="d0-pins">
      <svg viewBox="0 0 480 300" role="img" aria-labelledby="p1-t p1-d">
        <title id="p1-t">설명 페이지 한 장의 구성</title>
        <desc id="p1-d">맨 위 머리, 그 아래 블루로 강조된 그림 무대, 맨 아래 목록 영역이 있어요. 번호 1~3이 각 부분을 가리켜요.</desc>
        <rect class="d0-s-frame" x="1" y="1" width="478" height="298" rx="12"/>
        <rect class="d0-s-fill" x="24" y="24" width="180" height="14" rx="7"/>
        <rect class="d0-s-fill" x="24" y="48" width="300" height="10" rx="5"/>
        <rect class="d0-s-zone" x="24" y="80" width="432" height="128" rx="10"/>
        <rect class="d0-s-accent" x="48" y="112" width="160" height="64" rx="8"/>
        <path class="d0-s-line" d="M24 236 H456 M24 264 H360"/>
      </svg>
      <span class="d0-pin" style="left: 45%; top: 8%" aria-hidden="true">1</span>
      <span class="d0-pin" data-on style="left: 50%; top: 27%" aria-hidden="true">2</span>
      <span class="d0-pin" style="left: 80%; top: 79%" aria-hidden="true">3</span>
    </div>
  </div>
  <dl class="d0-pins__key">
    <div><dt><span class="d0-pin">1</span>머리</dt><dd>제목과 결론 한 줄이에요.</dd></div>
    <div data-on><dt><span class="d0-pin" data-on>2</span>그림 무대</dt><dd>페이지의 주인공 그림이 놓여요.</dd></div>
    <div><dt><span class="d0-pin">3</span>목록</dt><dd>주의할 점과 할 일이에요.</dd></div>
  </dl>
  <figcaption>그림 무대가 가장 큰 자리를 차지해요.</figcaption>
</figure>
```

```css
.d0-fig[data-variant="pins"] .d0-pins { position: relative; justify-self: center; width: 100%; max-width: 640px; }
.d0-fig[data-variant="pins"] svg { display: block; max-width: none; }
.d0-pin {
  display: inline-grid; place-items: center; flex: none; width: 24px; height: 24px; border-radius: 999px;
  background: #fff; box-shadow: inset 0 0 0 1.5px var(--d0-grey-700);
  color: var(--d0-grey-900); font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; line-height: 1;
}
.d0-pin[data-on] { background: var(--d0-blue-dark); box-shadow: none; color: #fff; }
.d0-pins .d0-pin { position: absolute; transform: translate(-50%, -50%); }
.d0-pins__key { display: grid; gap: 12px; margin: 0; }
.d0-pins__key dt { display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 600; }
.d0-pins__key [data-on] dt { color: var(--d0-blue-dark); }
.d0-pins__key dd { margin: 4px 0 0 32px; color: var(--d0-grey-600); font-size: 14px; }
@media (min-width: 900px) {
  .d0-fig[data-variant="pins"] { grid-template-columns: minmax(0, 1fr) minmax(220px, 300px); align-items: center; column-gap: 28px; }
  .d0-fig[data-variant="pins"] figcaption { grid-column: 1 / -1; }
}
```

- 핀 위치 = SVG 좌표 ÷ viewBox 크기 × 100%(위 예: 무대 윗변 가운데 (240, 80) → 240 ÷ 480 = 50%, 80 ÷ 300 = 27%). 래퍼 `.d0-pins`가 SVG와 같은 크기라 비율이 그대로 맞는다.
- 핀은 24px 원 + 13px 숫자다. 기본은 흰 원 + grey-700 테두리 + grey-900 숫자, 강조 하나만 blue-dark 원 + 흰 숫자(5.5:1). blue 원 위 흰 숫자는 3.99:1이라 쓰지 않는다.
- 핀은 3~6개. 화면 위 핀은 `aria-hidden`이고, 범례 `dt`가 같은 번호와 이름을 소리 내어 전한다. SVG `<desc>`는 번호가 무엇을 가리키는지 한 문장으로 말한다.
- 375px에서도 핀은 24px 그대로다. 핀끼리 겹치면(중심 간격 28px 미만) 핀을 줄이거나 부분을 묶는다. 범례는 900px 아래에서 그림 아래로 내려간다.
- 핀 옆에 글자를 붙이지 않는다. 이름은 범례에만 쓴다. 범례 `dd`는 한 문장이다.

## 금지

- 텍스트 상자 + 화살표 줄(문장이 든 상자), 정보 없는 장식 그림, 3D·그라디언트·그림자·아이콘 일러스트, Mermaid 등 자동 배치 도식.
- 무대 없이 맨바닥에 둔 도식(비율 막대·카드 안 격자 제외), 무대 안에 figcaption, 무대에 테두리·그림자.
- 1.5·2.5 외 선 굵기(썸네일 격자 머리 테두리 제외), 각진 선 끝, 강조 경로 아닌 선에 그리기 모션.
- 회색만으로 된 도식(blue·의미색 표식 0개), 의미색 `<text>` 글자, 테두리·라벨 없이 혼자 뜻을 전하는 orange 표식.
- 노드 7개 초과, SVG 안 문장, 375px에서 11px 아래로 줄어들거나 데스크톱에서 16px을 넘는 라벨(h2보다 큰 라벨), 블루 강조가 흩어진 그림(강조 묶음은 하나).
- 폭 100% SVG 안 `<text>`(비율 막대 라벨은 HTML로), 절반 폭에 옆이 빈 비율 막대.
- `<title>` 없는 정보 SVG, SVG 안 hex·rgb 색값, `width`·`height` 고정 속성으로 반응형을 깨는 SVG.
