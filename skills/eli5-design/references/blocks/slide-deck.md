# slide-deck — 한 장씩 넘기는 발표 덱

[덱 출력](../output/deck.md)의 마크업·CSS·JS 정본이다. 덱 구성·문장·Slide Gate는 덱 출력 문서가 정하고, 이 파일은 그 덱을
화면에 한 장씩 띄우고 넘기는 구현을 정한다. 문서형 `main.d0-page` 대신 `main.d0-deck`을 쓴다.

덱을 만들기 전에 [output/deck.md](../output/deck.md)의 Audience × Purpose와 Story Gate부터 통과한다.

## 전달 모드 마크업과 밀도

루트에서 전달 모드를 하나 고른다. 생략하면 Presentation이고, 한 덱 안에서 섞지 않는다.
장수(표지·목차 포함 5~12장)와 한 장씩 넘기는 동작은 두 모드가 같다.

```html
<!-- 발표자와 함께 보는 Presentation (생략해도 같음) -->
<main class="d0-deck" data-pattern="report" data-variant="status" data-delivery="present">
  <!-- 슬라이드와 네비 -->
</main>

<!-- 맥락·본문·출처를 포함해 혼자 읽는 Slidedoc -->
<main class="d0-deck" data-pattern="report" data-variant="status" data-delivery="read">
  <!-- 슬라이드와 네비 -->
</main>
```

아래 기본 타이포·그림 면적·본문 밀도는 Presentation 기준이다. Slidedoc은 [덱 출력의 전달 하위 모드 표](../output/deck.md)의
본문 최대 8줄·18~20px·그림 영역 40~60%를 쓰고, 그 외 제목·Impact·Meta와 구현 동작은 유지한다.
맥락·본문은 몸 안의 `p.d0-slide__text`로 두고, 출처는 기존 `p.d0-slide__src`를 쓴다.
짧은 문단 2개와 불릿 3개 이내로 구성하며, 문단·불릿·해석·출처를 합쳐 렌더 최대 8줄을 넘으면 내용을 나눈다.

Slidedoc은 아래 CSS를 기본 CSS 뒤에 추가한다. 폰트를 더 줄여 내용을 밀어 넣지 않고, 그림 옆에 맥락과 본문을 배치한 뒤 모드별 면적과 줄 수를 측정한다.

```css
/* read 본문: 1280×800 한 장 모드에서 약 18px, present는 2cqi(약 22px) */
.d0-deck[data-delivery="read"] .d0-slide__text,
.d0-deck[data-delivery="read"] .d0-slide__points,
.d0-deck[data-delivery="read"] .d0-slide__note,
.d0-deck[data-delivery="read"] .d0-slide[data-kind="screenshot"] .d0-shot__note,
.d0-deck[data-delivery="read"] .d0-slide[data-kind="screenshot"] .d0-shot figcaption {
  font-size: 1.65cqi;
  line-height: var(--d0-leading-body);
}
.d0-deck[data-delivery="read"] .d0-slide__text {
  margin: 0;
  color: var(--d0-grey-800);
  text-wrap: pretty;
}
.d0-deck[data-delivery="read"] .d0-slide__points { gap: 0.6cqi; }

@container (width < 730px) {
  .d0-deck[data-delivery="read"] .d0-slide__text,
  .d0-deck[data-delivery="read"] .d0-slide__points,
  .d0-deck[data-delivery="read"] .d0-slide[data-kind="screenshot"] .d0-shot__note {
    font-size: 15px;
  }
  .d0-deck[data-delivery="read"] .d0-slide__note,
  .d0-deck[data-delivery="read"] .d0-slide[data-kind="screenshot"] .d0-shot figcaption {
    font-size: 13px;
  }
}
```

## 해부 구조

- **덱** `main.d0-deck[data-pattern][data-variant]` 하나. `data-pattern`은 패턴 8개(`compare` `flow` `preview` `report`
  `guide` `timeline` `incident` `faq`) 중 하나(덱의 주 패턴)로 필수이고, `data-variant`는 그 패턴의 변형 이름표다(없으면 생략). 레시피로 짠 덱은 `data-recipe`를 더할 수 있다. 스타일은 이름표와 무관하다.
- **슬라이드** `section.d0-slide`(목차만 `nav.d0-slide`) = 머리 → 몸 → 발. `id`(`s-01`…), `aria-labelledby`(제목 id), `tabindex="-1"`.
  16:9, 흰 면 + radius card, 안쪽 패딩은 슬라이드 폭에 비례한다(위 4.5%, 좌우 5%, 아래 3%).
  - 머리 `header.d0-slide__head`: 결론 제목(`h1` 표지만, 나머지 `h2`, `.d0-slide__title`) + 보조 한 줄(`p.d0-slide__sub`) 또는 리드(`p.d0-slide__lead`, 표지 등 impact가 아닌 장만), 둘 다 선택.
  - 몸: 그림 하나(`figure.d0-slide__fig` = SVG + 해석 한 줄 `figcaption.d0-slide__note`). **회색 무대는 기본 없음**이다. SVG를 `figure`에 바로 둔다.
    무대가 꼭 필요할 때만(흰 면 위에서 그림 경계가 흐려지는 와이어프레임 등) `div.d0-slide__stage[data-stage]`로 감싼다.
    근거 슬라이드(종류 생략)의 기본 배치는 그림 + 요점 나란히다: `div.d0-slide__body[data-layout="split"]` 안에 그림과 `ul.d0-slide__points`(2~3개).
  - 발 `footer.d0-slide__foot`: 출처 한 줄(`p.d0-slide__src`, 선택) + 쪽수 `p.d0-slide__num` `n / N`(렌더 텍스트).
- **네비** `nav.d0-deck__nav`: 덱의 마지막 자식. 이전·다음 `button[data-deck="prev|next"]`, 쪽수 `p.d0-deck__count`(`n / N`),
  목차 `button[data-deck="toc"]`, 안내 `p.d0-deck__hint`("←/→로 넘겨요", 터치 기기는 "밀어서 넘겨요"). 한 장 모드에서만 보인다.
- **제목 목차** `nav.d0-slide[data-kind="toc"]`: 표지 바로 다음 장. `ul.d0-slide__toc`에 작은 점 불렛과 항목마다 `a href="#s-03"`을 둔다. 항목 글자 = 해당 슬라이드 제목. 목차 장에는 쪽수를 표시하지 않는다.
- **헤딩 순서.** 표지 h1 → 나머지 h2. 슬라이드 안에서 h3 이하는 쓰지 않는다.
- **구도**(선택). 슬라이드에 `data-composition`을 달 수 있다. 값과 교차 규칙은 [composition.md](../composition.md)가 정본이다.

## 한 장씩 보기

- **점진적 향상.** 스크립트가 덱을 준비한 뒤 마지막에 `data-mode="single"`을 붙일 때만 한 장 모드가 된다.
  JS가 없거나 중간에 실패하면 속성이 붙지 않아 슬라이드가 세로로 나열되고(폭 최대 1200px, 사이 40px), 네비는 숨는다.
- **레터박스.** 한 장 모드에서 덱은 뷰포트 전체(`100dvh`)를 차지하고 슬라이드 한 장을 가운데 둔다. 1200px 상한은 풀린다.
  슬라이드 폭 = `min(100vw − 2 × 거터, (100dvh − 크롬) × 16 / 9)`. 거터 32px(640px 이하 16px), 크롬 = 위아래 패딩 + 네비 + 간격 = 88px(640px 이하 76px).
  거터·크롬·슬라이드 폭은 덱 지역 변수 `--deck-gutter`·`--deck-chrome`·`--slide-w`다(토큰이 아니라 `--d0-` 접두사를 쓰지 않는다).
  1280×800에서 슬라이드는 1216 × 684px, 그 아래 44px 네비가 붙는다. 한 장 모드 동안 `html`의 스크롤을 막고 스크롤바 자리도 비우지 않는다(100vw가 정확해진다).
- **활성 장.** 보이는 장에 `data-active`가 붙고 나머지는 `display: none`이다. 전환은 140ms opacity 페이드 하나뿐이고, reduced-motion이면 없다.
- **키.** →·Space·PageDown = 다음, ←·Shift+Space·PageUp = 이전, Home·End = 처음·끝, F = 전체 화면(실패해도 무해).
  - 이벤트 대상이 입력 칸(`input` `textarea` `select` `[contenteditable]`, 탭 목록)이면 어떤 키도 가로채지 않는다(커서 이동).
  - 대상이 `button` `a` `summary` `[role="button"]`이면 Space·Enter를 가로채지 않는다. 버튼에 포커스가 있을 때 Space는 그 버튼의 클릭 한 번만 일으킨다(이중 전진 없음).
  - Enter는 넘김 키가 아니다.
  - Space·Shift+Space·PageDown·PageUp은 활성 장이 넘쳐 세로로 스크롤되고 아직 끝에 닿지 않았으면 장 안을 한 화면(85%) 스크롤하고, 끝에 닿은 뒤에 장을 넘긴다. ←/→는 항상 장을 넘긴다.
- **포커스.** 장을 넘길 때 포커스가 사라지는 장 안의 컨트롤(목차 링크 등)에 있었거나 키보드로 그 장 자체에 있었으면 새 장(`tabindex="-1"`)으로 옮긴다.
  포커스가 네비 버튼이나 `body`에 있거나, 마우스로 장을 눌러 생긴 포커스면 옮기지 않는다(넘길 때마다 슬라이드에 포커스 링이 생기지 않는다). 네비 쪽수는 `aria-live="polite"`라 화면 낭독기가 새 쪽수를 읽는다.
- **목차 버튼.** `data-deck="toc"`는 목차 슬라이드(`[data-kind="toc"]`)로 이동한다(오버레이 없음). 목차가 없으면 첫 장으로 간다.
  목차 링크와 덱 안 `a[href="#s-…"]`는 기본 이동을 막고 그 장으로 넘긴다.
- **hash.** 넘길 때마다 `history.replaceState(null, '', '#s-03')`로 주소를 맞춘다(기록은 쌓지 않는다). srcdoc처럼 실패하는 환경은 try/catch로 건너뛴다.
  로드할 때 `location.hash`가 덱 안 슬라이드 id면 그 장부터 보이고, `hashchange`에도 따라간다.
- **iframe(srcdoc).** 프레임 안에서는 키 이벤트가 프레임에 포커스가 있어야 들어온다. 스크립트는 프레임 안을 감지하면 문서 `pointerdown`마다
  `window.focus()`를 불러 프레임 문서가 키를 받게 한다(슬라이드 자체에는 포커스를 주지 않는다. 주면 넘길 때마다 포커스 링이 생긴다).
  네비 안내 "←/→로 넘겨요"가 프레임 안에서도 보인다.
- **좁은 화면·터치.** 슬라이드 폭이 730px 미만이면(375px 화면은 항상) 16:9를 풀고 px 고정 글자로 바뀐다(아래 타이포 표).
  장이 뷰포트보다 길면 장 안에서 세로로 스크롤한다(`max-height: calc(100dvh − 크롬)`, `overflow-y: auto`). 네비는 화면 아래에 붙는다.
  터치 기기는 좌우 스와이프와 버튼으로 넘긴다: 터치·펜 포인터가 가로로 48px 넘게, 세로보다 크게 움직이면 다음(왼쪽으로 밀기)·이전(오른쪽으로 밀기)이다.
  마우스 드래그는 글자 선택과 부딪혀 쓰지 않는다. 덱과 장에 `touch-action: pan-y`라 세로 스크롤은 브라우저가 그대로 한다.
  외부 키보드가 붙은 경우의 키 규칙은 데스크톱과 같다.
- **인쇄.** 한 장 모드 규칙은 전부 `@media screen` 안에 있다. 인쇄하면 모든 슬라이드가 다시 보이고, 한 장 = 가로 한 페이지(`break-after: page`), 네비는 숨는다.

## 타이포

`cqi` = 슬라이드 안쪽 폭(패딩 뺀 폭)의 1%. 1280×800 한 장 모드에서 슬라이드 1216px, 안쪽 1094px이라 1cqi ≈ 10.9px다.
JS 없는 세로 나열(1280 화면, 슬라이드 1136px, 안쪽 1022px)은 1cqi ≈ 10.2px다.

| 역할 | 클래스 | cqi / 굵기 | 1280 한 장 | 1280 나열 | 계약 범위 | 730 미만(px 고정) |
| --- | --- | --- | --- | --- | --- | --- |
| Display(표지 h1) | `h1.d0-slide__title` | 5.6 / 700 | 61px | 57px | 56–72 | 26px |
| Impact·assertion 제목 | `.d0-slide__title` | 6 / 700 | 66px | 61px | 60 이상 | 28px |
| 슬라이드 제목 | `.d0-slide__title` | 3.6 / 700 | 39px | 37px | 36–44 | 20px |
| 마지막 장 | `closing`의 `.d0-slide__title` | 4.5 / 700 | 49px | 46px | Lead~Display 사이 | 24px |
| Lead | `.d0-slide__lead` | 2.4 / 400 grey-700 | 26px | 25px | 24–30 | 17px |
| 본문·요점·보조·해석 | `.d0-slide__points` `__sub` `__note` `dd` 목차 | 2 / 400 | 22px | 20px | 20–24 | 15px(해석 13px) |
| Meta(눈썹·출처·쪽수·`dt`) | `__eyebrow` `__src` `__num` | 1.4 / 400~600 grey-600 | 15px | 14px | 14–18 | 12px |
| 큰 숫자 | `.d0-slide__stat` | 10 / 600 blue-dark | 109px | 102px | 72–120 | 48px |

- 화면이 줄면 덱 전체가 같은 비율로 줄어든다. `vw` 글자는 쓰지 않는다.
- **그림 글자.** 기본(split) SVG는 viewBox 폭 400, 글자 17, 최대 폭 42cqi다(1280 한 장에서 약 19px, 375에서 13px).
  가로형 차트(`evidence`·`breakdown`)는 viewBox 폭 800, 글자 20, 최대 폭 84cqi이고(1280에서 약 23px), 730 미만에서는 글자를 30으로 키운다(375에서 약 11.7px).
  라벨 사이 간격은 글자 30 기준으로 잡는다. 글자 크기는 `--sl-font`로 바뀌므로 SVG 안 `font-size` 속성을 쓰지 않는다.
- **색.** [shell.md](shell.md) 색 정본을 따른다. 강조할 계열 하나만 blue(`data-on`), 나머지 grey-400, 의미색은 면·점·선에만. 큰 숫자는 blue-dark 또는 grey-900.

## 슬라이드 종류 `data-kind`

| 종류 | 몸 | 배치 |
| --- | --- | --- |
| (생략) 근거 | split: 그림(3) + 요점(2) | 몸(그림 + 요점)이 슬라이드 면의 60~80% |
| `cover` | 결론 h1 + 대표 도식 + 요약 0~1행 | `data-cover`로 도식 위치를 고른다 |
| `toc` | `ul.d0-slide__toc` | 그림 예외, 작은 점 불렛으로 제목만 표시 |
| `assertion` | 주장 한 문장(제목)만 | 그림 예외, Impact 기본, 제목이 세로 가운데 |
| `evidence` | 결론 제목 + 가로형 차트 + 해석 한 줄 | 그림(`figure`)이 슬라이드 면의 60~80% |
| `screenshot` | 결론 제목 + `figure.d0-shot` | 화면 상자가 몸 행 높이를 채운다(폭은 화면 비율, 왼쪽 정렬) |
| `breakdown` | 결론 제목 + 전체 → 구성 요소 도식 | 그림이 슬라이드 면의 60~80% |
| `stat` | 숫자 하나 + 해석 한 줄 | 큰 숫자가 그림 |
| `summary` | 참고용 정리 목록 3행 이내 | 그림 예외, 마지막 요청 장에는 쓰지 않는다 |
| `closing` | 큰 마무리 한 문장 + 구분선 + 작은 `dl` 메타 행. 상위 종류이고 `data-closing`이 세부(decision·request·action·criteria·takeaway) | 그림 예외, 마지막 장 전용 |

- **screenshot.** 화면·spotlight(`span.d0-shot__spot`)·번호 주석(`p.d0-shot__note`)·dim의 마크업과 CSS는 [mockup-frame.md](mockup-frame.md)가 정본이다.
  이 파일은 슬라이드 안 자리와 크기만 정한다: `figure.d0-shot`이 몸 행(`minmax(0, 1fr)`)을 채우고, 화면 상자는 그 높이를 다 쓰며 폭은 비율(기본 16:10)로 정해진다.
  주석·캡션은 본문 크기(2cqi)로 키운다. 화면 비율이 다르면 `.d0-shot__screen`에 `style="aspect-ratio: 가로 / 세로"`를 적는다. 730 미만에서는 높이 자동, 폭 100%.
- **그림 면적.** 그림 영역(`figure` 또는 `figure.d0-shot` bbox, 해석 줄·주석 포함. split이면 몸 전체)의 넓이 ÷ 슬라이드 면(패딩 포함) = 60~80%.
  제목 한 줄 기준으로 1280 한 장 모드에서 split·evidence 약 61%, breakdown·screenshot 약 64%다.
  split에 보조 한 줄(`__sub`)을 달면 몸이 약 55%로 떨어지므로 범위·조건은 출처 줄에 쓴다. 제목이 두 줄이면 그림이 그만큼 줄어든다.

## 커버 변형 `data-cover`

커버는 독자가 알아야 할 결론 문장과 대표 도식 하나로 시작한다. `비교 발표` 같은 유형·메타 정보는 크게 쓰지 않고 필요하면 작은 `.d0-slide__eyebrow`에만 둔다. 요약 3행을 반복하지 않고 도식·리드에 흡수하며, 결정할 것만 `dl.d0-slide__summary` 한 행으로 남길 수 있다.
`div.d0-slide__cover` 안에 `header.d0-slide__head`와 `figure.d0-slide__fig`를 둔다. 커버 도식은 근거 장의 60~80% 면적 게이트 대신 주제의 실체와 의미 있는 그림 면적을 확인한다.

| 값 | 위치 | 예시 |
| --- | --- | --- |
| `contrast` | 제목 아래 가로 A/B 대비 | compare |
| `bottom` | 제목 아래 가로 흐름·시간 막대 | flow, timeline |
| `side` | 오른쪽 기기·변화 차트·완성 화면, 그림 비율에 맞춘 열 | preview, report, guide |
| `center` | 가운데 경과선, 결론을 그 위에 가운데 정렬 | incident |
| `map` | 오른쪽 아래 작은 용어 지도 | faq |

```html
<section class="d0-slide" id="cover-example" data-kind="cover" data-cover="bottom" aria-labelledby="cover-example-t" tabindex="-1">
  <div class="d0-slide__cover">
    <header class="d0-slide__head"><h1 class="d0-slide__title" id="cover-example-t">요청 한 줄이 검사 뒤 설명 페이지 한 장이 된다</h1></header>
    <figure class="d0-slide__fig">
      <svg viewBox="0 0 800 180" role="img" aria-label="요청에서 검사까지 이어지는 과정"><title>요청에서 검사까지 이어지는 과정</title>
        <path class="d0-sl-link" d="M100 80H700"/>
        <circle cx="100" cy="80" r="24" fill="var(--d0-grey-200)"/><circle cx="400" cy="80" r="24" fill="var(--d0-blue)"/><circle cx="700" cy="80" r="24" fill="var(--d0-green)"/>
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

큰 한 문장을 세로 중앙에 두고(4.5cqi, 1280 한 장에서 약 49px), 그 아래 구분선과 작은 `dl.d0-slide__meta` 행을 둔다.
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
  안에는 문장 하나, 숫자 하나, 그림 하나 중 하나만 둔다. 카드·요점 목록·두 번째 그림 금지. 제목은 6cqi(1280에서 60px 이상).
  - `assertion` + impact가 기본형이다. 제목 한 문장이 그 하나다(리드·보조 줄도 두지 않는다).
  - `stat` + impact는 큰 숫자(10cqi, 96px 이상)가 그 하나다. 제목은 숫자를 읽는 법을 알려 주는 머리 줄이라 3.6cqi로 두어 숫자와 다투지 않게 한다.
  - 덱의 Impact 장은 전체의 20~30%다(8~9장이면 2장, 12장이면 3장). 판정은 덱 출력의 Slide Gate.
- **quiet.** 밀도를 낮추는 쉬는 장이다. 제목 + 한 줄, 또는 작은 그림 하나만 두고 요점 목록을 두지 않는다. 제목 굵기가 600으로 내려간다.
- 생략 = normal.

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

  <!-- stat + impact: 큰 숫자가 하나뿐인 그림 -->
  <section class="d0-slide" id="s-08" data-kind="stat" data-emphasis="impact" aria-labelledby="s-08-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-08-t">늦게 도착하는 알림이 절반에 가깝다</h2></header>
    <figure class="d0-slide__fig">
      <p class="d0-slide__stat"><data value="47">47</data>%</p>
      <figcaption class="d0-slide__note">10분 넘게 늦은 알림의 비율 · 지난달보다 12%p 늘었다</figcaption>
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

/* screenshot: 슬라이드 안 자리와 크기만. 화면·spot·dim·번호는 mockup-frame.md */
.d0-slide[data-kind="screenshot"] .d0-shot { min-height: 0; height: 100%; }
.d0-slide[data-kind="screenshot"] .d0-shot__screen {
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
.d0-slide[data-kind="stat"] .d0-slide__fig { grid-template-rows: 1fr auto; align-content: center; }
.d0-slide[data-kind="stat"] .d0-slide__note { color: var(--d0-grey-800); }

/* closing(decision·request·action·criteria·takeaway 공통): 세로 중앙의 큰 문장 하나 + 디바이더 아래 작은 사실 행 */
.d0-slide[data-kind="closing"] { grid-template-rows: minmax(0, 1fr) auto auto; }
.d0-slide[data-kind="closing"] .d0-slide__head { align-self: center; max-width: 88cqi; }
.d0-slide[data-kind="closing"] .d0-slide__title { font-size: 4.5cqi; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
.d0-slide__meta { margin: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2.4cqi; padding-top: 1.4cqi; border-top: 1px solid var(--d0-grey-200); }
.d0-slide__meta > div { display: grid; gap: 0.4cqi; align-content: start; }
.d0-slide__meta dt { color: var(--d0-grey-600); font-size: 1.4cqi; }
.d0-slide__meta dd { margin: 0; color: var(--d0-grey-700); font-size: 1.4cqi; line-height: var(--d0-leading-body); }

/* summary: 참고용 정리 목록 */
.d0-slide[data-kind="summary"] .d0-slide__points { align-self: start; }

/* 강조: impact = blue-light 전체 면, 큰 것 하나 */
.d0-slide[data-emphasis="impact"] { background: var(--d0-blue-light); box-shadow: none; }
.d0-slide[data-emphasis="impact"] .d0-slide__title { font-size: 6cqi; line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display); }
.d0-slide[data-kind="stat"][data-emphasis="impact"] .d0-slide__title { font-size: 3.6cqi; } /* 숫자가 그 하나 */
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
.d0-sl-head text { fill: var(--d0-grey-800); font-weight: 600; text-anchor: start; }

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
.d0-deck__hint { margin: 0 0 0 auto; color: var(--d0-grey-700); font-size: 13px; }
.d0-deck__hint [data-hint="touch"] { display: none; }
@media (pointer: coarse) {
  .d0-deck__hint [data-hint="key"] { display: none; }
  .d0-deck__hint [data-hint="touch"] { display: inline; }
}

/* 한 장 모드: JS가 data-mode="single"을 붙일 때만. 화면에서만 걸고 인쇄는 세로 나열로 돌아간다 */
@media screen {
  html:has(.d0-deck[data-mode="single"]) { overflow: hidden; scrollbar-gutter: auto; }
  .d0-deck[data-mode="single"] {
    --deck-gutter: 32px;
    --deck-chrome: 88px;                 /* 위 16 + 네비 44 + 사이 12 + 아래 16 */
    --slide-w: min(100vw - 2 * var(--deck-gutter), (100dvh - var(--deck-chrome)) * 16 / 9);
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
  }
}
@keyframes d0-deck-in { from { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .d0-deck[data-mode="single"] > .d0-slide[data-active] { animation: none; transition: none; }
}

/* 좁은 슬라이드(730px 미만, 본문이 11px 아래로 내려가는 폭): 16:9를 풀고 px 고정 */
@container (max-width: 730px) {
  .d0-slide { aspect-ratio: auto; gap: 16px; padding: 20px 16px 14px; }
  .d0-slide[data-kind="cover"] { grid-template-rows: auto auto auto; }
  .d0-slide__cover,
  .d0-deck[data-pattern] .d0-slide__cover { grid-template-columns: 1fr; gap: 16px; }
  .d0-slide__cover > .d0-slide__fig { height: auto; }
  .d0-slide[data-cover="center"] .d0-slide__head { max-width: none; }
  .d0-slide:is([data-cover="contrast"], [data-cover="bottom"], [data-cover="center"]) .d0-slide__fig { --sl-font: 30px; }
  .d0-slide[data-kind="cover"] .d0-slide__summary dd { font-size: 12px; }
  .d0-slide[data-kind="closing"] { min-height: min(560px, calc(100dvh - 116px)); }
  .d0-slide[data-kind="closing"] .d0-slide__head { max-width: none; }
  .d0-slide[data-kind="closing"] .d0-slide__title { font-size: 24px; }
  .d0-slide__meta { grid-template-columns: 1fr; gap: 8px; padding-top: 12px; }
  .d0-slide__meta > div { grid-template-columns: 48px 1fr; gap: 8px; }
  .d0-slide__meta dt, .d0-slide__meta dd { font-size: 12px; }
  .d0-slide__head { gap: 6px; }
  .d0-slide__eyebrow { font-size: 12px; }
  .d0-slide__title { font-size: 20px; }
  h1.d0-slide__title { font-size: 26px; }
  .d0-slide[data-kind="assertion"] .d0-slide__title,
  .d0-slide[data-emphasis="impact"] .d0-slide__title { font-size: 28px; }
  .d0-slide[data-kind="stat"][data-emphasis="impact"] .d0-slide__title { font-size: 20px; }
  .d0-slide__lead { font-size: 17px; }
  .d0-slide__sub { font-size: 15px; }
  .d0-slide__fig { gap: 8px; }
  .d0-slide__stage { padding: 12px; }
  .d0-slide__fig svg,
  .d0-slide[data-kind] .d0-slide__fig svg { max-width: none; height: auto; }
  .d0-slide[data-kind="evidence"] .d0-slide__fig,
  .d0-slide[data-kind="breakdown"] .d0-slide__fig { --sl-font: 30px; }
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
  .d0-slide[data-kind="screenshot"] .d0-shot,
  .d0-slide[data-kind="screenshot"] .d0-shot__screen { height: auto; width: 100%; justify-self: stretch; }
  .d0-slide[data-kind="screenshot"] .d0-shot__note { font-size: 15px; }
  .d0-slide[data-kind="screenshot"] .d0-shot figcaption { font-size: 13px; }
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
  var pointerFocus = false;                                /* 마지막 포커스가 마우스·터치로 생겼나 */
  document.addEventListener('pointerdown', function () { pointerFocus = true; }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Tab') pointerFocus = false; }, true);

  function indexOfId(id) {
    for (var i = 0; i < slides.length; i++) if (slides[i].id === id) return i;
    return -1;
  }
  function fromHash() {
    var id = '';
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (err) { id = ''; }
    return id ? indexOfId(id) : -1;
  }
  function show(i, opt) {
    opt = opt || {};
    i = Math.max(0, Math.min(slides.length - 1, i));
    if (i === idx) return;
    var old = slides[idx];
    var a = document.activeElement;
    /* 사라지는 장 안의 컨트롤에 있던 포커스, 또는 키보드로 그 장 자체에 있던 포커스만 새 장으로 옮긴다.
       마우스로 눌러 장 자체에 생긴 포커스는 옮기지 않는다(넘길 때마다 포커스 링이 생긴다) */
    var moveFocus = !!(old && a && old.contains(a) && (a !== old || !pointerFocus));
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
    else if (k === 'Home') { e.preventDefault(); show(0); return; }
    else if (k === 'End') { e.preventDefault(); show(slides.length - 1); return; }
    else if (k === 'f' || k === 'F') { toggleFullscreen(); return; }
    else return;
    e.preventDefault();
    if (paging && pageWithin(d)) return;
    show(idx + d);
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
    if (i >= 0) show(i, { hash: false });
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
  show(start >= 0 ? start : 0, { hash: false });
  deck.setAttribute('data-mode', 'single');               /* 여기까지 왔을 때만 한 장 모드 */
})();
```

- 쪽수 `n / N`은 목차를 제외한 슬라이드마다 마크업에 직접 쓴다(스크립트가 없을 때와 인쇄에서 보인다). 한 장 모드에서는 네비 쪽수가 대신 보인다. 슬라이드를 빼거나 더하면 쪽수를 함께 고친다.
- 차트·도식을 바꿀 때도 기본 SVG는 viewBox 폭 400·글자 17·최대 42cqi, 가로형은 800·글자 20(좁은 화면 30)·최대 84cqi를 유지한다.
  다른 도식 모양은 [diagram.md](diagram.md)를 따르되 클래스는 이 파일의 `d0-sl-*` 규칙(강조 하나만 blue)으로 칠한다.
- 스크롤 리빌 모션은 붙이지 않는다. 장을 바꿀 때의 짧은 opacity 페이드만 있고 reduced-motion이면 즉시 바뀐다.
- 화면은 넓은데 높이가 낮아(예: 1280×400) 슬라이드 폭만 730px 아래로 내려가면, 장은 16:9를 유지한 채 안쪽 글자만 px 고정으로 바뀌고 넘치는 몫은 장 안에서 스크롤한다.

## 덱 게이트 (구현)

의미 검사(한 장 한 주장, 결론 제목, 제목만 읽어도 이어짐, Impact 비율 등)는 [덱 출력](../output/deck.md)의 Slide Gate가 먼저다.
여기는 마크업·타이포·키·hash·인쇄·reduced-motion·375·iframe을 코드와 측정으로 확인한다. 나머지(토큰 인라인, 시맨틱, 접근성, 색 규칙, 개행)는 page와 같다.

아래 체크 항목은 그대로 적용하되 본문 3줄·본문 20~24px·그림 영역 60~80%는 Presentation 기준이다. Slidedoc의 해당 세 기준만 덱 출력의 전달 하위 모드 표와 위 CSS로 판정한다. 제목·Meta·장수·한 장 보기와 나머지 구현 검사는 공통이다.

**HARD (코드로 확인)**

- [ ] `main.d0-deck[data-pattern]`이 하나이고 `data-pattern`이 패턴 8개 중 하나다. 슬라이드(`.d0-slide`)는 표지·목차 포함 5~12장이다
- [ ] 마지막 장은 `data-kind="closing"`이고 `data-closing`이 decision·request·action·criteria·takeaway 중 하나이며 큰 제목 한 문장 + 구분선 + 작은 `dl.d0-slide__meta` 2~3칸을 두고 같은 무게의 불릿 목록·Impact가 없다
- [ ] 첫 장이 `data-kind="cover"` + h1이고 바로 다음 장이 `nav[data-kind="toc"]`다. 목차가 `ul.d0-slide__toc`이고 `li` 수 = 표지·목차를 뺀 장 수, 항목 글자 = 각 장 제목, `href` = 그 장 `id`; 목차에는 번호·쪽수가 없다
- [ ] `data-kind`가 정본 값(생략 | cover | toc | assertion | evidence | screenshot | breakdown | stat | summary | closing)만 쓴다
- [ ] 근거(생략)·`evidence`·`breakdown` 장마다 `figure.d0-slide__fig`가 정확히 1개이고 그 안에 `role="img"` + `<title>`을 가진 SVG가 있다.
      `screenshot`은 `figure.d0-shot` 1개, `stat`은 `.d0-slide__stat` 1개. `toc`·`summary`·`closing`·`assertion`은 그림 예외이고 `cover`에는 대표 도식이 있다
- [ ] `data-emphasis="impact"` 장에 카드·요점 목록·두 번째 그림이 없다
- [ ] 슬라이드당 `li` 3개 이하(`toc` 제외), 본문 텍스트(`p`·`li`·`dd`, 제목·쪽수 제외)가 렌더 기준 3줄 이하다
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
- [ ] 1280 한 장 모드에서 제목 36~44px, 표지 h1 56~72px, Impact 제목 60px 이상, closing 제목은 Lead~Display 사이(약 49px), 리드 24~30px, 본문 20~24px, Meta 14~18px, 큰 숫자 72~120px이다
- [ ] SVG 글자 렌더 크기(font-size × SVG 렌더 배율)가 1280에서 28px 이하, 375에서 11px 이상이다
- [ ] `evidence`·`breakdown`·`screenshot`의 `figure`, 근거 split의 몸이 슬라이드 면(패딩 포함)의 60~80%다
- [ ] 375×812에서 장이 16:9를 풀고, 글자가 11px 이상, 페이지 가로 스크롤이 없으며, 좌우 스와이프(48px 초과)로 장이 넘어간다. 긴 장은 장 안에서 세로로 스크롤된다

## 금지

- 명사 제목(`현황`, `분석 결과`), 슬라이드 하나에 그림 둘 이상, 불릿 4개 이상, Presentation의 여러 줄 문단 또는 Slidedoc의 최대 8줄 상한을 넘긴 본문.
- 슬라이드 높이를 px로 고정하기, `vw` 글자 크기, 데스크톱에서 16:9 풀기.
- 자동 넘김, opacity 페이드 외의 전환(밀기·확대·3D 넘김), 스크롤 리빌, reduced-motion에서 전환 남기기.
- 키보드 이동을 입력 칸 안에서 가로채기, 버튼 포커스 상태의 Space를 넘김 키로도 처리하기(이중 전진), CSS만으로 한 장 모드 켜기(JS 실패 시 장이 사라진다).
- 목차 없는 덱, 목차 글자와 슬라이드 제목이 다른 덱, 쪽수를 `aria-label`에만 두기.
- Impact 면에 카드·어두운 배경, 계열마다 다른 색, 그라디언트 배경, 그림자 짙은 카드, 의미 없는 아이콘·사람 일러스트.
