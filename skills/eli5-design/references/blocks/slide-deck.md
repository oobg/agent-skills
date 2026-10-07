# slide-deck — 한 장씩 넘기는 발표 덱

[덱 출력](../output/deck.md)의 마크업·CSS·JS 정본이다. 덱 구성·문장·Slide Gate는 덱 출력 문서가 정하고, 이 파일은 그 덱을
화면에 한 장씩 띄우고 넘기는 구현을 정한다. 문서형 `main.d0-page` 대신 `main.d0-deck`을 쓴다.

덱을 만들기 전에 [output/deck.md](../output/deck.md)의 Audience × Purpose와 Story Gate부터 통과한다.

**전제.** 덱도 [shell.md](shell.md) 공통 CSS(tokens.css 인라인, `color-scheme`, `box-sizing: border-box` 리셋, `body` 기본 타이포)를 먼저 붙이고 그 뒤에 이 파일의 CSS를 붙인다. 리셋이 없으면 슬라이드 폭에 패딩이 더해져 화면 밖으로 넘친다(1280에서 1216px 장이 약 1338px가 된다).

## 슬라이드 종류 `data-kind`

| 종류 | 몸 | 배치 |
| --- | --- | --- |
| (생략) 근거 | split: 그림(3) + 요점(2) | 그림 비율 하한은 덱 출력 밀도 표 |
| `cover` | 결론 h1 + 대표 도식 + 요약 0~1행 | `data-cover`로 도식 위치를 고른다. 진한 면 `data-surface="dark"` 가능 |
| `toc` | `ul.d0-slide__toc` | 그림 예외, 작은 점 불렛으로 제목만 표시 |
| `assertion` | 주장 한 문장(제목)만 | 그림 예외, Impact 기본, 제목이 세로 가운데 |
| `evidence` | 결론 제목 + 가로형 차트 + 해석 한 줄 | 그림 비율 하한은 덱 출력 밀도 표 |
| `screenshot` | 결론 제목 + `figure.d0-shot` | 화면 상자가 몸 행 높이를 채운다(폭은 화면 비율, 왼쪽 정렬) |
| `breakdown` | 결론 제목 + 전체 → 구성 요소 도식 | 그림 비율 하한은 덱 출력 밀도 표 |
| `stat` | 숫자가 주장인 장. 기본형은 숫자 + 기준 줄 + 근거 그림 하나 | 기본형은 비대칭(왼쪽 숫자, 오른쪽 근거 그림, 아래 출처). 숫자만 두는 순수 Impact stat은 큰 숫자가 그림(아래 [핵심 수치](#핵심-수치-data-kindstat)) |
| `summary` | 참고용 정리 목록 3행 이내 | 그림 예외, 마지막 요청 장에는 쓰지 않는다 |
| `section` | 큰 번호 `p.d0-slide__index` + 챕터 제목 h2 | 그림 예외, 8장 이상이고 챕터가 2~3개로 뚜렷할 때만. 진한 면 가능 |
| `closing` | 큰 마무리 한 문장 + 구분선 + 작은 `dl` 메타 행. 상위 종류이고 `data-closing`이 세부(decision·request·action·criteria·takeaway) | 그림 예외, 마지막 장 전용. 진한 면 가능 |

- **screenshot.** 화면·spotlight(`span.d0-shot__spot`)·번호 주석(`p.d0-shot__note`)·dim의 마크업과 CSS는 [mockup-frame.md](mockup-frame.md)가 정본이다.
  이 파일은 슬라이드 안 자리와 크기만 정한다. mockup-frame의 화면 폭 상한(560px)과 900px 이상 2열 격자는 page 전용이고, 덱은 아래 덱 격자가 덮는다.
  **덱 격자.** `figure.d0-shot`이 몸 행(`minmax(0, 1fr)`)을 채운다. 왼쪽 화면 열(`max-content`)의 화면 상자는 몸 행 높이를 다 쓰고 폭은 비율(기본 16:10)로 정해진다. 주석·캡션은 오른쪽 주석 레일 열(`minmax(0, 1fr)`)에 위에서부터 쌓인다.
  1280 한 장 모드에서 16:10 화면은 몸 영역의 약 70%다. 화면이 16:9보다 넓으면 주석 열이 좁아지므로 주석을 줄인다.
  주석·캡션은 본문 크기(2cqi)로 키운다. 화면 비율이 다르면 `.d0-shot__screen`에 `style="aspect-ratio: 가로 / 세로"`를 적는다. 730 미만에서는 화면 → 주석 → 캡션 1열이고 높이 자동, 폭 100%.
- **Impact screenshot.** 그림이 있는 Impact라 제목은 일반 장 크기(3.6cqi, 1280에서 약 39px)다. 화면이 그 장의 하나이고 제목은 화면을 읽는 법을 알려 주는 머리 줄이다. 그림 비율 권장 하한 55%를 그대로 받고 따로 예외를 두지 않는다.
  Impact는 글자 크기가 아니라 한 주장에 시선을 모으는 장이라는 점으로 정해진다. 화면 하나 외에 요점·카드·두 번째 그림을 더하면 Impact가 아니다.
- **그림 면적.** 실제로 그려진 그림 요소(`svg`·`img`, screenshot은 `.d0-shot__screen`)의 렌더 box ÷ 몸 영역(슬라이드 안쪽 폭 × 몸 행 높이, 머리·발·패딩 제외)으로 잰다. `figure` box나 split 열 box가 아니다. 측정 정의와 하한은 [덱 출력](../output/deck.md) 밀도 표가 정본이다.
  split의 SVG는 그림 열을 채우므로(아래 [그림 글자](#그림-글자)) 열을 넓히면 그림도 커진다. 제목이 길면 보조 한 줄(`__sub`)을 달 수 있다. 몸 영역 기준이라 제목 두 줄·보조 줄이 비율을 바꾸지 않는다.

## 커버 변형 `data-cover`

커버는 독자가 알아야 할 결론 문장과 대표 도식 하나로 시작한다. `비교 발표` 같은 유형·메타 정보는 크게 쓰지 않고 필요하면 작은 `.d0-slide__eyebrow`에만 둔다. 요약 3행을 반복하지 않고 도식·리드에 흡수하며, 결정할 것만 `dl.d0-slide__summary` 한 행으로 남길 수 있다.
표지 메타 행은 제목과 그림 해석 줄을 되풀이하지 않는다. 다른 정보(필요한 것·결정할 것·입력/결과·다음 단계)가 없으면 메타 행을 뺀다. 마무리 메타도 제목에 이미 있는 기한·대상을 칸으로 되풀이하지 않는다.
`div.d0-slide__cover` 안에 `header.d0-slide__head`와 `figure.d0-slide__fig`를 둔다. 커버 도식은 근거 장의 그림 비율 게이트(밀도 표 하한) 대신 주제의 실체와 의미 있는 그림 면적을 확인한다.

| 값 | 위치 | 예시 |
| --- | --- | --- |
| `contrast` | 제목 아래 가로 A/B 대비 | compare |
| `bottom` | 제목 아래 가로 흐름·시간 막대 | flow, timeline |
| `side` | 오른쪽 작은 그림(기기·변화 차트·완성 화면), 그림 비율에 맞춘 열. 가로로 긴 도식은 넣지 않는다 | preview, report, guide |
| `center` | 가운데 경과선, 결론을 그 위에 가운데 정렬 | incident |
| `map` | 오른쪽 아래 작은 용어 지도 | faq |

- **side(생략 포함).** 세로·정사각형에 가까운 작은 그림(viewBox 400 안팎) 전용이다. 그림과 해석 줄을 한 묶음으로 열의 세로 가운데에 두어(그림 행 `auto auto`) 해석 줄이 그림 바로 아래에 붙는다.
  가로로 긴 도식(예: viewBox 800 흐름·시간 막대)은 side 열에 넣지 않는다. 좁은 열에서 그림이 납작해지고 글자가 작아진다. `bottom`·`contrast`·`center`처럼 제목 아래 전체 폭으로 두거나, 표지용으로 줄인 400 폭 도식을 다시 그린다.
- **map.** 그림 열이 좁다(1280에서 약 370px). 800 폭 지도를 그대로 넣으면 1280에서 글자가 약 7.5px로 줄어 읽히지 않는다. 표지용으로 줄인 viewBox 400 지도(항목을 줄이고 라벨을 짧게)를 기본으로 하고, 800 폭이 꼭 필요하면 `bottom`처럼 그림 열이 넓은 구도로 옮긴다.
  아래 CSS의 `--sl-font: 30px`(800 지도, 731px 이상에서 약 14px)는 그대로 둔 지도를 위한 안전망이지 권장 경로가 아니다. 판정은 같은 장의 해석 줄 옆에서 그림 라벨이 읽히는가로 한다.

```html
<section class="d0-slide" id="cover-example" data-kind="cover" data-cover="bottom" aria-labelledby="cover-example-t" tabindex="-1">
  <div class="d0-slide__cover">
    <header class="d0-slide__head"><h1 class="d0-slide__title" id="cover-example-t">요청 한 줄이 검사 뒤 설명 페이지 한 장이 된다</h1></header>
    <figure class="d0-slide__fig">
      <svg viewBox="0 0 800 180" role="img" aria-label="요청에서 검사까지 이어지는 과정"><title>요청에서 검사까지 이어지는 과정</title>
        <path class="d0-sl-link" d="M100 80H700"/>
        <circle class="d0-s-node" cx="100" cy="80" r="24"/><circle class="d0-s-node" data-on cx="400" cy="80" r="24"/><circle class="d0-s-node" data-tone="green" cx="700" cy="80" r="24"/>
        <g class="d0-sl-label"><text x="100" y="140">요청</text><text x="400" y="140">그림</text><text x="700" y="140">검사</text></g>
      </svg>
      <figcaption class="d0-slide__note">그림을 먼저 그리고 검사를 통과한 한 장을 넘긴다.</figcaption>
    </figure>
  </div>
  <footer class="d0-slide__foot"><p class="d0-slide__num">1 / 9</p></footer>
</section>
```

## 마지막 장 `data-kind="closing"`

공용 [closing](closing.md) 블록의 덱 형태다. page에서는 같은 블록을 `footer.d0-closing`으로 쓴다.

마지막 장은 상위 종류 `data-kind="closing"` 하나이고, 무엇을 마무리하는지는 `data-closing`이 말한다. 구도와 CSS는 종류와 무관하게 같다.

| `data-closing` | 쓰임 | 메타 라벨 예 |
| --- | --- | --- |
| `decision` | 선택지·방안 중 하나를 고르게 한다 | 담당 / 기한 / 다음 |
| `request` | 도움·자원·승인을 요청한다 | 요청 / 기한 / 다음 |
| `action` | 독자가 직접 해 볼 행동을 정한다 | 대상 / 언제 / 다음 |
| `criteria` | 끝났는지 확인할 기준을 남긴다 | 확인할 것 / 통과 기준 / 다음 |
| `takeaway` | 앞으로 지킬 것을 남긴다 | 지킬 것 / 담당 / 다음 |

덱마다 `data-closing` 값은 하나이고, 애매하면 마지막 장이 하는 일에 가장 가까운 종류를 고른다. 라벨은 예일 뿐이며 덱에 나온 사실에 맞게 바꾼다.

큰 한 문장을 세로 중앙에 두고(5cqi, 1280 한 장에서 약 54px, 730px 미만 27px), 그 아래 구분선과 작은 `dl.d0-slide__meta` 행을 둔다.
메타는 담당·기한·다음 행동 중 덱에 이미 나온 사실만 2~3칸으로 적는다. 없는 담당이나 날짜를 만들어 채우지 않는다.
결정 문장과 같은 무게의 불릿 목록을 두지 않고, Impact로 색칠하지 않는다. 제목이 그 결정 문장 하나다.

```html
<section class="d0-slide" id="closing-example" data-kind="closing" data-closing="decision" aria-labelledby="closing-example-t" tabindex="-1">
  <header class="d0-slide__head"><h2 class="d0-slide__title" id="closing-example-t">이번 주 안에 발송 주기를 정해 주세요</h2></header>
  <dl class="d0-slide__meta">
    <div><dt>담당</dt><dd>서비스 운영 팀</dd></div>
    <div><dt>기한</dt><dd>이번 주 금요일</dd></div>
    <div><dt>다음</dt><dd>다음 주에 적용한다</dd></div>
  </dl>
  <footer class="d0-slide__foot"><p class="d0-slide__num">9 / 9</p></footer>
</section>
```

## 강조 `data-emphasis`

- **impact.** 슬라이드 전체 면이 `var(--d0-blue-light)`다(그림자 없음). 글자 grey-900, 보조·출처는 grey-700(grey-600은 blue-light 위 4.49로 미달), 숫자는 blue-dark.
  안에는 문장 하나, 숫자 하나, 그림 하나 중 하나만 둔다. 카드·요점 목록·두 번째 그림 금지. Impact는 글자 크기가 아니라 한 주장에 시선을 모으는 장이다.
  제목 크기는 면 안의 하나가 무엇이냐로 정한다. 그림 없는 순수 Impact(`assertion`)만 6cqi(1280에서 약 66px)이고, 그림·숫자가 있는 Impact(screenshot·evidence·breakdown·근거·`stat`)는 일반 장 제목 크기(3.6cqi, 약 39px)다. 비대칭(`data-layout="asym"`) 장은 Impact여도 asym 제목 크기다(아래 비대칭 구도). 그림 비율 하한은 Impact라고 낮추지 않는다.
  - `assertion` + impact가 기본형이다. 제목 한 문장이 그 하나다(리드·보조 줄도 두지 않는다).
  - `stat` + impact(순수 Impact stat)는 큰 숫자(10cqi, 96px 이상)가 그 하나다. 제목은 숫자를 읽는 법을 알려 주는 머리 줄이라 일반 크기로 두어 숫자와 다투지 않게 한다. 숫자 자체가 결론일 때만 쓰는 예외형이고, stat 기본형(숫자 + 근거 그림)은 Impact가 아니다(아래 [핵심 수치](#핵심-수치-data-kindstat)).
  - 덱의 Impact 장은 전체의 20~30%다(8~9장이면 2장, 12장이면 3장). 판정은 덱 출력의 Slide Gate.
- **quiet.** 밀도를 낮추는 쉬는 장이다. 제목 + 한 줄, 또는 작은 그림 하나만 두고 요점 목록을 두지 않는다. 제목 굵기가 600으로 내려간다.
- 생략 = normal.

## 제목 문법

한 장의 제목은 작은 머리 줄 → 1~2줄 결론 제목 순서다. 머리 줄은 표지면 `.d0-slide__eyebrow`, 챕터가 있으면 섹션 태그 `.d0-slide__tag`(아래 크롬) 중 하나만 둔다.

- **결론어 하나만 굵게(선택).** 제목 안에서 결론을 담은 구간 하나를 `b.d0-slide__key`로 감싸면 나머지 구절은 regular·grey-700으로 내려가고 그 구간만 700·grey-900으로 남는다. 감싸지 않으면 지금처럼 제목 전체가 700이다.
- `data-tone="blue"`를 달면 그 구간이 blue-dark가 된다. 제목마다 강조 구간 1개, blue 1개까지이고, 그림의 `data-on` 강조와 같은 뜻일 때만 blue를 쓴다. 진한 면에서는 blue를 쓰지 않는다(아래 대비).
- 목차 항목 글자는 `textContent`가 같으면 되므로 `b`를 옮기지 않아도 된다. `+`·`/`·`|` 같은 기호를 제목 장식으로 고정하지 않는다.

```html
<h2 class="d0-slide__title" id="s-05-t">재시도는 <b class="d0-slide__key" data-tone="blue">대기열에서 절반 넘게</b> 생긴다</h2>
```

## 슬라이드 크롬

장마다 같은 자리에 같은 작은 요소가 있어 실루엣이 달라도 한 덱으로 읽힌다. 셋 다 선택이고, 한 장에 기본 2개 이하다.

| 요소 | 클래스 | 언제 |
| --- | --- | --- |
| 섹션 태그 pill | `p.d0-slide__tag`(머리 맨 위, eyebrow 자리) | 섹션 장(`section`)이 있는 덱에서 그 챕터에 속한 장만. 글자는 챕터 이름 그대로 |
| 쪽번호 | `p.d0-slide__num` | 목차를 뺀 모든 장(기존 규칙). 옅게 보이게 하려고 grey-600보다 밝게 하지 않는다(흰 바탕 4.5:1). 크기로만 작게 둔다 |
| 얇은 푸터 | 출처 `p.d0-slide__src`가 있으면 발 위에 1px grey-100 선이 자동으로 생긴다 | 출처·기준이 있을 때만. 키 안내만 있는 표지에는 선이 없다 |

로고·회사명·제품 브랜드 표식은 크롬에 두지 않는다.

## 비대칭 구도 `data-layout="asym"`

제목을 좁은 열에 작게 두고 핵심 그림을 반대편 넓은 열에 크게 둔다(제목 열 2 : 그림 열 3). 기본은 제목 왼쪽·그림 오른쪽이고 `data-flip`을 더하면 그림 왼쪽·제목 오른쪽이다.

- **언제.** 그림 하나가 그 장의 근거 전부이고, 제목 줄을 위에 따로 두면 그림이 낮게 눌릴 때(세로로 긴 연결 도식, 정사각형에 가까운 그림, 주석이 붙은 그림). 근거(생략)·`evidence`·`breakdown` 장에 쓴다. `stat` 기본형도 이 격자를 쓴다(아래 [핵심 수치](#핵심-수치-data-kindstat)).
- **어떻게.** `section.d0-slide`에 `data-layout="asym"`을 달고 머리·그림·발을 바로 자식으로 둔다(`.d0-slide__body`를 쓰지 않는다). 머리에는 제목과 보조 한 줄(`__sub`)까지만 둔다. `stat` 기본형만 제목 아래에 큰 숫자(`p.d0-slide__stat`)와 기준 줄(`p.d0-slide__base`)을 더 둔다. 제목은 3.2cqi(1280 한 장에서 약 35px)다. Impact 장이어도 같다. 레이아웃의 가용 폭이 제목 크기를 정하고, Impact는 이를 덮어쓰지 않는다.
- **그림 비율.** 머리가 몸 행 안으로 들어가므로 몸 영역은 슬라이드 안쪽 폭 × 첫 행 높이다. 권장 하한은 근거 split과 같은 45%다(밀도 표, breakdown·evidence여도 같다). 그림 열 SVG는 viewBox 400~480을 권장한다(800이면 1280에서 글자가 14px로 줄어든다).
- **리듬.** 모든 장을 좌우 번갈아 놓지 않는다. 덱에 1~3장, 그림이 실제로 핵심인 장에만 쓴다. `stat` 기본형도 이 장수에 세고, 이웃한 비대칭 장과 붙여 두지 않는다. 730px 미만에서는 머리 → 그림 1열로 돌아간다.

```html
<section class="d0-slide" id="s-06" data-layout="asym" aria-labelledby="s-06-t" tabindex="-1">
  <header class="d0-slide__head">
    <p class="d0-slide__tag">원인</p>
    <h2 class="d0-slide__title" id="s-06-t">세 가지 늦음은 <b class="d0-slide__key">대기열 하나</b>에서 갈라진다</h2>
    <p class="d0-slide__sub">4주 차 발송 기록 기준</p>
  </header>
  <figure class="d0-slide__fig">…converge SVG(diagram.md (h))…<figcaption class="d0-slide__note">대기열만 나누면 셋이 함께 준다.</figcaption></figure>
  <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>6 / 10</p></footer>
</section>
```

## 핵심 수치 `data-kind="stat"`

숫자가 주장인 장이다. Impact와 다르다. Impact는 일부러 비워 두고 한 주장·숫자에 시선을 모으는 장이고, stat은 숫자 + 그 숫자를 읽게 하는 근거 그림 하나가 기본이다.
빈 공간을 채우려고 그림을 더하지 않는다. 다만 제목이 주장하는 비교·변화를 읽는 데 필요한 근거는 화면에 둔다(근거 게이트는 [덱 출력](../output/deck.md) Slide Gate의 [Evidence]).

- **기본형(비대칭).** `data-kind="stat" data-layout="asym"`. 왼쪽 머리 열에 제목 → 큰 숫자 `p.d0-slide__stat` → 작은 기준 줄 `p.d0-slide__base`(`출시 전 18%에서`처럼 비교 기준·분모·기간 중 필요한 것)를 쌓고, 오른쪽 그림 열에 근거 그림 하나, 발에 출처 줄을 둔다.
  제목은 asym 제목(3.2cqi)이고 흰 면이다. 숫자 + 근거 그림 두 가지가 있으므로 Impact 면(`data-emphasis="impact"`)을 달지 않는다. 그림 비율 권장 하한은 비대칭 45%다(덱 출력 밀도 표).
  큰 숫자 + 비대칭 + 근거 그림은 stat 기본형 한 벌이라 "한 장에 특징 몰아넣기"로 세지 않는다. 여기에 주석·진한 면을 더하지 않는다.
- **순수 Impact stat(예외형).** 숫자 자체가 결론이고 비교할 기준이 없거나 기준이 숫자 옆 한 줄로 충분할 때만 `data-kind="stat" data-emphasis="impact"`로 숫자만 남긴다(아래 스니펫 s-08). 비교 기준이 있으면 해석 줄에 숨기지 않고 숫자 옆에 작은 기준 글자 `span.d0-slide__base`로 둔다(숫자 `p.d0-slide__stat` 안 마지막 자식).
  권장(게이트 아님): 짧은 덱에서 보통 0~1장이고 두 장을 잇달아 두지 않는다.
- **근거 그림 고르는 순서.** 위에서부터 내용에 맞는 첫 번째를 쓴다. 새 블록을 만들지 않고 이 파일의 `d0-sl-*` 차트 CSS나 근거 변형(`metric-list`·`bar-list`·`tiles`)을 그대로 쓴다.
  1. **같은 기준·0에서 시작하는 전/후 막대.** 값이 전/후 두 개뿐이고 크기 차이를 읽어야 할 때. `rect.d0-sl-bar` 두 개(지금 값만 `data-on`) + `line.d0-sl-axis` 기준선. 보조값 `18% → 5% · −13%p`를 해석 줄에 둘 수 있다.
  2. **slope·dumbbell.** 변화의 방향 자체가 핵심일 때. 두 점 `circle.d0-sl-bar`(지금 점만 `data-on`)를 `path.d0-sl-link`로 잇고 강조 선은 `data-on`이다.
  3. **line·sparkline.** 실제 시계열 값이 3개 이상일 때만 쓴다. 두 점으로 추세선을 긋지 않는다(두 점이면 1·2번). 선은 `path.d0-sl-link`, 마지막 점만 `data-on`.
  4. **100% 막대·점 격자.** "전체 중 몇 %"라는 구성비 자체가 핵심일 때. 트랙 `rect.d0-sl-total` 위에 `rect.d0-sl-bar[data-on]`(폭 = 비율), 또는 점 격자에서 해당 몫만 `circle.d0-sl-bar[data-on]`이고 나머지는 `circle.d0-sl-total`이다. 막대가 아니라 다른 모양이 필요하면 `bar-list` 구성비를 쓴다.
  5. **metric-list.** 서로 관련된 숫자가 여럿일 때. 그림 자리에 `figure[data-variant="metric-list"]`를 둔다. 이때 머리의 큰 숫자를 목록에 다시 쓰지 않는다(한 사실은 한 번).
- **값.** 그림의 값 라벨은 그림 라벨이라 머리 숫자와 같은 값이어도 반복으로 세지 않는다. 해석 줄은 숫자를 되풀이하지 않고 "그래서 무엇을 뜻하나"를 쓴다. 막대 높이·폭은 값에서 계산한다. 출처가 없으면 출처 줄을 지어내지 않고 뺀다.
- **좁은 화면.** 730px 미만에서는 비대칭 규칙대로 머리(제목 → 숫자 → 기준 줄) → 그림 → 발 1열이다. 숫자 48px, 기준 줄 15px.

```html
<section class="d0-slide" id="s-05" data-kind="stat" data-layout="asym" aria-labelledby="s-05-t" tabindex="-1">
  <header class="d0-slide__head">
    <h2 class="d0-slide__title" id="s-05-t">알림을 통째로 끄는 사람이 <b class="d0-slide__key">줄었다</b></h2>
    <p class="d0-slide__stat"><data value="5">5</data>%</p>
    <p class="d0-slide__base">출시 전 18%에서</p>
  </header>
  <figure class="d0-slide__fig">
    <svg viewBox="0 0 400 320" role="img" aria-labelledby="s-05-f">
      <title id="s-05-f">알림을 모두 끈 사용자 비율. 출시 전 18%, 출시 후 5%. 13%p 줄었다.</title>
      <line class="d0-sl-axis" x1="40" y1="260" x2="360" y2="260"/>
      <rect class="d0-sl-bar" x="72" y="60" width="96" height="200" rx="6"/>
      <rect class="d0-sl-bar" data-on x="232" y="204.4" width="96" height="55.6" rx="6"/>
      <g class="d0-sl-value" aria-hidden="true"><text x="120" y="46">18%</text><text x="280" y="190" data-on>5%</text></g>
      <g class="d0-sl-label" aria-hidden="true"><text x="120" y="296">출시 전</text><text x="280" y="296" data-on>출시 후</text></g>
    </svg>
    <figcaption class="d0-slide__note">끄는 비율이 출시 전의 3분의 1 아래로 내려왔다.</figcaption>
  </figure>
  <footer class="d0-slide__foot">
    <p class="d0-slide__src">출처: 내부 집계(합성)</p>
    <p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>5 / 9</p>
  </footer>
</section>
```

- 막대 높이: 기준선 y=260, 가장 큰 값(18%) = 200. 5%는 200 × 5 ÷ 18 ≈ 55.6이다. 값이 바뀌면 같은 식으로 다시 계산한다.
- 그림 열 SVG는 viewBox 400 폭(세로 300~360)을 쓴다. 1280 한 장 모드에서 글자 약 26px, 그림 비율 약 50%다.
- CSS는 기본 CSS의 "핵심 수치" 블록(`.d0-slide__stat`·`.d0-slide__base`)과 덱 강화 CSS의 "핵심 수치 기본형" 블록(비대칭 CSS 뒤)이다.

## 섹션 장 `data-kind="section"`

챕터를 넘길 때 한 번 숨을 고르는 장이다. 큰 번호(`02`)와 챕터 제목만 둔다.

- **언제.** 표지·목차 포함 8장 이상이고 챕터가 2~3개로 뚜렷할 때만 쓴다. 챕터마다 한 장이고, 한 챕터만 있으면 쓰지 않는다. 5~12장 상한에 섹션 장도 센다.
- **마크업.** 머리 안에 `p.d0-slide__index`(번호, `aria-hidden` 없이 글자로 둔다) → `h2.d0-slide__title`. 보조 한 줄(`__sub`)은 선택이다. 그림·요점·리드를 두지 않는다.
- **제목.** 챕터 이름이나 그 챕터가 답할 질문을 20자 안팎으로 쓴다. 표지·목차처럼 결론 제목 규칙의 예외다(제목만 읽기 검사에서 섹션 제목은 이어 읽기의 구분점으로 본다).
- **목차.** 섹션 장도 목차 `li`가 된다(`li` 수 = 표지·목차를 뺀 장 수 규칙 그대로). 섹션 항목 `li`에 `data-section`을 달면 굵게 보인다.
- **리듬.** 섹션 장은 구도 연속·밀도 리듬 계산에서 뺀다(목차처럼). Impact가 아니고 Impact 비율에도 들지 않는다.

```html
<section class="d0-slide" id="s-03" data-kind="section" data-surface="dark" aria-labelledby="s-03-t" tabindex="-1">
  <header class="d0-slide__head">
    <p class="d0-slide__index">01</p>
    <h2 class="d0-slide__title" id="s-03-t">왜 늦어지나</h2>
  </header>
  <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>3 / 10</p></footer>
</section>
```

## 진한 면 `data-surface="dark"`

장면을 바꿀 때만 쓰는 면이다. 내용을 담는 기본 배경이 아니다.

- **어디에.** `data-kind="cover"`·`"section"`·`"closing"` 장에만 단다. 근거·evidence·breakdown·screenshot·stat·assertion·summary 장, Impact 장, page에는 쓰지 않는다. 덱 Impact는 지금처럼 blue-light 면이다.
- **자리.** 표지는 진한 면의 기본 후보다. 마무리(closing)는 바로 앞 장이 Impact가 아닐 때만 진한 면으로 두고, 앞 장이 Impact면 흰 면으로 둔다. 섹션 장은 진하게 하면 그 덱의 섹션 장을 모두 같게 둔다.
- **몇 장.** 덱당 1~3장이다. 표지·마무리를 먼저 고르고 남는 몫만 섹션 장에 쓴다. 섹션 장을 모두 같게 두는 까닭은 챕터마다 면이 다르면 박자가 깨지기 때문이다. 그래서 섹션 장이 2개면 표지 + 섹션 2장, 또는 섹션 없이 표지·마무리다.
- **모양.** 슬라이드 전체 면이 `var(--d0-blue-dark)`이고 그림자가 없다. 제목·결론어·번호는 `#fff`, 보조 글자(eyebrow·리드·보조 줄·해석·출처·쪽번호·메타)는 `var(--d0-blue-light)`다. 구분선은 `color-mix(in srgb, #fff 32%, transparent)`다. 그라디언트·글래스·사진·패턴을 깔지 않는다.
- **글자.** 큰 글자 위주로 둔다. 작은 본문은 표지 요약 한 행과 closing 메타 정도로 줄인다.
- **대표 도식(표지).** 아래 덱 강화 CSS가 공용 도형(`d0-s-*`)과 덱 차트(`d0-sl-*`)를 자동으로 바꾼다. blue와 의미색(green·orange·red) 칠은 진한 면에 남지 않는다(blue 1.38:1). 강조는 채움/빈 모양 차이로 말한다.
  - 선·빈 노드·프레임 테두리·축은 blue-light, 강조(`data-on`) 노드·단계·선·막대·`d0-s-accent`는 흰색이다.
  - 의미 없는 자리·자리 표시 채움(`d0-s-fill`·`d0-s-track`·`d0-s-cell`·`d0-sl-total`, 화면 모형 속 글 줄 등)은 흰색 24% 면이다. `d0-s-zone`은 면 없이 blue-light 점선이다.
  - 선택·상태·구성 차이처럼 뜻이 있는 영역(`d0-s-key` 등)은 기존 토큰(blue-light·grey-300·흰색)만 쓴다. 임의 색·불투명도를 새로 만들지 않고, 그 뜻을 라벨이나 모양으로도 말한다. 진한 자리(`d0-s-key`) 기본은 grey-300이다.
  - 길이로 값을 말하는 막대(`d0-s-bar`·`d0-sl-bar`, 의미색 막대 포함)는 색 차이에 기대지 않고 모양으로 나눈다. 기준 막대(전·비교 대상)는 채움 없이 blue-light 2px 테두리(배경 4.94, 흰색 24% 트랙 위 3.08), 강조 막대(`data-on`, 지금)는 흰 채움(5.50, 트랙 위 3.43)이고 그 값 라벨(`text[data-on]`)은 흰색 굵은 글씨다.
    숫자 라벨이 있어도 막대는 배경과 트랙 모두에 3:1 이상이어야 한다. 낮은 대비는 뜻 없는 채움·구분선에만 허용한다. 값이 아닌 자리 표시(제목 줄 자리 등)에는 막대 클래스를 쓰지 않고 `d0-s-key`·`d0-s-fill`을 쓴다.
    예외: 비교가 아닌 진행 막대(시간 막대)는 단계 원 모양이 상태를 말하므로 트랙 blue-light 테두리, 지난 구간 blue-light 채움(4.94), 현재 구간 흰 채움(5.50)을 쓸 수 있다.
  - 번호(`d0-s-num`)는 빈 원 위 blue-light, 흰 원(`data-on`) 위 blue-dark(5.50)다. 흰 원 위 흰 숫자로 사라지지 않는다.
  - 의미색 원은 색이 남지 않으므로 원 안 기호와 라벨로 나눈다. 완료(`data-tone="green"`)는 흰 원 + blue-dark ✓(`d0-s-tick`), 실패·막힘(`red`)은 흰 테두리 원 + 흰 ×(`d0-s-stop` 두 획), 주의(`orange`)는 blue-light 테두리 원 + `!`(`text.d0-s-num`)다. 빈 원이나 흰 원만 두고 기호를 빼지 않는다. 막힘·주의는 원 옆에 상태 라벨(`막힘`·`주의`)을 함께 쓴다.
  - 진행 단계는 색이 아니라 채움·크기·링으로 나눈다. 완료 = 흰 원 + blue-dark ✓, 현재 = 한 단계 큰 빈 원(blue-dark 면 + 흰 테두리) + 바깥 흰 링(이중 링), 예정 = 작은 blue-light 테두리 빈 원이다(진행 막대 색은 위 값 막대 예외).
    진행 단계에서 ✓ 원 옆에 단계 이름이 있으면 `완료` 라벨은 따로 두지 않아도 된다. 대신 접근성 이름에 상태를 넣는다. 그림 `<title>`에 "탐색 완료"처럼 적고, 원에도 `<title>탐색 완료</title>`를 단다(`role="img"` 그림 안 도형은 보조 기술에 따로 읽히지 않으므로 그림 `<title>`이 기준이다).
  - 원 밖의 빨간 선·막힘 표시(`d0-s-stop`)는 흰색, 의미색 막대는 위 기준 막대처럼 테두리만이고 값·상태를 라벨로 적는다.
  - 라벨은 blue-light, 강조 라벨(`text[data-on]`)은 흰색이다. 배지(`.d0-pill`)는 면을 빼고 blue-light 테두리 + 흰 글자, 의미색 점은 흰색이다.
  - 덱에서 새로 만든 로컬 도형 클래스는 진한 면 색을 직접 정한다. 위 역할(선·빈 테두리 blue-light, 옅은 자리 흰색 24%, 진한 자리 grey-300, 강조 흰색, 흰 면 위 표식 blue-dark)을 따른다.
- **포커스.** 키보드 포커스(`:focus-visible`)일 때만 슬라이드 안쪽에 흰 링(2px, 오프셋 −8px, 5.50)을 그린다. 흰 면 장은 지금처럼 바깥 blue-dark 링(오프셋 4px)이다.
  스크립트는 키보드로 장을 넘길 때(←·→·Space·PageUp·PageDown·Home·End)와 사라지는 장 안 컨트롤(목차 링크 등)에 포커스가 있을 때만 새 장에 포커스를 준다.
  해시가 붙은 주소로 열거나 해시로 장을 옮길 때는 장을 보여 주기만 하고 포커스를 주지 않는다. 브라우저가 해시 대상 장에 스스로 준 포커스도 풀어 링이 생기지 않는다. 이전·다음 버튼은 포커스를 버튼에 둔다.

진한 면 대비(tokens.css 값으로 계산, 바탕 `var(--d0-blue-dark)`):

| 앞 | 비율 | 쓰는 곳 |
| --- | --- | --- |
| `#fff` | 5.50 | 제목·결론어·번호·강조 도형·강조 막대 채움(흰색 24% 트랙 위 3.43)·완료 흰 원·포커스 링(글자 AA 통과) |
| blue-light | 4.94 | 보조 글자·쪽번호·메타·선·빈 노드 테두리·배지 테두리(글자 AA 통과)·기준 막대 테두리(흰색 24% 트랙 위 3.08) |
| grey-100 | 4.82 | 쓸 수 있으나 기본은 blue-light |
| grey-200 | 4.35 | 18.66px/700 이상 큰 글자만 |
| grey-300 | 3.48 | 진한 자리(`d0-s-key`)만, 글자 금지. 값 막대 금지(흰색 24% 트랙 위 2.17) |
| 흰색 24% 면 | 1.61 | 옅은 자리(트랙·칸·채움)·구분선만. 뜻 없는 면이라 낮은 대비를 허용하고, 그 위 값 막대는 3:1 이상(기준 테두리 blue-light 3.08, 강조 채움 흰색 3.43) |
| blue-dark(흰 도형 위) | 5.50 | 흰 원 안 번호·체크 |
| blue | 1.38 | 금지 |
| grey-900 | 3.01 | 금지(진한 면 위 어두운 글자) |


## 그림 글자

덱 SVG 글자의 정본은 이 절이다. [diagram](diagram.md) 라벨 절의 글자 크기(`.d0-s-text` 14px, 560px 이하 20·22px)는 page(`.d0-page`) 전용이라 슬라이드 안에는 걸리지 않는다.

- **글자 클래스.** 덱 그림의 라벨·값·머리 글자는 `g.d0-sl-label`·`g.d0-sl-value`·`g.d0-sl-head` 안 `text`로 쓴다. 공용 도형 글자 `.d0-s-text`는 덱에서 쓰지 않는다.
- **크기는 `--sl-font` 하나.** 글자 크기는 viewBox 단위 `--sl-font`(기본 17px)로만 정하고, 커버·breakdown·가로형(800)·좁은 화면 규칙이 그림 단위로 이 값을 바꾼다(아래 CSS). SVG 안 `font-size` 속성이나 인라인 `style`은 쓰지 않는다.
- **번호·주의 표식.** 공용 도형의 번호와 주의 `!`(`text.d0-s-num`)도 슬라이드 안에서는 `--sl-font`를 따른다(`.d0-slide .d0-s-num`). 같은 그림의 라벨과 번호가 한 크기로 맞는다.
- **선 두께.** 공용 도형을 쓰는 덱은 슬라이드 SVG 도형(`path`·`circle`·`rect`·`line`)에 `vector-effect: non-scaling-stroke`를 걸어 그림 배율과 상관없이 화면 px 두께를 지킨다. 완료 체크선(`.d0-s-tick`)은 2.5px다(진한 면은 2px, 진한 면 절 CSS).
- **붙이는 조건.** 아래 CSS의 공용 도형 세 줄(선 두께·번호 글자·체크선)은 슬라이드에 `d0-s-*` 도형을 둔 덱에 붙인다. `d0-sl-*` 차트만 쓰는 덱에는 붙이지 않는다.
- **렌더 크기.** 렌더 글자 = `--sl-font` × SVG 렌더 폭 ÷ viewBox 폭이다. 1280에서 28px 이하, 320·375에서 11px 이상이다(덱 게이트).

## 근거 변형과 주석

evidence 장의 그림 자리(`figure.d0-slide__fig`)에는 SVG 차트 대신 공용 [evidence](evidence.md) 변형 하나를 둘 수 있다. figure에 `data-variant`를 달고 근거 요소를 그 안 첫 자식으로 둔다.

| `data-variant` | 근거 요소 | 언제 |
| --- | --- | --- |
| `metric-list` | `div.d0-mlist`(큰 숫자 + 짧은 라벨 세로 목록 + 옆 작은 차트) | 한 변화가 지표 2~4개에 함께 나타날 때 |
| `bar-list` | `ol.d0-barlist`(가로 막대 목록) | 같은 단위의 비율·구성(40/30/20/10%)을 견줄 때 |
| `tiles` | `dl.d0-tiles`(옅은 면 타일 4개 또는 6개) | 같은 단위·성격의 현황 지표를 훑을 때 |

- 그림 비율의 분자는 근거 요소(`.d0-mlist`·`.d0-barlist`·`.d0-tiles`)의 렌더 box다(screenshot의 `.d0-shot__screen`처럼). 근거 요소는 몸 행을 채운다.
- 근거 요소 안의 값·라벨 `dd`·`li`는 그림 라벨로 보고 장당 텍스트 줄 수·불릿 수에서 뺀다. metric-list의 작은 차트는 글자 없는 SVG라 글자 크기 게이트를 받지 않는다(`role="img"` + `<title>`은 둔다).
- **요약 근거 장(evidence overview).** 숫자 보고·성과 요약처럼 여러 지표를 동시에 봐야 가치가 있을 때만 `evidence` 장 + `metric-list` 변형으로 만든다. 새 종류·블록이 아니다. 오른쪽 차트(`svg.d0-mlist__chart`, 3fr 열)가 주인공이고 왼쪽 지표 2~4행은 보조다. 해석 한 줄과 출처 줄을 붙인다.
  지표를 카드·pill로 감싸지 않고, 글자를 덱 하한 아래로 줄여 밀도를 높이지 않는다. 덱당 1~2장 권장. 판정은 [덱 출력](../output/deck.md)의 요약 근거 장 규칙.
- **주석(annotation).** 그림 위 번호 표식 + 짧은 주석은 [diagram](diagram.md) annotate 변형이다. 덱에서는 근거 split의 요점 열 자리에 `ol.d0-annot__notes`(2~3개, 한 줄씩)를 두고, 그림 `figure.d0-slide__fig` 안에 `div.d0-annot`(SVG + 번호 `span.d0-pin`)을 둔다. 주석 `li`는 불릿으로 센다. 주석 SVG는 높이를 내용대로 두므로 viewBox 400×240처럼 세로 비율을 0.6 안팎으로 그려 split 하한 45%를 맞춘다(400×200이면 1280에서 약 41%).

## 언제 쓰나

- 출력 형식이 덱일 때만 쓴다. 패턴 8개 모두 덱으로 낼 수 있다. 문서형 page 안에 슬라이드 한 장을 끼워 넣지 않는다(그건 diagram + section-head다).
- 슬라이드 수는 표지·목차를 포함해 5~12장이다. 넘으면 덱을 나눈다.

## 스니펫

아래 HTML·CSS·JS를 그대로 모으면 9장짜리 샘플 덱이 된다(근거 split 1, impact 2장 = 22%).

```html
<main class="d0-deck" data-pattern="report" data-variant="status">
  <section class="d0-slide" id="s-01" data-kind="cover" data-cover="side" aria-labelledby="s-01-t" tabindex="-1">
    <div class="d0-slide__cover"><header class="d0-slide__head">
      <p class="d0-slide__eyebrow">알림 개편 · 3분기 업무 보고</p>
      <h1 class="d0-slide__title" id="s-01-t">알림 개편은 일정대로 가고, 남은 결정은 발송 주기 하나다</h1>
      <p class="d0-slide__lead">재시도만 줄이면 주기는 어느 쪽이든 괜찮다</p>
    </header><figure class="d0-slide__fig"><svg viewBox="0 0 400 220" role="img" aria-label="마지막 주에 재시도가 늘었다"><title>마지막 주에 재시도가 늘었다</title><rect class="d0-sl-bar" x="60" y="110" width="80" height="70"/><rect class="d0-sl-bar" data-on x="250" y="40" width="80" height="140"/><g class="d0-sl-label"><text x="100" y="208">첫 주</text><text x="290" y="208">마지막 주</text></g></svg><figcaption class="d0-slide__note">마지막 주에 재시도가 몰렸다.</figcaption></figure></div>
    <dl class="d0-slide__summary"><div><dt>결정할 것</dt><dd>발송 주기를 매일과 매주 중에 고른다</dd></div></dl>
    <footer class="d0-slide__foot">
      <p class="d0-slide__src"><kbd>←</kbd> <kbd>→</kbd> 키로 넘겨요 · <kbd>F</kbd> 전체 화면</p>
      <p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>1 / 9</p>
    </footer>
  </section>

  <nav class="d0-slide" id="s-02" data-kind="toc" aria-labelledby="s-02-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-02-t">제목만 읽기</h2></header>
    <ul class="d0-slide__toc">
      <li><a href="#s-03">재시도를 줄이지 않으면 발송 주기를 바꿔도 늦어진다</a></li>
      <li><a href="#s-04">재시도는 앞 세 주보다 마지막 주에 몰렸다</a></li>
      <li><a href="#s-05">재시도가 4주 만에 두 배 넘게 늘었다</a></li>
      <li><a href="#s-06">늦은 알림은 설정 화면의 주기 선택에서 갈린다</a></li>
      <li><a href="#s-07">재시도의 절반 넘게가 대기열에서 생긴다</a></li>
      <li><a href="#s-08">늦게 도착하는 알림이 절반에 가깝다</a></li>
      <li><a href="#s-09">이번 주 안에 발송 주기를 정해 주세요</a></li>
    </ul>
  </nav>

  <!-- assertion + impact: 주장 한 문장만 -->
  <section class="d0-slide" id="s-03" data-kind="assertion" data-emphasis="impact" aria-labelledby="s-03-t" tabindex="-1">
    <header class="d0-slide__head">
      <h2 class="d0-slide__title" id="s-03-t">재시도를 줄이지 않으면 발송 주기를 바꿔도 늦어진다</h2>
    </header>
    <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>3 / 9</p></footer>
  </section>

  <!-- 근거(종류 생략): 그림 + 요점 split, 무대 없음 -->
  <section class="d0-slide" id="s-04" aria-labelledby="s-04-t" tabindex="-1">
    <header class="d0-slide__head">
      <h2 class="d0-slide__title" id="s-04-t">재시도는 앞 세 주보다 마지막 주에 몰렸다</h2>
    </header>
    <div class="d0-slide__body" data-layout="split">
      <figure class="d0-slide__fig">
        <svg viewBox="0 0 400 200" role="img" aria-labelledby="s-04-f">
          <title id="s-04-f">주별 재시도 건수. 1주 120건, 2주 135건, 3주 180건, 4주 260건.</title>
          <line class="d0-sl-axis" x1="24" y1="168" x2="376" y2="168"/>
          <rect class="d0-sl-bar" x="44" y="108" width="48" height="60" rx="4"/>
          <rect class="d0-sl-bar" x="132" y="100.5" width="48" height="67.5" rx="4"/>
          <rect class="d0-sl-bar" x="220" y="78" width="48" height="90" rx="4"/>
          <rect class="d0-sl-bar" data-on x="308" y="38" width="48" height="130" rx="4"/>
          <g class="d0-sl-value" aria-hidden="true">
            <text x="68" y="100">120</text><text x="156" y="92">135</text><text x="244" y="70">180</text><text x="332" y="30" data-on>260</text>
          </g>
          <g class="d0-sl-label" aria-hidden="true">
            <text x="68" y="190">1주</text><text x="156" y="190">2주</text><text x="244" y="190">3주</text><text x="332" y="190">4주</text>
          </g>
        </svg>
        <figcaption class="d0-slide__note">늘어난 몫은 대부분 마지막 주에 몰렸다.</figcaption>
      </figure>
      <ul class="d0-slide__points">
        <li>앞 세 주는 조금씩 늘었다</li>
        <li>재시도가 쌓이면 알림 도착이 늦어진다</li>
      </ul>
    </div>
    <footer class="d0-slide__foot">
      <p class="d0-slide__src">주별 재시도 건수, 팀 A 기준 · 출처: 발송 기록 집계(합성)</p>
      <p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>4 / 9</p>
    </footer>
  </section>

  <!-- evidence: 결론 제목 + 가로형 차트 + 해석 한 줄 -->
  <section class="d0-slide" id="s-05" data-kind="evidence" aria-labelledby="s-05-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-05-t">재시도가 4주 만에 두 배 넘게 늘었다</h2></header>
    <figure class="d0-slide__fig">
      <svg viewBox="0 0 800 320" role="img" aria-labelledby="s-05-f">
        <title id="s-05-f">주별 재시도 건수 막대. 1주 110건, 2주 125건, 3주 170건, 4주 250건. 4주가 1주의 두 배를 넘는다.</title>
        <line class="d0-sl-axis" x1="40" y1="250" x2="760" y2="250"/>
        <rect class="d0-sl-bar" x="88" y="166.4" width="96" height="83.6" rx="6"/>
        <rect class="d0-sl-bar" x="268" y="155" width="96" height="95" rx="6"/>
        <rect class="d0-sl-bar" x="448" y="120.8" width="96" height="129.2" rx="6"/>
        <rect class="d0-sl-bar" data-on x="628" y="60" width="96" height="190" rx="6"/>
        <g class="d0-sl-value" aria-hidden="true">
          <text x="136" y="152">110</text><text x="316" y="141">125</text><text x="496" y="107">170</text><text x="676" y="46" data-on>250</text>
        </g>
        <g class="d0-sl-label" aria-hidden="true">
          <text x="136" y="296">1주</text><text x="316" y="296">2주</text><text x="496" y="296">3주</text><text x="676" y="296">4주</text>
        </g>
      </svg>
      <figcaption class="d0-slide__note">지금 속도면 다음 달 재시도가 발송량을 넘는다.</figcaption>
    </figure>
    <footer class="d0-slide__foot">
      <p class="d0-slide__src">출처: 발송 기록 집계(합성)</p>
      <p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>5 / 9</p>
    </footer>
  </section>

  <!-- screenshot: figure.d0-shot 안쪽 마크업·CSS는 mockup-frame.md -->
  <section class="d0-slide" id="s-06" data-kind="screenshot" aria-labelledby="s-06-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-06-t">늦은 알림은 설정 화면의 주기 선택에서 갈린다</h2></header>
    <figure class="d0-shot">
      <div class="d0-shot__screen">
        <svg viewBox="0 0 320 200" role="img" aria-labelledby="s-06-f">
          <title id="s-06-f">알림 설정 화면. 위에 받을 알림 목록, 가운데에 발송 주기 선택 칸, 아래에 저장 버튼이 있다.</title>
          <rect class="d0-sl-total" x="20" y="20" width="180" height="14" rx="4"/>
          <rect class="d0-sl-total" x="20" y="46" width="280" height="10" rx="3"/>
          <rect class="d0-sl-total" x="20" y="64" width="240" height="10" rx="3"/>
          <rect class="d0-sl-bar" x="28" y="92" width="64" height="28" rx="6"/>
          <rect class="d0-sl-bar" data-on x="100" y="92" width="64" height="28" rx="6"/>
          <rect class="d0-sl-total" x="20" y="150" width="88" height="26" rx="6"/>
        </svg>
        <span class="d0-shot__spot" data-dim style="--x:6%;--y:42%;--w:48%;--h:20%" aria-hidden="true"><b class="d0-shot__num">1</b></span>
      </div>
      <p class="d0-shot__note"><b class="d0-shot__num">1</b>가운데 주기 칸에서 매일과 매주가 갈린다.</p>
      <figcaption>설정 화면의 발송 주기 칸만 밝게 남겼다.</figcaption>
    </figure>
    <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>6 / 9</p></footer>
  </section>

  <!-- breakdown: 전체 → 구성 요소, 지금 말하는 부품만 blue -->
  <section class="d0-slide" id="s-07" data-kind="breakdown" aria-labelledby="s-07-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-07-t">재시도의 절반 넘게가 대기열에서 생긴다</h2></header>
    <figure class="d0-slide__fig">
      <svg viewBox="0 0 800 320" role="img" aria-labelledby="s-07-f">
        <title id="s-07-f">4주 차 재시도 250건의 구성. 대기열 지연 140건, 형식 오류 70건, 기타 40건.</title>
        <g class="d0-sl-head" aria-hidden="true"><text x="40" y="30">전체 250건</text></g>
        <rect class="d0-sl-total" x="40" y="48" width="720" height="44" rx="6"/>
        <path class="d0-sl-link" d="M40 92 L40 150 M760 92 L760 150"/>
        <rect class="d0-sl-bar" data-on x="40" y="150" width="398" height="44" rx="6"/>
        <rect class="d0-sl-bar" x="446" y="150" width="194" height="44" rx="6"/>
        <rect class="d0-sl-bar" x="648" y="150" width="112" height="44" rx="6"/>
        <g class="d0-sl-label" aria-hidden="true">
          <text x="239" y="244">대기열 지연</text><text x="543" y="244">형식 오류</text><text x="704" y="244">기타</text>
        </g>
        <g class="d0-sl-value" aria-hidden="true">
          <text x="239" y="292" data-on>140</text><text x="543" y="292">70</text><text x="704" y="292">40</text>
        </g>
      </svg>
      <figcaption class="d0-slide__note">대기열 하나만 고쳐도 재시도가 절반 아래로 준다.</figcaption>
    </figure>
    <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>7 / 9</p></footer>
  </section>

  <!-- 순수 Impact stat(예외형): 숫자 자체가 결론일 때만. 기본형(숫자 + 근거 그림)은 위 핵심 수치 절 -->
  <section class="d0-slide" id="s-08" data-kind="stat" data-emphasis="impact" aria-labelledby="s-08-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-08-t">늦게 도착하는 알림이 절반에 가깝다</h2></header>
    <figure class="d0-slide__fig">
      <p class="d0-slide__stat"><data value="47">47</data>%<span class="d0-slide__base">지난달 35%에서</span></p>
      <figcaption class="d0-slide__note">10분 넘게 늦은 알림의 비율 · 한 달 사이 12%p 늘었다</figcaption>
    </figure>
    <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>8 / 9</p></footer>
  </section>

  <section class="d0-slide" id="s-09" data-kind="closing" data-closing="decision" aria-labelledby="s-09-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-09-t">이번 주 안에 발송 주기를 정해 주세요</h2></header>
    <dl class="d0-slide__meta"><div><dt>담당</dt><dd>서비스 운영 팀</dd></div><div><dt>기한</dt><dd>이번 주 금요일</dd></div><div><dt>다음</dt><dd>다음 주에 적용한다</dd></div></dl>
    <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>9 / 9</p></footer>
  </section>

  <!-- 한 장 모드 네비: 마크업에 두고 CSS가 data-mode="single"일 때만 보인다 -->
  <nav class="d0-deck__nav" aria-label="슬라이드 넘기기">
    <button type="button" class="d0-deck__btn" data-deck="prev" aria-label="이전 장">
      <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>
    </button>
    <p class="d0-deck__count" aria-live="polite"><span class="d0-sr-only">쪽 </span><span data-deck-now>1</span> / <span data-deck-total>9</span></p>
    <button type="button" class="d0-deck__btn" data-deck="next" aria-label="다음 장">
      <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>
    </button>
    <button type="button" class="d0-deck__btn" data-deck="toc">목차</button>
    <p class="d0-deck__hint"><span data-hint="key">←/→로 넘겨요</span><span data-hint="touch">밀어서 넘겨요</span></p>
  </nav>
</main>
```

```css
/* shell.md 기본값(토큰 인라인, color-scheme, box-sizing, body 글꼴·keep-all, .d0-sr-only, :focus-visible, reduced-motion)은 그대로 쓴다.
   덱 페이지는 .d0-page 대신 .d0-deck을 쓰고, body 배경만 grey-100으로 바꿔 흰 슬라이드 면이 보이게 한다. */
body { background: var(--d0-grey-100); }
.d0-deck {
  container-type: inline-size;              /* 세로 나열에서 슬라이드 폭 = 덱 안쪽 폭 */
  display: grid; gap: 40px;
  max-width: 1200px; margin: 0 auto; padding: 40px 32px 96px;
}
.d0-deck__nav { display: none; }            /* 한 장 모드에서만 보인다 */
.d0-slide {
  container-type: inline-size;              /* 안쪽 글자의 cqi = 슬라이드 안쪽 폭 */
  aspect-ratio: 16 / 9;
  display: grid; grid-template-rows: auto minmax(0, 1fr) auto; gap: 2.4cqi;
  padding: 4.5cqi 5cqi 3cqi;
  overflow: hidden;
  background: #fff; border-radius: var(--d0-radius-card); box-shadow: var(--d0-shadow-card);
  scroll-margin-top: 24px;
}
.d0-slide:focus { outline: none; }
.d0-slide:focus-visible { outline: 2px solid var(--d0-blue-dark); outline-offset: 4px; }

/* 머리 */
.d0-slide__head { display: grid; gap: 0.8cqi; align-content: start; }
.d0-slide__eyebrow { margin: 0; color: var(--d0-grey-600); font-size: 1.4cqi; font-weight: 600; }
.d0-slide__title {
  margin: 0; color: var(--d0-grey-900);
  font-size: 3.6cqi; font-weight: 700;
  line-height: var(--d0-leading-title); letter-spacing: var(--d0-tracking-title);
  text-wrap: balance;
}
h1.d0-slide__title { font-size: 5.6cqi; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
.d0-slide__sub { margin: 0; color: var(--d0-grey-600); font-size: 2cqi; }
.d0-slide__lead { margin: 0; color: var(--d0-grey-700); font-size: 2.4cqi; line-height: var(--d0-leading-body); }

/* 몸: 그림 하나. 무대는 기본 없음 */
.d0-slide__fig { margin: 0; min-height: 0; display: grid; grid-template-rows: minmax(0, 1fr) auto; gap: 1.2cqi; }
.d0-slide__fig svg { display: block; justify-self: center; width: 100%; max-width: 42cqi; height: 100%; max-height: 100%; min-height: 0; overflow: visible; }
.d0-slide__stage {                          /* 선택: 흰 면 위에서 그림 경계가 흐려질 때만 */
  min-height: 0; display: grid; place-items: center;
  padding: 2.4cqi; background: var(--d0-grey-50); border-radius: var(--d0-radius-card);
}
.d0-slide__note { margin: 0; color: var(--d0-grey-600); font-size: 2cqi; }

.d0-slide__body[data-layout="split"] { min-height: 0; display: grid; grid-template-columns: 3fr 2fr; gap: 3cqi; align-items: center; }
.d0-slide__body[data-layout="split"] > .d0-slide__fig { height: 100%; }
.d0-slide__body[data-layout="split"] > .d0-slide__fig svg { max-width: 100%; } /* split: 그림 열을 채운다 */
@container (min-width: 731px) {
  .d0-slide__body[data-layout="split"] > .d0-slide__fig svg[viewBox^="0 0 400 "] { --sl-font: 15px; } /* 넓어진 split 그림: 15 × 637 ÷ 400 ≈ 24px(28px 상한 여유) */
}
.d0-slide__points { margin: 0; padding-left: 1.2em; list-style: disc; display: grid; gap: 1.2cqi; align-content: center; color: var(--d0-grey-800); font-size: 2cqi; line-height: var(--d0-leading-body); }
.d0-slide__points ::marker { color: var(--d0-blue); }

/* 커버: 내용의 모양에 따라 그림 위치와 비율을 달리한다 */
.d0-slide[data-kind="cover"] { grid-template-rows: minmax(0, 1fr) auto auto; }
.d0-slide__cover { min-height: 0; display: grid; grid-template-columns: 3fr 2fr; gap: 3cqi; align-items: center; }
.d0-slide__cover > .d0-slide__fig { height: 100%; align-content: center; }
.d0-slide__cover .d0-slide__fig svg { height: auto; max-height: 100%; }
.d0-slide[data-cover="contrast"] .d0-slide__cover,
.d0-slide[data-cover="bottom"] .d0-slide__cover,
.d0-slide[data-cover="center"] .d0-slide__cover { grid-template-columns: 1fr; grid-template-rows: auto minmax(0, 1fr); gap: 2cqi; }
.d0-slide:is([data-cover="contrast"], [data-cover="bottom"], [data-cover="center"]) .d0-slide__fig { --sl-font: 20px; }
.d0-slide:is([data-cover="contrast"], [data-cover="bottom"], [data-cover="center"]) .d0-slide__fig svg { max-width: 84cqi; }
.d0-slide[data-cover="center"] .d0-slide__head { max-width: 76cqi; justify-self: center; text-align: center; }
.d0-deck[data-pattern="preview"] .d0-slide__cover { grid-template-columns: 5fr 4fr; }
.d0-deck[data-pattern="report"] .d0-slide__cover { grid-template-columns: 5fr 4fr; }
.d0-deck[data-pattern="report"] .d0-slide__cover .d0-slide__fig { --sl-font: 24px; }
.d0-slide[data-cover="map"] .d0-slide__cover { grid-template-columns: 2fr 1fr; }
.d0-slide[data-cover="map"] .d0-slide__cover > .d0-slide__fig { height: auto; align-self: end; }
/* side(생략 포함): 그림과 해석 줄을 한 묶음으로 세로 가운데. 1fr 행이면 해석 줄만 아래로 떨어진다 */
.d0-slide:is([data-cover="side"], [data-kind="cover"]:not([data-cover])) .d0-slide__cover > .d0-slide__fig { grid-template-rows: auto auto; } /* side는 작은 그림 전용(가로로 긴 도식은 bottom 등으로) */
@container (min-width: 731px) {
  .d0-slide[data-cover="map"] .d0-slide__fig svg[viewBox^="0 0 800 "] { --sl-font: 30px; } /* 안전망: 좁은 지도 열(약 370px)에서 30 × 370 ÷ 800 ≈ 14px. 기본은 400 폭 표지용 지도 */
}
.d0-slide[data-kind="cover"] .d0-slide__summary > div { padding: 0.8cqi 0; }
.d0-slide[data-kind="cover"] .d0-slide__summary dd { font-size: 1.4cqi; }

/* 표지: 남길 결정 한 행 */
.d0-slide__summary { margin: 0; align-self: center; display: grid; }
.d0-slide__summary > div { display: grid; grid-template-columns: 14cqi 1fr; gap: 2cqi; align-items: baseline; padding: 1.4cqi 0; border-top: 1px solid var(--d0-grey-100); }
.d0-slide__summary > div:last-child { border-bottom: 1px solid var(--d0-grey-100); }
.d0-slide__summary dt { color: var(--d0-grey-600); font-size: 1.4cqi; font-weight: 600; }
.d0-slide__summary dd { margin: 0; color: var(--d0-grey-900); font-size: 2cqi; }
.d0-slide__summary > div:last-child dt { color: var(--d0-blue-dark); }

/* 제목 목차: 작은 점 불렛 + 제목 링크 */
.d0-slide__toc { margin: 0; padding: 0; list-style: none; align-self: start; display: grid; gap: 0.2cqi; }
.d0-slide__toc li { display: grid; grid-template-columns: 0.4cqi minmax(0, 1fr); align-items: baseline; column-gap: 1.2cqi; }
.d0-slide__toc li::before { content: ""; width: 0.4cqi; height: 0.4cqi; align-self: center; border-radius: 50%; background: var(--d0-blue); }
.d0-slide__toc a {
  display: block; min-height: 24px; padding: 0.5cqi 0;
  color: var(--d0-grey-900); font-size: 2cqi; text-decoration: none;
  border-bottom: 1px solid var(--d0-grey-100);
}
.d0-slide__toc a:hover { color: var(--d0-blue-dark); }

/* assertion: 주장 한 문장을 세로 가운데에 */
.d0-slide[data-kind="assertion"] { grid-template-rows: minmax(0, 1fr) auto; }
.d0-slide[data-kind="assertion"] .d0-slide__head { align-self: center; gap: 2cqi; }
.d0-slide[data-kind="assertion"] .d0-slide__title { font-size: 6cqi; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }

/* evidence·breakdown: 가로형 차트가 몸을 채운다 */
.d0-slide[data-kind="evidence"] .d0-slide__fig,
.d0-slide[data-kind="breakdown"] .d0-slide__fig { --sl-font: 20px; }
.d0-slide[data-kind="evidence"] .d0-slide__fig svg,
.d0-slide[data-kind="breakdown"] .d0-slide__fig svg { max-width: 84cqi; }
.d0-slide[data-kind="evidence"] .d0-slide__note,
.d0-slide[data-kind="breakdown"] .d0-slide__note { justify-self: center; color: var(--d0-grey-800); }

/* screenshot: 슬라이드 안 자리와 크기만. 화면·spot·dim·번호는 mockup-frame.md
   덱 격자: 화면 열이 몸 높이를 채우고 주석·캡션은 오른쪽 열. mockup-frame의 560px 상한·900px 2열(page 전용)을 덮는다 */
.d0-slide[data-kind="screenshot"] .d0-shot {
  min-height: 0; height: 100%;
  grid-template-columns: max-content minmax(0, 1fr); grid-template-rows: repeat(3, auto) minmax(0, 1fr); align-content: stretch;
}
.d0-slide[data-kind="screenshot"] .d0-shot :is(.d0-shot__note, figcaption) { grid-column: 2; }
.d0-slide[data-kind="screenshot"] .d0-shot__screen {
  grid-column: 1; grid-row: 1 / -1;
  height: 100%; min-height: 0; max-width: 100%; justify-self: start;
  aspect-ratio: 16 / 10;                    /* 화면 비율이 다르면 style="aspect-ratio: 1280 / 720"처럼 이미지 비율을 적는다 */
}
.d0-slide[data-kind="screenshot"] .d0-shot__note,
.d0-slide[data-kind="screenshot"] .d0-shot figcaption { font-size: 2cqi; }

/* 핵심 수치 */
.d0-slide__stat {
  margin: 0; align-self: center; justify-self: start;
  color: var(--d0-blue-dark); font-size: 10cqi; font-weight: 600;
  line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display);
  font-variant-numeric: tabular-nums;
}
.d0-slide[data-kind="stat"] .d0-slide__fig:has(> .d0-slide__stat) { grid-template-rows: 1fr auto; align-content: center; } /* 순수 Impact stat: 숫자가 그림 자리 */
.d0-slide[data-kind="stat"] .d0-slide__note { color: var(--d0-grey-800); }
/* 기준 줄: 숫자를 읽게 하는 비교 기준·분모·기간. 기본형은 숫자 아래 p, 순수 Impact stat은 숫자 옆 span */
.d0-slide__base { margin: 0; color: var(--d0-grey-700); font-size: 2cqi; font-weight: 400; line-height: var(--d0-leading-body); letter-spacing: normal; font-variant-numeric: tabular-nums; }
.d0-slide__stat > .d0-slide__base { display: inline-block; margin-left: 1.6cqi; vertical-align: baseline; }  /* 순수 Impact stat: 숫자 옆 작은 기준 글자 */

/* closing(decision·request·action·criteria·takeaway 공통): 세로 중앙의 큰 문장 하나 + 디바이더 아래 작은 사실 행 */
.d0-slide[data-kind="closing"] { grid-template-rows: minmax(0, 1fr) auto auto; }
.d0-slide[data-kind="closing"] .d0-slide__head { align-self: center; max-width: 88cqi; }
.d0-slide[data-kind="closing"] .d0-slide__title { font-size: 5cqi; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); } /* 섹션 제목(4.5cqi)보다 한 단계 크게, 표지 h1(5.6cqi)보다는 작게 */
.d0-slide__meta { margin: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2.4cqi; padding-top: 1.4cqi; border-top: 1px solid var(--d0-grey-200); }
.d0-slide__meta > div { display: grid; gap: 0.4cqi; align-content: start; }
.d0-slide__meta dt { color: var(--d0-grey-600); font-size: 1.4cqi; }
.d0-slide__meta dd { margin: 0; color: var(--d0-grey-700); font-size: 1.4cqi; line-height: var(--d0-leading-body); }

/* summary: 참고용 정리 목록 */
.d0-slide[data-kind="summary"] .d0-slide__points { align-self: start; }

/* 강조: impact = blue-light 전체 면, 큰 것 하나 */
.d0-slide[data-emphasis="impact"] { background: var(--d0-blue-light); box-shadow: none; }
.d0-slide[data-emphasis="impact"] .d0-slide__title { font-size: 6cqi; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
/* 그림·숫자가 있는 Impact(screenshot·evidence·breakdown·근거·stat)는 일반 제목. 순수 Impact(assertion)만 6cqi */
.d0-slide[data-emphasis="impact"]:has(.d0-slide__fig, .d0-shot) .d0-slide__title { font-size: 3.6cqi; line-height: var(--d0-leading-title); letter-spacing: var(--d0-tracking-title); }
.d0-slide[data-emphasis="impact"] :is(.d0-slide__sub, .d0-slide__lead, .d0-slide__note, .d0-slide__src, .d0-slide__num, .d0-slide__eyebrow) { color: var(--d0-grey-700); }
.d0-slide[data-emphasis="quiet"] .d0-slide__title { font-weight: 600; }

/* 발: 출처 + 쪽수 */
.d0-slide__foot { display: flex; justify-content: space-between; align-items: baseline; gap: 2cqi; }
.d0-slide__src { margin: 0; color: var(--d0-grey-600); font-size: 1.4cqi; }
.d0-slide__num { margin: 0 0 0 auto; color: var(--d0-grey-600); font-size: 1.4cqi; font-variant-numeric: tabular-nums; }
.d0-slide kbd {
  display: inline-block; min-width: 1.6em; padding: 0 0.4em;
  border: 1px solid var(--d0-grey-300); border-radius: var(--d0-radius-sm);
  font: inherit; text-align: center; color: var(--d0-grey-800);
}

/* SVG 차트: 강조 계열 하나만 blue. 글자 크기는 --sl-font */
.d0-sl-axis, .d0-sl-link { fill: none; stroke: var(--d0-grey-300); stroke-width: 1.5; stroke-linecap: round; }
.d0-sl-bar { fill: var(--d0-grey-400); }
.d0-sl-bar[data-on] { fill: var(--d0-blue); }
.d0-sl-total { fill: var(--d0-grey-200); }
.d0-sl-value text, .d0-sl-label text, .d0-sl-head text { font-family: var(--d0-font); font-size: var(--sl-font, 17px); text-anchor: middle; font-variant-numeric: tabular-nums; }
.d0-sl-value text { fill: var(--d0-grey-700); font-weight: 600; }
.d0-sl-value text[data-on] { fill: var(--d0-blue-dark); }
.d0-sl-label text { fill: var(--d0-grey-600); }
.d0-sl-label text[data-on] { fill: var(--d0-blue-dark); font-weight: 600; }
.d0-sl-head text { fill: var(--d0-grey-800); font-weight: 600; text-anchor: start; }
/* 공용 도형(d0-s-*, diagram.md 공용 CSS)을 Impact 장에 둘 때: blue-light 위 grey-500 선은 3:1 미달이라 한 단계 진하게 */
.d0-slide[data-emphasis="impact"] :is(.d0-s-edge, .d0-s-node, .d0-s-step, .d0-s-frame):not([data-on]):not([data-tone]) { stroke: var(--d0-grey-600); }
/* 공용 도형(d0-s-*)을 슬라이드에 둔 덱만(그림 글자 절): 선은 화면 px 두께, 번호·주의 ! 글자는 --sl-font */
.d0-slide svg :is(path, circle, rect, line) { vector-effect: non-scaling-stroke; }
.d0-slide .d0-s-num { font-size: var(--sl-font, 17px); }
.d0-slide .d0-s-tick { stroke-width: 2.5; }

/* 네비 */
.d0-deck__nav { align-items: center; gap: 8px; min-height: 44px; }
.d0-deck__btn {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 44px; height: 44px; padding: 0 14px;
  border: 0; border-radius: var(--d0-radius-control);
  background: #fff; color: var(--d0-grey-800); font-size: 15px; font-weight: 600;
}
.d0-deck__btn:hover { color: var(--d0-blue-dark); }
.d0-deck__btn[aria-disabled="true"] { color: var(--d0-grey-400); cursor: default; }
.d0-deck__btn svg { width: 18px; height: 18px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.d0-deck__count { min-width: 64px; margin: 0; text-align: center; color: var(--d0-grey-800); font-size: 15px; font-weight: 600; font-variant-numeric: tabular-nums; }
.d0-deck__hint { margin: 0 0 0 auto; color: var(--d0-grey-700); font-size: 13px; white-space: nowrap; }
.d0-deck__hint [data-hint="touch"] { display: none; }
@media (hover: none) and (pointer: coarse) {
  .d0-deck__hint [data-hint="key"] { display: none; }
  .d0-deck__hint [data-hint="touch"] { display: inline; }
  .d0-slide__src:has(kbd) { display: none; }  /* 표지의 키 안내: 터치에서는 네비 '밀어서 넘겨요'가 대신한다 */
}

/* 한 장 모드: JS가 data-mode="single"을 붙일 때만. 화면에서만 걸고 인쇄는 세로 나열로 돌아간다 */
@media screen {
  html:has(.d0-deck[data-mode="single"]) { overflow: hidden; scrollbar-gutter: auto; }
  .d0-deck[data-mode="single"] {
    --deck-gutter: 32px;
    --deck-chrome: 88px;                 /* 위 16 + 네비 44 + 사이 12 + 아래 16 */
    /* 높이로는 730px 아래로 줄이지 않는다(그 아래는 16:9가 풀려 장 안에서 스크롤한다) */
    --slide-w: min(100vw - 2 * var(--deck-gutter), max((100dvh - var(--deck-chrome)) * 16 / 9, 730px));
    max-width: none; height: 100vh; height: 100dvh; margin: 0;
    padding: 16px var(--deck-gutter);
    grid-template-rows: minmax(0, 1fr) auto; grid-template-columns: minmax(0, 1fr);
    justify-items: center; align-items: center; gap: 12px;
    overflow: hidden; touch-action: pan-y;
  }
  .d0-deck[data-mode="single"] > .d0-slide {
    grid-area: 1 / 1; width: var(--slide-w);
    max-height: calc(100dvh - var(--deck-chrome));
    overflow-x: hidden; overflow-y: auto; overscroll-behavior: contain; touch-action: pan-y;
  }
  .d0-deck[data-mode="single"] > .d0-slide:not([data-active]) { display: none; }
  .d0-deck[data-mode="single"] > .d0-slide[data-active] { animation: d0-deck-in var(--d0-dur-fast) var(--d0-ease); }
  .d0-deck[data-mode="single"] .d0-slide__num { display: none; }  /* 네비 쪽수가 대신한다 */
  /* 키 작은 창(높이로 줄인 폭이 730px 아래): 폭은 730px에서 멈추고 16:9를 풀어 장 안에서 세로로 스크롤한다 */
  @media (max-height: 498px) {
    .d0-deck[data-mode="single"] > .d0-slide { aspect-ratio: auto; }
    .d0-slide, .d0-slide[data-kind="cover"] { grid-template-rows: repeat(3, max-content); }  /* 몸을 내용 높이로 둬 그림을 줄이지 않는다 */
  }
  .d0-deck[data-mode="single"] > .d0-deck__nav { grid-row: 2; display: flex; width: var(--slide-w); }
  /* 넓은 덱: 패딩·간격을 슬라이드 폭 기준으로 다시 잰다(덱 폭 ≠ 슬라이드 폭) */
  @container (min-width: 731px) {
    .d0-deck[data-mode="single"] > .d0-slide {
      padding: calc(var(--slide-w) * 0.045) calc(var(--slide-w) * 0.05) calc(var(--slide-w) * 0.03);
      gap: calc(var(--slide-w) * 0.024);
    }
  }
  @media (max-width: 640px) {
    .d0-deck[data-mode="single"] {
      --deck-gutter: 16px;
      --deck-chrome: 76px;               /* 위 12 + 네비 44 + 사이 8 + 아래 12 */
      padding: 12px var(--deck-gutter); gap: 8px; align-items: start;
    }
    .d0-deck[data-mode="single"] > .d0-deck__nav { gap: 4px; }   /* 320에서도 안내가 한 줄에 들어가게 */
    .d0-deck__count { min-width: 48px; }
  }
}
@keyframes d0-deck-in { from { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .d0-deck[data-mode="single"] > .d0-slide[data-active] { animation: none; transition: none; }
}

/* 좁은 슬라이드(730px 미만, 본문이 11px 아래로 내려가는 폭): 16:9를 풀고 px 고정 */
@container (max-width: 730px) {
  .d0-slide { aspect-ratio: auto; grid-template-rows: repeat(3, max-content); gap: 16px; padding: 20px 16px 14px; }  /* 몸은 내용 높이: 긴 장은 그림을 줄이지 않고 장 안에서 스크롤 */
  .d0-slide[data-kind="cover"] { grid-template-rows: repeat(3, max-content); }
  .d0-slide__cover,
  .d0-deck[data-pattern] .d0-slide__cover { grid-template-columns: 1fr; gap: 16px; }
  .d0-slide__cover > .d0-slide__fig { height: auto; }
  .d0-slide[data-cover="center"] .d0-slide__head { max-width: none; }
  .d0-slide:is([data-cover="contrast"], [data-cover="bottom"], [data-cover="center"]) .d0-slide__fig { --sl-font: 30px; }
  .d0-slide[data-kind="cover"] .d0-slide__summary dd { font-size: 12px; }
  .d0-slide[data-kind="closing"] { min-height: min(560px, calc(100dvh - 116px)); }
  .d0-slide[data-kind="closing"] .d0-slide__head { max-width: none; }
  .d0-slide[data-kind="closing"] .d0-slide__title { font-size: 27px; }
  .d0-slide__meta { grid-template-columns: 1fr; gap: 8px; padding-top: 12px; }
  .d0-slide__meta > div { grid-template-columns: 48px 1fr; gap: 8px; }
  .d0-slide__meta dt, .d0-slide__meta dd { font-size: 12px; }
  .d0-slide__head { gap: 6px; }
  .d0-slide__eyebrow { font-size: 12px; }
  .d0-slide__title { font-size: 20px; }
  h1.d0-slide__title { font-size: 26px; }
  .d0-slide[data-kind="assertion"] .d0-slide__title,
  .d0-slide[data-emphasis="impact"] .d0-slide__title { font-size: 28px; }
  .d0-slide[data-emphasis="impact"]:has(.d0-slide__fig, .d0-shot) .d0-slide__title { font-size: 20px; } /* 위 데스크톱 :has 규칙(특이도 높음)이 28px을 덮지 않게 같은 선택자로 */
  .d0-slide__lead { font-size: 17px; }
  .d0-slide__sub { font-size: 15px; }
  .d0-slide__fig { gap: 8px; }
  .d0-slide__stage { padding: 12px; }
  .d0-slide__fig svg,
  .d0-slide[data-kind] .d0-slide__fig svg { max-width: none; height: auto; }
  .d0-slide[data-kind="evidence"] .d0-slide__fig,
  .d0-slide[data-kind="breakdown"] .d0-slide__fig { --sl-font: 30px; }
  .d0-slide__fig svg[viewBox^="0 0 800 "] { --sl-font: 30px; }  /* 가로형(800) 그림은 커버 종류·패턴 규칙과 상관없이 30(svg에 걸어 그림 단위 규칙을 이긴다) */
  .d0-slide__note { font-size: 13px; }
  .d0-slide__body[data-layout="split"] { grid-template-columns: 1fr; gap: 16px; }
  .d0-slide__points, .d0-slide__summary dd, .d0-slide__toc a, .d0-slide[data-kind="stat"] .d0-slide__note,
  .d0-slide[data-kind="evidence"] .d0-slide__note, .d0-slide[data-kind="breakdown"] .d0-slide__note { font-size: 15px; }
  .d0-slide__points { gap: 6px; }
  .d0-slide__summary > div { grid-template-columns: 1fr; gap: 2px; padding: 10px 0; }
  .d0-slide__summary dt, .d0-slide__src, .d0-slide__num { font-size: 12px; }
  .d0-slide__toc li { grid-template-columns: 4px minmax(0, 1fr); column-gap: 8px; }
  .d0-slide__toc li::before { width: 4px; height: 4px; }
  .d0-slide__toc a { padding: 8px 0; }
  .d0-slide__stat { font-size: 48px; }
  .d0-slide__base { font-size: 15px; }
  .d0-slide[data-kind="screenshot"] .d0-shot,
  .d0-slide[data-kind="screenshot"] .d0-shot__screen { height: auto; width: 100%; justify-self: stretch; }
  .d0-slide[data-kind="screenshot"] .d0-shot { grid-template-columns: minmax(0, 1fr); grid-template-rows: none; }
  .d0-slide[data-kind="screenshot"] .d0-shot :is(.d0-shot__screen, .d0-shot__note, figcaption) { grid-column: 1; grid-row: auto; }
  .d0-slide[data-kind="screenshot"] .d0-shot__note { font-size: 15px; }
  .d0-slide[data-kind="screenshot"] .d0-shot figcaption { font-size: 13px; }
}
/* 320 폭(슬라이드 안쪽 256px): 그림 글자를 한 단계 더 키워 렌더 11px 이상을 지킨다 */
@container (max-width: 270px) {
  .d0-slide__fig { --sl-font: 20px; }                            /* 기본(400): 20 × 256 ÷ 400 = 12.8px */
  .d0-slide__fig svg[viewBox^="0 0 800 "] { --sl-font: 36px; }   /* 가로형(800): 36 × 256 ÷ 800 = 11.5px */
}
@media (max-width: 640px) {
  .d0-deck { gap: 32px; padding: 24px 16px 64px; }
}

/* 인쇄: 슬라이드 한 장 = 가로 한 페이지 */
@media print {
  @page { size: landscape; margin: 0; }
  body { background: #fff; }
  .d0-deck { max-width: none; padding: 0; gap: 0; }
  .d0-slide { break-after: page; break-inside: avoid; border-radius: 0; box-shadow: none; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
  /* 한 장 모드였어도 모든 슬라이드를 되살리고 네비를 숨긴다 */
  .d0-deck[data-mode="single"] > .d0-slide { display: grid; width: auto; max-height: none; overflow: hidden; animation: none; }
  .d0-deck__nav { display: none !important; }
}
```

아래 CSS는 덱 강화 규칙이다. 위 CSS와 [diagram](diagram.md) 공용 CSS·pins의 `.d0-pin` CSS 뒤에, 근거 변형을 쓰면 [evidence](evidence.md) 변형 CSS 뒤에 붙인다.

```css
/* 제목 문법: 결론어 하나만 굵게(선택) */
.d0-slide__title:has(.d0-slide__key) { font-weight: 400; color: var(--d0-grey-700); }
.d0-slide__key { font-weight: 700; color: var(--d0-grey-900); }
.d0-slide__key[data-tone="blue"] { color: var(--d0-blue-dark); }

/* 크롬: 섹션 태그 pill, 출처가 있을 때만 얇은 푸터 선 */
.d0-slide__tag {
  justify-self: start; display: inline-flex; align-items: center;
  margin: 0; padding: 0.3cqi 1cqi; border-radius: 999px;
  background: var(--d0-blue-light); color: var(--d0-blue-dark);
  font-size: 1.3cqi; font-weight: 600; line-height: 1.4;
}
.d0-slide__foot:has(.d0-slide__src):not(:has(kbd)) { padding-top: 1cqi; border-top: 1px solid var(--d0-grey-100); }

/* 비대칭 구도: 제목 열 2 : 그림 열 3, data-flip이면 반대 */
.d0-slide[data-layout="asym"] { grid-template-columns: minmax(0, 2fr) minmax(0, 3fr); grid-template-rows: minmax(0, 1fr) auto; column-gap: 4cqi; }
.d0-slide[data-layout="asym"] > .d0-slide__head { grid-column: 1; grid-row: 1; align-self: center; }
.d0-slide[data-layout="asym"] > .d0-slide__fig { grid-column: 2; grid-row: 1; height: 100%; }
.d0-slide[data-layout="asym"] > .d0-slide__foot { grid-column: 1 / -1; }
.d0-slide[data-layout="asym"][data-flip] { grid-template-columns: minmax(0, 3fr) minmax(0, 2fr); }
.d0-slide[data-layout="asym"][data-flip] > .d0-slide__head { grid-column: 2; }
.d0-slide[data-layout="asym"][data-flip] > .d0-slide__fig { grid-column: 1; }
.d0-slide[data-layout="asym"] .d0-slide__title,
.d0-slide[data-layout="asym"][data-emphasis="impact"]:has(.d0-slide__fig, .d0-shot) .d0-slide__title { font-size: 3.2cqi; } /* 가용 폭이 제목 크기를 정한다: 그림 있는 Impact 규칙보다 특이도를 높여 덮이지 않게 */
.d0-slide[data-layout="asym"] .d0-slide__fig svg { max-width: 100%; }

/* 핵심 수치 기본형: 왼쪽 머리 열에 제목 → 큰 숫자 → 기준 줄(.d0-slide__base, 기본 CSS), 오른쪽 근거 그림(asym 격자 그대로) */
.d0-slide[data-kind="stat"][data-layout="asym"] > .d0-slide__head > .d0-slide__stat { margin-top: 1.6cqi; align-self: start; }
.d0-sl-link[data-on] { stroke: var(--d0-blue); stroke-width: 3; }  /* slope·line 근거의 강조 선. 점은 circle.d0-sl-bar */

/* 섹션 장: 큰 번호 + 챕터 제목 */
.d0-slide[data-kind="section"] { grid-template-rows: minmax(0, 1fr) auto; }
.d0-slide[data-kind="section"] .d0-slide__head { align-self: center; gap: 1.6cqi; max-width: 80cqi; }
.d0-slide__index {
  margin: 0; color: var(--d0-blue-dark);
  font-size: 7cqi; font-weight: 600; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display);
  font-variant-numeric: tabular-nums;
}
.d0-slide[data-kind="section"] .d0-slide__title { font-size: 4.5cqi; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
.d0-slide__toc li[data-section] a { font-weight: 600; }

/* 진한 면: cover·section·closing만. blue-dark 위 #fff 5.50, blue-light 4.94 */
.d0-slide[data-surface="dark"] { background: var(--d0-blue-dark); box-shadow: none; }
.d0-slide[data-surface="dark"]:focus-visible { outline-color: #fff; outline-offset: -8px; } /* 키보드 포커스만: 슬라이드 안쪽 흰 링 5.50 */
.d0-slide[data-surface="dark"] :is(.d0-slide__title, .d0-slide__key, .d0-slide__index) { color: #fff; }
.d0-slide[data-surface="dark"] .d0-slide__title:has(.d0-slide__key) { color: var(--d0-blue-light); }
.d0-slide[data-surface="dark"] :is(.d0-slide__eyebrow, .d0-slide__sub, .d0-slide__lead, .d0-slide__note, .d0-slide__src, .d0-slide__num,
  .d0-slide__meta dt, .d0-slide__meta dd, .d0-slide__summary dt, .d0-slide__summary dd) { color: var(--d0-blue-light); }
.d0-slide[data-surface="dark"] :is(.d0-slide__meta, .d0-slide__summary > div, .d0-slide__foot) { border-color: color-mix(in srgb, #fff 32%, transparent); }
.d0-slide[data-surface="dark"] .d0-slide__tag { background: transparent; box-shadow: inset 0 0 0 1px var(--d0-blue-light); color: #fff; }
.d0-slide[data-surface="dark"] kbd { border-color: var(--d0-blue-light); color: #fff; }
/* 진한 면 위 대표 도식: 선·빈 노드 blue-light, 강조 흰색. blue·의미색 표식은 두지 않는다 */
.d0-slide[data-surface="dark"] :is(.d0-s-edge, .d0-s-ring, .d0-s-line, .d0-s-life, .d0-sl-link, .d0-sl-axis) { stroke: var(--d0-blue-light); }
.d0-slide[data-surface="dark"] :is(.d0-s-node, .d0-s-step, .d0-s-frame) { fill: var(--d0-blue-dark); stroke: var(--d0-blue-light); }
.d0-slide[data-surface="dark"] :is(.d0-s-node, .d0-s-step)[data-on] { fill: #fff; stroke: #fff; }
.d0-slide[data-surface="dark"] .d0-s-edge[data-on] { stroke: #fff; }
/* 값 막대는 색 하나에 기대지 않는다: 기준 막대 = blue-light 테두리만(배경 4.94, 흰색 24% 트랙 위 3.08), 강조 막대 = 흰 채움(5.50, 트랙 위 3.43) + 굵은 값 라벨 */
.d0-slide[data-surface="dark"] :is(.d0-sl-bar, .d0-s-bar) { fill: none; stroke: var(--d0-blue-light); stroke-width: 2px; vector-effect: non-scaling-stroke; }
.d0-slide[data-surface="dark"] :is(.d0-sl-label, .d0-sl-value, .d0-sl-head) text,
.d0-slide[data-surface="dark"] .d0-s-text { fill: var(--d0-blue-light); }
.d0-slide[data-surface="dark"] .d0-sl-value text[data-on] { fill: #fff; font-weight: 700; }
.d0-slide[data-surface="dark"] :is(.d0-sl-label, .d0-sl-head) text[data-on],
.d0-slide[data-surface="dark"] .d0-s-text[data-on] { fill: #fff; }
.d0-slide[data-surface="dark"] .d0-s-muted { fill: var(--d0-blue-light); }
/* 면·자리: 옅은 자리 흰색 24%, 진한 자리 grey-300(3.48), 강조 면 흰색(5.50), 영역은 면 없는 blue-light 점선 */
.d0-slide[data-surface="dark"] :is(.d0-s-fill, .d0-s-track, .d0-s-cell, .d0-sl-total) { fill: color-mix(in srgb, #fff 24%, transparent); }
.d0-slide[data-surface="dark"] .d0-s-key { fill: var(--d0-grey-300); }
.d0-slide[data-surface="dark"] :is(.d0-s-accent, .d0-s-sum) { fill: #fff; }
.d0-slide[data-surface="dark"] :is(.d0-s-zone, .d0-s-head) { fill: none; stroke: var(--d0-blue-light); }
/* 번호: 빈 원 위 blue-light, 흰 원(data-on) 위 blue-dark. 흰 원 위 흰 숫자가 사라지지 않게 */
.d0-slide[data-surface="dark"] .d0-s-num { fill: var(--d0-blue-light); }
.d0-slide[data-surface="dark"] .d0-s-num[data-on] { fill: var(--d0-blue-dark); }
/* 의미색은 기호로: 완료 green = 흰 원 + blue-dark ✓(d0-s-tick), 실패 red = 흰 테두리 원 + 흰 ×(d0-s-stop), orange = blue-light 테두리 원 + !(d0-s-num). 기호는 빼지 않는다(완료 라벨 생략 조건은 본문) */
.d0-slide[data-surface="dark"] :is(.d0-s-node, .d0-s-step)[data-tone="green"] { fill: #fff; stroke: #fff; }
.d0-slide[data-surface="dark"] :is(.d0-s-node, .d0-s-step)[data-tone="red"] { fill: var(--d0-blue-dark); stroke: #fff; stroke-width: 2.5; }    /* 안에 흰 × (d0-s-stop) */
.d0-slide[data-surface="dark"] :is(.d0-s-node, .d0-s-step)[data-tone="orange"] { fill: var(--d0-blue-dark); stroke: var(--d0-blue-light); } /* 안에 ! (text.d0-s-num, blue-light 4.94) */
.d0-slide[data-surface="dark"] .d0-s-tick { stroke: var(--d0-blue-dark); stroke-width: 2; }                                         /* 흰 원 위 ✓ 5.50 */
.d0-slide[data-surface="dark"] :is(.d0-s-edge[data-tone="red"], .d0-s-stop) { stroke: #fff; }                                        /* 원 안 ×·원 밖 막힘 표시 5.50 */
.d0-slide[data-surface="dark"] :is(.d0-s-bar, .d0-sl-bar)[data-tone] { fill: none; stroke: var(--d0-blue-light); }  /* 의미색 막대도 기준 막대처럼 테두리만 */
.d0-slide[data-surface="dark"] :is(.d0-s-bar, .d0-sl-bar)[data-on] { fill: #fff; stroke: none; }                      /* 강조 막대: 흰 채움(의미색 규칙보다 뒤) */
/* 배지: 면을 빼고 blue-light 테두리 + 흰 글자, 의미색 점은 흰색 */
.d0-slide[data-surface="dark"] .d0-pill { background: transparent; box-shadow: inset 0 0 0 1px var(--d0-blue-light); color: #fff; }
.d0-slide[data-surface="dark"] .d0-pill::before { background: #fff; }
/* 덱에서 새로 만든 로컬 도형 클래스는 진한 면 색을 직접 정한다(위 역할대로) */

/* 근거 변형(evidence.md)을 evidence 장 그림 자리에: 근거 요소가 몸 행을 채운다 */
.d0-slide__fig > :is(.d0-mlist, .d0-barlist, .d0-tiles) { min-height: 0; height: 100%; }
.d0-slide__fig .d0-mlist { grid-template-columns: minmax(0, 2fr) minmax(0, 3fr); gap: 4cqi; }
.d0-slide__fig .d0-mlist__rows { gap: 2.4cqi; align-content: center; }
.d0-slide__fig :is(.d0-mlist__rows, .d0-tiles) dd { font-size: 4.4cqi; }
.d0-slide__fig :is(.d0-mlist__rows, .d0-tiles) dt { font-size: 1.8cqi; }
.d0-slide[data-kind] .d0-slide__fig svg.d0-mlist__chart { justify-self: stretch; width: 100%; max-width: none; height: 100%; max-height: 100%; }
.d0-slide__fig .d0-barlist { align-content: center; gap: 2.4cqi; }
.d0-slide__fig .d0-barlist li { gap: 0.8cqi 2cqi; }
.d0-slide__fig .d0-barlist :is(.d0-barlist__label, .d0-barlist__value) { font-size: 2.2cqi; }
.d0-slide__fig .d0-barlist__track { height: 1.4cqi; }
.d0-slide__fig .d0-tiles { grid-auto-rows: 1fr; gap: 1.6cqi; }
.d0-slide__fig .d0-tiles > div { padding: 2.4cqi; align-content: center; }

/* 주석(diagram.md annotate)을 덱 그림에: SVG 높이를 내용대로 두어 번호 위치가 맞게 */
.d0-slide__fig .d0-annot { align-self: center; justify-self: center; max-width: 100%; }
.d0-slide .d0-slide__fig .d0-annot svg { height: auto; max-height: none; max-width: 100%; }
.d0-slide__fig .d0-annot > .d0-pin { width: 2.8cqi; height: 2.8cqi; font-size: 1.5cqi; }
.d0-slide .d0-annot__notes { gap: 1.6cqi; }
.d0-slide .d0-annot__notes li { grid-template-columns: 2.6cqi minmax(0, 1fr); column-gap: 1.2cqi; font-size: 2cqi; }
.d0-slide .d0-annot__notes .d0-pin { width: 2.6cqi; height: 2.6cqi; font-size: 1.4cqi; }

@container (max-width: 730px) {
  .d0-slide__tag { padding: 2px 10px; font-size: 12px; }
  .d0-slide__foot:has(.d0-slide__src):not(:has(kbd)) { padding-top: 8px; }
  .d0-slide[data-layout="asym"],
  .d0-slide[data-layout="asym"][data-flip] { grid-template-columns: minmax(0, 1fr); grid-template-rows: repeat(3, max-content); }
  .d0-slide[data-layout="asym"] > :is(.d0-slide__head, .d0-slide__fig, .d0-slide__foot),
  .d0-slide[data-layout="asym"][data-flip] > :is(.d0-slide__head, .d0-slide__fig) { grid-column: 1; grid-row: auto; height: auto; }
  .d0-slide[data-layout="asym"] .d0-slide__title,
  .d0-slide[data-layout="asym"][data-emphasis="impact"]:has(.d0-slide__fig, .d0-shot) .d0-slide__title { font-size: 20px; } /* 위 데스크톱 asym 규칙과 같은 특이도로 */
  .d0-slide[data-kind="section"] { min-height: min(420px, calc(100dvh - 116px)); }
  .d0-slide__index { font-size: 40px; }
  .d0-slide[data-kind="section"] .d0-slide__title { font-size: 24px; }
  .d0-slide__fig > :is(.d0-mlist, .d0-barlist, .d0-tiles) { height: auto; }
  .d0-slide__fig .d0-mlist { grid-template-columns: minmax(0, 1fr); gap: 16px; }
  .d0-slide[data-kind] .d0-slide__fig svg.d0-mlist__chart { height: auto; max-height: 200px; }
  .d0-slide__fig :is(.d0-mlist__rows, .d0-tiles) dd { font-size: 26px; }
  .d0-slide__fig :is(.d0-mlist__rows, .d0-tiles) dt { font-size: 13px; }
  .d0-slide__fig .d0-mlist__rows, .d0-slide__fig .d0-barlist { gap: 12px; }
  .d0-slide__fig .d0-barlist :is(.d0-barlist__label, .d0-barlist__value) { font-size: 15px; }
  .d0-slide__fig .d0-barlist__track { height: 8px; }
  .d0-slide__fig .d0-tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); grid-auto-rows: auto; gap: 8px; }
  .d0-slide__fig .d0-tiles > div { padding: 14px; }
  .d0-slide__fig .d0-annot > .d0-pin, .d0-slide .d0-annot__notes .d0-pin { width: 24px; height: 24px; font-size: 13px; }
  .d0-slide .d0-annot__notes { gap: 8px; }
  .d0-slide .d0-annot__notes li { grid-template-columns: 24px minmax(0, 1fr); column-gap: 8px; font-size: 15px; }
}
```

```js
/* 한 장 모드: 준비가 끝나면 마지막에 data-mode="single"을 붙인다. 중간에 실패하면 세로 나열 그대로다. */
(function () {
  var deck = document.querySelector('.d0-deck');
  if (!deck) return;
  var slides = Array.prototype.slice.call(deck.querySelectorAll('.d0-slide'));
  var nav = deck.querySelector('.d0-deck__nav');
  if (!slides.length || !nav) return;
  var btnPrev = nav.querySelector('[data-deck="prev"]');
  var btnNext = nav.querySelector('[data-deck="next"]');
  var outNow = nav.querySelector('[data-deck-now]');
  var outTotal = nav.querySelector('[data-deck-total]');
  var TEXT = 'input, textarea, select, [contenteditable]:not([contenteditable="false"]), [role="tablist"], [role="slider"]';
  var CTRL = 'button, a[href], summary, [role="button"]';
  var idx = -1;

  function indexOfId(id) {
    for (var i = 0; i < slides.length; i++) if (slides[i].id === id) return i;
    return -1;
  }
  function fromHash() {
    var id = '';
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (err) { id = ''; }
    return id ? indexOfId(id) : -1;
  }
  /* 브라우저는 해시 대상 장(tabindex="-1")에 스스로 포커스를 준다. 해시 진입·이동에서는 그 포커스를 풀어 링이 생기지 않게 한다 */
  function dropSlideFocus() {
    var a = document.activeElement;
    if (a && slides.indexOf(a) >= 0) a.blur();
  }
  function show(i, opt) {
    opt = opt || {};
    i = Math.max(0, Math.min(slides.length - 1, i));
    if (i === idx) { if (opt.from === 'hash') dropSlideFocus(); return; }
    var old = slides[idx];
    var a = document.activeElement;
    /* 포커스는 키보드로 넘길 때(opt.from === 'key')와 사라지는 장 안 컨트롤(목차 링크 등)에 포커스가 있을 때만 새 장으로 옮긴다.
       해시 진입·이동은 장을 보여 주기만 하고 포커스를 주지 않는다 */
    var inner = !!(old && a && a !== old && old.contains(a));
    var moveFocus = opt.from !== 'hash' && (opt.from === 'key' || inner);
    slides.forEach(function (s, k) {
      if (k === i) s.setAttribute('data-active', ''); else s.removeAttribute('data-active');
    });
    idx = i;
    slides[i].scrollTop = 0;
    if (outNow) outNow.textContent = String(i + 1);
    if (btnPrev) btnPrev.setAttribute('aria-disabled', String(i === 0));
    if (btnNext) btnNext.setAttribute('aria-disabled', String(i === slides.length - 1));
    if (opt.hash !== false) {
      try { history.replaceState(null, '', '#' + slides[i].id); } catch (err) { /* srcdoc 등: 주소 동기화 생략 */ }
    }
    if (moveFocus) slides[i].focus({ preventScroll: true });
    else if (opt.from === 'hash') dropSlideFocus();
  }
  /* 장 안이 넘치면 Space·PageDown은 먼저 장 안을 스크롤한다. 스크롤했으면 true */
  function pageWithin(dir) {
    var s = slides[idx];
    if (s.scrollHeight - s.clientHeight < 2) return false;
    if (dir > 0 && s.scrollTop + s.clientHeight >= s.scrollHeight - 1) return false;
    if (dir < 0 && s.scrollTop <= 0) return false;
    s.scrollBy(0, dir * s.clientHeight * 0.85);
    return true;
  }
  function toggleFullscreen() {
    try {
      var p = document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
      if (p && p.catch) p.catch(function () {});
    } catch (err) { /* 전체 화면을 못 쓰는 환경 */ }
  }

  document.addEventListener('keydown', function (e) {
    if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey || e.isComposing) return;
    var t = e.target && e.target.closest ? e.target : null;
    if (t && t.closest(TEXT)) return;                     /* 입력 칸: 모든 키를 그대로 둔다 */
    var k = e.key, d = 0, paging = false;
    if (k === ' ' || k === 'Spacebar' || k === 'Enter') {
      if (k === 'Enter' || (t && t.closest(CTRL))) return; /* 버튼·링크의 Space·Enter는 그 컨트롤 몫 */
      d = e.shiftKey ? -1 : 1; paging = true;
    }
    else if (k === 'ArrowRight') d = 1;
    else if (k === 'ArrowLeft') d = -1;
    else if (k === 'PageDown') { d = 1; paging = true; }
    else if (k === 'PageUp') { d = -1; paging = true; }
    else if (k === 'Home') { e.preventDefault(); show(0, { from: 'key' }); return; }
    else if (k === 'End') { e.preventDefault(); show(slides.length - 1, { from: 'key' }); return; }
    else if (k === 'f' || k === 'F') { toggleFullscreen(); return; }
    else return;
    e.preventDefault();
    if (paging && pageWithin(d)) return;
    show(idx + d, { from: 'key' });
  });

  deck.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target : null;
    if (!t) return;
    var b = t.closest('button[data-deck]');
    if (b) {
      var act = b.getAttribute('data-deck');
      if (act === 'prev') show(idx - 1);
      else if (act === 'next') show(idx + 1);
      else if (act === 'toc') {
        var toc = deck.querySelector('.d0-slide[data-kind="toc"]');
        show(toc ? slides.indexOf(toc) : 0);
      }
      return;
    }
    var a = t.closest('a[href^="#"]');
    if (!a) return;
    var i = indexOfId(a.getAttribute('href').slice(1));
    if (i < 0) return;
    e.preventDefault();
    show(i);
  });
  window.addEventListener('hashchange', function () {
    var i = fromHash();
    if (i >= 0) show(i, { hash: false, from: 'hash' });
  });

  /* 스와이프: 터치·펜만. 가로 이동 > 세로 이동이고 48px 넘으면 넘긴다 */
  var sx = null, sy = 0, pid = null;
  deck.addEventListener('pointerdown', function (e) {
    if (e.pointerType === 'mouse') return;
    sx = e.clientX; sy = e.clientY; pid = e.pointerId;
  });
  deck.addEventListener('pointerup', function (e) {
    if (sx === null || e.pointerId !== pid) return;
    var dx = e.clientX - sx, dy = e.clientY - sy;
    sx = null;
    if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 48) show(idx + (dx < 0 ? 1 : -1));
  });
  deck.addEventListener('pointercancel', function () { sx = null; });

  /* iframe(srcdoc) 안: 누르면 프레임이 키 입력을 받게 한다 */
  var framed = true;
  try { framed = window.self !== window.top; } catch (err) { framed = true; }
  if (framed) {
    document.addEventListener('pointerdown', function () {
      try { window.focus(); } catch (err) { /* 무시 */ }  /* 슬라이드에 포커스를 주지 않는다: 넘길 때마다 포커스 링이 생긴다 */
    });
  }

  if (outTotal) outTotal.textContent = String(slides.length);
  var start = fromHash();
  show(start >= 0 ? start : 0, { hash: false, from: start >= 0 ? 'hash' : '' });
  if (start >= 0) window.addEventListener('load', dropSlideFocus);  /* 로드 끝에 해시 대상에 생긴 포커스도 푼다 */
  deck.setAttribute('data-mode', 'single');               /* 여기까지 왔을 때만 한 장 모드 */
})();
```

- 쪽수 `n / N`은 목차를 제외한 슬라이드마다 마크업에 직접 쓴다(스크립트가 없을 때와 인쇄에서 보인다). 한 장 모드에서는 네비 쪽수가 대신 보인다. 슬라이드를 빼거나 더하면 쪽수를 함께 고친다.
- 차트·도식을 바꿀 때도 기본 SVG는 viewBox 폭 400·글자 17·최대 42cqi(split 안은 그림 열 폭), 가로형은 800·글자 20(좁은 화면 30, 320 폭 36)·최대 84cqi를 유지한다. map·side 표지에는 400 폭 표지용 도식을 쓴다. 그대로 둔 800 지도는 안전망으로 731px 이상에서도 글자 30이다.
  다른 도식 모양은 [diagram.md](diagram.md)를 따르되 클래스는 이 파일의 `d0-sl-*` 규칙(강조 하나만 blue)으로 칠한다.
- 스크롤 리빌 모션은 붙이지 않는다. 장을 바꿀 때의 짧은 opacity 페이드만 있고 reduced-motion이면 즉시 바뀐다.
- 화면은 넓은데 높이가 낮으면(높이 498px 이하, 예: 1280×400, 812×375 가로 폰) 슬라이드 폭은 730px에서 멈추고 16:9를 풀어 안쪽 글자는 px 고정, 넘치는 몫은 장 안에서 세로로 스크롤한다.
  좁은 장과 키 작은 창에서는 행이 내용 높이(`max-content`)라 그림을 줄여 장에 끼워 넣지 않는다.

## 덱 게이트 (구현)

의미 검사(한 장 한 주장, 결론 제목, 제목만 읽어도 이어짐, Impact 비율 등)는 [덱 출력](../output/deck.md)의 Slide Gate가 먼저다.
여기는 마크업·타이포·키·hash·인쇄·reduced-motion·375·iframe을 코드와 측정으로 확인한다. 나머지(토큰 인라인, 시맨틱, 접근성, 색 규칙, 개행)는 page와 같다.

줄 수·본문 크기·그림 비율 하한은 [덱 출력](../output/deck.md) 밀도 표가 정본이다. 아래 항목의 해당 값은 그 표의 값으로 읽는다.

**HARD (코드로 확인)**

- [ ] `main.d0-deck[data-pattern]`이 하나이고 `data-pattern`이 패턴 8개 중 하나다. 슬라이드(`.d0-slide`)는 표지·목차 포함 5~12장이다
- [ ] 마지막 장은 `data-kind="closing"`이고 `data-closing`이 decision·request·action·criteria·takeaway 중 하나이며 큰 제목 한 문장 + 구분선 + 작은 `dl.d0-slide__meta` 2~3칸을 두고 같은 무게의 불릿 목록·Impact가 없다
- [ ] 첫 장이 `data-kind="cover"` + h1이고 바로 다음 장이 `nav[data-kind="toc"]`다. 목차가 `ul.d0-slide__toc`이고 `li` 수 = 표지·목차를 뺀 장 수, 항목 글자 = 각 장 제목, `href` = 그 장 `id`; 목차에는 번호·쪽수가 없다
- [ ] `data-kind`가 정본 값(생략 | cover | toc | assertion | evidence | screenshot | breakdown | stat | summary | section | closing)만 쓴다. `section` 장은 머리에 `p.d0-slide__index` + h2만 있고 그림·요점이 없다
- [ ] `data-surface="dark"`는 `cover`·`section`·`closing` 장에만 있고 덱당 1~3장이며, Impact 장과 겹치지 않는다. 그 장 안 글자는 `#fff`·blue-light뿐이고 blue·의미색 표식이 없다
- [ ] 진한 면 `closing`의 바로 앞 장이 Impact가 아니다(앞 장이 Impact면 마무리는 흰 면). 진한 면 장의 `:focus-visible` 링은 흰색이고 슬라이드 안쪽에 있다
- [ ] `data-layout="asym"` 장은 머리·`figure.d0-slide__fig`·발이 슬라이드 바로 자식이고 `.d0-slide__body`가 없다
- [ ] 제목 하나에 `b.d0-slide__key`가 1개 이하이고 `data-tone="blue"`가 1개 이하다
- [ ] 근거(생략)·`evidence`·`breakdown` 장마다 `figure.d0-slide__fig`가 정확히 1개이고 그 안에 `role="img"` + `<title>`을 가진 SVG가 있다.
      `evidence` 장은 SVG 대신 근거 변형(`figure[data-variant="metric-list|bar-list|tiles"]` 안 `.d0-mlist`·`.d0-barlist`·`.d0-tiles` 1개)이어도 된다(metric-list의 작은 차트는 `role="img"` + `<title>`).
      `screenshot`은 `figure.d0-shot` 1개, `stat`은 `.d0-slide__stat` 1개다. `stat` 기본형(`data-layout="asym"`)은 숫자가 머리 안에 있고 `figure.d0-slide__fig` 1개(SVG `role="img"` + `<title>` 또는 근거 변형)가 있으며 Impact가 아니다. 순수 Impact stat은 숫자가 `figure.d0-slide__fig` 안에 있고 다른 그림이 없다. `toc`·`summary`·`section`·`closing`·`assertion`은 그림 예외이고 `cover`에는 대표 도식이 있다
- [ ] `data-emphasis="impact"` 장에 카드·요점 목록·두 번째 그림이 없다
- [ ] 슬라이드당 `li` 3개 이하(`toc`와 근거 변형 `.d0-barlist`의 `li` 제외), 본문 텍스트가 [덱 출력](../output/deck.md) 밀도 표의 줄 수 이하다. 세는 범위는 [덱 출력](../output/deck.md) 밀도 표가 정본이다(몸의 `p`·`li`·`dd`. 제목·쪽수·출처와 그림 해석 줄 `figcaption.d0-slide__note`는 빼고, 해석 줄은 따로 1줄 이하)
- [ ] 목차를 제외한 슬라이드마다 쪽수 `n / N`이 렌더 텍스트로 있고 순서가 맞다
- [ ] 슬라이드가 `section`(목차는 `nav`) + `aria-labelledby` + `tabindex="-1"`이고 헤딩은 표지 h1 → h2만 쓴다
- [ ] 차트·도식 하나에 `data-on` 강조가 1계열이다. 의미색은 상태 표식에만, 그라디언트·3D·장식 아이콘이 없다
- [ ] `nav.d0-deck__nav`에 `button[data-deck="prev"]`·`[data-deck="next"]`·`[data-deck="toc"]`, 쪽수, 안내 "←/→로 넘겨요"가 있고 버튼이 24px 이상이다
- [ ] 한 장 모드 규칙이 `.d0-deck[data-mode="single"]` 아래에만 있고, `data-mode`는 스크립트 끝에서 붙는다(JS가 없으면 세로 나열 + 네비 숨김)
- [ ] →·Space·PageDown이 다음, ←·Shift+Space·PageUp이 이전, Home·End가 처음·끝으로 쪽수를 바꾼다
- [ ] 버튼에 포커스가 있을 때 Space 한 번 = 한 장 전진이다. 입력 칸 안의 Space·화살표는 가로채지 않는다
- [ ] 넘길 때 주소가 `#s-NN`으로 바뀌고(`replaceState`, try/catch), `#s-NN`으로 열면 그 장부터 보인다
- [ ] `prefers-reduced-motion: reduce`에서 활성 장의 `animation-name`이 `none`이다
- [ ] `@media print`에서 모든 슬라이드가 보이고, 슬라이드마다 `break-after: page`, `@page { size: landscape }`, 네비가 숨는다
- [ ] srcdoc iframe 안에서 한 번 누른 뒤 →로 장이 넘어가고, 콘솔 오류가 없다

**VISUAL (측정으로 확인)**

- [ ] 1280×800에서 보이는 `.d0-slide`가 1개이고, 높이 ÷ 폭이 0.5625(±1px), 가로 가운데(±1px), 덱 안에 다 들어온다(가로·세로 스크롤 없음). 내용이 넘치지 않는다(`scrollHeight` ≤ `clientHeight`)
- [ ] 1280 한 장 모드에서 제목 36~44px(asym 제목 약 35px), 섹션 번호 약 76px·섹션 제목 약 49px, 표지 h1 56~72px, 순수 Impact(`assertion`) 제목 약 66px(그림·숫자가 있는 Impact는 일반 제목 크기), closing 제목은 약 54px(섹션 제목보다 크고 표지 h1보다 작다), 리드 24~30px, 본문은 밀도 표의 본문 크기, Meta 14~18px, 큰 숫자 72~120px이다
- [ ] SVG 글자 렌더 크기(font-size × SVG 렌더 배율)가 1280에서 28px 이하, 320·375에서 11px 이상이다(커버 그림 포함)
- [ ] 그린 그림(`svg`·`img`·`.d0-shot__screen` box) ÷ 몸 영역이 [덱 출력](../output/deck.md) 밀도 표의 권장 하한 이상이다. 미달이면 HARD 실패가 아니라 그림이 그 장의 근거인지, 열 비율·viewBox·구도를 고칠지 확인하고, 재검토 후 그대로 두면 이유 한 줄을 HTML 주석이나 결과 보고에 남긴다(1280×800 한 장 모드에서 잰다(슬라이드 폭 730px 미만의 1열 배치는 제외))
- [ ] 375×812에서 장이 16:9를 풀고, 글자가 11px 이상, 페이지 가로 스크롤이 없으며, 좌우 스와이프(48px 초과)로 장이 넘어간다. 긴 장은 장 안에서 세로로 스크롤된다
- [ ] 320×568(터치)에서 SVG 실제 글자가 11px 이상이고, 네비가 넘치지 않고 안내가 한 줄이며, 표지 키 안내가 보이지 않는다
- [ ] 키 작은 창(375×400)에서 슬라이드 폭 = `100vw − 2 × 거터`, 812×375에서 730px 이상이다

## 금지

- 명사 제목(`현황`, `분석 결과`), 슬라이드 하나에 그림 둘 이상, 불릿 4개 이상, 여러 줄 문단, 상한을 넘긴 본문.
- 슬라이드 높이를 px로 고정하기, `vw` 글자 크기, 데스크톱에서 16:9 풀기.
- 자동 넘김, opacity 페이드 외의 전환(밀기·확대·3D 넘김), 스크롤 리빌, reduced-motion에서 전환 남기기.
- 키보드 이동을 입력 칸 안에서 가로채기, 버튼 포커스 상태의 Space를 넘김 키로도 처리하기(이중 전진), CSS만으로 한 장 모드 켜기(JS 실패 시 장이 사라진다).
- 목차 없는 덱, 목차 글자와 슬라이드 제목이 다른 덱, 쪽수를 `aria-label`에만 두기.
- Impact 면에 카드·어두운 배경, 계열마다 다른 색, 그라디언트 배경, 그림자 짙은 카드, 의미 없는 아이콘·사람 일러스트.
- 진한 면(`data-surface="dark"`)을 본문 장·Impact·page에 쓰기, 덱에 4장 이상, 진한 면 위 blue·의미색·grey 글자, 진한 면에 그라디언트·글래스·사진·패턴.
- 장식용 초대형 숫자·연도(숫자가 주장 자체일 때만 `stat`), 비교를 주장하는 stat에서 비교 기준을 해석 줄 속에만 숨기고 숫자만 크게 두기, 두 점으로 그은 추세선, 큰 원 안에 숫자를 넣어 크기로 견주기(값 비교가 부정확하다. 막대나 bar-list), 크롬의 로고·브랜드명.
- 모든 장을 좌우 번갈아 비대칭으로 두기, 크롬 셋(태그·쪽번호·푸터)을 매 장 강제하기, 제목 기호(`+`·`/`) 장식 고정, 제목에 강조 구간 둘 이상.
