# slide-deck — 발표용 슬라이드 덱

slides 프리셋([slides.md](../formats/slides.md))의 페이지 골격이다. 페이지가 곧 덱이고, 16:9 슬라이드를
세로로 나열해 스크롤하거나 키보드로 한 장씩 넘긴다. 문서형 `main.d0-page` 대신 `main.d0-deck`을 쓴다.

## 해부 구조

- **덱** `main.d0-deck[data-variant]` 하나. 변형 이름표는 `report`·`proposal`·`strategy`·`tech`다(스타일은 같다).
  폭은 컨테이너(최대 1200px)이고 슬라이드 사이 세로 간격은 40px(모바일 32px)이다.
- **슬라이드** `section.d0-slide` = 머리 → 몸 → 발. `id`(`s-01`…), `aria-labelledby`(제목 id), `tabindex="-1"`(키보드 이동 때 포커스).
  16:9(`aspect-ratio: 16 / 9`), 흰 면 + radius card, 안쪽 패딩은 슬라이드 폭에 비례(위 4.5%, 좌우 5%, 아래 3%).
  - 머리 `header.d0-slide__head`: 액션 타이틀(`h1` 표지만, 나머지 `h2`, `.d0-slide__title`) + 보조 한 줄(`p.d0-slide__sub`, 선택).
  - 몸: 근거 그림 하나(`figure.d0-slide__fig` = 무대 `div[data-stage]` 안 SVG + 해석 한 줄 `figcaption`).
    **기본 배치는 그림 + 요점 나란히(split)다.** `div.d0-slide__body[data-layout="split"]` 안에 그림과 요점(`ul.d0-slide__points`, 2~3개)을 둔다.
    그림만 전체 폭으로 두면 SVG `max-width: 42cqi` 때문에 무대 좌우가 비므로, 전체 폭 그림은 예외다
    (가로로 긴 도식처럼 그림 자체가 무대 폭을 채울 때만, 요점은 `figcaption` 한 줄로 줄인다).
  - 발 `footer.d0-slide__foot`: 출처 한 줄(`p.d0-slide__src`, 선택) + 쪽수 `p.d0-slide__num` `n / N`(렌더 텍스트).
- **슬라이드 종류** `data-kind`: 없음(근거 슬라이드, 기본), `cover`(표지: h1 + 요약 3행 `dl`), `toc`(제목 목차),
  `stat`(핵심 수치: 숫자 하나 + 라벨 + 증감 한 줄), `summary`(마지막 할 일·요약: 3행 이내 목록).
  그림 예외는 `cover`·`toc`·`summary`뿐이다. `stat`은 큰 숫자가 그림이다.
- **제목 목차** `nav.d0-slide[data-kind="toc"]`: 표지 바로 다음 장. h2 `제목만 읽기` + `ol` + 항목마다 `a href="#s-03"`.
  항목 글자는 해당 슬라이드 액션 타이틀과 같다. 표지와 목차 자신은 넣지 않는다.
- **헤딩 순서.** 표지 h1 → 목차 h2 → 슬라이드 h2. 슬라이드 안에서 h3 이하는 쓰지 않는다. `main`은 덱 하나다.
- **타이포**(`cqi` = 슬라이드 안쪽 폭의 1%, 1200px 슬라이드의 안쪽 폭 1080px 기준 환산): 액션 타이틀 3.1cqi(33px)/700, 표지 h1 3.3cqi(36px)/700,
  보조 1.6cqi(17px)/400 grey-600, 본문·요점 1.8cqi(19px)/400 grey-800, 해석 1.5cqi(16px) grey-600, 출처·쪽수 1.2cqi(13px) grey-600, 핵심 수치 10cqi(108px)/600.
  슬라이드 폭에 비례하므로 화면이 줄면 덱 전체가 같은 비율로 줄어든다. 1280px 화면(슬라이드 1136px)에서 타이틀은 약 32px다.
- **그림 글자.** 슬라이드 SVG는 viewBox 폭 400, 글자 17, `max-width: 42cqi`다. 1200px 슬라이드에서 라벨이 약 19px(본문과 같은 크기),
  375px 화면에서 11.5px 안팎이다. 문서형 diagram의 데스크톱 16px 상한 대신 이 값을 쓴다(발표 화면 예외). viewBox 폭을 넓히면 글자를 같은 비율로 키운다(W ≤ 23.5 × f).
- **색.** shell.md 색 정본을 따른다. 강조할 계열 하나만 blue(`data-on`), 나머지 grey-400, 의미색은 상태에만(면·점·선). 핵심 수치는 grey-900 또는 blue-dark.

## 언제 쓰나

- slides 프리셋 전용이다. 문서형 프리셋 페이지 안에 슬라이드 한 장을 끼워 넣지 않는다(그건 diagram + section-head다).
- 슬라이드 수는 표지·목차를 포함해 5~12장이다. 넘으면 덱을 나눈다.
- 모바일: 슬라이드 폭이 730px 미만이면(본문이 11px 아래로 내려가는 폭, 375px 화면은 항상) 16:9를 풀고 세로로 늘린다.
  글자는 px 고정값(제목 20, 본문 15, 해석 13, 수치 48)으로 바뀐다. 데스크톱에서는 비율을 풀지 않는다.

## 스니펫

```html
<main class="d0-deck" data-variant="report">
  <section class="d0-slide" id="s-01" data-kind="cover" aria-labelledby="s-01-t" tabindex="-1">
    <header class="d0-slide__head">
      <p class="d0-slide__eyebrow">알림 개편 · 3분기 업무 보고</p>
      <h1 class="d0-slide__title" id="s-01-t">알림 개편은 일정대로 가고, 남은 결정은 발송 주기 하나다</h1>
    </header>
    <dl class="d0-slide__summary">
      <div><dt>현재 상태</dt><dd>새 알림 화면을 팀 A가 쓰고 있다</dd></div>
      <div><dt>문제</dt><dd>재시도가 늘어 발송이 늦어진다</dd></div>
      <div><dt>결정할 것</dt><dd>발송 주기를 매일과 매주 중에 고른다</dd></div>
    </dl>
    <footer class="d0-slide__foot">
      <p class="d0-slide__src"><kbd>←</kbd> <kbd>→</kbd> 키로 넘겨요 · <kbd>F</kbd> 전체 화면</p>
      <p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>1 / 6</p>
    </footer>
  </section>

  <nav class="d0-slide" id="s-02" data-kind="toc" aria-labelledby="s-02-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-02-t">제목만 읽기</h2></header>
    <ol class="d0-slide__toc">
      <li><a href="#s-03">재시도가 4주 만에 두 배 넘게 늘었다</a></li>
      <li><a href="#s-04">발송이 늦은 알림이 전체의 절반에 가깝다</a></li>
      <!-- 표지·목차를 뺀 모든 슬라이드 제목을 순서대로 -->
    </ol>
    <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>2 / 6</p></footer>
  </nav>

  <section class="d0-slide" id="s-03" aria-labelledby="s-03-t" tabindex="-1">
    <header class="d0-slide__head">
      <h2 class="d0-slide__title" id="s-03-t">재시도가 4주 만에 두 배 넘게 늘었다</h2>
      <p class="d0-slide__sub">주별 재시도 건수, 팀 A 기준</p>
    </header>
    <div class="d0-slide__body" data-layout="split">
    <figure class="d0-slide__fig">
      <div class="d0-slide__stage" data-stage>
        <svg viewBox="0 0 400 200" role="img" aria-labelledby="s-03-f">
          <title id="s-03-f">주별 재시도 건수. 1주 120건, 2주 135건, 3주 180건, 4주 260건.</title>
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
      </div>
      <figcaption class="d0-slide__note">늘어난 몫은 대부분 마지막 주에 몰렸다.</figcaption>
    </figure>
    <ul class="d0-slide__points">
      <li>앞 세 주는 조금씩 늘었다</li>
      <li>재시도가 쌓이면 알림 도착이 늦어진다</li>
    </ul>
    </div>
    <footer class="d0-slide__foot">
      <p class="d0-slide__src">출처: 발송 기록 집계(합성)</p>
      <p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>3 / 6</p>
    </footer>
  </section>

  <!-- 예외: 그림이 무대 폭을 채울 때만 split 없이 figure 하나를 몸에 바로 둔다 -->
  <!--
  <figure class="d0-slide__fig">…무대 + figcaption…</figure>
  -->

  <section class="d0-slide" id="s-04" data-kind="stat" aria-labelledby="s-04-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-04-t">발송이 늦은 알림이 전체의 절반에 가깝다</h2></header>
    <figure class="d0-slide__fig">
      <p class="d0-slide__stat"><data value="47">47</data>%</p>
      <figcaption class="d0-slide__note">10분 넘게 늦게 도착한 알림의 비율 · 지난달보다 12%p 늘었다</figcaption>
    </figure>
    <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>4 / 6</p></footer>
  </section>
</main>
```

```css
/* shell.md 기본값(토큰 인라인, color-scheme, box-sizing, body 글꼴·keep-all, .d0-sr-only, :focus-visible, reduced-motion)은 그대로 쓴다.
   덱 페이지는 .d0-page 대신 .d0-deck을 쓰고, body 배경만 grey-100으로 바꿔 흰 슬라이드 면이 보이게 한다. */
body { background: var(--d0-grey-100); }
.d0-deck {
  container-type: inline-size;              /* 슬라이드 자신의 cqi가 덱 폭(= 슬라이드 폭)을 따르게 한다 */
  display: grid; gap: 40px;
  max-width: 1200px; margin: 0 auto; padding: 40px 32px 96px;
}
.d0-slide {
  container-type: inline-size;              /* 안쪽 글자의 cqi = 슬라이드 폭 */
  aspect-ratio: 16 / 9;
  display: grid; grid-template-rows: auto minmax(0, 1fr) auto; gap: 2.4cqi;
  padding: 4.5cqi 5cqi 3cqi;
  overflow: hidden;
  background: #fff; border-radius: var(--d0-radius-card); box-shadow: var(--d0-shadow-card);
  scroll-margin-top: 24px;
}
.d0-slide:focus { outline: none; }
.d0-slide:focus-visible { outline: 2px solid var(--d0-blue-dark); outline-offset: 4px; }

.d0-slide__head { display: grid; gap: 0.8cqi; }
.d0-slide__eyebrow { margin: 0; color: var(--d0-grey-600); font-size: 1.3cqi; font-weight: 600; }
.d0-slide__title {
  margin: 0; color: var(--d0-grey-900);
  font-size: 3.1cqi; font-weight: 700;
  line-height: var(--d0-leading-title); letter-spacing: var(--d0-tracking-title);
  text-wrap: balance;
}
h1.d0-slide__title { font-size: 3.3cqi; letter-spacing: var(--d0-tracking-display); }
.d0-slide__sub { margin: 0; color: var(--d0-grey-600); font-size: 1.6cqi; }

/* 몸: 그림 하나 */
.d0-slide__fig { margin: 0; min-height: 0; display: grid; grid-template-rows: minmax(0, 1fr) auto; gap: 1.2cqi; }
.d0-slide__stage {
  min-height: 0; display: grid; place-items: center;
  padding: 2.4cqi; background: var(--d0-grey-50); border-radius: var(--d0-radius-card);
}
.d0-slide__stage svg { display: block; width: 100%; max-width: 42cqi; height: 100%; max-height: 100%; overflow: visible; }
.d0-slide__note { margin: 0; color: var(--d0-grey-600); font-size: 1.5cqi; }

.d0-slide__body[data-layout="split"] { min-height: 0; display: grid; grid-template-columns: 3fr 2fr; gap: 3cqi; align-items: center; }
.d0-slide__body[data-layout="split"] > .d0-slide__fig { height: 100%; }
.d0-slide__points { margin: 0; padding-left: 1.2em; display: grid; gap: 1.2cqi; color: var(--d0-grey-800); font-size: 1.8cqi; line-height: var(--d0-leading-body); }
.d0-slide__points ::marker { color: var(--d0-blue); }

/* 표지 요약 3행 */
.d0-slide__summary { margin: 0; align-self: center; display: grid; }
.d0-slide__summary > div { display: grid; grid-template-columns: 12cqi 1fr; gap: 2cqi; padding: 1.4cqi 0; border-top: 1px solid var(--d0-grey-100); }
.d0-slide__summary > div:last-child { border-bottom: 1px solid var(--d0-grey-100); }
.d0-slide__summary dt { color: var(--d0-grey-600); font-size: 1.5cqi; font-weight: 600; }
.d0-slide__summary dd { margin: 0; color: var(--d0-grey-900); font-size: 1.8cqi; }
.d0-slide__summary > div:last-child dt { color: var(--d0-blue-dark); }

/* 제목 목차 */
.d0-slide__toc { margin: 0; padding: 0; list-style: none; counter-reset: d0-toc 2; align-self: start; display: grid; gap: 0.4cqi; }
.d0-slide__toc li { counter-increment: d0-toc; }
.d0-slide__toc a {
  display: grid; grid-template-columns: 4cqi 1fr; align-items: baseline;
  min-height: 24px; padding: 0.7cqi 0;
  color: var(--d0-grey-900); font-size: 1.8cqi; text-decoration: none;
  border-bottom: 1px solid var(--d0-grey-100);
}
.d0-slide__toc a::before { content: counter(d0-toc); color: var(--d0-blue-dark); font-weight: 600; font-variant-numeric: tabular-nums; }
.d0-slide__toc a:hover { color: var(--d0-blue-dark); }

/* 핵심 수치 */
.d0-slide__stat {
  margin: 0; align-self: center; justify-self: start;
  color: var(--d0-blue-dark); font-size: 10cqi; font-weight: 600;
  line-height: var(--d0-leading-display); letter-spacing: var(--d0-tracking-display);
  font-variant-numeric: tabular-nums;
}
.d0-slide[data-kind="stat"] .d0-slide__fig { grid-template-rows: 1fr auto; align-content: center; }
.d0-slide[data-kind="stat"] .d0-slide__note { font-size: 1.8cqi; color: var(--d0-grey-800); }

/* 발: 출처 + 쪽수 */
.d0-slide__foot { display: flex; justify-content: space-between; align-items: baseline; gap: 2cqi; }
.d0-slide__src { margin: 0; color: var(--d0-grey-600); font-size: 1.2cqi; }
.d0-slide__num { margin: 0 0 0 auto; color: var(--d0-grey-600); font-size: 1.2cqi; font-variant-numeric: tabular-nums; }
.d0-slide kbd {
  display: inline-block; min-width: 1.6em; padding: 0 0.4em;
  border: 1px solid var(--d0-grey-300); border-radius: var(--d0-radius-sm);
  font: inherit; text-align: center; color: var(--d0-grey-800);
}

/* SVG 차트: 강조 계열 하나만 blue */
.d0-sl-axis { stroke: var(--d0-grey-300); stroke-width: 1.5; stroke-linecap: round; }
.d0-sl-bar { fill: var(--d0-grey-400); }
.d0-sl-bar[data-on] { fill: var(--d0-blue); }
.d0-sl-value text, .d0-sl-label text { font-family: var(--d0-font); font-size: 17px; text-anchor: middle; font-variant-numeric: tabular-nums; }
.d0-sl-value text { fill: var(--d0-grey-700); font-weight: 600; }
.d0-sl-value text[data-on] { fill: var(--d0-blue-dark); }
.d0-sl-label text { fill: var(--d0-grey-600); }

/* 좁은 슬라이드(730px 미만, 본문이 11px 아래로 내려가는 폭): 16:9를 풀고 세로로 늘린다 */
@container (max-width: 730px) {
  .d0-slide { aspect-ratio: auto; gap: 16px; padding: 20px 16px 14px; }
  .d0-slide__head { gap: 6px; }
  .d0-slide__eyebrow { font-size: 12px; }
  .d0-slide__title { font-size: 20px; }
  h1.d0-slide__title { font-size: 24px; }
  .d0-slide__sub { font-size: 14px; }
  .d0-slide__fig { gap: 8px; }
  .d0-slide__stage { padding: 12px; }
  .d0-slide__stage svg { max-width: none; height: auto; }
  .d0-slide__note { font-size: 13px; }
  .d0-slide__body[data-layout="split"] { grid-template-columns: 1fr; gap: 16px; }
  .d0-slide__points, .d0-slide__summary dd, .d0-slide__toc a, .d0-slide[data-kind="stat"] .d0-slide__note { font-size: 15px; }
  .d0-slide__points { gap: 6px; }
  .d0-slide__summary > div { grid-template-columns: 1fr; gap: 2px; padding: 10px 0; }
  .d0-slide__summary dt, .d0-slide__src, .d0-slide__num { font-size: 12px; }
  .d0-slide__toc a { grid-template-columns: 28px 1fr; padding: 8px 0; }
  .d0-slide__stat { font-size: 48px; }
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
}
```

```js
/* 키보드 이동: ←/→/PageUp/PageDown으로 이전·다음 슬라이드. F는 전체 화면(실패해도 무해). */
(function () {
  var deck = document.querySelector('.d0-deck');
  if (!deck) return;
  var slides = Array.prototype.slice.call(deck.querySelectorAll('.d0-slide'));
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  function current() {
    var best = 0, bestDist = Infinity;
    slides.forEach(function (s, i) {
      var d = Math.abs(s.getBoundingClientRect().top);
      if (d < bestDist) { bestDist = d; best = i; }
    });
    return best;
  }
  function go(i) {
    var s = slides[Math.max(0, Math.min(slides.length - 1, i))];
    s.focus({ preventScroll: true });
    s.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block: 'start' });
  }
  function toggleFullscreen() {
    try {
      var p = document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
      if (p && p.catch) p.catch(function () {});
    } catch (err) { /* 전체 화면을 못 쓰는 환경: 아무것도 하지 않는다 */ }
  }

  document.addEventListener('keydown', function (e) {
    if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target;
    if (t && t.closest && t.closest('input, textarea, select, [contenteditable=""], [contenteditable="true"], [role="tablist"]')) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); go(current() + 1); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(current() - 1); }
    else if (e.key === 'f' || e.key === 'F') { toggleFullscreen(); }
  });

  /* 제목 목차 링크: 해당 슬라이드로 이동하고 포커스도 옮긴다 */
  deck.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.d0-slide__toc a[href^="#"]');
    if (!a) return;
    var i = slides.indexOf(document.getElementById(a.getAttribute('href').slice(1)));
    if (i < 0) return;
    e.preventDefault();
    go(i);
  });
})();
```

- 쪽수 `n / N`은 마크업에 직접 쓴다(스크립트가 없어도 보인다). 슬라이드를 빼거나 더하면 모든 쪽수와 목차를 함께 고친다.
- 목차 번호는 CSS 카운터로 3부터 센다(`counter-reset: d0-toc 2`). 쪽수와 같은 번호라 목차 번호로 슬라이드를 찾는다.
- 차트·도식을 바꿀 때도 viewBox 폭 400·글자 17·`max-width: 42cqi`를 유지한다. 다른 도식 모양은 [diagram.md](diagram.md)를 따르되 클래스는 이 파일의 `d0-sl-*` 규칙(강조 하나만 blue)으로 칠한다.
- 스크롤 리빌 모션은 붙이지 않는다. 슬라이드는 처음부터 다 보인다. 이동 스크롤만 reduced-motion이면 즉시다.

## 덱 게이트

slides 프리셋은 문서형 게이트 중 페이지 섹션 수·앞쪽 핵심 섹션 그림·첫 화면·720px 프레임·히어로 위치·섹션 간격·첫 화면 면적과 색 비중·
h1 32/h2 20 고정 타이포·도식 라벨 데스크톱 16px 상한·본문 50자 대신 아래를 쓴다. 나머지(토큰 인라인, 시맨틱, 접근성, 색 규칙, 개행 규칙)는 그대로다.

**HARD (코드로 확인)**

- [ ] `main.d0-deck`이 하나이고 슬라이드(`.d0-slide`)가 표지·목차 포함 5~12장이다
- [ ] 모든 슬라이드(`toc` 제외)의 제목이 액션 타이틀이다: 서술어(`다`·`요`·`죠`·`니다`로 끝나는 문장)로 끝나고 명사로만 끝나지 않는다
- [ ] 첫 장이 `data-kind="cover"`이고 h1이 있으며, 그 바로 다음 장이 `nav[data-kind="toc"]`다. 목차 `li` 수 = 표지·목차를 뺀 슬라이드 수이고, 항목 글자가 각 슬라이드 제목과 같으며 `href`가 그 슬라이드 `id`를 가리킨다
- [ ] 근거 슬라이드(`data-kind` 없음)마다 `figure.d0-slide__fig`가 정확히 1개이고 그 안에 `role="img"`와 `<title>`을 가진 SVG가 있다. `stat`은 `.d0-slide__stat` 1개. `cover`·`toc`·`summary`만 그림 없이 둔다
- [ ] 슬라이드당 `li`가 3개 이하다(`toc` 제외), 본문 텍스트(`p`·`li`·`dd`, 제목·쪽수 제외)가 렌더 기준 3줄 이하다
- [ ] 슬라이드마다 쪽수 `n / N`이 렌더 텍스트로 있고 순서가 맞다
- [ ] 슬라이드가 `section`(목차는 `nav`) + `aria-labelledby` + `tabindex="-1"`이고, 헤딩은 표지 h1 → h2만 쓴다
- [ ] 같은 숫자 문자열 2회 이하 규칙은 제목 목차의 반복을 빼고 센다
- [ ] 차트·도식 하나에 blue 계열 강조(`data-on`)가 1계열이다. 나머지 계열은 grey, 의미색은 상태 표식에만, 그라디언트·3D·장식 아이콘이 없다
- [ ] ←/→/PageUp/PageDown 키가 이전·다음 슬라이드로 포커스와 스크롤을 옮기고, 입력 칸 안에서는 가로채지 않는다
- [ ] `@media print`에서 슬라이드마다 `break-after: page`이고 `@page { size: landscape }`다

**VISUAL (측정으로 확인)**

- [ ] 1280px 화면에서 모든 슬라이드의 높이 ÷ 폭이 0.5625(±1px)이고 내용이 넘치지 않는다(`scrollHeight` ≤ `clientHeight`)
- [ ] 1280px 화면(슬라이드 약 1136px)에서 액션 타이틀 렌더 크기가 28~36px, 본문 17px 이상, 가장 작은 글자 12px 이상, 핵심 수치 96px 이상이다
- [ ] SVG 글자 렌더 크기가 1280px에서 22px 이하, 375px에서 11px 이상이다(font-size × SVG 렌더 폭 ÷ viewBox 폭)
- [ ] 1280px에서 근거 슬라이드의 무대 좌우가 비지 않는다: 기본은 split(그림 + 요점)이고, 전체 폭 그림은 SVG가 무대 안쪽 폭의 대부분을 채울 때만 쓴다
- [ ] 375px 화면에서 슬라이드가 비율을 풀어 세로로 늘어나고, 글자가 11px 이상이며, 페이지 가로 스크롤이 없다
- [ ] 제목 목차만 위에서 아래로 읽어도 주장 → 근거 → 할 일이 이어진다(목차를 소리 내어 읽어 본다)

## 금지

- 명사 제목(`현황`, `분석 결과`), 슬라이드 하나에 그림 둘 이상, 불릿 4개 이상, 여러 줄 문단.
- 슬라이드 높이를 px로 고정하기, `vw` 글자 크기(덱 폭과 따로 논다), 데스크톱에서 16:9 풀기.
- 자동 넘김·전환 애니메이션·스크롤 리빌, 키보드 이동을 입력 칸 안에서 가로채기.
- 목차 없는 덱, 목차 글자와 슬라이드 제목이 다른 덱, 쪽수를 `aria-label`에만 두기.
- 계열마다 다른 색, 그라디언트 배경, 그림자 짙은 카드, 의미 없는 아이콘·사람 일러스트.
