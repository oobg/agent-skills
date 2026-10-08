# deck 레시피

발표·화면 공유로 한 장씩 넘기며 설득하는 덱이다. 요청에 `발표`, `슬라이드`, `장표`, `덱`, `화면 공유` 같은 신호가 있을 때 쓴다. 혼자 읽는 문서면 page 레시피다.

## 순서

1. **독자와 결정.** 누가 보는지, 다 보고 무엇을 이해·결정해야 하는지 한 문장으로 적는다.
2. **장 수.** 사용자가 정한 장 수를 따른다. 정하지 않았으면 주장 수만큼이고 표지·마지막 장을 합쳐 대개 5~12장이다.
3. **제목 목록.** 장마다 결론 문장 제목을 먼저 적고 이어 읽어 본다. 제목만 읽어도 `주장 → 근거 → 결정`이 이어져야 한다. 앞 장이 다음 장을 필요하게 만들지 않으면 그 장을 뺀다.
4. **장마다 주장 하나와 그 근거 하나.** 주장 문장만 띄우는 장보다, 그 주장을 증명하는 그림을 같은 장에 둔다. 문서 목차(배경 → 요약 → 영향)를 장으로 옮기지 않는다.
5. **만들지 않는 장.** 목차, 영향 요약, 앞 내용을 되짚는 장, 내용 없는 구분 장은 자동으로 만들지 않는다. 사용자가 원하거나 긴 덱에서 탐색에 실제로 필요할 때만 둔다. 영향은 관련 근거 장이나 마지막 결정 장에 붙인다.
6. **조립과 검토.** 아래 뼈대로 쓰고 `python3 scripts/inline_assets.py deck out.html`로 채운 뒤 [final-review.md](../final-review.md)를 거친다. 모든 장을 넘겨 보며 본다.

## 장 종류 (`data-kind`)

| 종류 | 몸 | 언제 |
| --- | --- | --- |
| `cover` | 결론 h1 + 대표 그림 + 결정할 것 0~1행 | 첫 장. 제목만 보고도 결론과 결정할 것을 안다 |
| (생략) 근거 | `div.d0-slide__body[data-layout="split"]` = 그림 + 요점 2~3개 | 기본 근거 장 |
| `evidence` | 가로형 차트 하나 + 해석 한 줄 | 차트가 넓어야 읽힐 때 |
| `breakdown` | 전체 → 구성 요소 2~5개 | 무엇이 무엇으로 이루어졌나 |
| `screenshot` | 실제 화면 + 봐야 할 곳 스포트라이트 + 번호 주석 | 화면을 짚을 때. 마크업은 [blocks/mockup-frame.md](../blocks/mockup-frame.md) |
| `stat` | 큰 숫자 + 기준 줄 + 근거 그림(`data-layout="asym"`) | 숫자가 주장일 때. 숫자만 남기는 형태는 숫자 자체가 결론일 때만 |
| `assertion` | 주장 한 문장 | 근거 장 사이의 전환점이 꼭 필요할 때만 |
| `toc`·`section`·`summary` | 목차, 큰 번호 + 챕터 제목, 정리 목록 3행 | 위 5번처럼 원할 때만 |
| `closing` | 큰 결정·요청 한 문장 + 구분선 + 메타 2~3칸 | 마지막 장. `data-closing`: `decision`·`request`·`action`·`criteria`·`takeaway` |

- 발표자가 말로 보탠다는 전제라 장당 본문은 3줄·불릿 3개 안팎이 기본값이다. 제목은 주제명(`현황`)이 아니라 `-다`체 결론 문장이다.
- 표지 그림 위치는 `data-cover`로 고른다: `side`(오른쪽 작은 그림, 기본), `bottom`(제목 아래 가로 흐름·시간 막대), `contrast`(제목 아래 A/B 대비), `center`(가운데 경과선), `map`(오른쪽 아래 작은 용어 지도). 가로로 긴 그림은 `side`에 넣지 않는다.
- 숫자 하나에 한 장이다. 제목이 변화·비교를 주장하면 비교 기준(전 값, 분모, 기간)을 화면에 둔다.
- `data-emphasis="impact"`(옅은 blue 면)는 한 주장에 시선을 모을 장에만 고른다. 정해진 비율은 없다. 진한 면 `data-surface="dark"`는 표지·섹션·마지막 장에만 쓴다.
- 루트 `data-pattern`은 선택이다. `report`·`preview`를 달면 `side` 표지의 그림 열이 조금 넓어진다.

## 차트 글자와 모양

- 덱 SVG 글자는 `g.d0-sl-label`·`g.d0-sl-value`·`g.d0-sl-head` 안 `text`로 쓰고, 크기는 CSS의 `--sl-font`가 정한다. SVG에 `font-size`를 쓰지 않는다.
- 기본 그림은 viewBox 폭 400, 가로형(`evidence`·`breakdown`·`bottom` 표지)은 800이다. 비대칭 장은 400~480이다.
- 막대는 `rect.d0-sl-bar`(강조 계열 하나만 `data-on`), 트랙 `rect.d0-sl-total`, 축 `.d0-sl-axis`, 잇는 선 `.d0-sl-link`, 목표선·기준선 `path.d0-s-target`이다. 노드·단계 같은 도형은 page와 같은 `d0-s-*` 클래스를 쓴다([diagrams/index.md](../diagrams/index.md)).
- 같은 단위 값 여럿은 `figure.d0-slide__fig[data-variant="bar-list"]` 안 `ol.d0-barlist`, 지표 2~4개가 함께 변하면 `metric-list`(`div.d0-mlist`)를 그림 자리에 둔다.
- 막대 길이·점 위치는 값에서 계산한다. 출처가 원자료에 없으면 출처 줄을 만들지 않는다.
- SVG `text`에 적은 `text-anchor="start|end"`는 그대로 지켜진다(속성이 없을 때만 가운데 정렬). 축 눈금 숫자는 `text-anchor="end"`로 축 왼쪽에 붙인다.
- 절차·구조 장은 글 상자를 화살표로 잇지 않고, 역할·대상을 노드로 그려 실제 이름을 직접 라벨한다([diagrams/flow.md](../diagrams/flow.md)).
- 추이 차트는 세로축 눈금·단위와 기준선 값까지 적는다. 아래는 `evidence` 장 그림 자리의 꺾은선이다.

```html
<svg viewBox="0 0 800 320" role="img" aria-labelledby="pw-t"><title id="pw-t">사무실 주간 전력 사용량(kWh). 1주 410, 2주 395, 3주 430, 4주 380, 5주 360, 6주 350. 기준 400</title>
  <g class="d0-sl-head" aria-hidden="true"><text x="120" y="32">kWh</text></g>
  <path class="d0-sl-axis" d="M110 280 H780 M110 40 V280"/>
  <g class="d0-sl-label" aria-hidden="true"><text x="98" y="286" text-anchor="end">300</text><text x="98" y="206" text-anchor="end">350</text><text x="98" y="126" text-anchor="end">400</text><text x="98" y="46" text-anchor="end">450</text></g>
  <path class="d0-s-target" d="M110 120 H780"/><g class="d0-sl-label" aria-hidden="true"><text x="780" y="110" text-anchor="end">기준 400</text></g>
  <path class="d0-sl-link" data-on d="M140 104 L260 128 L380 72 L500 152 L620 184 L740 200"/>
  <circle class="d0-sl-bar" cx="140" cy="104" r="6"/><circle class="d0-sl-bar" cx="380" cy="72" r="6"/><circle class="d0-sl-bar" data-on cx="740" cy="200" r="8"/>
  <g class="d0-sl-value" aria-hidden="true"><text x="740" y="232" data-on>350</text></g>
  <g class="d0-sl-label" aria-hidden="true"><text x="140" y="310">1주</text><text x="380" y="310">3주</text><text x="740" y="310">6주</text></g>
</svg>
```

- y = 280 − (값 − 300) × 1.6처럼 축 범위에서 계산한다. 눈금은 3~5개, 점마다 값을 다 적지 않고 제목이 말하는 값(마지막 값, 기준)만 적는다.

## 뼈대

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>알림 발송 주기 결정</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"><!-- 넘기기 전 subset_font.py가 바꾼다 -->
<style>
/* eli5:tokens.css */
/* eli5:page.css */
/* eli5:deck.css */
/* eli5:deck-shapes.css */
/* eli5:deck-enhance.css */
</style>
</head>
<body>
<main class="d0-deck">
  <section class="d0-slide" id="s-01" data-kind="cover" data-cover="side" aria-labelledby="s-01-t" tabindex="-1">
    <div class="d0-slide__cover">
      <header class="d0-slide__head"><h1 class="d0-slide__title" id="s-01-t">재시도만 줄이면 발송 주기는 어느 쪽이든 괜찮다</h1></header>
      <figure class="d0-slide__fig"><svg viewBox="0 0 400 220" role="img" aria-labelledby="s-01-f"><title id="s-01-f">…</title>…</svg></figure>
    </div>
    <dl class="d0-slide__summary"><div><dt>결정할 것</dt><dd>발송 주기를 매일과 매주 중에 고른다</dd></div></dl>
    <footer class="d0-slide__foot"><p class="d0-slide__src"><kbd>←</kbd> <kbd>→</kbd> 키로 넘겨요</p><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>1 / 6</p></footer>
  </section>

  <section class="d0-slide" id="s-02" aria-labelledby="s-02-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-02-t">재시도는 마지막 주에 몰렸다</h2></header>
    <div class="d0-slide__body" data-layout="split">
      <figure class="d0-slide__fig">
        <svg viewBox="0 0 400 200" role="img" aria-labelledby="s-02-f"><title id="s-02-f">주별 재시도 건수 …</title>
          <rect class="d0-sl-bar" x="44" y="108" width="48" height="60" rx="4"/><rect class="d0-sl-bar" data-on x="308" y="38" width="48" height="130" rx="4"/>
          <g class="d0-sl-value" aria-hidden="true"><text x="68" y="100">120</text><text x="332" y="30" data-on>260</text></g>
          <g class="d0-sl-label" aria-hidden="true"><text x="68" y="190">1주</text><text x="332" y="190">4주</text></g>
        </svg>
        <figcaption class="d0-slide__note">늘어난 몫은 대부분 마지막 주에 몰렸다.</figcaption>
      </figure>
      <ul class="d0-slide__points"><li>재시도가 쌓이면 도착이 늦어진다</li></ul>
    </div>
    <footer class="d0-slide__foot"><p class="d0-slide__src">출처: 발송 기록 집계(합성)</p><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>2 / 6</p></footer>
  </section>

  <!-- stat 기본형: data-kind="stat" data-layout="asym", 머리에 h2 → p.d0-slide__stat → p.d0-slide__base, 오른쪽 figure.d0-slide__fig에 근거 그림 -->

  <section class="d0-slide" id="s-06" data-kind="closing" data-closing="decision" aria-labelledby="s-06-t" tabindex="-1">
    <header class="d0-slide__head"><h2 class="d0-slide__title" id="s-06-t">이번 주 안에 발송 주기를 정해 주세요</h2></header>
    <dl class="d0-slide__meta"><div><dt>담당</dt><dd>서비스 운영 팀</dd></div><div><dt>다음</dt><dd>다음 주에 적용한다</dd></div></dl>
    <footer class="d0-slide__foot"><p class="d0-slide__num"><span class="d0-sr-only">쪽 </span>6 / 6</p></footer>
  </section>

  <nav class="d0-deck__nav" aria-label="슬라이드 넘기기">
    <button type="button" class="d0-deck__btn" data-deck="prev" aria-label="이전 장"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg></button>
    <p class="d0-deck__count" aria-live="polite"><span class="d0-sr-only">쪽 </span><span data-deck-now>1</span> / <span data-deck-total>6</span></p>
    <button type="button" class="d0-deck__btn" data-deck="next" aria-label="다음 장"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg></button>
    <p class="d0-deck__hint"><span data-hint="key">←/→로 넘겨요</span><span data-hint="touch">밀어서 넘겨요</span></p>
  </nav>
</main>
<script>
/* eli5:deck.js */
</script>
</body>
</html>
```

- 장마다 `section.d0-slide` + `id` + `aria-labelledby` + `tabindex="-1"`이고, 헤딩은 표지 h1, 나머지 h2다. 쪽수 `n / N`은 장마다 직접 쓴다.
- 목차 장을 두면 `nav.d0-slide[data-kind="toc"]` 안 `ul.d0-slide__toc > li > a[href="#s-NN"]`이고, 네비에 `button[data-deck="toc"]`을 더한다.
- 비대칭 장(`data-layout="asym"`)은 머리·그림·발을 슬라이드 바로 자식으로 두고 `.d0-slide__body`를 쓰지 않는다.
- 덱 CSS를 고치거나 진한 면·크기 규칙의 세부가 필요하면 [shell/implementation.md](../shell/implementation.md)를 연다.
