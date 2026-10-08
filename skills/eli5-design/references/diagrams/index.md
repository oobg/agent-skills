# diagrams — SVG 도식 공통

손으로 그리는 인라인 SVG의 공통 규칙이다. 무엇을 그릴지 고른 뒤 아래 표에서 상세 파일 하나만 연다.

| 그리는 것 | 파일 |
| --- | --- |
| 연결 그래프, 단계, 주고받기, 진행선, 여러 원인이 하나로 모이기 | [flow.md](flow.md) |
| 같은 틀의 나란한 비교, 전/후·선택지 막대, 비율 막대, 숫자 하나 크게, 없음 자리 | [comparison.md](comparison.md) |
| 화면 골격, 표 썸네일, 번호 핀, 번호 주석, 파일 트리, 그림 곁 노트 | [annotation.md](annotation.md) |

## 공통

- `figure.d0-fig` 안에 SVG 하나, 필요하면 아래 `figcaption` 한 줄이다. SVG는 `role="img"` + `<title>` + `<desc>`(무엇이 강조됐는지 위치로 한두 문장). 장식 SVG만 `aria-hidden="true"`.
- `viewBox`만 두고 `width`·`height` 속성은 쓰지 않는다. 그림은 놓인 자리 폭을 채우고, 축 폭에서 너무 커 보이는 단순 도식(점·단계 3~4개, 막대 두 개)만 `data-fit="compact"`를 단다.
- **글자 있는 SVG의 viewBox 폭.** 기본 축 560, `.d0-wide` 안 750, 2열 칸 360(넓은 구간 2열 칸 480). 이 폭으로 그리면 CSS가 좁은 화면에서 글자를 키워 읽히게 한다. 다른 폭이 꼭 필요하면 렌더에서 글자가 읽히는지 본다. deck은 [recipes/deck.md](../recipes/deck.md)의 400·800을 따른다.
- SVG `<text>`에는 노드·값 이름(`고친 파일`, `6분`)과 그 곁 한 줄 구절(역할·조건·결과, `요청이 설명과 맞을 때`, `코드는 빼고 출력만`)까지 둔다. 여러 줄 설명은 SVG 밖 figcaption·HTML에 둔다. 설명 문장이 든 상자를 화살표로 이은 것은 도식이 아니다.
- 색은 SVG에 직접 쓰지 않고 아래 클래스로 칠한다. 파랑은 메인·초점이고, 사물·범주는 보조 색(`data-hue`)으로 나눠 칠해도 된다. 보조 색을 상태(의미색)에 쓰거나 의미색과 섞지 않는다. 강조는 색만으로 말하지 않고 채움/빈 모양·굵기·라벨 중 하나를 함께 바꾼다.
- 선 굵기는 기본 1.5, 강조 2.5 두 가지다. 화살촉은 같은 `path`의 서브패스로 그린다(`marker` 금지). 자동 배치 도구(Mermaid 등)는 쓰지 않는다.
- **좁은 화면.** 다시 배치할 수 있으면 세로형 SVG를 `data-view="narrow"`로 함께 두고, 좌표·관계를 지켜야 하면 `.d0-fig__scroll` 안 가로 스크롤로 둔다. 예시는 [flow.md](flow.md) 갈래가 있는 흐름.
- 비유 사물은 원 노드·선·빈 틀·회색 막대로 조립하지 않고 면과 부분으로 그린 삽화로 둔다: 채운 면, 부분 2~4개, 보조 색, 작은 디테일 하나(아래 예시). 노드·선은 흐름·관계에만 쓴다.
- 노드는 7개 안팎까지다. 많으면 묶어서 `+12` 같은 노드 하나로 줄인다.
- 경계는 그림 안 선·면으로 만든다. 영역이 둘 이상이면(내 쪽 \| 바깥) 같은 문법의 틀로 나란히 두어 한 상자만 틀 밖에 떠 있지 않게 한다. SVG만 든 `figure.d0-fig`(compact 제외)는 CSS가 외곽선 카드(1px 테두리, 면·그림자 없음)에 담는다. 그림 안에 이미 바깥 틀을 그렸으면(나란한 칸, 화면 틀) `data-frame="none"`을 단다. 회색 무대(`data-stage`)는 글자 없는 그림이 떠 보일 때만 쓴다.

## 클래스 (page·deck 공용)

| 표식 | 클래스 |
| --- | --- |
| 글자 / 흐린 글자 / 강조 글자 | `.d0-s-text` / `.d0-s-text.d0-s-muted` / `.d0-s-text[data-on]` (deck은 `g.d0-sl-label`·`g.d0-sl-value` 안 `text`) |
| 선 / 강조 선 / 되돌아가는 점선 / 남은 길 점선 | `.d0-s-edge` / `[data-on]` / `[data-back]` / `[data-ahead]` |
| 빈 노드 / 채운 강조 노드 / 바깥 고리 | `.d0-s-node` / `.d0-s-node[data-on]` / `.d0-s-ring` |
| 번호 원 / 번호 글자 | `.d0-s-step`(`[data-on]`) / `.d0-s-num`(`[data-on]`) |
| 완료 체크 | `.d0-s-node[data-tone="green"]` 또는 `.d0-s-step[data-tone="green"]` + 흰 체크선 `.d0-s-tick` |
| 실패·위험 / 주의 | `[data-tone="red"]` + 라벨 / `[data-tone="orange"]` + 라벨(옅은 면 + 진한 테두리) |
| 막힘 표시 | `.d0-s-stop` + 라벨 |
| 막대 / 강조 막대 / 트랙 | `.d0-s-bar` / `.d0-s-bar[data-on]` / `.d0-s-track` |
| 목표선·기준선 | `.d0-s-target` + 값 라벨 |
| 화면·카드 틀 / 자리 채움 / 바뀌는 영역 / 강조 면 | `.d0-s-frame` / `.d0-s-fill` / `.d0-s-zone` / `.d0-s-accent` |
| 참여자 세로선 / 기준선·구분선 | `.d0-s-life` / `.d0-s-line` |
| 삽화 면 / 삽화 속 진한 디테일 / 보조 색 글자 | `.d0-s-obj` / `.d0-s-ink` / `.d0-s-text[data-hue]`. 색은 자기나 조상 `g`의 `data-hue="sky|mint|lavender|pink|butter|blue"`, 없으면 회색 |

새 표식이 꼭 필요하면 `assets/page.css` 도식 공용 클래스에 Day0·보조 색 토큰만 쓰는 클래스 하나를 더한다.

비유 삽화 예시(쿠키 틀 하나에서 같은 쿠키 셋이 나오고 틀은 남음):

```html
<svg viewBox="0 0 560 230" role="img" aria-labelledby="ck-t ck-d">
  <title id="ck-t">쿠키 틀 하나와 같은 쿠키 셋</title>
  <desc id="ck-d">왼쪽 별 모양 틀 하나로 오른쪽 쟁반에 같은 별 쿠키 셋을 찍어 냈고, 틀은 그대로 남아 있다.</desc>
  <g data-hue="sky">
    <rect class="d0-s-obj" x="96" y="22" width="28" height="30" rx="8"/>
    <path class="d0-s-obj" stroke-width="2.5" transform="translate(110 104)" d="M0 -46 L13.5 -18.6 L43.7 -14.2 L21.9 7.1 L27 37.2 L0 23 L-27 37.2 L-21.9 7.1 L-43.7 -14.2 L-13.5 -18.6Z"/>
  </g>
  <text class="d0-s-text" x="110" y="176" text-anchor="middle">틀 하나</text>
  <text class="d0-s-text d0-s-muted" x="110" y="198" text-anchor="middle">찍고 나도 그대로</text>
  <path class="d0-s-edge" d="M184 104 H244 M236 98 l8 6 -8 6"/>
  <text class="d0-s-text d0-s-muted" x="214" y="90" text-anchor="middle">찍어 냄</text>
  <rect class="d0-s-obj" x="262" y="52" width="282" height="108" rx="18"/>
  <g data-hue="butter">
    <g transform="translate(318 106)"><path class="d0-s-obj" d="M0 -30 L8.8 -12.1 L28.5 -9.3 L14.3 4.6 L17.6 24.3 L0 15 L-17.6 24.3 L-14.3 4.6 L-28.5 -9.3 L-8.8 -12.1Z"/><circle class="d0-s-ink" cx="-5" cy="0" r="3"/><circle class="d0-s-ink" cx="6" cy="6" r="3"/></g>
    <g transform="translate(403 106)"><path class="d0-s-obj" d="M0 -30 L8.8 -12.1 L28.5 -9.3 L14.3 4.6 L17.6 24.3 L0 15 L-17.6 24.3 L-14.3 4.6 L-28.5 -9.3 L-8.8 -12.1Z"/><circle class="d0-s-ink" cx="-5" cy="0" r="3"/><circle class="d0-s-ink" cx="6" cy="6" r="3"/></g>
    <g transform="translate(488 106)"><path class="d0-s-obj" d="M0 -30 L8.8 -12.1 L28.5 -9.3 L14.3 4.6 L17.6 24.3 L0 15 L-17.6 24.3 L-14.3 4.6 L-28.5 -9.3 L-8.8 -12.1Z"/><circle class="d0-s-ink" cx="-5" cy="0" r="3"/><circle class="d0-s-ink" cx="6" cy="6" r="3"/></g>
  </g>
  <text class="d0-s-text" data-hue="butter" x="403" y="186" text-anchor="middle">같은 모양 쿠키 셋</text>
  <text class="d0-s-text d0-s-muted" x="403" y="208" text-anchor="middle">쟁반</text>
</svg>
```

## 렌더

라벨이 선·점 위에 얹히거나 좁은 화면에서 몰리는지는 렌더를 봐야 안다. 다 그린 뒤 [final-review.md](../final-review.md)대로 넓은 화면과 좁은 화면에서 본다.
