# checklist — 따라하기 체크리스트

## 해부 구조

- 맨 위 진행률(완료 수 / 전체 + 막대). 그 아래 행 + 1px `grey-100` 디바이더. 행에 상자·배경을 두지 않는다.
- 행 = 체크박스(실제 `input type="checkbox"`, 24px 원) → 제목 label(15px/600, 사용자가 하는 동작) → 결과 한 줄(14px grey-600, 끝나면 보이는 것) → 행 끝 칸(기본: 소요 시간, owner: 담당·기한, 없으면 생략).
- 결과 한 줄은 축 한 줄 안에서 끝나는 한 문장이다([shell/contract.md](../shell/contract.md) 줄 길이 절). 넘치면 문장을 줄인다.
- 결정 본문이 header 요약 행에 있으면 할 일 행은 짧게 가리킨다(`PR로 올릴지 답하기` + `위 결정 1`). 결정 문장을 다시 쓰지 않는다.
- 행 안 요소는 첫 줄 기준으로 맞춘다(`align-items: start`). 체크박스·시간·배지가 행 높이로 늘어나지 않는다.
- 체크하면 행이 `data-status="done"`이 되고 진행률(네이티브 `<progress>`)이 갱신된다. 소요 시간은 `<time datetime="PT3M">`.
- 색: 진행 막대는 blue, 끝난 체크는 green 원 + 흰 체크선(흰 바탕 위 green 3.47, green 위 흰 선 3.47로 그래픽 3:1 통과). 체크 모양과 취소선이 색 없이도 완료를 말한다.
  green은 글자에 쓰지 않는다(완료 행 글자는 grey-600). linked 변형은 번호 원도 완료를 말하므로 취소선을 빼고 제목을 그대로 읽히게 둔다.

## 언제 쓰나 / 변형

- 기본(guide): 단계. 총 단계 수 상한 대신 아래 **구간** 규칙으로 한 번에 이해할 작업량을 나눈다. 행 끝 칸 = 소요 시간 `<time datetime="PT3M">`. 모든 행에 시간이 있을 때만 이 칸을 둔다.
- `data-variant="owner"`(incident 재발 방지, report 다음 할 일): 행 끝 칸 = 담당·기한 `.d0-check__meta`
  (`팀 A · <time datetime="2026-10-20">10월 20일</time>`). 담당·기한이 없는 행은 메타 요소를 **빼고** 행에 `data-meta="none"`을 둔다.
  빈 `span`으로 자리를 채우지 않는다. 640px 이하에서는 메타가 설명 아래 줄로 내려간다.
  - **메타 슬롯.** 메타 = 주체 `span.d0-check__owner` + (기한 `<time>` 또는 조건 `span.d0-check__when`) 하나. 주체는 사람·팀 이름이다.
  - **조건 슬롯(`.d0-check__when`).** 날짜가 아니라 "언제·무엇 뒤에" 시작하는지(`머지 후`, `백엔드 배포 확인 뒤`)를 `<time>` 없이 텍스트로 쓴다.
    약 12자 이내로 쓰고, 더 길거나 날짜와 조건이 모두 있으면 조건을 결과 한 줄 앞에 넣는다(`백엔드 배포를 확인한 뒤 시작해요.`). `<time>`은 실제 날짜·기간에만 쓴다.
  - `추후`·`예정`·`검토 중`만으로 기한·조건 칸을 채우지 않는다. 언제 시작하는지 모르면 그것을 정하는 행동과 주체를 행으로 쓴다.
  - report 다음 단계에서는 모든 행에 주체가 있어야 하므로 `data-meta="none"`을 쓰지 않는다.
- 목록 전체에 행 끝 칸이 없으면 `.d0-check`에 `data-meta="none"`을 둬 모든 행을 `auto 1fr` 2열로 만든다.
- **시간이 일부 행에만 있으면 시간 열을 만들지 않는다.** 그 행의 결과 한 줄 끝에 넣는다(`… 보여요. 약 20분`). 한 행에만 붙은 오른쪽 끝 숫자는 근거 없이 튀어 보인다.
- 입력 예시가 필요한 행은 `<details>`로 행 안에 접어 둔다. 붙여 넣을 명령·설정은 그 `<details>` 안에 [code-block.md](code-block.md)로 둔다(기본·owner 변형).
  linked 변형은 행 안에 접지 않고 아래 **활성 단계 코드 영역**에 펼쳐 둔다.
- `data-variant="linked"`(guide 따라하기 기본): 왼쪽 sticky 무대에 단계별 화면 와이어프레임 SVG 1장, 오른쪽에 체크리스트를 두는 2열이다. 그림 지점과 번호로 대응하는 목록이 함께 본문인 2열((b))이라 `.d0-wide`(축 중심 그대로 양쪽으로 프레임까지, [shell/contract.md](../shell/contract.md) 넓은 구간 (b)) 안에 두고 넓은 구간 2열 분할선(문서에서 6/6 또는 7/5 하나)을 따른다([shell/contract.md](../shell/contract.md) 2열 절).
  - 행마다 `data-step="n"`과 `data-caption`(그 단계 그림 설명 한 줄)을 둔다. SVG는 단계마다 `g[data-step="n"]` 그룹 하나를 갖고, 그룹마다 누를 곳 하나만 blue다.
  - 행 위에서 마우스를 움직이거나(hover), 키보드 포커스가 들어오거나(focus-within), 행을 누르면 무대가 그 단계 그림으로 바뀐다. 체크하면 다음 미완료 단계의 무대·캡션·코드를 함께 보여 준다.
    hover는 실제 포인터 이동(`pointermove`, 좌표 변화)일 때만 받는다. 구간이 접혀 가만히 있는 포인터 밑으로 다른 행이 올라와도 체크로 옮겨 간 단계가 그대로다.
    figure의 `data-active-step`이 보이는 그룹을 고르고, 현재 행은 `data-current`로 번호 원이 blue-dark(흰 숫자 5.5)가 된다.
  - 마지막 hover·focus·click 단계는 목록을 떠나도 유지한다. 처음 로드할 때는 첫 미완료 단계를 보여 주고, 모두 완료하면 마지막 단계를 유지한다. 체크 해제 시에는 해제한 단계를 보여 준다.
  - 체크한 단계는 그룹에 `data-done`이 붙어 green 원 + 흰 체크선(`.d0-s-tick`, 3.47)이 나타난다. 행 번호 원은 green-bg + grey-900 숫자(15.12)다.
    체크 원·번호 원이 이미 완료를 말하므로 제목에 취소선을 긋지 않는다(grey-600만). 끝난 단계도 다시 읽으러 오는 곳이라 글자를 지우지 않는다.
  - 그림 이름은 바뀐 단계에 맞춰 figcaption과 SVG `<desc>`를 함께 고친다(`<strong>2단계</strong> 파란 입력창에 주제를 적어요.`). 별도 `aria-live`는 두지 않는다.
  - 960px 미만: sticky를 풀고 무대 1장을 목록 위에 둔다. 행을 누르거나 체크하면 그림이 바뀐다. 무대를 한 장만 두는 이유는 같은 SVG를 행마다 복제하지 않기 위해서다.
    단계 그림이 목록에서 멀어 읽기 어려우면 대신 행 `<details>` 안 작은 그림으로 바꾼다(이때는 linked를 쓰지 않는다).
  - **활성 단계 코드 영역.** 단계별 붙여 넣을 명령·입력 예시는 무대 `figcaption` 바로 아래 `div.d0-check__code[aria-live="polite"]` 한 곳에 둔다.
    단계마다 항목 `.d0-check__code-item[data-step="n"]` 하나 = [code-block.md](code-block.md) `figure.d0-code` + 필요하면 보조 한 줄 `p.d0-note`. 소제목·접기 없이 펼친 채다.
    무대의 `data-active-step`과 같은 번호 항목만 보이므로 단계를 바꾸면 코드도 바뀐다. 코드가 없는 단계는 안내 한 줄 `p.d0-check__code-item.d0-note[data-step="n"]`(예: `이 단계는 붙여 넣을 코드가 없어요.`)을 둔다.
  - 명령은 `pre`에 `white-space: pre-wrap; overflow-wrap: anywhere`로 줄을 바꿔 가로 스크롤을 만들지 않는다(code-block의 `pre` 기본값 `white-space: pre`를 이 영역에서만 덮는다).
  - 960px 미만: 코드 영역은 숨기고, JS가 코드 항목 노드를 각 단계 행(`.d0-check__row[data-step] > div`) 아래로 옮겨 펼쳐 붙인다(접지 않는다). 960px 이상으로 돌아오면 영역으로 되돌린다.
    노드를 옮기므로 복사 버튼 리스너는 그대로다. 코드 없는 단계의 안내 한 줄은 옮기지 않는다(행에는 붙일 코드가 없다).
  - 단계 전환은 바로 바뀌고, 0.2초 페이드는 `prefers-reduced-motion: no-preference`일 때만 둔다.

## 구간 (`data-phased`) — 긴 따라하기

따라하기 구조는 **구간 → 단계 → 단계별 화면·설명**이다.
**한 화면에서 사용자가 선택하거나 기억해야 하는 상세 단계가 많으면, 현재 작업 단위만 펼쳐 보여준다.** 숫자 기준(5단계 초과 등)으로 접지 않는다.

- **나누는 곳.** 상한은 총 단계 수가 아니라 한 번에 이해해야 하는 작업량에 건다. 단계가 길어지면 작업 목적이 바뀌는 지점에서 구간으로 나눈다. 숫자로 기계적으로 자르지 않는다. 한 구간은 보통 3~5단계다.
  - 6단계인데 전부 짧다 → 구간 없이 그대로, 또는 구간 머리만 두고 모두 펼친다(`data-phased="open"`).
  - 6단계인데 설명이 길다 → 2~3구간.
  - 10단계 이상 → 거의 항상 구간으로 나눈다.
  - 단계마다 화면·코드·주의가 붙는다 → 더 일찍 나눈다.
- **구간 이름은 결과로.** `준비`·`설정` 같은 추상어보다 끝나면 얻는 결과를 우선한다(`쓸 수 있는 상태`, `첫 초안`). 구간마다 머리 행 하나에 이름 + 상태 + 끝나면 얻는 결과 한 줄(약 25자 이내, `에이전트가 eli5-design을 불러 써요.`)을 둔다.
- **화면 = 진행률 한 줄 + 구간 머리 행.** 같은 정보를 두 곳에 쓰지 않는다. 구간 이름·결과는 머리 행에만, 진행 수는 맨 위 전체 수와 머리 행의 구간 수에만 있다.
  1. **맨 위 진행률.** `전체 n / N 완료` + 막대 한 줄. 이것이 전체 진행의 유일한 표시다.
  2. **구간 머리 행 = 지도.** `상태 표시 · 이름 · 진행 수` 한 줄 + 그 아래 작은 결과 한 줄. 머리 행을 위에서 아래로 읽으면 그대로 전체 구간 지도다.
     구간 이름을 잇는 [status rail](timeline.md)을 진행률 아래에 또 두지 않고, 구간 끝에 결과를 되풀이하는 [checkpoint](checkpoint.md) 줄도 두지 않는다.
     - 끝남: green 원 + 흰 `✓`, 진행 수 없음. 진행: blue-dark 테두리 원 + `k / n`(그 구간에서 **체크한** 단계 수 / 구간 단계 수). 예정: grey 테두리 원 + `n단계`.
     - 구간 단계를 모두 체크하면 펼쳐져 있어도 `✓`다(펼침은 위치, ✓는 체크 결과). 진행 중 구간은 첫 미완료 단계가 있는 구간 하나다. 그 밖에 일부만 체크한 구간도 `k / n`으로 센다.
     - 상태 표시 원은 `role="img"`와 `aria-label`(`완료`·`진행 중`·`예정`)로 상태를 읽어 준다. 색만으로 구분하지 않는다(✓ 모양, 테두리만 있는 원).
  3. **현재 구간만 펼침.** 펼친 구간도 같은 머리 행 아래에 단계 행이 붙을 뿐 별도 머리를 두지 않는다. 끝났거나 예정인 구간은 머리 행 한 줄로 접히고, 누르면 펼친다.
  375px에서도 같다. 결과 한 줄은 이름 아래 줄이라 좁아져도 진행 수와 겹치지 않는다.
- **동작.** 체크하면 다음 미완료 단계로 가고, 구간을 넘으면 다음 구간을 펼치고 이전 구간을 한 줄로 접는다. linked 변형의 왼쪽 무대(현재 단계 그림 + 짧은 설명 + 코드 영역), 마지막 hover·focus·click 단계 유지는 그대로다.
  펼칠 구간은 활성 단계(체크로 옮겨 간 단계, 해제한 단계)가 있는 구간이다. hover·focus·click은 펼침·접힘도 머리 행 수도 바꾸지 않는다. 진행 수(전체 n / N, 구간 k / n)는 체크한 수만 센다.
  접히는 구간 안에 키보드 포커스가 있으면 새 현재 단계의 체크박스로 포커스를 옮긴다.
- **JS 없을 때·인쇄.** 접힘은 JS가 붙이는 `data-collapsed`로만 생기므로 JS가 없으면 모든 구간이 펼쳐진다. 숨김 규칙은 `@media screen` 안에만 있어 인쇄에서도 전 구간이 펼쳐진다.
  JS 없는 머리 행은 정적 글자(이름 · `n단계` · 결과)를 그대로 보여 준다. 결과는 HTML에 정적으로 쓰고 JS는 진행 수와 상태만 바꾼다.
- 시각 톤은 기본 체크리스트와 같다. 구간마다 카드·배경·박스를 두지 않고 구간 경계도 행과 같은 1px grey-100 선이다.

**긴 절차일 때 고려.** 구간 접기 대신 현재 단계 ±1만 크게 보이고 나머지를 작게 줄이는 방식, 보이는 단계 창을 옮겨 가는 윈도잉, 왼쪽 미니 목차 + 오른쪽 한 단계 상세 방식도 있다. 단계가 15개를 넘거나 단계마다 화면이 크게 바뀌면 이 방식들을 검토하되, 같은 페이지에서 구간 접기와 섞지 않는다.

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

무대 SVG의 클래스(`d0-s-frame`, `d0-s-accent`, `d0-s-tick` 등)와 무대 CSS는 [diagrams/index.md](../diagrams/index.md)·[shell/contract.md](../shell/contract.md)를 따른다. 아래는 2단계만 줄였다.

```html
<div class="d0-wide">
<div class="d0-check d0-cols" data-variant="linked">
  <figure class="d0-fig d0-check__stage" data-stage data-active-step="1">
    <div class="d0-fig__stage">
      <svg viewBox="0 0 560 342" role="img" aria-labelledby="ls-t ls-d">
        <title id="ls-t">단계별 화면</title>
        <desc id="ls-d">설정 화면이에요. 왼쪽 메뉴의 내보내기가 파랗게 강조돼 있어요.</desc>
        <g data-step="1">
          <rect class="d0-s-frame" x="1.5" y="1.5" width="557" height="339" rx="19"/>
          <rect class="d0-s-fill" x="25" y="31" width="124" height="19" rx="9.5"/>
          <rect class="d0-s-accent" x="25" y="68" width="124" height="25" rx="9.5"/>
          <rect class="d0-s-fill" x="25" y="112" width="124" height="19" rx="9.5"/>
          <rect class="d0-s-fill" x="180" y="31" width="352" height="280" rx="16"/>
          <g class="d0-check__ok"><circle class="d0-s-node" cx="513" cy="47" r="17" data-tone="green"/><path class="d0-s-tick" d="M506 47 L512 53 L522 41"/></g>
        </g>
        <g data-step="2">
          <rect class="d0-s-frame" x="1.5" y="1.5" width="557" height="339" rx="19"/>
          <rect class="d0-s-fill" x="25" y="31" width="311" height="19" rx="9.5"/>
          <rect class="d0-s-zone" x="25" y="75" width="507" height="62" rx="16"/>
          <rect class="d0-s-accent" x="44" y="96" width="187" height="19" rx="9.5"/>
          <rect class="d0-s-fill" x="25" y="162" width="373" height="19" rx="9.5"/>
          <g class="d0-check__ok"><circle class="d0-s-node" cx="513" cy="47" r="17" data-tone="green"/><path class="d0-s-tick" d="M506 47 L512 53 L522 41"/></g>
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
</div>
```

```css
/* 2열 격자는 .d0-cols(정본 assets/page.css)가 만든다 */
@media (min-width: 960px) {
  .d0-check__stage { position: sticky; top: 24px; }
}
.d0-check__stage g[data-step], .d0-check__ok { display: none; }
/* 선택자는 페이지의 단계 수만큼 둔다(구간을 쓰면 15까지) */
.d0-check__stage[data-active-step="1"] g[data-step="1"],
.d0-check__stage[data-active-step="2"] g[data-step="2"],
.d0-check__stage[data-active-step="3"] g[data-step="3"],
.d0-check__stage[data-active-step="4"] g[data-step="4"],
.d0-check__stage[data-active-step="5"] g[data-step="5"],
.d0-check__stage[data-active-step="6"] g[data-step="6"],
.d0-check__stage[data-active-step="7"] g[data-step="7"],
.d0-check__stage[data-active-step="8"] g[data-step="8"],
.d0-check__stage[data-active-step="9"] g[data-step="9"],
.d0-check__stage[data-active-step="10"] g[data-step="10"],
.d0-check__stage[data-active-step="11"] g[data-step="11"],
.d0-check__stage[data-active-step="12"] g[data-step="12"],
.d0-check__stage[data-active-step="13"] g[data-step="13"],
.d0-check__stage[data-active-step="14"] g[data-step="14"],
.d0-check__stage[data-active-step="15"] g[data-step="15"],
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
.d0-check__stage[data-active-step="7"] .d0-check__code > [data-step="7"],
.d0-check__stage[data-active-step="8"] .d0-check__code > [data-step="8"],
.d0-check__stage[data-active-step="9"] .d0-check__code > [data-step="9"],
.d0-check__stage[data-active-step="10"] .d0-check__code > [data-step="10"],
.d0-check__stage[data-active-step="11"] .d0-check__code > [data-step="11"],
.d0-check__stage[data-active-step="12"] .d0-check__code > [data-step="12"],
.d0-check__stage[data-active-step="13"] .d0-check__code > [data-step="13"],
.d0-check__stage[data-active-step="14"] .d0-check__code > [data-step="14"],
.d0-check__stage[data-active-step="15"] .d0-check__code > [data-step="15"] { display: grid; }
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
.d0-check[data-variant="linked"] .d0-check__row[data-status="done"] label { text-decoration: none; } /* 체크 원·번호 원이 완료를 말한다 */
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
  var rows = Array.prototype.slice.call(list.querySelectorAll('.d0-check__row'));
  if (!rows.length) return;
  function show(row) {
    var n = row.dataset.step;
    stage.dataset.activeStep = n;
    var strong = document.createElement('strong');
    strong.textContent = n + '단계';
    cap.replaceChildren(strong, ' ' + row.dataset.caption);
    desc.textContent = row.dataset.desc;
    rows.forEach(function (r) { r.toggleAttribute('data-current', r === row); });
    list.dispatchEvent(new CustomEvent('d0-step')); // 선택 변경 알림. 구간 JS는 받아도 펼침·진행 수를 바꾸지 않는다
  }
  function sync() {
    var n = 0;
    rows.forEach(function (row) {
      var checked = row.querySelector('.d0-check__box').checked;
      var group = stage.querySelector('g[data-step="' + row.dataset.step + '"]');
      if (checked) { row.dataset.status = 'done'; n++; }
      else delete row.dataset.status;
      group.toggleAttribute('data-done', checked);
    });
    list.querySelector('[data-count]').textContent = n;
    var bar = list.querySelector('progress');
    bar.value = n; bar.textContent = n + ' / ' + bar.max;
  }
  function firstIncomplete(candidates) {
    return candidates.find(function (row) { return !row.querySelector('.d0-check__box').checked; });
  }
  // hover는 실제 포인터 이동일 때만 받는다. 구간이 접히며 가만히 있는 포인터 밑으로 행이 올라와도
  // (브라우저가 보내는 mouseenter) 체크로 옮겨 간 단계를 덮어쓰지 않는다.
  var px = null, py = null;
  rows.forEach(function (row) {
    row.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse' || (e.clientX === px && e.clientY === py)) return;
      px = e.clientX; py = e.clientY;
      if (!row.hasAttribute('data-current')) show(row);
    });
    row.addEventListener('focusin', function () { show(row); });
    row.addEventListener('click', function (e) {
      // 체크박스·label의 활성 이동은 change에서 한 번만 처리한다.
      if (e.target.closest('.d0-check__box, label')) return;
      show(row);
    });
  });
  list.addEventListener('change', function (e) {
    if (!e.target.matches('.d0-check__box')) return;
    var row = e.target.closest('.d0-check__row');
    sync();
    var next = firstIncomplete(rows.slice(rows.indexOf(row) + 1)) || firstIncomplete(rows);
    show(e.target.checked ? (next || rows[rows.length - 1]) : row);
  });
  sync();
  show(firstIncomplete(rows) || rows[rows.length - 1]);
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

### 구간 스니펫

기본·linked 변형 모두에 붙는다. `.d0-check`(linked는 `.d0-check__list` 안)에 진행률 → 구간 목록 순서로 둔다. 진행률과 구간 사이에 status rail을 두지 않는다. 아래는 linked 목록 쪽만 2구간 4단계로 줄였다.
구간을 쓰면 진행률 라벨은 `전체 n / N 완료`로 쓴다. 머리 행 `h3` 안 네 칸(상태 원·이름·진행 수·결과)이 정본이고, 정적 글자는 JS 없을 때 보이는 머리다.

```html
<div class="d0-check" data-variant="linked" data-phased>
  <!-- 무대 figure.d0-check__stage는 linked 스니펫과 같다(단계 4개 그룹) -->
  <div class="d0-check__list">
    <label class="d0-check__progress" for="ph-progress">전체 <output data-count>0</output> / 4 완료</label>
    <progress class="d0-check__bar" id="ph-progress" max="4" value="0">0 / 4</progress>
    <ol class="d0-check__phases">
      <li class="d0-check__phase" data-phase="1">
        <h3 class="d0-check__phase-head">
          <span class="d0-check__phase-mark" aria-hidden="true"></span>
          <span class="d0-check__phase-name">쓸 수 있는 상태</span>
          <span class="d0-check__phase-count">2단계</span>
          <span class="d0-check__phase-result">내보내기 메뉴를 쓸 수 있어요.</span>
        </h3>
        <ol>
          <li class="d0-check__row" data-step="1" data-current data-meta="none" data-caption="…" data-desc="…">…</li>
          <li class="d0-check__row" data-step="2" data-meta="none" data-caption="…" data-desc="…">…</li>
        </ol>
      </li>
      <li class="d0-check__phase" data-phase="2">
        <h3 class="d0-check__phase-head">
          <span class="d0-check__phase-mark" aria-hidden="true"></span>
          <span class="d0-check__phase-name">첫 파일 받기</span>
          <span class="d0-check__phase-count">2단계</span>
          <span class="d0-check__phase-result">첫 파일을 받아요.</span>
        </h3>
        <ol>
          <li class="d0-check__row" data-step="3" data-meta="none" data-caption="…" data-desc="…">…</li>
          <li class="d0-check__row" data-step="4" data-meta="none" data-caption="…" data-desc="…">…</li>
        </ol>
      </li>
    </ol>
  </div>
</div>
```

단계가 짧고 적어 모두 펼쳐 둘 때는 `data-phased="open"`을 쓴다. 머리 행은 같고 접지 않는다.

```css
/* 구간: 머리 행이 지도다(상태 원 · 이름 · 진행 수 / 결과 한 줄). status rail·checkpoint는 쓰지 않는다 */
.d0-check__phase { border-top: 1px solid var(--d0-grey-100); }
.d0-check__phase-head {
  display: grid; grid-template-columns: 24px minmax(0, 1fr) auto; column-gap: 12px; align-items: start;
  margin: 0; padding: 12px 0; color: var(--d0-grey-900); font-size: 15px; font-weight: 600; line-height: var(--d0-leading-body);
}
.d0-check__phase-head:has(> .d0-check__phase-toggle) { padding: 0; } /* JS가 넣은 버튼이 같은 격자·여백을 이어받는다 */
.d0-check__phase-toggle {
  grid-column: 1 / -1; display: grid; grid-template-columns: inherit; column-gap: inherit; align-items: start;
  width: 100%; padding: 12px 0; border: 0; background: none; color: inherit; font: inherit; text-align: left; cursor: pointer;
}
.d0-check__phase-toggle:focus-visible { outline: 2px solid var(--d0-blue); outline-offset: 2px; border-radius: var(--d0-radius-sm); }
.d0-check__phase-mark {
  grid-column: 1; grid-row: 1; justify-self: center; display: grid; place-content: center; box-sizing: border-box;
  width: 18px; height: 18px; margin-top: calc((15px * var(--d0-leading-body) - 18px) / 2);
  border: 2px solid var(--d0-grey-500); border-radius: 999px; background: #fff; color: #fff; font-size: 11px; line-height: 1;
}
.d0-check__phase-name { grid-column: 2; grid-row: 1; min-width: 0; }
.d0-check__phase-count { grid-column: 3; grid-row: 1; color: var(--d0-grey-600); font-size: var(--d0-text-compact); font-weight: 600; font-variant-numeric: tabular-nums; white-space: nowrap; line-height: calc(15px * var(--d0-leading-body)); }
.d0-check__phase-count:empty { display: none; }
.d0-check__phase-result { grid-column: 2 / -1; grid-row: 2; color: var(--d0-grey-600); font-size: var(--d0-text-compact); font-weight: 500; }
.d0-check__phase[data-state="current"] .d0-check__phase-mark { border-color: var(--d0-blue-dark); }
.d0-check__phase[data-state="done"] .d0-check__phase-mark { border-color: var(--d0-green); background: var(--d0-green); }
.d0-check__phase[data-state="done"] .d0-check__phase-mark::after { content: "✓"; }
.d0-check__phase:is([data-state="done"], [data-state="planned"]) .d0-check__phase-name { color: var(--d0-grey-700); font-weight: 500; }
/* JS가 붙일 때만, 화면에서만 접힌다. 인쇄는 이 규칙이 없어 전 구간이 펼쳐진다 */
@media screen { .d0-check__phase[data-collapsed] > :not(.d0-check__phase-head) { display: none; } }
```

green 원 위 흰 `✓`는 체크박스와 같은 3.47:1(그래픽 3:1)이다. grey-500 테두리는 흰 바탕 위 3.2:1이다.

```js
// 구간: linked·기본 JS보다 뒤에 붙인다. 진행률·무대는 그 JS가, 머리 행 상태·접힘은 이 JS가 맡는다.
document.querySelectorAll('.d0-check[data-phased]').forEach(function (list, li) {
  var phases = Array.prototype.slice.call(list.querySelectorAll('.d0-check__phase'));
  if (!phases.length) return;
  var keepOpen = list.dataset.phased === 'open';
  var LABEL = { done: '완료', current: '진행 중', planned: '예정' };
  function rowsOf(el) { return Array.prototype.slice.call(el.querySelectorAll('.d0-check__row')); }
  function isDone(r) { return r.querySelector('.d0-check__box').checked; }
  function setOpen(ph, open) {
    ph.toggleAttribute('data-collapsed', !open);
    ph.querySelector('.d0-check__phase-toggle').setAttribute('aria-expanded', String(open));
  }
  phases.forEach(function (ph, i) {
    var head = ph.querySelector('.d0-check__phase-head');
    var steps = ph.querySelector(':scope > ol');
    if (!steps.id) steps.id = 'd0-phase-' + li + '-' + (i + 1);
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'd0-check__phase-toggle';
    btn.setAttribute('aria-controls', steps.id);
    while (head.firstChild) btn.appendChild(head.firstChild); // 네 칸을 버튼 안으로 옮길 뿐 다시 쓰지 않는다
    head.appendChild(btn);
    var mark = head.querySelector('.d0-check__phase-mark');
    mark.removeAttribute('aria-hidden'); mark.setAttribute('role', 'img');
    btn.addEventListener('click', function () { setOpen(ph, ph.hasAttribute('data-collapsed')); });
  });
  // 머리 행 상태·진행 수는 체크만 센다. relayout(체크 변화·첫 로드)일 때만 펼침·접힘과 포커스를 바꾼다.
  function update(relayout) {
    var all = rowsOf(list);
    var first = all.find(function (r) { return !isDone(r); });
    var cur = first ? phases.indexOf(first.closest('.d0-check__phase')) : -1; // 진행 중 구간: 첫 미완료 단계가 있는 구간
    var active = list.querySelector('.d0-check__row[data-current]') || first || all[all.length - 1];
    var open = phases.indexOf(active.closest('.d0-check__phase'));
    phases.forEach(function (ph, i) {
      var rs = rowsOf(ph), k = rs.length, n = rs.filter(isDone).length;
      var state = n === k ? 'done' : i === cur ? 'current' : 'planned';
      ph.dataset.state = state;
      ph.querySelector('.d0-check__phase-count').textContent =
        state === 'done' ? '' : (state === 'current' || n) ? n + ' / ' + k : k + '단계';
      ph.querySelector('.d0-check__phase-mark').setAttribute('aria-label', LABEL[state]);
      if (relayout) setOpen(ph, keepOpen || i === open);
    });
    var f = document.activeElement;
    if (relayout && f && list.contains(f) && f.closest('[data-collapsed]')) active.querySelector('.d0-check__box').focus();
  }
  list.addEventListener('change', function (e) {
    if (e.target.matches('.d0-check__box')) setTimeout(function () { update(true); }, 0); // linked JS가 다음 단계를 고른 뒤
  });
  list.addEventListener('d0-step', function () { update(false); }); // linked 선택 변경: 펼침·진행 수는 그대로
  setTimeout(function () { update(true); }, 0);
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
- 총 단계 수로 기계적으로 접기, 구간마다 카드·배경 상자, 추상어 이름만 있고 머리 행에 결과 한 줄이 없는 구간, JS 없이도 접혀 있는 구간.
- 구간 이름·결과·진행 수를 두 곳 이상에 쓰기: 진행률 아래 구간 status rail, 펼친 구간의 별도 머리(`보낼 링크 · 1 / 4`), 구간 끝 checkpoint 줄. 진행 수를 활성 단계 위치로 세기(모두 끝났는데 `1 / 4`).
- linked 변형에서 행 안에 코드 접힘(`<details>`)을 두지 않는다. 코드는 활성 단계 코드 영역에 펼쳐 두고, 960px 미만에서도 행 아래에 펼쳐 붙인다.
