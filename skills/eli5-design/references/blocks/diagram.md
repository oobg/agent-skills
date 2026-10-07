# diagram — SVG 도식

페이지의 주인공이다. 대상의 **모양**을 선과 면으로 그린다. 글은 그림 아래 주석 한 줄로 줄인다.

## 해부 구조

- `figure.d0-fig` = 인라인 SVG 하나 → 아래 `figcaption` 한 줄(13px grey-600, "그래서 무엇이 보이는가"). 장르는 `data-genre`(아래 장르 절).
- **무대는 기본 없음, 필요할 때만.** 글자 없는 도식이 여백 없이 떠서 경계가 안 보일 때, 흰 면 요소에 받침 면이 필요할 때만
  `figure.d0-fig[data-stage]` + 무대 패널 `div.d0-fig__stage`(grey-50, `--d0-radius-card`, 패딩 28px / 모바일 20px)를 쓰고 `figcaption`은 패널 **밖**에 둔다.
  **무대 패딩 때문에 렌더 라벨이 하한 아래로 내려가면 무대를 쓰지 않는다**(아래 라벨 절). 글자 있는 도식은 375px에서 그렇게 되므로 무대 없이 두고, 경계는 그림 안 선·면(세로선의 끝, 프레임, 트랙)으로 만든다.
  기준과 CSS는 [shell.md](shell.md) 그림 무대 절. 아래 스니펫은 모두 무대 없이 SVG를 `figure` 바로 안에 둔다. 글자 없는 그림에 무대를 더하려면 `data-stage`를 달고 SVG를 `div.d0-fig__stage`로 감싼다.
- **그림은 축 폭을 채운다.** SVG 렌더 폭은 놓인 자리(축 720px, narrow 640px, `.d0-wide` 열) 폭의 100%가 기본이다. 축 폭에서 너무 커 보이는 단순 도식(점·단계 3~4개)은 `data-fit="compact"`(75%, 가운데)로 둔다.
  옆에 남는 폭을 설명 문단·목록으로 채우지 않는다. 설명은 figcaption과 그림 아래 explanation으로 둔다. 그림 지점과 번호로 대응하는 주석·범례만 `.d0-wide` 안 2열(문서의 분할선, 그림/주석이면 7/5)로 옆에 둘 수 있다([shell.md](shell.md) 2열 절, 아래 (g)·(i)).
- SVG는 `role="img"` + `<title>`(그림 이름) + `<desc>`(무엇이 강조됐는지 한두 문장). 장식 SVG만 `aria-hidden="true"`.
- 색은 SVG 안에 직접 쓰지 않는다. 아래 `d0-s-*` 클래스가 `var(--d0-*)`를 쓴다. 강조 묶음은 블루 하나(같은 의미 계열은 행이 여럿이어도 한 묶음, 정의는 [composition.md](../composition.md) 강조 순서), 상태가 있는 표식은
  의미색 `data-tone="green|orange|red"`(완료·통과 / 주의·준비 / 실패·위험)를 단다. **회색만으로 된 도식은 금지**다. 색 규칙 정본은 [shell.md](shell.md) 색 절.
- 페이지의 핵심 도식 하나는 무대를 blue-light로 칠할 수 있다(`figure.d0-fig[data-stage="blue"]`). 그 위 회색 선은 grey-600, 흐린 라벨은 grey-700로
  자동으로 한 단계 진해진다(blue-light 위 grey-500 선 2.87, grey-600 글자 4.49라 미달). blue 무대는 면 단위 옅은 표면이라 색 비율에서 빼고 장면 수로 센다(페이지당 1개).
  blue 무대는 축 안이나 `.d0-wide` 열 안의 무대에만 쓰고 `.d0-wide` 전체 폭에는 칠하지 않는다. 무대 규칙(글자 있는 도식은 무대 없음)을 그대로 따른다. Impact 안에는 그림 무대를 두지 않는다.
- 강조는 색만으로 말하지 않는다. 채움/빈 모양, 굵기, 라벨 중 하나를 함께 바꾼다.
- **선.** 굵기는 기본 1.5, 강조 2.5 두 가지뿐이다. 모든 선은 `stroke-linecap: round`, `stroke-linejoin: round`. 노드에 그림자·그라디언트 없음.
- **그리기 모션.** 강조 경로(`data-on` 엣지·화살표)에 `class="… d0-draw"`와 `pathLength="1"`을 붙이면 섹션이 드러날 때 600ms 동안 그려진다.
  갈래마다 `path`를 따로 둔다(한 `path`의 서브패스는 순서대로 이어 그려진다). 동작·reduced-motion 처리는 [shell.md](shell.md) 모션.
- 반응형: `viewBox`만 두고 `width`·`height` 속성은 쓰지 않는다. CSS가 폭 100%, 높이 auto로 맞춘다.
- **텍스트 상자를 화살표로 이은 것은 도식이 아니다.** 상자 안에 문장이 들어가는 순간 글이다. Mermaid 등 자동 배치 도구는 쓰지 않고 손으로 그린다.

## 라벨

이 절의 글자 크기(`.d0-s-text`·`.d0-s-num`)와 렌더 게이트는 **page 규칙**이다. deck의 도식 글자는 [slide-deck.md](slide-deck.md) 타이포 절의 그림 글자 규칙(`d0-sl-label`·`d0-sl-value`, `--sl-font`, SVG 안 `font-size` 속성 금지)을 따른다. 도형 클래스는 page·deck 공용이다(아래 공용 CSS).

- 설명 문장은 SVG 밖 `figcaption`·HTML에 둔다. 확대·번역·복사가 되기 때문이다.
- SVG `<text>`는 짧은 노드·값 라벨(명사 1~3단어, `고친 파일`, `6분`)에만 쓴다.
- **게이트.** 렌더 라벨은 1280px에서 **13px 이상 20px 이하**(h2 20px보다 크지 않게), 375·320px에서 **11px 이상**이다. 권장은 데스크톱 16~18px다.
- **측정 기준(정본).** 렌더 글자 크기 = font-size f × (SVG 렌더 폭 ÷ viewBox 폭 W). 렌더 폭은 SVG box 폭(무대가 있으면 무대 안쪽 폭, compact면 그 75%)이다.
  글자 박스 높이(`getBBox`·`getBoundingClientRect`의 height)는 쓰지 않는다. 줄 높이와 글꼴 여백이 섞여 크게 나온다.
- **글자 있는 SVG는 viewBox 폭 560으로 그린다.** 축 720px은 모바일 폭의 약 2.1배라, 한 viewBox로 데스크톱 13~20px과 모바일 11px 이상을 함께 맞추려면 좁은 화면에서 글자를 키워야 한다.
  그래서 f는 기본 14, 560px 이하 화면 20, 340px 이하 22다(아래 공용 CSS). 이 모바일 확대는 `.d0-page` 안에만 걸고 덱 슬라이드에는 걸지 않는다. 글자 없는 SVG(와이어프레임·핀 그림·썸네일)는 이 계산을 받지 않으므로 viewBox 폭이 자유롭다.

| 놓는 곳 | 렌더 폭 | f | 렌더 라벨 |
| --- | --- | --- | --- |
| 축(1280) | 720px | 14 | 18.0px |
| narrow 축(1280) | 640px | 14 | 16.0px |
| `.d0-wide` 7/5 그림 열(1280) | 약 643px | 14 | 16.1px |
| compact(1280) | 540px | 14 | 13.5px |
| `.d0-wide` 6/6 열(1280) | 약 544px | 14 | 13.6px |
| 390px 화면 | 358px | 20 | 12.8px |
| 375px 화면 | 343px | 20 | 12.3px |
| 320px 화면 | 288px | 22 | 11.3px |

- **무대와 라벨.** 무대는 렌더 폭을 패딩만큼 줄인다(데스크톱 56px, 모바일 40px). 375px에서 무대 안쪽 303px이면 20 × 303 ÷ 560 = 10.8px로 11px 아래다. 그래서 글자 있는 도식에는 무대를 두지 않는다.
  narrow 축에서는 compact를 쓰지 않는다(14 × 480 ÷ 560 = 12px). 다른 W를 쓰면 위 식으로 1280·375·320px 세 폭을 다시 계산한다.
- **너무 커지는 그림.** 작은 viewBox(예: 폭 240)를 축 폭으로 키우면 라벨·노드가 과대해진다(14 × 720 ÷ 240 = 42px). 글자 있는 그림은 viewBox 폭 560으로 다시 그려 축 폭에 맞추고, 그래도 단순해 커 보이면 `data-fit="compact"`를 쓴다.
- 번호 글자(`.d0-s-num`)도 같은 식을 따른다.
- 노드·원은 viewBox 단위로 그린다. 노드 r 14~17(축 720px에서 렌더 지름 36~44px), 바깥 고리 r 26을 넘기지 않는다. 이 반지름은 page 규칙이다. deck SVG(viewBox 400·800, 렌더 배율이 다름)는 [slide-deck.md](slide-deck.md) 샘플처럼 viewBox에 맞춰 키운다(예: viewBox 800에서 r 24).
- 선 굵기 1.5·2.5는 viewBox 단위다. viewBox 560을 축 720px에 그리면 렌더 약 1.9·3.2px이다.
- 375px에서 라벨이 11px 아래로 주는 넓은 그림(가로로 아주 긴 타임라인 등)은 세로로 돌리거나 `.d0-fig__scroll` 상자에 넣는다. 페이지 가로 스크롤은 금지다.
- 폭을 꽉 채워야 하고 늘어나는 그림(비율 막대)은 글자를 SVG 밖 HTML에 두고 SVG는 도형만 그린다. 아래 (b) 비율 변형 참고.

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
| (h) converge 모으기 | 왼쪽 문제 2~4개(작은 pill 라벨)에서 곡선이 오른쪽 해결 하나로 모인다 | 여러 문제가 실제로 한 원인·한 해결에 닿을 때(flow 구조, report 제안) |
| (i) annotate 주석 `data-variant="annotate"` | 기존 그림(도식·차트·와이어프레임) 위 번호 표식 2~4개 + 짧은 주석 목록 | 그림의 몇 곳을 짚어 한 줄씩 덧붙일 때(page·deck 공용) |

## 장르 (`data-genre`)

변형이 **무엇을** 그리는지라면 장르는 **어떤 목소리로** 그리는지다. 거의 모든 도식이 구조형 선 도식이면 페이지가 한 화면처럼 보인다.
`figure.d0-fig[data-genre="structural|narrative|editorial"]`, 생략하면 structural이다. 구도와 묶는 법은 [composition.md](../composition.md).

| 장르 | 그리는 것 | 언제 | 어울리는 구도 |
| --- | --- | --- | --- |
| Structural (생략) | 선·면으로 대상의 모양과 연결. 위 변형 (a)~(g) | 무엇이 무엇에 닿나, 어떤 모양인가 | Canvas, Split |
| Narrative | 방향과 진행 상태. 지나온 것 / 현재 / 남은 것을 굵기·채움·점선 차이로 | 지금 어디까지 왔나, 무엇이 남았나 | Sequence |
| Editorial | 선 거의 없이 실제 숫자 하나를 크게(56px), 객체 하나는 작게, 주변 라벨 최소 | 이것 하나만 기억하면 될 때 | Hero, Evidence |

- **같은 페이지에서 장르를 섞기를 권장한다.** 섹션이 3~4개면 structural 외에 narrative나 editorial을 하나 두는 것을 먼저 검토한다. 맞는 내용이 없으면 structural만으로 둔다(강제가 아니다). 장르를 바꾸려고 섹션을 더하지 않고 기존 섹션의 그림을 바꾼다. editorial은 페이지당 최대 1개다.
- 장르가 바뀌어도 공통 규칙(선 굵기 1.5·2.5, 토큰 색, `role="img"` + `<title>`, 회색만 있는 도식 금지, 라벨 크기 게이트)은 그대로다.

### Structural — 구조

위 변형 (a)~(g)가 모두 structural이다. 대상의 실제 모양을 선과 면으로 그리고, 닿는 것·바뀌는 것 하나만 blue로 칠한다. 속성은 생략한다.

### Narrative — 진행

선 하나가 방향을 갖고 흘러가며, 그 위 위치가 상태를 말한다. 단계 그림 (e)가 "몇 번째인가"라면 narrative는 "얼마나 왔고 얼마나 남았나"다.

- **세 상태를 굵기·채움·선 모양으로 가른다.** 선 굵기는 1.5·2.5 두 가지뿐이므로 채움과 점선을 함께 바꾼다.

  | 상태 | 선 | 점 | 라벨 |
  | --- | --- | --- | --- |
  | 지나온 것 | 2.5 blue 실선(`d0-s-edge[data-on]`) | 작은 채움 원 r 9.5(`d0-s-node[data-on]`) | grey-600(`d0-s-muted`) |
  | 현재 | 선이 여기서 끝난다 | 큰 채움 원 r 17 + 바깥 고리 r 26 | blue-dark 600(`data-on`) |
  | 남은 것 | 1.5 grey-500 점선(`d0-s-edge[data-ahead]`) | 빈 원 r 9.5(`d0-s-node`) | grey-600(`d0-s-muted`) |

- 진행 방향은 왼쪽 → 오른쪽(또는 아래 → 위로 오르는 곡선)이다. 곡선 하나로 그리고, 지나온 구간과 남은 구간은 현재 점에서 나눈 `path` 두 개다.
- 지나온 구간에만 `d0-draw`를 붙여 그려지게 한다. 남은 점선은 처음부터 보인다.
- 현재는 하나다. 끝난 구간이 상태(통과·실패)를 말해야 하면 그 점에 `data-tone`을 단다.
- **현재 위치가 없는 절차**(일반 사용 순서, 아직 시작 전 계획)에 narrative를 쓰면 독자가 설 대표 시점 하나를 정해 현재로 그린다(예: 가장 많이 막히는 단계, 다음 결정 지점). 대표 시점을 정할 수 없으면 narrative 대신 steps (e)를 쓴다.
- 점은 3~6개. 라벨은 점마다 1~2단어, 현재 라벨만 blue-dark다. 날짜가 주인공이면 [timeline.md](timeline.md)를 쓴다.

```html
<figure class="d0-fig" data-genre="narrative">
  <svg viewBox="0 0 560 205" role="img" aria-labelledby="n1-t n1-d">
    <title id="n1-t">배포까지 남은 길</title>
    <desc id="n1-d">접수와 확인을 지나 지금 검토에 와 있어요. 배포와 완료가 남았어요.</desc>
    <path class="d0-s-edge" data-ahead d="M261 75 C317 75 342 62 392 62 C442 62 467 62 504 62"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M37 131 C93 131 109 100 149 100 C190 100 218 75 261 75"/>
    <circle class="d0-s-node" data-on cx="37" cy="131" r="9.5"/>
    <circle class="d0-s-node" data-on cx="149" cy="100" r="9.5"/>
    <circle class="d0-s-ring" cx="261" cy="75" r="26"/>
    <circle class="d0-s-node" data-on cx="261" cy="75" r="17"/>
    <circle class="d0-s-node" cx="392" cy="62" r="9.5"/>
    <circle class="d0-s-node" cx="504" cy="62" r="9.5"/>
    <text class="d0-s-text d0-s-muted" x="37" y="177" text-anchor="middle">접수</text>
    <text class="d0-s-text d0-s-muted" x="149" y="146" text-anchor="middle">확인</text>
    <text class="d0-s-text" data-on x="261" y="137" text-anchor="middle">지금 검토</text>
    <text class="d0-s-text d0-s-muted" x="392" y="109" text-anchor="middle">배포</text>
    <text class="d0-s-text d0-s-muted" x="504" y="109" text-anchor="middle">완료</text>
  </svg>
  <figcaption>절반을 지났어요. 검토가 끝나면 바로 배포해요.</figcaption>
</figure>
```

```css
.d0-s-edge[data-ahead] { stroke-dasharray: 4 5; } /* 남은 길: 1.5 grey-500 점선 */
```

### Editorial — 하나를 크게

선을 거의 쓰지 않는다. **실제 숫자** 하나를 크게 HTML로 쓰고, SVG는 그 뜻을 받치는 작은 객체 하나만 그린다. 문서 밀도는 그대로 두고 그 자리의 구도만 바꾼다.

- **큰 글자는 HTML이다.** SVG `<text>`는 라벨 크기 게이트(렌더 20px 이하)를 받으므로 큰 숫자를 SVG 안에 넣지 않는다(비율 막대가 라벨을 HTML로 빼는 것과 같은 이유). 확대·복사·번역도 된다.
- **큰 숫자는 색이 아니라 크기로** 말한다. 56px/600(모바일 40px) grey-900이 기본이고, 페이지의 큰 숫자 blue-dark 하나를 여기에 쓸 때만 `data-tone="blue"`다([hero.md](hero.md)).
- **객체는 하나, 최대 120px.** 원 하나의 몫, 막대 하나, 상자 하나처럼 글자 없는 도형 하나다. 선·축·범례·눈금을 두지 않는다. blue는 그 객체의 강조 부분 하나에만.
- 라벨은 figcaption 한 문장뿐이다(15px grey-700, 무엇을 잰 숫자인지). 무대를 두지 않는다.
- 숫자는 정본 위치 하나에만 둔다. 히어로·Impact와 같은 숫자면 editorial을 쓰지 않는다.
- **실제 숫자일 때만** 쓴다. 문구나 대답(`네 번에 한 번`, `네, 돼요`)을 큰 글자로 쓰지 않는다. 그런 말은 섹션 제목이나 Impact 문장으로 쓴다.
- 96px 이상 숫자는 쓰지 않는다. 더 크게 말해야 하면 Impact 숫자([shell.md](shell.md) 강조 절)이고, editorial을 Impact 안에 넣지 않는다.
- 섹션을 더해서 쓰지 않는다. 기존 섹션의 그림을 editorial로 바꿀 때만 쓴다.

```html
<figure class="d0-fig" data-genre="editorial">
  <svg viewBox="0 0 120 120" role="img" aria-labelledby="e1-t e1-d">
    <title id="e1-t">지난 주문 중 전부 검사한 몫</title>
    <desc id="e1-d">원 하나의 4분의 1이 채워져 있어요.</desc>
    <circle class="d0-s-bar" cx="60" cy="60" r="58"/>
    <path class="d0-s-accent" d="M60 60 V2 A58 58 0 0 1 118 60 Z"/>
  </svg>
  <p class="d0-ed__num"><data value="25">25</data>%</p>
  <figcaption>지난 주문 네 번 중 한 번은 전부 검사해요.</figcaption>
</figure>
```

```css
.d0-fig[data-genre="editorial"] {
  grid-template-columns: minmax(64px, 120px) minmax(0, 1fr); grid-template-areas: "obj num" "obj cap";
  align-items: end; column-gap: 24px; row-gap: 6px;
}
.d0-fig[data-genre="editorial"] > svg { grid-area: obj; align-self: center; width: 100%; max-width: 120px; }
.d0-ed__num { grid-area: num; margin: 0; color: var(--d0-grey-900); font-size: 56px; font-weight: 600; line-height: 1; letter-spacing: var(--d0-tracking-display); font-variant-numeric: tabular-nums; }
.d0-fig[data-genre="editorial"][data-tone="blue"] .d0-ed__num { color: var(--d0-blue-dark); }
.d0-fig[data-genre="editorial"] figcaption { grid-area: cap; align-self: start; color: var(--d0-grey-700); font-size: 15px; }
@media (max-width: 640px) {
  .d0-fig[data-genre="editorial"] { grid-template-columns: 72px minmax(0, 1fr); column-gap: 16px; }
  .d0-ed__num { font-size: 40px; }
}
```

- 원의 나머지는 grey-400(값이 큰 숫자로 적혀 있다), 몫은 blue. 몫 경로는 중심 → 12시 → 호 → 중심이다(25%면 3시까지).
- 375px에서도 객체와 숫자가 한 줄에 놓인다(객체 72px + 숫자 40px).
- 그림이 120px로 작고 숫자가 주인공이라 축 폭 75% 게이트에서 빠진다. 축 왼쪽에 두고 옆에 남는 폭은 채우지 않는다.

## 공용 CSS

```css
/* .d0-fig, .d0-fig__stage, figcaption은 shell.md에 있다 */
/* 그림 폭(.d0-fig svg 100%, compact 75%)은 shell.md 정본 CSS에 있다 */
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
.d0-s-edge[data-tone="red"] { stroke: var(--d0-red); }                                   /* 되돌림·실패 경로. data-back과 함께 쓰면 빨간 점선 */
.d0-s-stop { fill: none; stroke: var(--d0-red); stroke-width: 2.5; stroke-linecap: round; } /* 막힘 표시: 경로를 가로지르는 짧은 선·X, 라벨과 함께 */
/* 핵심 무대 blue-light: 회색 선·흐린 글자를 한 단계 진하게 */
.d0-fig[data-stage="blue"] :is(.d0-s-edge, .d0-s-node, .d0-s-step, .d0-s-frame):not([data-on]):not([data-tone]) { stroke: var(--d0-grey-600); }
.d0-fig[data-stage="blue"] .d0-s-muted, .d0-fig[data-stage="blue"] .d0-s-num:not([data-on]) { fill: var(--d0-grey-700); }
/* 도식 viewBox 폭은 560으로 맞춘다. 렌더 라벨 = 글자 × 렌더 폭 ÷ 560.
   데스크톱 축 720: 14 × 720 ÷ 560 = 18px(무대 안 664px: 16.6px). 기본 정의보다 뒤에 둔다.
   page(.d0-page) 안에만 건다. 덱 슬라이드 SVG(.d0-sl-* 글자, 주의 ! 표식 text.d0-s-num)는 slide-deck.md 글자 규칙을 따른다 */
@media (max-width: 560px) {
  .d0-page :is(.d0-s-text, .d0-s-num) { font-size: 20px; } /* 390: 20 × 358 ÷ 560 = 12.8px, 375: 12.3px, 560: 18.9px */
}
@media (max-width: 340px) {
  .d0-page :is(.d0-s-text, .d0-s-num) { font-size: 22px; } /* 320: 22 × 288 ÷ 560 = 11.3px */
}
```

대비(무대 grey-50 기준, tokens.css 값으로 계산): blue 3.75, blue-dark 5.18, green 3.26, red 3.36, orange 2.32(미달), grey-500 3.01, grey-400 2.06, grey-300 1.49.
blue-light 무대 위: blue 3.58, green 3.11, red 3.20, grey-600 4.49, grey-500 2.87(미달). 전체 표는 [shell.md](shell.md) 색 절.
뜻을 혼자 전하는 선·면(노드 테두리, 엣지, 화살표, 프레임, 강조)은 blue나 grey-500 이상이다. grey-400 이하 면·선은
값이 라벨 글자로 함께 적힌 막대, 이름이 카드 제목으로 적힌 격자 칸, 자리만 잡는 와이어프레임 면, 참여자 이름이 적힌 세로선에만 쓴다.
흰 숫자는 blue-dark 원 위에만 둔다(5.5:1). blue 원 위 흰 글자는 3.99:1이라 쓰지 않는다. green 원에는 숫자 대신 흰 체크선(`.d0-s-tick`, 그래픽 3.47:1)을 둔다.
**의미색 표식은 혼자 뜻을 전하지 않는다.** 완료 단계는 체크 모양, 실패 노드는 라벨, orange 면은 진한 테두리나 값 라벨을 함께 둔다.

### 흔한 표식 → 클래스 (page·deck 공용)

도형은 page와 deck 모두 이 클래스로 칠한다. SVG에 `fill`·`stroke` 값(`var(--d0-*)` 포함)을 직접 쓰지 않는다. deck에서는 이 공용 CSS의 도형 규칙을 함께 붙이고, 글자만 [slide-deck.md](slide-deck.md)의 `d0-sl-label`·`d0-sl-value`로 쓴다.

| 표식 | 클래스 |
| --- | --- |
| 화면·카드 틀 | `.d0-s-frame` |
| 속 빈 노드 / 채운 강조 노드 | `.d0-s-node` / `.d0-s-node[data-on]` |
| 작은 점(상태 점) | `.d0-s-node`를 r 4~6으로, 상태는 `data-on`·`data-tone` |
| 완료 체크(초록) | `.d0-s-node[data-tone="green"]` + 흰 체크선 `.d0-s-tick` |
| 실패·위험 노드 | `.d0-s-node[data-tone="red"]` + 라벨 |
| 되돌림 화살표(빨강) | `.d0-s-edge[data-tone="red"]`, 돌아가는 길이면 `data-back`을 더해 점선 |
| 점선 절단·끊긴 연결 | `.d0-s-edge[data-back]`(grey-500 점선) |
| 막힘 표시 | `.d0-s-stop`(red 2.5 짧은 선·X) + 라벨 |
| 남은 길(narrative) | `.d0-s-edge[data-ahead]` |
| 범위·영역 | `.d0-s-zone`(`data-tone="red"` 가능) |

새 표식이 필요하면 새 블록을 만들지 않고 이 공용 CSS에 토큰만 쓰는 클래스 하나를 더한다([blocks.md](../blocks.md) 블록 추가 판별).

## (a) graph — 연결 그래프

```html
<figure class="d0-fig">
  <svg viewBox="0 0 560 348" role="img" aria-labelledby="g1-t g1-d">
    <title id="g1-t">고친 파일과 연결된 검사</title>
    <desc id="g1-d">파일 두 개 중 고친 파일 하나에서 선이 검사 세 개로 이어져 블루로 칠해져 있어요. 다른 파일에 붙은 검사 두 개는 비어 있어요.</desc>
    <text class="d0-s-text d0-s-muted" x="451" y="25" text-anchor="middle">검사</text>
    <path class="d0-s-edge" d="M93 261 C272 261 272 249 451 249 M93 261 C272 261 272 311 451 311"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M93 124 C272 124 272 62 451 62"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M93 124 C272 124 272 124 451 124"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M93 124 C272 124 272 187 451 187"/>
    <circle class="d0-s-ring" cx="93" cy="124" r="26"/>
    <circle class="d0-s-node" data-on cx="93" cy="124" r="17"/>
    <circle class="d0-s-node" cx="93" cy="261" r="17"/>
    <circle class="d0-s-node" data-on cx="451" cy="62" r="14"/>
    <circle class="d0-s-node" data-on cx="451" cy="124" r="14"/>
    <circle class="d0-s-node" data-on cx="451" cy="187" r="14"/>
    <circle class="d0-s-node" cx="451" cy="249" r="14"/>
    <circle class="d0-s-node" cx="451" cy="311" r="14"/>
    <text class="d0-s-text" data-on x="93" y="180" text-anchor="middle">고친 파일</text>
    <text class="d0-s-text d0-s-muted" x="93" y="311" text-anchor="middle">다른 파일</text>
    <text class="d0-s-text" data-on x="476" y="132">3개</text>
  </svg>
  <figcaption>고친 파일에서 선을 따라간 검사 세 개만 다시 돌아요.</figcaption>
</figure>
```

- **무대 없이 둔다.** 글자 있는 도식이라 무대를 두면 375px 라벨이 11px 아래로 준다(라벨 절). 흩어진 노드의 경계는 열 머리 라벨(`검사`)과 열마다 같은 x로 맞춘 노드가 만든다.
- 노드는 7개까지. 열은 2~3개(원인 → 중간 → 결과). 더 많으면 묶어서 `+12` 같은 노드 하나로 줄인다.
- 시작 노드(고친 것)는 블루 채움 + 바깥 고리. 닿는 노드·선만 `data-on`. 닿지 않는 것은 흰 채움 + grey-500 테두리.
- 상태가 있으면 노드에 의미색을 단다: 고장 난 곳 `data-tone="red"`, 통과한 곳 `green`(incident 영향 그래프 등). 의미색 노드에도 라벨을 붙인다.
- 강조 엣지는 갈래마다 `path` 하나 + `d0-draw`라 세 갈래가 함께 그려진다. 회색 엣지는 그리지 않고 처음부터 보인다.
- 노드는 원 또는 둥근 상자(`rect rx="8"`, 글자 없음). 상자 안에 문장을 넣지 않는다.

## (b) bars — 전/후 막대

```html
<figure class="d0-fig" data-fit="compact">
  <svg viewBox="0 0 560 174" role="img" aria-labelledby="b1-t b1-d">
    <title id="b1-t">내보내기 대기 시간 전과 후</title>
    <desc id="b1-d">전에는 14분, 지금은 6분이에요.</desc>
    <text class="d0-s-text d0-s-muted" x="0" y="53">전</text>
    <rect class="d0-s-bar" x="50" y="25" width="404" height="40" rx="9.5"/>
    <text class="d0-s-text" x="467" y="53">14분</text>
    <text class="d0-s-text" data-on x="0" y="134">후</text>
    <rect class="d0-s-track" x="50" y="106" width="404" height="40" rx="9.5"/>
    <rect class="d0-s-bar" data-on x="50" y="106" width="173" height="40" rx="9.5"/>
    <text class="d0-s-text" data-on x="235" y="134">6분</text>
  </svg>
  <figcaption>기다리는 시간이 절반 아래로 줄었어요.</figcaption>
</figure>
```

- **배치.** 막대는 경계가 분명해 무대 없이 둔다. 막대 둘은 단순해 축 폭에서 커 보이므로 위 스니펫처럼 `data-fit="compact"`가 기본이다. 막대 쌍이 둘이면 축 폭을 채운다.
  설명은 figcaption과 그림 아래 explanation이 맡는다. 그림 옆 열에 두지 않는다.

- 막대 폭 = 값 / 최댓값 × 트랙 폭(위 예: 6 / 14 × 404 = 173). 숫자를 지어 맞추지 않는다.
- **막대 수.** 전/후 비교 쌍은 2개까지(막대 4개). 비교 쌍이 3개 이상이면 [kpi-cards.md](kpi-cards.md)의 막대 변형(카드 하나에 쌍 하나)을 쓴다.
- 값 라벨은 막대 끝 바로 뒤(+13)에 둔다. 범례를 따로 두지 않는다. 후(지금) 막대만 블루.
- 막대가 전/후가 아니라 상태(통과·실패 건수)를 말하면 `data-tone="green|red"`로 칠한다. 값 라벨은 그대로 둔다.
- **선택지 비교 형태.** 선택지(A안·B안)의 비용·시간을 견줄 때는 전/후 라벨 대신 선택지 이름을 행 라벨로 쓰고, 행마다 같은 트랙(`d0-s-track`)과 같은 축을 둔다.
  `data-on`(blue)은 추천안 하나에만 단다. 추천이 아직 없으면 지금 방식 행(기준선) 하나를 blue로 둔다. 추천도 지금 방식도 없으면 회색만 남으므로 막대 대신 side-by-side 와이어 카드를 쓴다. 전/후 의미가 없으므로 "후 막대만 blue" 규칙 대신 이 규칙을 따른다. 행 수 상한은 옵션 상한(3)이다.
- 막대가 3개 이상이면 행 간격 81을 유지하고 viewBox 높이를 `행 수 × 81 + 12`로 늘린다.

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
- 비율 막대는 놓인 자리(축 또는 `.d0-wide` 열) 폭을 꽉 채운다. 따로 폭을 줄이지 않는다.

## (c) grid — 미니 격자 (JS 생성)

결과물이 표일 때 "어떤 모양의 표인가"를 썸네일로 그린다. 같은 함수로 카드 여러 장을 만든다.

```html
<figure class="d0-fig" data-fit="compact">
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
- 무대 없이 둔다. 머리 행·키 열·합계 칸이 표의 테두리를 만든다. 글자 없는 썸네일이라 혼자 둘 때는 `data-fit="compact"`로 두고 figcaption은 아래에 둔다. 카드 안에 넣으면 카드가 받침이다.
- 글자 없는 그림이라 라벨 규칙의 예외다. 이름은 카드 제목이 말한다. 실제 결과물의 행·열 수에 맞춘다.

## (d) wireframe — 화면 골격

```html
<figure class="d0-fig">
  <svg viewBox="0 0 560 342" role="img" aria-labelledby="w1-t w1-d">
    <title id="w1-t">주문 관리 화면 골격</title>
    <desc id="w1-d">위쪽 바 오른쪽 버튼과 그 아래 필터 영역이 블루로 강조돼 있어요. 아래는 카드 두 장과 표 영역이에요.</desc>
    <rect class="d0-s-frame" x="1.5" y="1.5" width="557" height="339" rx="19"/>
    <path class="d0-s-line" d="M1.5 65 H558"/>
    <rect class="d0-s-fill" x="25" y="25" width="131" height="16" rx="8"/>
    <rect class="d0-s-accent" x="420" y="17" width="115" height="31" rx="9.5"/>
    <rect class="d0-s-zone" x="25" y="87" width="510" height="44" rx="9.5"/>
    <rect class="d0-s-fill" x="25" y="152" width="246" height="68" rx="12"/>
    <rect class="d0-s-fill" x="289" y="152" width="246" height="68" rx="12"/>
    <rect class="d0-s-fill" x="25" y="243" width="510" height="19" rx="6"/>
    <rect class="d0-s-fill" x="25" y="274" width="510" height="19" rx="6"/>
    <rect class="d0-s-fill" x="25" y="305" width="342" height="19" rx="6"/>
  </svg>
  <figcaption>새 필터는 버튼 바로 아래, 표 위에 생겨요.</figcaption>
</figure>
```

- 바깥 틀(`d0-s-frame`)이 경계를 그리므로 무대 없이 둔다.
- 회색 면은 자리만 잡는다(글자 없는 막대). 바뀌는 곳은 블루 하나(버튼은 채움, 영역은 점선 테두리 `d0-s-zone`).
- 라벨이 필요하면 SVG 밖 figcaption에 쓴다. 넣는다면 바뀌는 곳 하나에만 짧은 명사로.
- 눌러 봐야 이해되는 화면이면 와이어프레임 대신 [mockup-frame.md](mockup-frame.md)을 쓴다.
- 부분마다 이름을 붙여야 하면(해부도) SVG 안에 글자를 넣지 말고 (g) 번호 핀을 얹는다.

## (e) steps — 단계

번호 원을 한 줄로 잇고, 현재(또는 핵심) 단계 하나만 blue-dark로 채운다. 라벨은 원 아래 짧은 명사다.
글 상자를 화살표로 잇는 흐름 줄 대신 이 그림을 쓴다.

```html
<figure class="d0-fig" data-fit="compact">
  <svg viewBox="0 0 560 162" role="img" aria-labelledby="s1-t s1-d">
    <title id="s1-t">내보내기 네 단계</title>
    <desc id="s1-d">첫 단계 '누르기'는 초록 체크로 지금과 같다는 표시예요. 두 번째 '묶음 고르기'가 블루로 채워져 있어요. 이번에 새로 생기는 단계예요.</desc>
    <path class="d0-s-edge" d="M93 56 H193 M243 56 H317 M367 56 H454"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M93 56 H193"/>
    <circle class="d0-s-step" data-tone="green" cx="68" cy="56" r="25"/>
    <circle class="d0-s-step" data-on cx="218" cy="56" r="25"/>
    <circle class="d0-s-step" cx="342" cy="56" r="25"/>
    <circle class="d0-s-step" cx="479" cy="56" r="25"/>
    <path class="d0-s-tick" d="M58 56 L65 64 L79 48"/>
    <text class="d0-s-num" data-on x="218" y="56">2</text>
    <text class="d0-s-num" x="342" y="56">3</text>
    <text class="d0-s-num" x="479" y="56">4</text>
    <text class="d0-s-text d0-s-muted" x="68" y="124" text-anchor="middle">누르기</text>
    <text class="d0-s-text" data-on x="218" y="124" text-anchor="middle">묶음 고르기</text>
    <text class="d0-s-text d0-s-muted" x="342" y="124" text-anchor="middle">미리보기</text>
    <text class="d0-s-text d0-s-muted" x="479" y="124" text-anchor="middle">받기</text>
  </svg>
  <figcaption>두 번째 단계가 새로 생겨요. 나머지는 지금과 같아요.</figcaption>
</figure>
```

- 선과 원이 한 줄로 이어져 경계가 분명하므로 무대 없이 둔다.
- 단계는 3~5개. 원 r 25(compact 540px에서 렌더 지름 약 48px), 원 사이는 1.5 grey-500 선. 원 중심 간격은 라벨 폭에 맞춰 124~156. 단계가 3~4개면 `data-fit="compact"`가 기본이다.
- 강조는 단계 하나만: 원 채움 blue-dark + 흰 번호 + 라벨 blue-dark + 그 단계로 들어오는 선(`data-on`, `d0-draw`). 색과 채움이 함께 바뀐다.
- **현재 단계가 없는 흐름**(구조·절차 설명)은 강조 그룹 하나를 칠할 수 있다: '항상 거치는 단계' 묶음이면 그 원들 뒤에 `d0-s-zone` 둥근 상자 하나
  (예: `<rect class="d0-s-zone" x="174" y="19" width="212" height="75" rx="37"/>`를 원보다 먼저 그린다) + 묶음 라벨, 결과 단계 하나면 위 단계 강조를 그 단계에 쓴다. 둘 중 하나만.
- 끝난 단계는 `data-tone="green"` 원 + 흰 체크선(`.d0-s-tick`, 번호 대신). 막힌 단계는 `red` 원 + 라벨. 체크 모양이 색 없이도 완료를 말한다.
- 라벨은 1~2단어(viewBox 단위로 모바일 20px 글자 기준 한 라벨 약 110 이내). 더 길면 figcaption이나 아래 목록으로 보낸다.
- 단계마다 설명이 필요하면 그림 아래 [step-columns.md](step-columns.md)를 붙이고, 그림의 번호와 같은 번호를 쓴다.

## (f) sequence — 주고받기

참여자 3~4명이 무엇을 주고받는지 그린다. 참여자 이름은 위, 세로선은 아래로, 메시지는 가로 화살표 위 짧은 라벨이다.

```html
<figure class="d0-fig">
  <svg viewBox="0 0 560 311" role="img" aria-labelledby="q1-t q1-d">
    <title id="q1-t">내보내기 요청이 오가는 순서</title>
    <desc id="q1-d">사용자가 서버에 내보내기를 누르면 서버가 저장소에 파일을 저장해요. 이 화살표가 블루예요. 그다음 서버가 사용자에게 받기 링크를 돌려줘요.</desc>
    <text class="d0-s-text" x="93" y="28" text-anchor="middle">사용자</text>
    <text class="d0-s-text" x="280" y="28" text-anchor="middle">서버</text>
    <text class="d0-s-text" x="467" y="28" text-anchor="middle">저장소</text>
    <path class="d0-s-life" d="M93 50 V292 M280 50 V292 M467 50 V292"/>
    <path class="d0-s-edge" d="M93 112 H277 M264 103 L277 112 L264 121"/>
    <text class="d0-s-text d0-s-muted" x="187" y="96" text-anchor="middle">누르기</text>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M280 180 H464 M451 171 L464 180 L451 190"/>
    <text class="d0-s-text" data-on x="373" y="165" text-anchor="middle">파일 저장</text>
    <path class="d0-s-edge" data-back d="M280 249 H96 M109 240 L96 249 L109 258"/>
    <text class="d0-s-text d0-s-muted" x="187" y="233" text-anchor="middle">받기 링크</text>
  </svg>
  <figcaption>파일은 서버가 저장소에 둔 뒤 링크로 돌려줘요.</figcaption>
</figure>
```

- **무대 없이 둔다.** 글자 있는 도식이라 무대를 두면 375px 라벨이 11px 아래로 준다(라벨 절). 그림의 경계는 위 참여자 이름과 세로선의 아래 끝이 만든다.
- 참여자는 3~4명, 메시지는 5개까지. 참여자 간격 187(4명이면 140, viewBox 폭 560 그대로).
- 세로선은 grey-300 1.5px(이름이 위에 적혀 있어 자리만 잡는다). 메시지 화살표는 grey-500 1.5px, 돌아오는 응답은 점선(`data-back`).
- 핵심 메시지 하나만 `data-on`(blue 2.5px + `d0-draw`) + 라벨 blue-dark. 화살촉은 같은 `path`의 서브패스로 그린다(`marker` 금지, 색이 CSS를 안 따른다).
- 라벨은 화살표 위 16(viewBox 단위), 두 세로선 가운데. 한 메시지 라벨은 1~2단어다. 조건·반복은 figcaption으로 보낸다.

## (g) pins — 번호 핀 오버레이

글자 없는 넓은 SVG(와이어프레임, 파일 구성 등) 위에 HTML 번호 핀(①②③)을 얹고, 이름과 뜻은 옆 범례 `dl`에 쓴다.
SVG에 글자가 없으므로 위 라벨 크기 게이트를 받지 않는다. 그림은 축 폭을 채우고 범례는 그림 아래에 둔다. 범례를 그림 옆 열에 두려면 figure를 `.d0-wide` 바로 안에 두고 2열 분할선(6/6, `data-split="7-5"`면 7/5)을 따른다([shell.md](shell.md) 2열 (b)). compact는 쓰지 않는다(핀 위치가 SVG 상자 기준이다). 핀 숫자와 범례는 HTML 텍스트 규칙을 따른다.
**연동 동작이 기본이다.** 범례 항목·핀·SVG 영역 묶음을 같은 번호(`data-pin="n"`)로 묶고, 한 번에 한 번호만 켠다.

```html
<figure class="d0-fig" data-variant="pins" data-active-pin="2">
    <div class="d0-pins">
      <svg viewBox="0 0 560 350" role="img" aria-labelledby="p1-t p1-d">
        <title id="p1-t">설명 페이지 한 장의 구성</title>
        <desc id="p1-d">맨 위 머리, 가운데 그림 무대, 맨 아래 목록 영역이 있어요. 번호 1~3이 각 부분을 가리켜요.</desc>
        <rect class="d0-s-frame" x="1" y="1" width="558" height="348" rx="14"/>
        <g data-pin="1">
          <rect class="d0-s-area" x="16" y="16" width="527" height="63" rx="9.5"/>
          <rect class="d0-s-accent" x="28" y="28" width="210" height="16" rx="8"/>
          <rect class="d0-s-fill" x="28" y="56" width="350" height="12" rx="6"/>
        </g>
        <g data-pin="2">
          <rect class="d0-s-zone" x="28" y="93" width="504" height="149" rx="12"/>
          <rect class="d0-s-accent" x="56" y="131" width="187" height="75" rx="9.5"/>
        </g>
        <g data-pin="3">
          <rect class="d0-s-area" x="16" y="259" width="527" height="65" rx="9.5"/>
          <path class="d0-s-line" d="M28 275 H532 M28 308 H420"/>
        </g>
      </svg>
      <span class="d0-pin" data-pin="1" style="left: 45%; top: 8%" aria-hidden="true">1</span>
      <span class="d0-pin" data-pin="2" style="left: 50%; top: 27%" aria-hidden="true">2</span>
      <span class="d0-pin" data-pin="3" style="left: 80%; top: 79%" aria-hidden="true">3</span>
    </div>
  <dl class="d0-pins__key">
    <div data-pin="1" tabindex="0"><dt><span class="d0-pin">1</span>머리</dt><dd>제목과 결론 한 줄이에요.</dd></div>
    <div data-pin="2" tabindex="0"><dt><span class="d0-pin">2</span>그림 무대</dt><dd>페이지의 주인공 그림이 놓여요.</dd></div>
    <div data-pin="3" tabindex="0"><dt><span class="d0-pin">3</span>목록</dt><dd>주의할 점과 할 일이에요.</dd></div>
  </dl>
  <figcaption>그림 무대가 가장 큰 자리를 차지해요.</figcaption>
</figure>
```

```css
.d0-fig[data-variant="pins"] .d0-pins { position: relative; width: 100%; } /* SVG와 같은 크기: 핀 % 위치가 그대로 맞는다 */
.d0-fig[data-variant="pins"] .d0-fig__stage > .d0-pins { justify-self: center; } /* 무대 있음: 무대 가운데(기존 동작) */
.d0-fig[data-variant="pins"] svg { display: block; max-width: none; }
.d0-pin {
  display: inline-grid; place-items: center; flex: none; width: 24px; height: 24px; border-radius: 999px;
  background: var(--pin-bg, #fff); box-shadow: inset 0 0 0 1.5px var(--pin-ring, var(--d0-grey-600));
  color: var(--pin-fg, var(--d0-grey-600)); font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; line-height: 1;
}
.d0-pins .d0-pin { position: absolute; transform: translate(-50%, -50%); }
.d0-pins__key { display: grid; gap: 12px; margin: 0; }
.d0-pins__key > div { padding-left: 10px; border-left: 2px solid var(--key-line, transparent); }
.d0-pins__key dt { display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 600; color: var(--key-dt, var(--d0-grey-900)); }
.d0-pins__key dd { margin: 4px 0 0 32px; color: var(--d0-grey-600); font-size: 14px; }
.d0-s-area { fill: var(--area-fill, none); stroke: var(--area-line, none); stroke-width: 1.5; stroke-dasharray: 4 3; }
/* 켜진 번호: 그림의 data-active-pin과 같은 data-pin(핀 3~6개라 6까지 적는다). 값은 자식 핀·dt·영역으로 상속된다 */
:is(.d0-fig[data-active-pin="1"] [data-pin="1"], .d0-fig[data-active-pin="2"] [data-pin="2"], .d0-fig[data-active-pin="3"] [data-pin="3"],
    .d0-fig[data-active-pin="4"] [data-pin="4"], .d0-fig[data-active-pin="5"] [data-pin="5"], .d0-fig[data-active-pin="6"] [data-pin="6"]) {
  --pin-bg: var(--d0-blue-dark); --pin-ring: transparent; --pin-fg: #fff;
  --key-line: var(--d0-blue); --key-dt: var(--d0-blue-dark);
  --area-fill: var(--d0-blue-light); --area-line: var(--d0-blue);
}
/* 꺼진 영역: 묶음 안 색 토큰을 회색으로 바꿔 모든 도형이 따라간다 */
.d0-fig[data-active-pin] g[data-pin]:not(.d0-fig[data-active-pin="1"] [data-pin="1"], .d0-fig[data-active-pin="2"] [data-pin="2"], .d0-fig[data-active-pin="3"] [data-pin="3"],
    .d0-fig[data-active-pin="4"] [data-pin="4"], .d0-fig[data-active-pin="5"] [data-pin="5"], .d0-fig[data-active-pin="6"] [data-pin="6"]) {
  --d0-blue: var(--d0-grey-400); --d0-blue-dark: var(--d0-grey-500); --d0-blue-light: var(--d0-grey-100);
  --d0-green: var(--d0-grey-400); --d0-green-bg: var(--d0-grey-100); --d0-orange: var(--d0-grey-400); --d0-orange-bg: var(--d0-grey-100);
  --d0-red: var(--d0-grey-400); --d0-red-bg: var(--d0-grey-100);
}
@media (prefers-reduced-motion: no-preference) {
  .d0-pins .d0-pin, .d0-pins__key > div, .d0-pins__key dt { transition: background-color 150ms, box-shadow 150ms, color 150ms, border-color 150ms; }
}
/* 번호 범례 열(2열 (b)): .d0-wide 바로 안에서만 그림 | 범례. 분할선은 .d0-cols와 같다(12열, 열 사이 48px). annotate도 같이 쓴다 */
@media (min-width: 960px) {
  .d0-wide > .d0-fig:is([data-variant="pins"], [data-variant="annotate"]) { grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 48px; align-items: center; }
  .d0-wide > .d0-fig:is([data-variant="pins"], [data-variant="annotate"]) > * { grid-column: span 6; }
  .d0-wide > .d0-fig[data-split="7-5"]:is([data-variant="pins"], [data-variant="annotate"]) > :first-child { grid-column: span 7; }
  .d0-wide > .d0-fig[data-split="7-5"]:is([data-variant="pins"], [data-variant="annotate"]) > :is(.d0-pins__key, .d0-annot__notes) { grid-column: span 5; }
  .d0-wide > .d0-fig:is([data-variant="pins"], [data-variant="annotate"]) > figcaption { grid-column: 1 / -1; }
}
```

```js
// 핀 연동: 범례 항목 hover·focus, 핀 hover에 그림의 data-active-pin만 바꾼다. 떠나도 마지막 번호를 유지한다.
document.querySelectorAll('.d0-fig[data-variant="pins"][data-active-pin]').forEach(function (fig) {
  function pick(e) {
    var el = e.target.closest && e.target.closest('.d0-pins > .d0-pin[data-pin], .d0-pins__key > [data-pin]');
    if (el && fig.contains(el)) fig.setAttribute('data-active-pin', el.getAttribute('data-pin'));
  }
  fig.addEventListener('mouseover', pick);
  fig.addEventListener('focusin', pick);
});
```

- 와이어프레임 틀(`d0-s-frame`)이 경계라 무대 없이 둔다. `.d0-pins`는 축 폭을 채우고 범례는 그 아래에 쌓인다. `.d0-wide` 안에서는 960px 이상에서 범례가 그림 오른쪽 열로 간다. 무대를 쓰면 `div.d0-fig__stage`가 `.d0-pins`를 감싸 무대 가운데에 놓이고, 무대가 남는 폭을 채운다. 나머지는 같다.
- **번호로 묶기.** 범례 항목(`dt`/`dd`를 감싼 `div`), 화면 위 핀, SVG 영역 묶음 `<g>`에 같은 `data-pin="n"`을 단다. 영역 묶음 밖에는 틀(`d0-s-frame`)만 둔다.
- **켜기.** 그림 `figure`의 `data-active-pin` 하나가 상태다. CSS가 같은 번호에 `--pin-*`·`--key-*`·`--area-*` 값을 넣어 켜고, JS는 이 속성만 바꾼다. 처음 값은 1번 또는 대표 항목이고, 이 값이 JS 없을 때의 정적 강조다. 범례 항목·핀에 `data-on`을 쓰지 않는다(SVG 안 `data-on`은 묶음 속 강조 도형 표시로 그대로 쓴다).
- **켜진 번호.** 핀은 blue-dark 원 + 흰 숫자(5.5:1), 범례 항목은 왼쪽 2px blue 선 + `dt` blue-dark, 영역은 원래 blue·blue-light 도형 그대로다. 묶음에 blue 도형이 없으면(체크 도장, 목록 줄) `d0-s-area` 사각형을 묶음 맨 앞에 깐다. 꺼지면 보이지 않고, 켜지면 blue-light 판 + blue 점선이 된다. 의미색 도형(green 체크 등)은 켜지면 제 색이다.
- **꺼진 번호.** 핀은 흰 원 + grey-600 테두리·숫자(5.0:1), 영역은 묶음 안 색 토큰을 회색으로 바꿔 grey-400·grey-100이 된다. 페이지 고유 클래스도 `--d0-*` 토큰을 쓰면 따라서 꺼진다. 그래서 SVG 도형 색은 꼭 토큰으로 쓴다.
- **입력.** 범례 항목은 `tabindex="0"`(또는 `button`)으로 Tab 순서에 넣고, hover·focus에 켠다. 핀은 hover에만 켠다. 화살표 키 이동은 두지 않는다. 마우스를 떼도 마지막 번호를 유지한다. 전환은 150ms 색 바뀜뿐이고, 줄이기 설정에서는 없다.
- **접근성.** SVG `<title>`·`<desc>`는 상태와 무관하게 고정이고, 색 대신 위치로 쓴다(`desc`에 "블루로 강조된" 같은 상태 색을 쓰지 않는다). 뜻은 범례 텍스트가 전한다. 화면 위 핀은 `aria-hidden`이다.
- 핀 위치 = SVG 좌표 ÷ viewBox 크기 × 100%(위 예: 무대 윗변 가운데 (280, 93) → 280 ÷ 560 = 50%, 93 ÷ 350 = 27%). 래퍼 `.d0-pins`가 SVG와 같은 크기라 비율이 그대로 맞는다. 핀은 24px 원 + 13px 숫자다. blue 원 위 흰 숫자는 3.99:1이라 쓰지 않는다.
- 핀은 3~6개다. 375px에서도 핀은 24px 그대로다. 핀끼리 겹치면(중심 간격 28px 미만) 핀을 줄이거나 부분을 묶는다. 범례는 `.d0-wide` 밖이거나 960px 아래면 그림 아래에 있다.
- 핀 옆에 글자를 붙이지 않는다. 이름은 범례에만 쓴다. 범례 `dd`는 한 문장이다.

## (h) converge — 모으기

여러 문제(원인)가 하나의 해결(또는 한 원인)로 모이는 관계를 곡선으로 잇는다. **문제들이 실제로 그 하나에 닿을 때만** 쓴다. 관계가 없는데 "정리돼 보이게" 모으지 않는다.

```html
<figure class="d0-fig" data-genre="structural">
  <svg viewBox="0 0 560 311" role="img" aria-labelledby="cv1-t cv1-d">
    <title id="cv1-t">세 가지 늦음이 대기열 하나로 모인다</title>
    <desc id="cv1-d">왼쪽 재시도 폭주, 중복 발송, 늦은 도착 세 가지에서 곡선이 오른쪽 대기열 노드 하나로 모여요.</desc>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M174 50 C311 50 342 156 439 156"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M174 156 H439"/>
    <path class="d0-s-edge d0-draw" data-on pathLength="1" d="M174 261 C311 261 342 156 439 156"/>
    <rect class="d0-s-frame" x="12" y="25" width="162" height="50" rx="25"/>
    <rect class="d0-s-frame" x="12" y="131" width="162" height="50" rx="25"/>
    <rect class="d0-s-frame" x="12" y="236" width="162" height="50" rx="25"/>
    <text class="d0-s-text" x="93" y="58" text-anchor="middle">재시도 폭주</text>
    <text class="d0-s-text" x="93" y="163" text-anchor="middle">중복 발송</text>
    <text class="d0-s-text" x="93" y="269" text-anchor="middle">늦은 도착</text>
    <circle class="d0-s-ring" cx="467" cy="156" r="28"/>
    <circle class="d0-s-node" data-on cx="467" cy="156" r="19"/>
    <text class="d0-s-text" data-on x="467" y="224" text-anchor="middle">대기열</text>
  </svg>
  <figcaption>세 가지 늦음은 모두 같은 대기열을 지나요.</figcaption>
</figure>
```

- 왼쪽은 문제 2~4개, 오른쪽은 하나다(노드 7개 상한 안). 문제는 둥근 상자(`rect` + `rx` = 높이 ÷ 2, `.d0-s-frame`) 안에 1~3단어 이름 또는 `문제 1` 같은 번호만 쓴다. 문장을 넣으면 텍스트 상자 도식이다.
- 강조 묶음은 하나다: 해결 노드(채움 + 바깥 고리)와 그리로 모이는 곡선이 같은 뜻이라 함께 blue다. 문제 상자는 흰 채움 + grey-500 테두리로 둔다.
  문제 하나만 해결에 닿고 나머지는 남으면 닿는 곡선만 `data-on`, 남는 곡선은 `data-back` 점선으로 그린다.
- 곡선은 갈래마다 `path` 하나(그리기 모션이 함께 시작). 해결 쪽 끝점을 노드 테두리(중심 − r − 고리 여백)에 맞춘다.
- 오른쪽이 해결이면 라벨은 해결 이름, 원인이면 원인 이름이다. 해결과 원인을 한 그림에 같이 모으지 않는다.
- **deck.** 가로형 viewBox 800을 쓰고 글자는 `d0-sl-label`·`d0-sl-value`(`--sl-font`)로 바꾼다. 문제 상자 200×56(rx 28), 해결 노드 r 30 + 고리 r 44가 기준이다.
  비대칭 장(`data-layout="asym"`)의 그림 열에 두면 viewBox 480×400처럼 세로로 늘려 다시 그린다.

```html
<svg viewBox="0 0 800 320" role="img" aria-labelledby="cv2-t"><title id="cv2-t">세 가지 늦음이 대기열 하나로 모인다</title>
  <path class="d0-s-edge" data-on d="M240 60 C420 60 460 160 594 160"/>
  <path class="d0-s-edge" data-on d="M240 160 H594"/>
  <path class="d0-s-edge" data-on d="M240 260 C420 260 460 160 594 160"/>
  <rect class="d0-s-frame" x="40" y="32" width="200" height="56" rx="28"/>
  <rect class="d0-s-frame" x="40" y="132" width="200" height="56" rx="28"/>
  <rect class="d0-s-frame" x="40" y="232" width="200" height="56" rx="28"/>
  <g class="d0-sl-label" aria-hidden="true"><text x="140" y="67">재시도 폭주</text><text x="140" y="167">중복 발송</text><text x="140" y="267">늦은 도착</text></g>
  <circle class="d0-s-ring" cx="640" cy="160" r="44"/>
  <circle class="d0-s-node" data-on cx="640" cy="160" r="30"/>
  <g class="d0-sl-value" aria-hidden="true"><text x="640" y="244" data-on>대기열</text></g>
</svg>
```

## (i) annotate — 번호 주석

이미 있는 그림(도식·차트·와이어프레임) 위에 번호 표식 2~4개를 얹고, 번호를 맞춘 짧은 주석을 그림 옆이나 아래 목록으로 붙인다. 새 그림 종류가 아니라 그림 블록의 변형이다.

- **pins와 다른 점.** pins (g)는 글자 없는 넓은 SVG의 부분 이름을 범례로 풀고, 한 번에 한 번호를 켜는 연동이 기본이다. annotate는 글자가 있는 그림에도 얹고, 번호가 모두 같은 무게로 늘 켜져 있으며 JS가 없다.
  screenshot의 `.d0-shot__note`는 화면 캡처 전용(spotlight·흐림 포함)이고, annotate는 도식·차트용이다.
- **주석.** `ol.d0-annot__notes`의 `li` 하나가 한 줄(1문장, 약 30자 이내)이다. 이유·조건처럼 긴 설명은 explanation으로 보낸다. 설명문을 전부 작은 주석으로 쪼개지 않는다.
- 주석은 카드·상자 없이 번호 + 글자 행이다. 번호는 blue-dark 원 + 흰 숫자(5.5:1), 24px이다. 그림 안 번호는 `aria-hidden`이고 뜻은 목록 글자가 전한다(`ol` 순서가 번호다).
- 번호 위치 = SVG 좌표 ÷ viewBox 크기 × 100%(pins와 같다). 번호가 그림의 강조 도형을 가리지 않게 도형 모서리 바깥에 둔다. 번호끼리 중심 간격 28px 이상.
- page는 주석 목록을 그림 아래에 둔다. 그림 옆 열에 두려면 figure를 `.d0-wide` 바로 안에 두고 2열 분할선을 따른다(960px 이상, (g) pins CSS). compact는 쓰지 않는다. deck은 근거 split의 요점 열 자리에 주석 목록을 두고 2~3개까지다([slide-deck](slide-deck.md) 근거 변형과 주석).
- `.d0-pin` 기본 CSS는 (g) pins 절에 있다. annotate를 쓰면 그 `.d0-pin` 규칙과 아래 CSS를 함께 붙인다.

```html
<figure class="d0-fig" data-variant="annotate">
  <div class="d0-annot">
    <svg viewBox="0 0 560 311" role="img" aria-labelledby="an1-t">
      <title id="an1-t">주별 재시도 막대. 1주 120건, 2주 135건, 3주 180건, 4주 260건.</title>
      <line class="d0-s-line" x1="31" y1="261" x2="529" y2="261"/>
      <rect class="d0-s-bar" x="62" y="176" width="75" height="86" rx="6"/>
      <rect class="d0-s-bar" x="187" y="165" width="75" height="96" rx="6"/>
      <rect class="d0-s-bar" x="311" y="134" width="75" height="128" rx="6"/>
      <rect class="d0-s-bar" data-on x="436" y="78" width="75" height="184" rx="6"/>
      <text class="d0-s-text" x="100" y="296" text-anchor="middle">1주</text><text class="d0-s-text" x="224" y="296" text-anchor="middle">2주</text>
      <text class="d0-s-text" x="348" y="296" text-anchor="middle">3주</text><text class="d0-s-text" data-on x="473" y="296" text-anchor="middle">4주</text>
    </svg>
    <span class="d0-pin" style="left: 30%; top: 46%" aria-hidden="true">1</span>
    <span class="d0-pin" style="left: 70%; top: 18%" aria-hidden="true">2</span>
  </div>
  <ol class="d0-annot__notes">
    <li><span class="d0-pin" aria-hidden="true">1</span>앞 세 주는 조금씩 늘었어요.</li>
    <li><span class="d0-pin" aria-hidden="true">2</span>마지막 주에 한 번에 크게 늘었어요.</li>
  </ol>
  <figcaption>늘어난 몫은 대부분 마지막 주에 몰렸어요.</figcaption>
</figure>
```

```css
.d0-annot, .d0-annot__notes { --pin-bg: var(--d0-blue-dark); --pin-ring: transparent; --pin-fg: #fff; } /* 번호는 모두 켜진 모양(흰 숫자 5.5:1) */
.d0-annot { position: relative; width: 100%; }
.d0-annot svg { display: block; max-width: none; }
.d0-annot > .d0-pin { position: absolute; transform: translate(-50%, -50%); }
.d0-annot__notes { margin: 0; padding: 0; list-style: none; display: grid; gap: 10px; align-content: center; }
.d0-annot__notes li { display: grid; grid-template-columns: 24px minmax(0, 1fr); column-gap: 10px; align-items: start; color: var(--d0-grey-800); font-size: 15px; line-height: var(--d0-leading-body); }
/* .d0-wide 안 2열은 (g) pins CSS의 번호 범례 열 규칙을 함께 쓴다 */
```

## 금지

- 관계가 없는 것들을 converge로 모으기, converge 상자 안 문장, 주석 5개 이상·주석마다 두 문장 이상인 annotate, 설명문 전체를 작은 주석으로 쪼개기.
- 텍스트 상자 + 화살표 줄(문장이 든 상자), 정보 없는 장식 그림, 3D·그라디언트·그림자·아이콘 일러스트, Mermaid 등 자동 배치 도식.
- 경계가 이미 보이는 도식에 기본값으로 두른 무대, 글자 있는 도식에 무대(375px 라벨 11px 미만), 무대 안에 figcaption, 무대에 테두리·그림자, 놓인 자리 폭의 75% 아래로 줄인 도식, 빈 옆자리를 채우려고 그림 옆에 붙인 설명 문단·목록.
- narrative·editorial로 말할 내용(진행 위치, 기억할 숫자 하나)이 있는데도 페이지 전체를 structural로만 채우기, editorial 2개 이상, 문구·대답을 쓴 editorial, 56px을 넘는 editorial 숫자, 장르를 바꾸려고 섹션 더하기, SVG `<text>`로 그린 큰 숫자, 선·축·범례를 단 editorial, 현재가 둘인 narrative, 1.5·2.5 외 굵기로 상태 나누기.
- 1.5·2.5 외 선 굵기(썸네일 격자 머리 테두리 제외), 각진 선 끝, 강조 경로 아닌 선에 그리기 모션.
- 회색만으로 된 도식(blue·의미색 표식 0개), 의미색 `<text>` 글자, 테두리·라벨 없이 혼자 뜻을 전하는 orange 표식.
- 노드 7개 초과, SVG 안 문장, 320·375px에서 11px 아래로 줄어들거나 1280px에서 13px 아래·20px 위인 라벨, viewBox 폭 560이 아닌 글자 있는 SVG를 다시 계산 없이 쓰기, 블루 강조가 흩어진 그림(강조 묶음은 하나).
- `preserveAspectRatio="none"`으로 늘어나는 SVG 안 `<text>`(비율 막대 라벨은 HTML로).
- `<title>` 없는 정보 SVG, SVG 안 hex·rgb 색값, `width`·`height` 고정 속성으로 반응형을 깨는 SVG.
