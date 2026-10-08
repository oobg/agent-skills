# side-by-side — 나란히 비교

## 해부 구조

- 같은 크기 2~3열. 열마다 독립 안이라 `<article>`(제목 h3). 열 = 안 이름 → 본문(미니 프로토타입 또는 비교 행) → 고르기 버튼(`aria-pressed`).
- 흰 글자 버튼 배경은 `--d0-blue-dark`(`--d0-blue`는 흰 글자 대비 4.5:1 미달).
- 후보 간 높이·정보량을 맞춘다. 고른 열은 기본이 **`고른 안` 배지 + 이유 한 줄(`.d0-option__why`) + 위쪽 blue 선**이다.
  전체 blue-light 배경은 반 폭 열에서 전체 포인트 상한(15%, [shell/contract.md](../shell/contract.md) 색 절)을 넘기기 쉬워 열이 작을 때(3열 또는 높이 200px 이하)만 `data-selected="fill"`로 쓴다.
- 640px 이하에서는 세로로 쌓이고 폭은 100%다.

## 레이아웃 변형 (`data-layout`)

모양 변형은 `data-layout`으로 고른다. 내용 변형 `data-variant`(`mock`·`decision`)와 따로 쓰므로 둘을 함께 달 수 있다(`data-variant="decision" data-layout="card"`). 카드는 후보를 비교하고 표는 기준을 비교한다. 각 선택지가 그림·설명을 가진 하나의 물건이거나 대상 둘을 몇 줄 기준으로 견주면 카드, 대상 셋 이상 × 기준 여럿이면 비교 표(`table.d0-table`)다.

- **split-plain(기본, 속성 없음).** 카드 없는 2~3열. 열마다 위쪽 선(1px grey-200)으로 시작 줄을 맞추고, 고른 열은 그 선이 2px blue가 된다. 면·radius·그림자 없음. 짧은 개념·문장 둘을 견줄 때 쓴다.
- **split-card(`data-layout="card"`).** 선택지 카드. 각 안이 그림·설명을 가진 '하나의 물건'일 때만 쓴다.
  **외곽선 카드**다. 면(배경색)은 없고 1px `--d0-grey-200` 테두리 + `--d0-radius-card`, 패딩 24px(640px 이하 20px), 그림자 없음. 그림 안쪽 면(`d0-s-fill` grey-100 등)이 카드 배경과 겹치지 않는다.
  카드는 축 폭을 같은 몫으로 나누고(2장이면 각 약 348px) 폭 상한은 **410px**이다(넓은 구간 960px에서도 가격표처럼 커 보이지 않게). 카드끼리 폭이 같다.
  카드 묶음은 섹션 폭 안에서 **가운데**(`justify-content: center`), 카드 안 내용(그림·행·배지·이유)은 **왼쪽 정렬**이다. 섹션 제목·리드는 그대로 왼쪽에 둔다.
  고른 카드는 테두리 색만 `--d0-blue`로 바꾸고(두께 1px 그대로라 레이아웃이 흔들리지 않는다) `고른 안` 배지를 단다. `data-recommended`는 테두리를 그대로 두고 `추천` 배지만 둔다. 카드 안에서는 `data-selected="fill"`도 면을 칠하지 않고 같은 blue 테두리로 표시한다.

## 언제 쓰나 / 변형

- 화면 시안을 실제처럼 눌러 보게 하려면 이 블록 대신 [mockup-frame.md](mockup-frame.md)을 쓴다. 이 블록의 mock 변형은 버튼 하나 수준의 작은 차이에만 쓴다.

- `data-variant="mock"`(시안): 각 열이 직접 눌러 보는 미니 프로토타입이다. 안의 버튼이 실제로 반응한다.
- `data-variant="decision"`(결정): 같은 순서의 `장점·비용·위험` 행. 추천 열에만 추천 이유 한 줄(`.d0-option__why`)을 붙인다.
- **추천했지만 결정 전(`data-recommended`).** 추천안 열에 `data-recommended` + h3 옆 `추천` 배지(`data-tone="blue"`) + 이유 한 줄(`.d0-option__why`)만 둔다. 아직 고른 것이 아니므로 `data-selected`·위쪽 blue 선·고르기 버튼이 없다. 모양은 다른 안과 같다. 결정이 나면 `data-selected` + `고른 안`으로 바꾼다.
- 변형 이름표가 없으면(개념 비교) 추천·선택 상태 없이 같은 구도의 카드만 나란히 둔다.
- **와이어 카드(`.d0-option__wire`).** 옵션마다 h3 바로 아래 글자 없는 와이어프레임 SVG(`role="img"` + `<title>`)를 두면 이 블록은
  **그림이다.** 수치 없는 결정 비교(어느 구조·배치로 갈까)의 대표 도식은 이 형태다. 결정 변형의 행과 함께 쓴다.

## 와이어 카드 스니펫

```html
<div class="d0-sbs" data-variant="decision" data-layout="card">
  <article class="d0-option">
    <h3>A안: 순서까지 고정</h3>
    <svg class="d0-option__wire" viewBox="0 0 240 140" role="img" aria-labelledby="oa-t">
      <title id="oa-t">A안: 모든 페이지가 같은 칸 네 개를 같은 순서로 써요</title>
      <rect class="d0-s-frame" x="1" y="1" width="238" height="138" rx="10"/>
      <rect class="d0-s-accent" x="16" y="16" width="208" height="20" rx="5"/>
      <rect class="d0-s-fill" x="16" y="44" width="208" height="20" rx="5"/>
      <rect class="d0-s-fill" x="16" y="72" width="208" height="20" rx="5"/>
      <rect class="d0-s-fill" x="16" y="100" width="208" height="20" rx="5"/>
    </svg>
    <dl class="d0-option__rows"><dt>장점</dt><dd>모든 페이지가 같아요.</dd><dt>위험</dt><dd>틀에 안 맞는 요청이 막혀요.</dd></dl>
  </article>
  <article class="d0-option" data-selected>
    <div class="d0-section-head__title"><h3>B안: 조각만 고정</h3><span class="d0-pill" data-tone="blue">고른 안</span></div>
    <svg class="d0-option__wire" viewBox="0 0 240 140" role="img" aria-labelledby="ob-t">
      <title id="ob-t">B안: 조각 모양은 같고, 고르는 조각과 순서는 페이지마다 달라요</title>
      <rect class="d0-s-frame" x="1" y="1" width="238" height="138" rx="10"/>
      <rect class="d0-s-accent" x="16" y="16" width="100" height="48" rx="6"/>
      <rect class="d0-s-fill" x="124" y="16" width="100" height="48" rx="6"/>
      <rect class="d0-s-zone" x="16" y="76" width="208" height="44" rx="6"/>
    </svg>
    <dl class="d0-option__rows"><dt>장점</dt><dd>요청마다 맞게 조립해요.</dd><dt>위험</dt><dd>원칙 점검이 필요해요.</dd></dl>
    <p class="d0-option__why">정함: 조각 모양만 지키면 돼요.</p>
  </article>
</div>
```

- SVG는 글자 없음(그림 글자 규칙 밖). 이름과 뜻은 h3·`<title>`·행이 말한다. 카드마다 같은 viewBox·같은 프레임 크기를 쓴다.
- 카드마다 blue 표식(`d0-s-accent`·`d0-s-zone`)은 하나씩, 두 안의 **차이 나는 자리**에 둔다. 회색만인 와이어는 금지다.
- 결정이 이미 났으면 고른 카드에 `data-selected` + `고른 안` 배지(h3 옆), 고르기 버튼은 빼고 이유 한 줄(`.d0-option__why`)만 둔다.

## 스니펫

CSS는 `assets/page.css`에 들어 있어 따로 붙이지 않는다.

```html
<div class="d0-sbs" data-variant="mock">
  <article class="d0-option">
    <h3>A안: 버튼을 위에</h3>
    <figure class="d0-mock"><span>주문 <data value="24">24</data>건</span><button type="button" class="d0-mock__btn">내보내기</button>
      <output class="d0-mock__msg"></output></figure>
    <button type="button" class="d0-option__pick" aria-pressed="false">A안 고르기</button>
  </article>
  <article class="d0-option">
    <h3>B안: 버튼을 아래에</h3>
    <figure class="d0-mock" data-layout="bottom"><span>주문 <data value="24">24</data>건</span><button type="button" class="d0-mock__btn">내보내기</button>
      <output class="d0-mock__msg"></output></figure>
    <button type="button" class="d0-option__pick" aria-pressed="false">B안 고르기</button>
  </article>
</div>
<!-- 결정 변형: 열 본문을 아래 행으로 바꾼다 -->
<!-- <dl class="d0-option__rows"><dt>장점</dt><dd>한 번에 끝나요</dd><dt>비용</dt><dd>하루 반</dd><dt>위험</dt><dd>알림이 늘어요</dd></dl>
     <p class="d0-option__why">추천: 팀 A가 가장 자주 쓰는 순서와 같아요.</p> -->
```

```js
document.querySelectorAll('.d0-sbs').forEach(function (group) {
  group.addEventListener('click', function (e) {
    var btn = e.target.closest('.d0-mock__btn');
    if (btn) {
      var mock = btn.closest('.d0-mock');
      var done = mock.toggleAttribute('data-done');
      mock.querySelector('.d0-mock__msg').textContent = done ? '파일을 만들고 있어요' : '';
    }
    var pick = e.target.closest('.d0-option__pick');
    if (pick) group.querySelectorAll('.d0-option').forEach(function (opt) {
      var on = opt.contains(pick);
      opt.toggleAttribute('data-selected', on);
      opt.querySelector('.d0-option__pick').setAttribute('aria-pressed', String(on));
    });
  });
});
```

## 금지

- 이유 없는 추천 배지, 추천안만 크고 자세한 열, 4열 이상.
- split-card에서: 카드 그림자·배경 면 칠하기, 2px 이상 테두리, 카드마다 다른 폭, 카드 묶음을 섹션 왼쪽에 붙이기, 카드 안 내용 가운데 정렬.
- 짧은 개념·문장 비교나 같은 기준을 여러 개 반복 대조하는 비교에 split-card(그 경우 split-plain 또는 표).
- 차이를 문단으로만 설명, 눌러도 반응하지 않는 가짜 프로토타입.
- 와이어 카드 SVG 안 글자, 카드마다 다른 viewBox·프레임 크기, `<title>` 없는 와이어.
