# checklist — 따라하기 체크리스트

## 해부 구조

- 맨 위 진행률(완료 수 / 전체 + 막대). 그 아래 행 + 1px `grey-100` 디바이더. 행에 상자·배경을 두지 않는다.
- 행 = 체크박스(실제 `input type="checkbox"`, 24px 원) → 제목 label(15px/600, 사용자가 하는 동작) → 결과 한 줄(14px grey-600, 끝나면 보이는 것) → 행 끝 칸(기본: 소요 시간, owner: 담당·기한, 없으면 생략).
- 결과 한 줄은 한 줄(약 50자 이내)이다. 넘치면 줄이거나 목록을 `.d0-split` 한쪽 섹션에 둬 열 폭을 줄인다.
- 결정 본문이 header 요약 행에 있으면 할 일 행은 짧게 가리킨다(`PR로 올릴지 답하기` + `위 결정 1`). 결정 문장을 다시 쓰지 않는다.
- 행 안 요소는 첫 줄 기준으로 맞춘다(`align-items: start`). 체크박스·시간·배지가 행 높이로 늘어나지 않는다.
- 체크하면 행이 `data-status="done"`이 되고 진행률(네이티브 `<progress>`)이 갱신된다. 소요 시간은 `<time datetime="PT3M">`.
- 색: 진행 막대는 blue, 끝난 체크는 green 원 + 흰 체크선(흰 바탕 위 green 3.47, green 위 흰 선 3.47로 그래픽 3:1 통과). 체크 모양과 취소선이 색 없이도 완료를 말한다.
  green은 글자에 쓰지 않는다(완료 행 글자는 grey-600).

## 언제 쓰나 / 변형

- 기본(guide): 단계(최대 7). 행 끝 칸 = 소요 시간 `<time datetime="PT3M">`. 모든 행에 시간이 있을 때만 이 칸을 둔다.
- `data-variant="owner"`(incident 재발 방지, report 다음 할 일): 행 끝 칸 = 담당·기한 `.d0-check__meta`
  (`팀 A · <time datetime="2026-10-20">10월 20일</time>`). 담당·기한이 없는 행은 메타 요소를 **빼고** 행에 `data-meta="none"`을 둔다.
  빈 `span`으로 자리를 채우지 않는다. 640px 이하에서는 메타가 설명 아래 줄로 내려간다.
  - **메타 슬롯.** 메타 = 주체 `span.d0-check__owner` + (기한 `<time>` 또는 조건 `span.d0-check__when`) 하나. 주체는 사람·팀 이름이다.
  - **조건 슬롯(`.d0-check__when`).** 날짜가 아니라 "언제·무엇 뒤에" 시작하는지(`머지 후`, `백엔드 배포 확인 뒤`)를 `<time>` 없이 텍스트로 쓴다.
    약 12자 이내로 쓰고, 더 길거나 날짜와 조건이 모두 있으면 조건을 결과 한 줄 앞에 넣는다(`백엔드 배포를 확인한 뒤 시작해요.`). `<time>`은 실제 날짜·기간에만 쓴다.
  - `추후`·`예정`·`검토 중`만으로 기한·조건 칸을 채우지 않는다. 언제 시작하는지 모르면 그것을 정하는 행동과 주체를 행으로 쓴다.
  - report 다음 단계에서는 모든 행에 주체가 있어야 하므로 `data-meta="none"`을 쓰지 않는다([report.md](../formats/report.md)).
- 목록 전체에 행 끝 칸이 없으면 `.d0-check`에 `data-meta="none"`을 둬 모든 행을 `auto 1fr` 2열로 만든다.
- **시간이 일부 행에만 있으면 시간 열을 만들지 않는다.** 그 행의 결과 한 줄 끝에 넣는다(`… 보여요. 약 20분`). 한 행에만 붙은 오른쪽 끝 숫자는 근거 없이 튀어 보인다.
- 입력 예시가 필요한 행은 `<details>`로 행 안에 접어 둔다. 붙여 넣을 명령·설정은 그 `<details>` 안에 [code-block.md](code-block.md)로 둔다(기본·owner 변형).
  linked 변형은 행 안에 접지 않고 아래 **활성 단계 코드 영역**에 펼쳐 둔다.
- `data-variant="linked"`(guide 따라하기 기본): 왼쪽 sticky 무대에 단계별 화면 와이어프레임 SVG 1장, 오른쪽에 체크리스트를 두는 2열이다.
  - 행마다 `data-step="n"`과 `data-caption`(그 단계 그림 설명 한 줄)을 둔다. SVG는 단계마다 `g[data-step="n"]` 그룹 하나를 갖고, 그룹마다 누를 곳 하나만 blue다.
  - 행에 마우스를 올리거나(hover), 키보드 포커스가 들어오거나(focus-within), 행을 누르거나, 체크하면 무대가 그 단계 그림으로 바뀐다.
    figure의 `data-active-step`이 보이는 그룹을 고르고, 현재 행은 `data-current`로 번호 원이 blue-dark(흰 숫자 5.5)가 된다.
  - hover는 미리 보기다. 마우스가 목록을 떠나면 마지막으로 포커스·클릭·체크한 단계로 돌아간다.
  - 체크한 단계는 그룹에 `data-done`이 붙어 green 원 + 흰 체크선(`.d0-s-tick`, 3.47)이 나타난다. 행 번호 원은 green-bg + grey-900 숫자(15.12)다.
  - 그림 이름은 바뀐 단계에 맞춰 figcaption과 SVG `<desc>`를 함께 고친다(`<strong>2단계</strong> 파란 입력창에 주제를 적어요.`). 별도 `aria-live`는 두지 않는다.
  - 960px 미만: sticky를 풀고 무대 1장을 목록 위에 둔다. 행을 누르거나 체크하면 그림이 바뀐다. 무대를 한 장만 두는 이유는 같은 SVG를 행마다 복제하지 않기 위해서다.
    단계 그림이 목록에서 멀어 읽기 어려우면 대신 행 `<details>` 안 작은 그림으로 바꾼다(이때는 linked를 쓰지 않는다).
  - **활성 단계 코드 영역.** 단계별 붙여 넣을 명령·입력 예시는 무대 `figcaption` 바로 아래 `div.d0-check__code[aria-live="polite"]` 한 곳에 둔다.
    단계마다 항목 `.d0-check__code-item[data-step="n"]` 하나 = [code-block.md](code-block.md) `figure.d0-code` + 필요하면 보조 한 줄 `p.d0-note`. 소제목·접기 없이 펼친 채다.
    무대의 `data-active-step`과 같은 번호 항목만 보이므로 단계를 바꾸면 코드도 바뀐다. 코드가 없는 단계는 안내 한 줄 `p.d0-check__code-item.d0-note[data-step="n"]`(예: `이 단계는 붙여 넣을 코드가 없어요.`)을 둔다.
  - 명령은 `pre`에 `white-space: pre-wrap; overflow-wrap: anywhere`로 줄을 바꿔 가로 스크롤을 만들지 않는다(code-block의 `pre` 기본값 `white-space: pre`를 이 영역에서만 덮는다).
  - 960px 미만: 코드 영역은 숨기고, JS가 코드 항목 노드를 각 단계 행(`.d0-check__row[data-step] > div`) 아래로 옮겨 펼쳐 붙인다(접지 않는다). 960px 이상으로 돌아오면 영역으로 되돌린다.
    노드를 옮기므로 복사 버튼 리스너는 그대로다. 코드 없는 단계의 안내 한 줄은 옮기지 않는다(행에는 붙일 코드가 없다).
  - 무대 SVG는 diagram 그림 블록으로 센다. 단계 전환은 바로 바뀌고, 0.2초 페이드는 `prefers-reduced-motion: no-preference`일 때만 둔다.

| 조건 | 열 정의 |
| --- | --- |
| 기본, 모든 행에 시간 | `auto 1fr auto` |
| `owner`, 메타 있는 행 | `auto 1fr auto` |
| 메타 없는 행 `[data-meta="none"]` 또는 목록 전체 `.d0-check[data-meta="none"]` | `auto 1fr` |

## 스니펫

```html
<div class="d0-check">
  <label class="d0-check__progress" for="check-progress"><output data-count>0</output> / 3 완료</label>
  <progress class="d0-check__bar" id="check-progress" max="3" value="0">0 / 3</progress>
  <ol>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-1">
      <div><label for="step-1">설정 열기</label><p>왼쪽 메뉴에 '내보내기'가 보여요.</p></div>
      <time class="d0-check__time" datetime="PT1M">1분</time>
    </li>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-2">
      <div><label for="step-2">받을 팀 고르기</label><p>목록에 팀 A가 체크돼요.</p>
        <details><summary>입력 예시</summary><p>팀 이름 칸에 '팀 A'를 입력해요.</p></details></div>
      <time class="d0-check__time" datetime="PT3M">3분</time>
    </li>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="step-3">
      <div><label for="step-3">자동 전송 켜기</label><p>스위치 옆에 '매일 아침 9시'가 보여요.</p></div>
      <time class="d0-check__time" datetime="PT1M">1분</time>
    </li>
  </ol>
</div>
```

```css
.d0-check__progress { display: block; color: var(--d0-grey-600); font-size: 14px; font-weight: 600; font-variant-numeric: tabular-nums; }
.d0-check__bar {
  appearance: none; display: block; width: 100%; height: 6px; margin: 8px 0 12px;
  border: 0; border-radius: 999px; background: var(--d0-grey-100); overflow: hidden; color: var(--d0-blue);
}
.d0-check__bar::-webkit-progress-bar { background: var(--d0-grey-100); }
.d0-check__bar::-webkit-progress-value { background: var(--d0-blue); transition: width var(--d0-dur) var(--d0-ease); }
.d0-check__bar::-moz-progress-bar { background: var(--d0-blue); }
.d0-check__row { display: grid; grid-template-columns: auto 1fr auto; align-items: start; gap: 12px; padding: 16px 0; border-top: 1px solid var(--d0-grey-100); }
.d0-check__row > div, .d0-check__row > details { min-width: 0; }
.d0-check__row label { color: var(--d0-grey-900); font-weight: 600; cursor: pointer; }
.d0-check__row p, .d0-check summary { color: var(--d0-grey-600); font-size: 14px; }
.d0-check__time { color: var(--d0-grey-600); font-size: var(--d0-text-compact); font-variant-numeric: tabular-nums; }
.d0-check__box {
  appearance: none; display: grid; place-content: center;
  width: 24px; height: 24px; margin: 0;
  border: 2px solid var(--d0-grey-500); border-radius: 999px; background: #fff; cursor: pointer;
}
.d0-check__box::after { content: ""; width: 10px; height: 6px; border: solid #fff; border-width: 0 0 2px 2px; transform: rotate(-45deg) translate(1px, -1px); }
.d0-check__row[data-status="done"] .d0-check__box { border-color: var(--d0-green); background: var(--d0-green); }
.d0-check__row[data-status="done"] label { color: var(--d0-grey-600); text-decoration: line-through; }
.d0-check details { margin-top: 6px; }
```

```js
document.querySelectorAll('.d0-check').forEach(function (list) {
  list.addEventListener('change', function (e) {
    if (!e.target.matches('.d0-check__box')) return;
    var row = e.target.closest('.d0-check__row');
    if (e.target.checked) row.dataset.status = 'done'; else delete row.dataset.status;
    var n = list.querySelectorAll('.d0-check__box:checked').length;
    list.querySelector('[data-count]').textContent = n;
    var bar = list.querySelector('progress');
    bar.value = n; bar.textContent = n + ' / ' + bar.max;
  });
});
```

### owner 변형 스니펫

```html
<div class="d0-check" data-variant="owner">
  <label class="d0-check__progress" for="fix-progress"><output data-count>0</output> / 3 완료</label>
  <progress class="d0-check__bar" id="fix-progress" max="3" value="0">0 / 3</progress>
  <ol>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="fix-1">
      <div><label for="fix-1">실패 알림을 채팅으로도 보내기</label><p>밤사이 실패를 아침 전에 알아요.</p></div>
      <span class="d0-check__meta"><span class="d0-check__owner">팀 A</span> · <time datetime="2026-10-20">10월 20일</time></span>
    </li>
    <li class="d0-check__row">
      <input type="checkbox" class="d0-check__box" id="fix-2">
      <div><label for="fix-2">재시도 횟수 3번으로 늘리기</label><p>잠깐 끊긴 연결은 저절로 다시 보내요.</p></div>
      <span class="d0-check__meta"><span class="d0-check__owner">팀 B</span> · <span class="d0-check__when">알림 변경 머지 후</span></span>
    </li>
    <li class="d0-check__row" data-meta="none">
      <input type="checkbox" class="d0-check__box" id="fix-3">
      <div><label for="fix-3">보관 기간 다시 정하기</label><p>담당은 다음 회의에서 정해요.</p></div>
    </li>
  </ol>
</div>
```

```css
.d0-check__meta { color: var(--d0-grey-700); font-size: var(--d0-text-compact); font-weight: 500; white-space: nowrap; font-variant-numeric: tabular-nums; }
.d0-check__owner { color: var(--d0-grey-900); font-weight: 600; }
.d0-check[data-meta="none"] .d0-check__row,
.d0-check__row[data-meta="none"] { grid-template-columns: auto 1fr; }
@media (max-width: 640px) {
  .d0-check[data-variant="owner"] .d0-check__row { grid-template-columns: auto 1fr; }
  .d0-check__meta { grid-column: 2; white-space: normal; }
}
```

JS는 기본 변형과 같다.

### linked 변형 스니펫

무대 SVG의 클래스(`d0-s-frame`, `d0-s-accent`, `d0-s-tick` 등)와 무대 CSS는 [diagram.md](diagram.md)·[shell.md](shell.md)를 따른다. 아래는 2단계만 줄였다.

```html
<div class="d0-check" data-variant="linked">
  <figure class="d0-fig d0-check__stage" data-stage data-active-step="1">
    <div class="d0-fig__stage">
      <svg viewBox="0 0 360 220" role="img" aria-labelledby="ls-t ls-d">
        <title id="ls-t">단계별 화면</title>
        <desc id="ls-d">설정 화면이에요. 왼쪽 메뉴의 내보내기가 파랗게 강조돼 있어요.</desc>
        <g data-step="1">
          <rect class="d0-s-frame" x="1" y="1" width="358" height="218" rx="12"/>
          <rect class="d0-s-fill" x="16" y="20" width="80" height="12" rx="6"/>
          <rect class="d0-s-accent" x="16" y="44" width="80" height="16" rx="6"/>
          <rect class="d0-s-fill" x="16" y="72" width="80" height="12" rx="6"/>
          <rect class="d0-s-fill" x="116" y="20" width="226" height="180" rx="10"/>
          <g class="d0-check__ok"><circle class="d0-s-node" cx="330" cy="30" r="11" data-tone="green"/><path class="d0-s-tick" d="M325 30 L329 34 L335.5 26.5"/></g>
        </g>
        <g data-step="2">
          <rect class="d0-s-frame" x="1" y="1" width="358" height="218" rx="12"/>
          <rect class="d0-s-fill" x="16" y="20" width="200" height="12" rx="6"/>
          <rect class="d0-s-zone" x="16" y="48" width="326" height="40" rx="10"/>
          <rect class="d0-s-accent" x="28" y="62" width="120" height="12" rx="6"/>
          <rect class="d0-s-fill" x="16" y="104" width="240" height="12" rx="6"/>
          <g class="d0-check__ok"><circle class="d0-s-node" cx="330" cy="30" r="11" data-tone="green"/><path class="d0-s-tick" d="M325 30 L329 34 L335.5 26.5"/></g>
        </g>
      </svg>
    </div>
    <figcaption><strong>1단계</strong> 왼쪽 메뉴의 파란 칸이 내보내기예요.</figcaption>
    <div class="d0-check__code" aria-live="polite">
      <p class="d0-check__code-item d0-note" data-step="1">이 단계는 붙여 넣을 코드가 없어요. 메뉴만 눌러요.</p>
      <div class="d0-check__code-item" data-step="2">
        <figure class="d0-code">
          <figcaption class="d0-code__bar"><span class="d0-code__label">터미널</span><output class="d0-code__status" aria-live="polite"></output><button type="button" class="d0-code__copy" hidden>복사</button></figcaption>
          <pre tabindex="0" role="group" aria-label="팀 등록 명령"><code><span class="d0-code__prompt" aria-hidden="true">$ </span>npx order-export init --team "팀 A"</code></pre>
        </figure>
        <p class="d0-note">팀 이름은 따옴표 안만 바꿔요.</p>
      </div>
    </div>
  </figure>
  <div class="d0-check__list">
    <label class="d0-check__progress" for="ls-progress"><output data-count>0</output> / 2 완료</label>
    <progress class="d0-check__bar" id="ls-progress" max="2" value="0">0 / 2</progress>
    <ol>
      <li class="d0-check__row" data-step="1" data-current data-meta="none"
          data-caption="왼쪽 메뉴의 파란 칸이 내보내기예요."
          data-desc="설정 화면이에요. 왼쪽 메뉴의 내보내기가 파랗게 강조돼 있어요.">
        <input type="checkbox" class="d0-check__box" id="ls-1">
        <div><span class="d0-check__no">1</span><label for="ls-1">설정에서 내보내기 열기</label><p>오른쪽에 '자동 전송' 칸이 보여요.</p></div>
      </li>
      <li class="d0-check__row" data-step="2" data-meta="none"
          data-caption="파란 입력창에 받을 팀을 적어요."
          data-desc="자동 전송 화면이에요. 받을 팀 입력창이 파란 점선으로 강조돼 있어요.">
        <input type="checkbox" class="d0-check__box" id="ls-2">
        <div><span class="d0-check__no">2</span><label for="ls-2">받을 팀 등록하기</label><p>목록에 팀 A가 생겨요.</p></div>
      </li>
    </ol>
  </div>
</div>
```

```css
.d0-check[data-variant="linked"] { display: grid; gap: 24px 48px; align-items: start; }
.d0-check[data-variant="linked"] > * { min-width: 0; }
@media (min-width: 960px) {
  .d0-check[data-variant="linked"] { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
  .d0-check__stage { position: sticky; top: 24px; }
}
.d0-check__stage g[data-step], .d0-check__ok { display: none; }
.d0-check__stage[data-active-step="1"] g[data-step="1"],
.d0-check__stage[data-active-step="2"] g[data-step="2"],
.d0-check__stage[data-active-step="3"] g[data-step="3"],
.d0-check__stage[data-active-step="4"] g[data-step="4"],
.d0-check__stage[data-active-step="5"] g[data-step="5"],
.d0-check__stage[data-active-step="6"] g[data-step="6"],
.d0-check__stage[data-active-step="7"] g[data-step="7"],
.d0-check__stage g[data-done] .d0-check__ok { display: inline; }
.d0-check__stage figcaption strong { color: var(--d0-blue-dark); font-weight: 600; }
.d0-check[data-variant="linked"] .d0-check__row { cursor: pointer; }
.d0-check[data-variant="linked"] .d0-check__row > div { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 4px 8px; }
.d0-check[data-variant="linked"] .d0-check__row > div > :is(p, details, .d0-check__code-item) { flex-basis: 100%; min-width: 0; }
/* 활성 단계 코드 영역: 무대 figcaption 아래, 활성 단계 항목만 보인다 */
.d0-check__code { display: grid; min-width: 0; }
.d0-check__code > [data-step] { display: none; }
.d0-check__stage[data-active-step="1"] .d0-check__code > [data-step="1"],
.d0-check__stage[data-active-step="2"] .d0-check__code > [data-step="2"],
.d0-check__stage[data-active-step="3"] .d0-check__code > [data-step="3"],
.d0-check__stage[data-active-step="4"] .d0-check__code > [data-step="4"],
.d0-check__stage[data-active-step="5"] .d0-check__code > [data-step="5"],
.d0-check__stage[data-active-step="6"] .d0-check__code > [data-step="6"],
.d0-check__stage[data-active-step="7"] .d0-check__code > [data-step="7"] { display: grid; }
.d0-check__code-item { gap: 8px; min-width: 0; }
.d0-check__row .d0-check__code-item { display: grid; margin-top: 4px; } /* 960px 미만: 행 아래에 펼쳐 붙인다 */
.d0-check__code-item .d0-code pre { white-space: pre-wrap; overflow-wrap: anywhere; } /* 좁은 열에서도 가로 스크롤 없음 */
@media (max-width: 959px) { .d0-check__code { display: none; } }
.d0-check__no {
  display: inline-grid; place-content: center; flex: none; min-width: 22px; height: 22px;
  margin-top: calc((15px * var(--d0-leading-body) - 22px) / 2);
  border-radius: 999px; background: var(--d0-blue-light); color: var(--d0-blue-dark);
  font-size: var(--d0-meta); font-weight: 700; font-variant-numeric: tabular-nums;
}
.d0-check__row[data-current] .d0-check__no { background: var(--d0-blue-dark); color: #fff; }
.d0-check__row[data-status="done"] .d0-check__no { background: var(--d0-green-bg); color: var(--d0-grey-900); }
@media (prefers-reduced-motion: no-preference) {
  .d0-check__stage g[data-step] { animation: d0-step-in var(--d0-dur) var(--d0-ease); }
  @keyframes d0-step-in { from { opacity: 0; } to { opacity: 1; } }
}
```

```js
document.querySelectorAll('.d0-check[data-variant="linked"]').forEach(function (list) {
  var stage = list.querySelector('.d0-check__stage');
  var cap = stage.querySelector('figcaption');
  var desc = stage.querySelector('desc');
  var rows = list.querySelectorAll('.d0-check__row');
  var pinned = list.querySelector('.d0-check__row[data-current]') || rows[0];
  function show(row) {
    var n = row.dataset.step;
    stage.dataset.activeStep = n;
    var strong = document.createElement('strong');
    strong.textContent = n + '단계';
    cap.replaceChildren(strong, ' ' + row.dataset.caption);
    desc.textContent = row.dataset.desc;
    rows.forEach(function (r) { r.toggleAttribute('data-current', r === row); });
  }
  function pin(row) { pinned = row; show(row); }
  rows.forEach(function (row) {
    row.addEventListener('mouseenter', function () { show(row); });
    row.addEventListener('focusin', function () { pin(row); });
    row.addEventListener('click', function () { pin(row); });
  });
  list.querySelector('ol').addEventListener('mouseleave', function () { show(pinned); });
  list.addEventListener('change', function (e) {
    if (!e.target.matches('.d0-check__box')) return;
    var row = e.target.closest('.d0-check__row');
    var group = stage.querySelector('g[data-step="' + row.dataset.step + '"]');
    if (e.target.checked) { row.dataset.status = 'done'; group.setAttribute('data-done', ''); }
    else { delete row.dataset.status; group.removeAttribute('data-done'); }
    var n = list.querySelectorAll('.d0-check__box:checked').length;
    list.querySelector('[data-count]').textContent = n;
    var bar = list.querySelector('progress');
    bar.value = n; bar.textContent = n + ' / ' + bar.max;
    pin(row);
  });
});
```

```js
// 활성 단계 코드 영역: 960px 이상은 무대 아래 한곳에, 미만은 각 단계 행 아래로 코드 항목 노드를 옮긴다(복사 버튼 리스너 유지)
document.querySelectorAll('.d0-check[data-variant="linked"]').forEach(function (list) {
  var box = list.querySelector('.d0-check__code');
  if (!box) return;
  var all = Array.prototype.slice.call(box.querySelectorAll(':scope > .d0-check__code-item')); // 단계 순서
  var wide = window.matchMedia('(min-width: 960px)');
  function place() {
    all.forEach(function (it) {
      var row = list.querySelector('.d0-check__row[data-step="' + it.dataset.step + '"] > div');
      if (wide.matches || !it.querySelector('.d0-code') || !row) box.appendChild(it); // 넓은 화면·코드 없는 안내는 영역에(순서대로)
      else row.appendChild(it);
    });
  }
  place();
  if (wide.addEventListener) wide.addEventListener('change', place);
});
```

code-block JS(복사 버튼)는 이 스크립트보다 먼저 붙여도, 나중에 붙여도 된다. 노드를 옮길 뿐 다시 만들지 않는다.

linked 목록에는 기본 변형 JS를 함께 붙이지 않는다(위 JS가 진행률까지 갱신한다). 기본 변형 JS를 쓰는 페이지면 그 선택자를 `.d0-check:not([data-variant="linked"])`로 좁힌다.

## 금지

- 행마다 카드, 행 배경, `grey-200` 이상 구분선, 완료 판정이 모호한 제목("확인하기", "점검").
- green 글자(완료 행 제목을 초록으로), 체크 모양 없이 색만 바뀌는 완료 표시.
- 요약 행의 결정 문장을 할 일 행에 다시 쓰기, 두 줄로 넘치는 결과 한 줄.
- 사용자가 할 일과 시스템이 하는 일을 한 목록에 섞기(시스템 일은 결과 한 줄로만).
- 일부 행에만 있는 시간 열, 메타 칸을 채우려는 빈 `span`·`-` 표시.
- 주체 없이 `추후 배포 예정`처럼 쓴 할 일, 기한·조건 칸에 `추후`·`예정`·`TBD`만 두기.
- linked 변형에서 행 안에 코드 접힘(`<details>`)을 두지 않는다. 코드는 활성 단계 코드 영역에 펼쳐 두고, 960px 미만에서도 행 아래에 펼쳐 붙인다.
