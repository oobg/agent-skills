# diagrams/comparison — 비교 도식

무엇과 무엇이 어떻게 다른지, 전과 후가 얼마나 다른지를 그린다. 공통 규칙과 클래스는 [index.md](index.md)에 있다.

## 같은 틀, 다른 것만

비교 그림은 공통 요소를 고정하고 차이만 움직인다.

- 양쪽은 같은 틀 크기·좌표계·순서·축척·모양이다. 두 그림을 2열에 둘 때는 같은 viewBox 크기로 그린다(2열 칸은 viewBox 폭 360).
- 위치 변화 자체가 주장일 때만 위치를 바꾼다. 한쪽은 세로, 한쪽은 가로로 그리면 배치 차이가 주장처럼 읽힌다.
- 모양만으로 뜻을 알 수 없는 노드·점선·빈칸·채움은 그 곁에 직접 라벨을 단다. 캡션에만 적지 않는다.
- **없음 자리.** 한쪽에 없는 항목은 대응하는 같은 자리를 비워 두고 `없음`, `서버에 없음`, `미확정`처럼 직접 라벨한다. 빈자리는 회색 점선(`.d0-s-edge[data-back]` 또는 점선 테두리) + 중립 라벨이 기본이고, 부재가 핵심 주장일 때만 라벨이나 테두리를 강조한다. 빈 영역 전체를 강조색으로 채우지 않는다.
- 강조는 그 그림이 말하는 차이에 둔다. 한 차이를 이루는 대응 한 쌍은 같은 blue를 두 자리에 써도 된다.

| | 좋은 예 | 나쁜 예 |
| --- | --- | --- |
| 상태를 각자 들고 있음 vs 공유함 | 두 화면을 같은 크기·자리로 그리고, 왼쪽은 화면마다 상태 상자, 오른쪽은 두 화면이 함께 가리키는 상자 하나. 상자마다 `상태` 라벨 | 왼쪽은 세로, 오른쪽은 가로로 그리고 상자에 라벨 없이 색만 다르다 |
| 앱 입력칸 vs 서버 필드 | 같은 행 순서로 나란히, 서버에 없는 행 자리에 점선 빈칸 + `서버에 없음` | 서버 쪽만 그리고 몇 개가 빠졌는지 캡션으로 말한다 |

## 전/후·선택지 막대

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
</figure>
```

- 막대 폭 = 값 ÷ 최댓값 × 트랙 폭(6 ÷ 14 × 404 = 173). 값 라벨은 막대 끝 바로 뒤에 두고 범례를 따로 두지 않는다.
- 막대가 3개 이상이면 행 간격 81을 유지하고 viewBox 높이를 `행 수 × 81 + 12`로 늘린다. 막대 둘이면 `data-fit="compact"`가 기본이다.
- 선택지(A안·B안)를 견줄 때는 선택지 이름을 행 라벨로, 행마다 같은 트랙과 축을 둔다. 추천안이 있으면 그 행을, 없으면 지금 방식 행을 강조한다.
- 같은 단위 값 3~6개나 구성비는 SVG 대신 HTML 가로 막대 목록 `ol.d0-barlist`가 간단하다(마크업은 레시피). 두 지표를 함께 견주면 막대 목록 두 개를 `div.d0-cols`에 나란히 둔다.
- 기준선·목표선은 `.d0-s-target`으로 긋는다. 막대는 0에서 시작한다.

## 추이

- 시간에 따른 값은 꺾은선이다. 세로축 눈금 3~5개와 단위, 기준선이 있으면 그 값을 그림에 적고, 점 값은 제목이 말하는 것(마지막 값 등)만 적는다. 덱 꺾은선 예시는 [recipes/deck.md](../recipes/deck.md)에 있다.

## 비율 막대

전체 한 줄 중 부분이 얼마인지 보인다. 컨테이너 폭을 꽉 채우므로 숫자 라벨은 SVG 밖 HTML에 둔다.

```html
<figure class="d0-fig" data-variant="ratio">
  <div class="d0-ratio__labels" aria-hidden="true"><span class="d0-ratio__part">58건 전부 검사</span><span>전체 234건</span></div>
  <svg viewBox="0 0 100 10" preserveAspectRatio="none" role="img" aria-labelledby="r1-t">
    <title id="r1-t">지난 주문 234건 중 58건(25%)을 전부 검사</title>
    <rect class="d0-s-bar" width="100" height="10"/><rect class="d0-s-bar" data-on width="24.8" height="10"/>
  </svg>
</figure>
```

- HTML로 그리는 몫 막대 `div.d0-share`(막대 + 아래 몫 이름표)도 있다. 부분 폭 = 부분 ÷ 전체 × 100. 부분은 blue, 나머지는 grey다. 부분이 여럿이면 rect를 이어 붙이고 blue는 하나만 쓴다.

## 숫자 하나 크게 (editorial)

선을 거의 쓰지 않고 실제 숫자 하나를 HTML로 크게, 뜻을 받치는 작은 객체(최대 120px) 하나만 SVG로 그린다.

```html
<figure class="d0-fig" data-genre="editorial">
  <svg viewBox="0 0 120 120" role="img" aria-labelledby="e1-t"><title id="e1-t">지난 주문 중 전부 검사한 몫</title>
    <circle class="d0-s-bar" cx="60" cy="60" r="58"/><path class="d0-s-accent" d="M60 60 V2 A58 58 0 0 1 118 60 Z"/>
  </svg>
  <p class="d0-ed__num"><data value="25">25</data>%</p>
  <figcaption>지난 주문 네 번 중 한 번은 전부 검사해요.</figcaption>
</figure>
```

- 실제 숫자일 때만 쓴다(문구·대답은 제목으로). 페이지에 하나, 히어로와 같은 숫자면 쓰지 않는다.

## 다른 비교 부품

| 비교 | 쓰는 것 |
| --- | --- |
| 옵션 2~3개를 같은 기준으로(장점·비용·위험, 와이어 카드) | [blocks/side-by-side.md](../blocks/side-by-side.md) |
| 같은 대상의 실제 두 상태(문제 → 수정, 기존 → 개선) | [blocks/before-after.md](../blocks/before-after.md) |
| 바뀐 항목만 행으로 | [blocks/diff-rows.md](../blocks/diff-rows.md) |
| 전/후 지표 카드 여러 장 | [blocks/kpi-cards.md](../blocks/kpi-cards.md) |
| 대상 여럿 × 기준 여럿 | 비교 표 `table.d0-table`(레시피의 마크업, 없음·미확정은 `data-state`) |
