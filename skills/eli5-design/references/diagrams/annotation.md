# diagrams/annotation — 화면·결과물 짚기

결과물이 어떤 모양인지, 화면이나 그림의 어디가 무엇인지를 그린다. 공통 규칙과 클래스는 [index.md](index.md)에 있다. 눌러 봐야 이해되는 화면은 [blocks/mockup-frame.md](../blocks/mockup-frame.md)다.

| 변형 | 그리는 것 | 언제 |
| --- | --- | --- |
| 화면 골격 | 상단 바·카드·버튼을 글자 없는 상자로, 바뀌는 곳만 blue | 어떤 화면의 어디가 바뀌나 |
| 표 썸네일 | 머리 행·키 열·합계 칸이 있는 미니 격자(JS 생성) | 결과물이 어떤 모양의 표인가 |
| 번호 핀 | 그림 위 HTML 번호 + 범례, hover·focus한 번호의 영역이 켜짐 | 화면·파일 같은 그림의 영역마다 이름·뜻을 붙일 때(파일 항목의 뜻은 코드 안 주석 대신 종이 그림 + 핀) |
| 번호 주석 | 기존 그림 위 번호 2~4개 + 한 줄 주석 목록(움직임 없음) | 영역이 없는 점(차트의 막대·값 하나)을 짚을 때 |
| 파일 트리 | 폴더·파일을 들여쓴 줄, 위치가 둘이면 같은 틀로 나란히 두고 다른 칸만 blue | 무엇을 어디에 두나 |
| 노트 | 그림 곁 짧은 해석 1~2개 | 그림의 한 지점 뜻·조건(없어도 본문이 이해될 때만) |

## 화면 골격

```html
<figure class="d0-fig" data-frame="none"><!-- 화면 틀을 그렸으니 외곽선 끔 -->
  <svg viewBox="0 0 560 342" role="img" aria-labelledby="w1-t w1-d">
    <title id="w1-t">주문 관리 화면 골격</title>
    <desc id="w1-d">위쪽 바 오른쪽 버튼과 그 아래 필터 영역이 강조돼 있어요.</desc>
    <rect class="d0-s-frame" x="1.5" y="1.5" width="557" height="339" rx="19"/>
    <path class="d0-s-line" d="M1.5 65 H558"/>
    <rect class="d0-s-fill" x="25" y="25" width="131" height="16" rx="8"/>
    <rect class="d0-s-accent" x="420" y="17" width="115" height="31" rx="9.5"/>
    <rect class="d0-s-zone" x="25" y="87" width="510" height="44" rx="9.5"/>
    <rect class="d0-s-fill" x="25" y="152" width="246" height="68" rx="12"/>
    <rect class="d0-s-fill" x="289" y="152" width="246" height="68" rx="12"/>
  </svg>
  <figcaption>새 필터는 버튼 바로 아래, 표 위에 생겨요.</figcaption>
</figure>
```

- 회색 면은 자리만 잡는다. 바뀌는 곳은 blue 하나(버튼은 채움, 영역은 점선 테두리 `.d0-s-zone`).
- 부분마다 이름을 붙여야 하면 SVG 안에 글자를 넣지 말고 번호 핀을 얹는다.

## 표 썸네일

```html
<figure class="d0-fig" data-fit="compact">
  <div data-grid='{"rows":8,"cols":6,"sumCol":true,"sumRow":true,"blanks":0.15,"seed":3,"label":"팀 행 × 일자 열 표"}'></div>
  <figcaption>팀마다 한 줄, 날짜마다 한 칸이에요.</figcaption>
</figure>
```

- `assets/page.js`가 SVG로 바꾼다. `rows`·`cols`(머리 행·키 열 포함), `headRow`·`keyCol`(기본 true), `sumRow`·`sumCol`, `blanks`(빈칸 비율), `seed`, `label`(접근 이름, 필수). 실제 결과물의 행·열 수에 맞춘다.

## 번호 핀

```html
<figure class="d0-fig" data-variant="pins" data-active-pin="1">
  <div class="d0-pins">
    <svg viewBox="0 0 560 350" role="img" aria-labelledby="p1-t"><title id="p1-t">설명 페이지 한 장의 구성</title>
      <rect class="d0-s-frame" x="1" y="1" width="558" height="348" rx="14"/>
      <g data-pin="1"><rect class="d0-s-area" x="16" y="16" width="527" height="63" rx="9.5"/><rect class="d0-s-accent" x="28" y="28" width="210" height="16" rx="8"/></g>
      <g data-pin="2"><rect class="d0-s-zone" x="28" y="93" width="504" height="149" rx="12"/></g>
    </svg>
    <span class="d0-pin" data-pin="1" style="left: 45%; top: 8%" aria-hidden="true">1</span>
    <span class="d0-pin" data-pin="2" style="left: 50%; top: 27%" aria-hidden="true">2</span>
  </div>
  <dl class="d0-pins__key">
    <div data-pin="1" tabindex="0"><dt><span class="d0-pin">1</span>머리</dt><dd>제목과 결론 한 줄이에요.</dd></div>
    <div data-pin="2" tabindex="0"><dt><span class="d0-pin">2</span>그림 자리</dt><dd>주인공 그림이 놓여요.</dd></div>
  </dl>
</figure>
```

- 핀 위치 = SVG 좌표 ÷ viewBox 크기 × 100%. 핀은 3~6개, 핀끼리 겹치지 않게(중심 간격 28px 이상) 둔다.
- 범례 항목·핀·SVG 영역 `g`에 같은 `data-pin`을 단다. `data-active-pin`이 켜진 번호이고 `assets/page.js`가 hover·focus에 바꾼다. 범례 `dd`는 한 문장이다.
- 범례는 넓은 화면에서 그림 오른쪽 바깥에 붙고 좁은 화면에서는 아래로 내려간다. 항목이 5개 이상이거나 그림보다 길면 figure에 `data-key="below"`를 단다.

## 번호 주석

```html
<figure class="d0-fig" data-variant="annotate">
  <div class="d0-annot">
    <svg viewBox="0 0 560 311" role="img" aria-labelledby="an1-t"><title id="an1-t">주별 재시도 막대 …</title>…</svg>
    <span class="d0-pin" style="left: 30%; top: 46%" aria-hidden="true">1</span>
    <span class="d0-pin" style="left: 70%; top: 18%" aria-hidden="true">2</span>
  </div>
  <ol class="d0-annot__notes">
    <li><span class="d0-pin" aria-hidden="true">1</span>앞 세 주는 조금씩 늘었어요.</li>
    <li><span class="d0-pin" aria-hidden="true">2</span>마지막 주에 한 번에 크게 늘었어요.</li>
  </ol>
</figure>
```

- 주석 `li` 하나가 한 줄이다. 번호는 강조 도형을 가리지 않게 도형 모서리 바깥에 둔다. deck은 근거 장 요점 자리에 주석 2~3개를 둔다.

## 노트

```html
<div class="d0-margined">
  <figure class="d0-fig">…</figure>
  <aside class="d0-margin">검사 지점: 테스트가 끝난 뒤 배포 전에 거쳐요.</aside>
</div>
```

- 그림 블록 하나와 노트 1~2개를 `div.d0-margined`로 묶는다. 첫머리에 그 지점 이름(그림 라벨과 같은 말)을 쓴다. 용어 풀이·출처·결론·핵심 근거는 노트에 두지 않는다. 표·글 블록에는 달지 않는다.
