# diagrams — SVG 도식 공통

손으로 그리는 인라인 SVG의 공통 규칙이다. 무엇을 그릴지 고른 뒤 아래 표에서 상세 파일 하나만 연다.

| 그리는 것 | 파일 |
| --- | --- |
| 연결 그래프, 단계, 주고받기, 진행선, 여러 원인이 하나로 모이기 | [flow.md](flow.md) |
| 같은 틀의 나란한 비교, 전/후·선택지 막대, 비율 막대, 숫자 하나 크게, 없음 자리 | [comparison.md](comparison.md) |
| 화면 골격, 표 썸네일, 번호 핀, 번호 주석, 그림 곁 노트 | [annotation.md](annotation.md) |

## 공통

- `figure.d0-fig` 안에 SVG 하나, 필요하면 아래 `figcaption` 한 줄이다. SVG는 `role="img"` + `<title>` + `<desc>`(무엇이 강조됐는지 위치로 한두 문장). 장식 SVG만 `aria-hidden="true"`.
- `viewBox`만 두고 `width`·`height` 속성은 쓰지 않는다. 그림은 놓인 자리 폭을 채우고, 축 폭에서 너무 커 보이는 단순 도식(점·단계 3~4개, 막대 두 개)만 `data-fit="compact"`를 단다.
- **글자 있는 SVG의 viewBox 폭.** 기본 축 560, `.d0-wide` 안 750, 2열 칸 360(넓은 구간 2열 칸 480). 이 폭으로 그리면 CSS가 좁은 화면에서 글자를 키워 읽히게 한다. 다른 폭이 꼭 필요하면 렌더에서 글자가 읽히는지 본다. deck은 [recipes/deck.md](../recipes/deck.md)의 400·800을 따른다.
- SVG `<text>`는 짧은 노드·값 라벨(명사 1~3단어, `고친 파일`, `6분`)에만 쓴다. 설명 문장은 SVG 밖 figcaption·HTML에 둔다. 문장이 든 상자를 화살표로 이은 것은 도식이 아니다.
- 색은 SVG에 직접 쓰지 않고 아래 클래스로 칠한다. 강조는 색만으로 말하지 않고 채움/빈 모양·굵기·라벨 중 하나를 함께 바꾼다. 회색만 남은 도식이 되지 않게 초점 하나는 blue나 의미색으로 둔다.
- 선 굵기는 기본 1.5, 강조 2.5 두 가지다. 화살촉은 같은 `path`의 서브패스로 그린다(`marker` 금지). 자동 배치 도구(Mermaid 등)는 쓰지 않는다.
- **좁은 화면.** 다시 배치할 수 있으면 세로형 SVG를 `data-view="narrow"`로 함께 두고, 좌표·관계를 지켜야 하면 `.d0-fig__scroll` 안 가로 스크롤로 둔다. 예시는 [flow.md](flow.md) 갈래가 있는 흐름.
- 노드는 7개 안팎까지다. 많으면 묶어서 `+12` 같은 노드 하나로 줄인다.
- 글자 있는 도식에는 회색 무대(`data-stage`)를 두지 않는다. 경계는 그림 안 선·면으로 만든다. 무대는 글자 없는 그림이 떠 보일 때만 쓴다.

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

새 표식이 꼭 필요하면 `assets/page.css` 도식 공용 클래스에 토큰만 쓰는 클래스 하나를 더한다.

## 렌더

라벨이 선·점 위에 얹히거나 좁은 화면에서 몰리는지는 렌더를 봐야 안다. 다 그린 뒤 [final-review.md](../final-review.md)대로 넓은 화면과 좁은 화면에서 본다.
