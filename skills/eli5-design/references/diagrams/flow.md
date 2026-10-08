# diagrams/flow — 흐름·연결 도식

무엇이 무엇에 닿는지, 어떤 순서로 가는지, 누가 누구에게 넘기는지를 그린다. 공통 규칙과 클래스는 [index.md](index.md)에 있다.

| 변형 | 그리는 것 | 언제 |
| --- | --- | --- |
| 갈래가 있는 흐름 | 역할 열 × 갈래 줄, 건너뜀·되돌림·종료 | 조건에 따라 거치는 사람이 달라질 때(아래 정본 예시) |
| 연결 그래프 | 노드(대상의 생김새, 없으면 원) + 곡선, 닿는 것만 blue | 의존·영향 범위·원인 → 결과 |
| 단계 | 번호 원을 선으로 잇고 라벨은 아래 | 몇 단계 중 어디인가, 핵심 단계 하나 |
| 주고받기 | 참여자 세로선 3~4개 + 가로 화살표와 짧은 라벨, 응답 점선이 요청한 쪽까지 돌아와 완료 표시로 끝남 | 누가 누구에게 무엇을 넘기고 무엇을 돌려받나 |
| 진행선 | 지나온 실선 / 현재 큰 점 / 남은 점선 | 얼마나 왔고 얼마나 남았나 |
| 모으기 | 왼쪽 문제 2~4개의 곡선이 오른쪽 하나로 | 여러 문제가 실제로 한 원인·해결에 닿을 때만 |

## 갈래가 있는 흐름 (정본 예시)

조건에 따라 거치는 사람이 달라지고, 되돌아가거나 중간에 끝나는 경로가 있는 흐름이다. 아래 예시가 보여 주는 표현 기법을 그대로 쓴다.

- **실제 역할 이름.** 열 머리에 원문의 역할·대상 이름(`사서`, `운영위원`)을 그대로 쓴다. `앞 단계`, `지금 단계` 같은 위치어로 바꾸지 않는다.
- **갈래 라벨 + 비율.** 갈래마다 조건과 비율을 그 줄 바로 위에 적는다(`국내 도서 · 82%`). 비율을 글로만 두지 않는다.
- **건너뜀.** 거치지 않는 칸은 같은 자리에 점선 원 + `건너뜀` 라벨로 남긴다. 빈 원만 두지 않는다.
- **되돌림과 종료.** 되돌아가는 길은 점선 화살표 + 조건 라벨(`정보 부족이면 사서에게`), 중간에 끝나는 길은 막힘 표시 + 라벨(`이미 소장이면 종료`)이다.
- **좁은 화면.** 같은 내용을 세로형으로 다시 그려 `data-view="narrow"`로 함께 둔다. CSS가 좁은 화면에서 가로형(`data-view="wide"`) 대신 보여 준다. 그림을 문단으로 다시 쓰지 않는다.

```html
<figure class="d0-fig">
  <svg data-view="wide" viewBox="0 0 560 292" role="img" aria-labelledby="lb-t lb-d">
    <title id="lb-t">희망 도서가 구매되기까지 거치는 사람</title>
    <desc id="lb-d">국내 도서는 사서 다음 운영위원을 건너뛰고 구매 담당으로 가요. 해외·희귀 자료만 운영위원을 거치고, 정보가 부족하면 사서에게 되돌아가요. 이미 소장한 책이면 사서 단계에서 끝나요.</desc>
    <text class="d0-s-text d0-s-muted" x="70" y="28" text-anchor="middle">신청자</text>
    <text class="d0-s-text d0-s-muted" x="200" y="28" text-anchor="middle">사서</text>
    <text class="d0-s-text d0-s-muted" x="330" y="28" text-anchor="middle">운영위원</text>
    <text class="d0-s-text d0-s-muted" x="470" y="28" text-anchor="middle">구매 담당</text>
    <text class="d0-s-text" x="0" y="96">국내 도서 · 82%</text>
    <path class="d0-s-edge" d="M86 120 H184 M216 120 H314 M346 120 H454"/>
    <circle class="d0-s-node" cx="70" cy="120" r="16"/><circle class="d0-s-node" cx="200" cy="120" r="16"/>
    <circle class="d0-s-edge" data-back cx="330" cy="120" r="16"/>
    <text class="d0-s-text d0-s-muted" x="330" y="156" text-anchor="middle">건너뜀</text>
    <circle class="d0-s-node" data-tone="green" cx="470" cy="120" r="16"/>
    <path class="d0-s-edge" d="M211 108 L240 80"/><path class="d0-s-stop" d="M240 68 L252 80 M252 68 L240 80"/>
    <text class="d0-s-text d0-s-muted" x="262" y="79">이미 소장이면 종료</text>
    <text class="d0-s-text" data-on x="0" y="188">해외·희귀 자료 · 18%</text>
    <path class="d0-s-edge" d="M86 212 H184 M346 212 H454"/>
    <path class="d0-s-edge" data-on d="M216 212 H314"/>
    <circle class="d0-s-node" cx="70" cy="212" r="16"/><circle class="d0-s-node" cx="200" cy="212" r="16"/>
    <circle class="d0-s-node" data-on cx="330" cy="212" r="16"/><circle class="d0-s-node" data-tone="green" cx="470" cy="212" r="16"/>
    <path class="d0-s-edge" data-back d="M322 227 C300 266 226 266 206 232 M200 242 L205 230 L216 236"/>
    <text class="d0-s-text d0-s-muted" x="265" y="284" text-anchor="middle">정보 부족이면 사서에게</text>
  </svg>
  <svg data-view="narrow" viewBox="0 0 560 492" role="img" aria-labelledby="lbn-t">
    <title id="lbn-t">희망 도서가 구매되기까지 거치는 사람(세로)</title>
    <text class="d0-s-text" x="200" y="34" text-anchor="middle">국내 82%</text>
    <text class="d0-s-text" data-on x="360" y="34" text-anchor="middle">해외·희귀 18%</text>
    <text class="d0-s-text d0-s-muted" x="0" y="107">신청자</text>
    <text class="d0-s-text d0-s-muted" x="0" y="227">사서</text>
    <text class="d0-s-text d0-s-muted" x="0" y="347">운영위원</text>
    <text class="d0-s-text d0-s-muted" x="0" y="467">구매 담당</text>
    <path class="d0-s-edge" d="M200 116 V204 M200 236 V324 M200 356 V444 M360 116 V204 M360 356 V444"/>
    <path class="d0-s-edge" data-on d="M360 236 V324"/>
    <circle class="d0-s-node" cx="200" cy="100" r="16"/><circle class="d0-s-node" cx="200" cy="220" r="16"/>
    <circle class="d0-s-edge" data-back cx="200" cy="340" r="16"/>
    <text class="d0-s-text d0-s-muted" x="176" y="347" text-anchor="end">건너뜀</text>
    <circle class="d0-s-node" data-tone="green" cx="200" cy="460" r="16"/>
    <path class="d0-s-edge" d="M188 230 L168 248"/><path class="d0-s-stop" d="M154 246 L166 258 M166 246 L154 258"/>
    <text class="d0-s-text d0-s-muted" x="0" y="282">소장이면 종료</text>
    <circle class="d0-s-node" cx="360" cy="100" r="16"/><circle class="d0-s-node" cx="360" cy="220" r="16"/>
    <circle class="d0-s-node" data-on cx="360" cy="340" r="16"/><circle class="d0-s-node" data-tone="green" cx="360" cy="460" r="16"/>
    <path class="d0-s-edge" data-back d="M375 334 C420 316 420 244 375 226 M384 222 L374 226 L380 235"/>
    <text class="d0-s-text d0-s-muted" x="420" y="287">정보 부족</text>
  </svg>
</figure>
```

- 두 그림은 같은 역할·갈래·라벨을 쓴다. 세로형도 viewBox 폭 560으로 그려 좁은 화면 글자 크기가 맞는다.
- 좌표·관계를 지켜야 해서 다시 배치할 수 없는 넓은 그림은 세로형 대신 그림 안 가로 스크롤로 둔다: `<div class="d0-fig__scroll" style="--min-w: 560px"><svg viewBox="0 0 750 300" …></svg></div>`. 페이지 전체가 가로로 넘치게 두지 않는다.

## 연결 그래프

```html
<figure class="d0-fig">
  <svg viewBox="0 0 560 348" role="img" aria-labelledby="g1-t g1-d">
    <title id="g1-t">고친 파일과 연결된 검사</title>
    <desc id="g1-d">고친 파일 하나에서 선이 검사 세 개로 이어져 강조돼 있어요. 다른 파일에 붙은 검사 두 개는 비어 있어요.</desc>
    <text class="d0-s-text d0-s-muted" x="451" y="25" text-anchor="middle">검사</text>
    <path class="d0-s-edge" d="M93 261 C272 261 272 249 451 249 M93 261 C272 261 272 311 451 311"/>
    <path class="d0-s-edge" data-on d="M93 124 C272 124 272 62 451 62"/>
    <path class="d0-s-edge" data-on d="M93 124 C272 124 272 124 451 124"/>
    <path class="d0-s-edge" data-on d="M93 124 C272 124 272 187 451 187"/>
    <circle class="d0-s-ring" cx="93" cy="124" r="26"/>
    <circle class="d0-s-node" data-on cx="93" cy="124" r="17"/>
    <circle class="d0-s-node" cx="93" cy="261" r="17"/>
    <circle class="d0-s-node" data-on cx="451" cy="62" r="14"/><circle class="d0-s-node" data-on cx="451" cy="124" r="14"/><circle class="d0-s-node" data-on cx="451" cy="187" r="14"/>
    <circle class="d0-s-node" cx="451" cy="249" r="14"/><circle class="d0-s-node" cx="451" cy="311" r="14"/>
    <text class="d0-s-text" data-on x="93" y="180" text-anchor="middle">고친 파일</text>
    <text class="d0-s-text d0-s-muted" x="93" y="311" text-anchor="middle">다른 파일</text>
    <text class="d0-s-text" data-on x="476" y="132">3개</text>
  </svg>
</figure>
```

- 열은 2~3개(원인 → 중간 → 결과). 열마다 노드의 x를 맞추고 열 머리 라벨을 둔다. 노드 r 14~17, 바깥 고리 r 26.
- 노드는 원이나 글자 없는 둥근 상자다. 상자 안에 문장을 넣지 않는다. 모든 노드에 이름이 보여야 한다(이름 없는 작은 도식은 읽히지 않는다).
- 상태가 있으면 의미색(`data-tone`)과 라벨을 함께 단다.

## 단계

```html
<figure class="d0-fig" data-fit="compact">
  <svg viewBox="0 0 560 162" role="img" aria-labelledby="s1-t s1-d">
    <title id="s1-t">내보내기 네 단계</title>
    <desc id="s1-d">첫 단계는 완료 체크, 두 번째 '묶음 고르기'가 강조돼 있어요.</desc>
    <path class="d0-s-edge" d="M93 56 H193 M243 56 H317 M367 56 H454"/>
    <path class="d0-s-edge" data-on d="M93 56 H193"/>
    <circle class="d0-s-step" data-tone="green" cx="68" cy="56" r="25"/><path class="d0-s-tick" d="M58 56 L65 64 L79 48"/>
    <circle class="d0-s-step" data-on cx="218" cy="56" r="25"/><text class="d0-s-num" data-on x="218" y="56">2</text>
    <circle class="d0-s-step" cx="342" cy="56" r="25"/><text class="d0-s-num" x="342" y="56">3</text>
    <circle class="d0-s-step" cx="479" cy="56" r="25"/><text class="d0-s-num" x="479" y="56">4</text>
    <text class="d0-s-text d0-s-muted" x="68" y="124" text-anchor="middle">누르기</text>
    <text class="d0-s-text" data-on x="218" y="124" text-anchor="middle">묶음 고르기</text>
    <text class="d0-s-text d0-s-muted" x="342" y="124" text-anchor="middle">미리보기</text>
    <text class="d0-s-text d0-s-muted" x="479" y="124" text-anchor="middle">받기</text>
  </svg>
</figure>
```

- 단계는 3~5개, 원 사이 간격은 라벨 폭에 맞춘다(124~156). 강조는 단계 하나(원 채움 + 흰 번호 + 라벨 + 들어오는 선).
- 현재 단계가 없는 흐름은 항상 거치는 묶음 뒤에 `.d0-s-zone` 둥근 상자 하나 + 묶음 라벨을 깔 수 있다.
- 끝난 단계는 green 원 + 체크선, 막힌 단계는 red 원 + 라벨이다.
- 그림이 단계 이름을 이미 보여 주므로 같은 단계를 카드·열로 다시 쓰지 않는다. 단계마다 그림에 없는 정보(기한, 담당)가 꼭 필요하면 그 정보만 단계 열(`ol.d0-steps`, [blocks/step-columns.md](../blocks/step-columns.md))로 붙인다.

## 주고받기

- 참여자 3~4명, 메시지 5개까지. 참여자 이름은 위, 세로선(`.d0-s-life`)은 아래로, 메시지는 가로 화살표 위 1~2단어 라벨이다.
- 돌아오는 응답은 `data-back` 점선, 핵심 메시지 하나만 `data-on`이다. 참여자 간격은 viewBox 560에서 187(4명이면 140).

```html
<path class="d0-s-edge" data-on d="M280 180 H464 M451 171 L464 180 L451 190"/>
<text class="d0-s-text" data-on x="373" y="165" text-anchor="middle">파일 저장</text>
```

## 진행선

- 지나온 구간 `.d0-s-edge[data-on]` + 작은 채움 원(r 9.5), 현재 큰 채움 원(r 17) + 고리(r 26) + 강조 라벨, 남은 구간 `.d0-s-edge[data-ahead]` + 빈 원이다. 현재는 하나다.
- 점은 3~6개, 진행 방향은 왼쪽 → 오른쪽이다. 지나온 구간과 남은 구간은 현재 점에서 나눈 `path` 두 개다.
- 현재 위치가 없는 절차에 쓰려면 독자가 설 대표 시점(가장 많이 막히는 단계 등)을 현재로 그린다. 정할 수 없으면 단계 도식을 쓴다. 날짜가 주인공이면 [blocks/timeline.md](../blocks/timeline.md)다.

## 모으기

- 왼쪽 문제는 둥근 상자(`.d0-s-frame`, rx = 높이 ÷ 2) 안 1~3단어, 오른쪽은 노드 하나 + 고리다. 해결 노드와 모이는 곡선이 강조 한 묶음이다.
- 문제 하나만 해결에 닿고 나머지는 남으면 닿는 곡선만 `data-on`, 남는 곡선은 `data-back` 점선이다. 해결과 원인을 한 그림에 함께 모으지 않는다.
- deck은 viewBox 800에 문제 상자 200×56, 해결 노드 r 30 + 고리 r 44가 기준이다.
