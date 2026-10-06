# diagram — SVG 도식

페이지의 주인공이다. 대상의 **모양**을 선과 면으로 그린다. 글은 그림 아래 주석 한 줄로 줄인다.

## 해부 구조

- `figure.d0-fig` = 인라인 SVG 하나 → `figcaption` 한 줄("그래서 무엇이 보이는가").
- SVG는 `role="img"` + `<title>`(그림 이름) + `<desc>`(무엇이 강조됐는지 한두 문장). 장식 SVG만 `aria-hidden="true"`.
- 색은 SVG 안에 직접 쓰지 않는다. 아래 `d0-s-*` 클래스가 `var(--d0-*)`를 쓴다. 강조는 블루 하나, 나머지는 회색.
- 강조는 색만으로 말하지 않는다. 채움/빈 모양, 굵기, 라벨 중 하나를 함께 바꾼다.
- 반응형: `viewBox`만 두고 `width`·`height` 속성은 쓰지 않는다. CSS가 폭 100%, 높이 auto로 맞춘다.
- **텍스트 상자를 화살표로 이은 것은 도식이 아니다.** 상자 안에 문장이 들어가는 순간 글이다.

## 라벨

- 설명 문장은 SVG 밖 `figcaption`·HTML에 둔다. 확대·번역·복사가 되기 때문이다.
- SVG `<text>`는 짧은 노드·값 라벨(명사 1~3단어, `고친 파일`, `6분`)에만 쓴다.
- **측정 기준(정본).** 렌더 글자 크기 = font-size f × (SVG 렌더 폭 ÷ viewBox 폭 W). SVG는 폭 100%로 커지므로 렌더 폭은
  `min(컨테이너 폭, max-width)`다. 글자 박스 높이(`getBBox`·`getBoundingClientRect`의 height)는 쓰지 않는다. 줄 높이와 글꼴 여백이 섞여 크게 나온다.
  - 375px 화면(컨테이너 343px)에서 **11px 이상**: `f × 343 ÷ W ≥ 11` → `W ≤ 31 × f`.
  - 데스크톱에서 **16px 이하**(h2 18px보다 작게): `f × max-width ÷ W ≤ 16` → `max-width ≤ W × 16 ÷ f`.
  - 예: W 360, f 14에 max-width 500이면 데스크톱 라벨이 19.4px로 h2보다 커진다. max-width를 400으로 두면 15.6px다.
- 아래 두 크기 중 하나를 고른다. 다른 W를 쓰면 위 두 식으로 max-width를 다시 계산해 해당 SVG에 둔다.

| 크기 | viewBox 폭 W | 글자 f | SVG max-width | 375px 라벨 | 데스크톱 라벨 | 노드 r 9→렌더 |
| --- | --- | --- | --- | --- | --- | --- |
| 기본 | 360 | 14 | 400px | 13.3px | 15.6px | 20px 지름 |
| `data-size="wide"` | 480 | 16 | 480px | 11.4px | 16.0px | 18px 지름 |

- 노드·원은 viewBox 단위로 그린다. 기본 크기에서 노드 r 9~11(렌더 지름 20~24px), 바깥 고리 r 17(38px)을 넘기지 않는다.
- 이 조건을 못 맞추는 넓은 그림(W > 31 × f)은 `.d0-fig__scroll` 상자에 넣는다. 페이지 가로 스크롤은 금지다.
- 폭을 꽉 채워야 하는 그림(비율 막대)은 글자를 SVG 밖 HTML에 두고 SVG는 도형만 그린다. 아래 (b) 비율 변형 참고.

## 변형

| 변형 | 그리는 것 | 언제 |
| --- | --- | --- |
| (a) graph 연결 그래프 | 노드 원 + 엣지 곡선, 닿는 것만 블루 | 무엇이 무엇에 닿나(의존, 영향 범위) |
| (b) bars 전/후 막대 | 시간·양을 막대 길이로 | 얼마나 줄었나·늘었나 |
| (b) bars `data-variant="ratio"` 비율 막대 | 전체 한 줄 안의 부분 | 전체 중 얼마인가(234건 중 58건) |
| (c) grid 미니 격자 | 표의 행·열 모양 썸네일(JS 생성) | 결과물이 어떤 모양의 표인가 |
| (d) wireframe 화면 골격 | 상단 바·카드·버튼을 상자로 | 어떤 화면의 어디가 바뀌나 |

## 공용 CSS

```css
.d0-fig { display: grid; gap: 12px; align-content: start; min-width: 0; }
.d0-fig svg { width: 100%; max-width: 400px; height: auto; }
.d0-fig[data-size="wide"] svg { max-width: 480px; }
.d0-fig[data-size="wide"] .d0-s-text { font-size: 16px; }
.d0-fig figcaption { color: var(--d0-grey-600); font-size: 14px; }
.d0-fig__scroll { overflow-x: auto; }
.d0-s-text { fill: var(--d0-grey-700); font-family: var(--d0-font); font-size: 14px; font-weight: 600; letter-spacing: var(--d0-tracking-body); font-variant-numeric: tabular-nums; }
.d0-s-text[data-on] { fill: var(--d0-blue-dark); }
.d0-s-muted { fill: var(--d0-grey-600); font-weight: 500; }
.d0-s-edge { fill: none; stroke: var(--d0-grey-500); stroke-width: 1.25; }
.d0-s-edge[data-on] { stroke: var(--d0-blue); stroke-width: 2.5; }
.d0-s-node { fill: #fff; stroke: var(--d0-grey-500); stroke-width: 1.5; }
.d0-s-node[data-on] { fill: var(--d0-blue); stroke: var(--d0-blue); }
.d0-s-ring { fill: none; stroke: var(--d0-blue); stroke-width: 2; }
.d0-s-track { fill: var(--d0-grey-100); }
.d0-s-bar { fill: var(--d0-grey-400); }
.d0-s-bar[data-on] { fill: var(--d0-blue); }
.d0-s-cell { fill: var(--d0-grey-200); }
.d0-s-head { fill: var(--d0-blue-light); stroke: var(--d0-blue); stroke-width: 0.75; }
.d0-s-key { fill: var(--d0-grey-400); }
.d0-s-sum { fill: var(--d0-blue); }
.d0-s-frame { fill: #fff; stroke: var(--d0-grey-500); stroke-width: 1.25; }
.d0-s-fill { fill: var(--d0-grey-100); }
.d0-s-line { fill: none; stroke: var(--d0-grey-300); stroke-width: 1; }
.d0-s-accent { fill: var(--d0-blue); }
.d0-s-zone { fill: var(--d0-blue-light); stroke: var(--d0-blue); stroke-width: 1.5; stroke-dasharray: 4 3; }
```

대비(흰 바탕 기준, tokens.css 값으로 계산): blue 3.99, grey-500 3.19, grey-400 2.19, grey-300 1.58.
뜻을 혼자 전하는 선·면(노드 테두리, 엣지, 프레임, 강조)은 blue나 grey-500 이상이다. grey-400 이하 면은
값이 라벨 글자로 함께 적힌 막대, 이름이 카드 제목으로 적힌 격자 칸, 자리만 잡는 와이어프레임 면에만 쓴다.

## (a) graph — 연결 그래프

```html
<figure class="d0-fig">
  <svg viewBox="0 0 360 224" role="img" aria-labelledby="g1-t g1-d">
    <title id="g1-t">고친 파일과 연결된 검사</title>
    <desc id="g1-d">파일 두 개 중 고친 파일 하나에서 선이 검사 세 개로 이어져 블루로 칠해져 있어요. 다른 파일에 붙은 검사 두 개는 비어 있어요.</desc>
    <text class="d0-s-text d0-s-muted" x="290" y="16" text-anchor="middle">검사</text>
    <path class="d0-s-edge" d="M60 168 C175 168 175 160 290 160 M60 168 C175 168 175 200 290 200"/>
    <path class="d0-s-edge" data-on d="M60 80 C175 80 175 40 290 40 M60 80 C175 80 175 80 290 80 M60 80 C175 80 175 120 290 120"/>
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
  <figcaption>고친 파일에서 선을 따라간 검사 세 개만 다시 돌아요.</figcaption>
</figure>
```

- 노드는 7개까지. 열은 2~3개(원인 → 중간 → 결과). 더 많으면 묶어서 `+12` 같은 노드 하나로 줄인다.
- 시작 노드(고친 것)는 블루 채움 + 바깥 고리. 닿는 노드·선만 `data-on`. 닿지 않는 것은 흰 채움 + grey-500 테두리.
- 노드는 원 또는 둥근 상자(`rect rx="8"`, 글자 없음). 상자 안에 문장을 넣지 않는다.

## (b) bars — 전/후 막대

```html
<figure class="d0-fig">
  <svg viewBox="0 0 360 112" role="img" aria-labelledby="b1-t b1-d">
    <title id="b1-t">내보내기 대기 시간 전과 후</title>
    <desc id="b1-d">전에는 14분, 지금은 6분이에요.</desc>
    <text class="d0-s-text d0-s-muted" x="0" y="34">전</text>
    <rect class="d0-s-track" x="32" y="16" width="260" height="26" rx="6"/>
    <rect class="d0-s-bar" x="32" y="16" width="260" height="26" rx="6"/>
    <text class="d0-s-text" x="300" y="34">14분</text>
    <text class="d0-s-text" data-on x="0" y="86">후</text>
    <rect class="d0-s-track" x="32" y="68" width="260" height="26" rx="6"/>
    <rect class="d0-s-bar" data-on x="32" y="68" width="111" height="26" rx="6"/>
    <text class="d0-s-text" data-on x="151" y="86">6분</text>
  </svg>
  <figcaption>기다리는 시간이 절반 아래로 줄었어요.</figcaption>
</figure>
```

- **배치.** 기본 막대는 SVG가 400px(`wide`는 480px)에서 멈춘다. 전체 폭 섹션에 혼자 두면 오른쪽이 빈다. 아래 중 하나로 둔다.
  `.d0-split` 한 열에 넣거나, 2열 figure(그림 왼쪽, figcaption 오른쪽 열)로 옆에 짧은 설명을 붙인다.
  전체 폭에 단독으로 둘 때만 `data-size="wide"`(480px)를 쓴다(이 경우 viewBox는 `0 0 480 …`).

```html
<figure class="d0-fig" data-layout="side">
  <svg>…</svg>
  <figcaption>기다리는 시간이 절반 아래로 줄었어요.</figcaption>
</figure>
```

```css
@media (min-width: 640px) {
  .d0-fig[data-layout="side"] { grid-template-columns: minmax(0, 400px) 1fr; align-items: center; gap: 24px; }
}
```

- 막대 폭 = 값 / 최댓값 × 트랙 폭(위 예: 6 / 14 × 260 = 111). 숫자를 지어 맞추지 않는다.
- **막대 수.** 전/후 비교 쌍은 2개까지(막대 4개). 비교 쌍이 3개 이상이면 [kpi-cards.md](kpi-cards.md)의 막대 변형(카드 하나에 쌍 하나)을 쓴다.
- 값 라벨은 막대 끝 바로 뒤(+8)에 둔다. 범례를 따로 두지 않는다. 후(지금) 막대만 블루.
- 막대가 3개 이상이면 행 간격 52를 유지하고 viewBox 높이를 `행 수 × 52 + 8`로 늘린다.

### 비율 막대 (`data-variant="ratio"`)

전체 한 줄 중 부분이 얼마인지 보여 준다. 막대는 **컨테이너 폭을 꽉 채운다**. 그래서 숫자 라벨은 SVG 밖 HTML에 둔다
(SVG 글자는 폭을 따라 커지기 때문이다). SVG는 `preserveAspectRatio="none"`으로 가로만 늘고, 높이는 CSS가 24px로 고정한다.

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
.d0-fig[data-variant="ratio"] svg { max-width: none; height: 24px; border-radius: 6px; overflow: hidden; }
.d0-ratio__labels { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px 16px; color: var(--d0-grey-600); font-size: 15px; font-variant-numeric: tabular-nums; }
.d0-ratio__part { color: var(--d0-blue-dark); font-weight: 650; }
```

- 부분 폭 = 부분 ÷ 전체 × 100(위 예: 58 ÷ 234 × 100 = 24.8). viewBox 폭이 100이라 그 값이 곧 퍼센트다.
- 부분은 blue, 나머지는 grey-400(값이 라벨로 적혀 있다). 모서리는 CSS `border-radius`로 둥글린다(`rx`는 늘어나며 찌그러진다).
- 라벨은 `aria-hidden`이고 접근 이름은 SVG `<title>`이 전체 문장으로 말한다. 부분이 둘 이상이면 rect를 이어 붙이고 블루는 하나만 쓴다.
- 섹션 폭의 절반만 쓰고 옆을 비우는 비율 막대는 금지다. 좁게 두고 싶으면 `.d0-split` 한쪽 열에 넣어 그 열을 채운다.

## (c) grid — 미니 격자 (JS 생성)

결과물이 표일 때 "어떤 모양의 표인가"를 썸네일로 그린다. 같은 함수로 카드 여러 장을 만든다.

```html
<figure class="d0-fig">
  <div data-grid='{"rows":8,"cols":6,"sumCol":true,"sumRow":true,"blanks":0.15,"seed":3,"label":"팀 행 × 일자 열 표"}'></div>
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
<figure class="d0-fig">
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
  <figcaption>새 필터는 버튼 바로 아래, 표 위에 생겨요.</figcaption>
</figure>
```

- 회색 면은 자리만 잡는다(글자 없는 막대). 바뀌는 곳은 블루 하나(버튼은 채움, 영역은 점선 테두리 `d0-s-zone`).
- 라벨이 필요하면 SVG 밖 figcaption에 쓴다. 넣는다면 바뀌는 곳 하나에만 짧은 명사로.
- 눌러 봐야 이해되는 화면이면 와이어프레임 대신 [mockup-frame.md](mockup-frame.md)을 쓴다.

## 금지

- 텍스트 상자 + 화살표 줄(문장이 든 상자), 정보 없는 장식 그림, 3D·그라디언트·그림자·아이콘 일러스트.
- 노드 7개 초과, SVG 안 문장, 375px에서 11px 아래로 줄어들거나 데스크톱에서 16px을 넘는 라벨(h2보다 큰 라벨), 블루 강조가 흩어진 그림(강조 묶음은 하나).
- 폭 100% SVG 안 `<text>`(비율 막대 라벨은 HTML로), 절반 폭에 옆이 빈 비율 막대.
- `<title>` 없는 정보 SVG, SVG 안 hex·rgb 색값, `width`·`height` 고정 속성으로 반응형을 깨는 SVG.
