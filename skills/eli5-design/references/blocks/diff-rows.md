# diff-rows — 바뀐 행

## 해부 구조

- 바뀐 항목만 행으로 나열한다. 행 = 항목명 | 전 | → | 후.
- 전 값은 `<del>`, 후 값은 `<ins>`로 감싸 바뀜을 마크업으로도 알린다(밑줄·취소선은 CSS로 끈다). 후 값만 블루로 강조한다. 머리 행의 `전`·`후` 라벨과 화살표가 색 없이도 방향을 알려 준다.
- 행 사이는 1px `grey-100` 디바이더 하나뿐이다. 행에 배경·테두리 상자를 두지 않는다.
- 보조문(행 설명, 후 값 주석)은 14px grey-600, 한 줄이다. 공백 포함 50자를 넘으면 문장을 줄인다([shell.md](shell.md) 줄 길이 절).

## 언제 쓰나 / 변형

- compare 전/후 변형, timeline 변경 내역에서 "무엇이 어떻게 바뀌었나"를 보여 줄 때.
- 항목마다 "나에게 달라지는 점"이 필요하면 후 값 아래 한 줄 주석을 둔다(`.d0-diff__note`).
- 한계·참고 목록은 배지 행 변형, 대응이 필요한 위험·차단 목록(report 이슈·위험)은 위험 행 변형(`data-variant="risk"`).

## 배지 행 변형 (한계·위험 목록)

행 목록은 `ul.d0-rows > li`, 행 = 배지(`span.d0-pill`) → `div`(제목 `strong` 15px/600 + 한 줄 `p` 14px grey-600).
배지는 제목 **첫 줄 가운데**에 맞춘다. 행은 `align-items: start`, 배지 위 여백은 줄 높이에서 계산한다:
`margin-top = (제목 글자 15px × --d0-leading-body − 배지 높이 22px) ÷ 2` = (23.25 − 22) ÷ 2 ≈ 0.6px.
고정 `1px`로 두면 반올림 차이로 중심이 어긋난다. 작은 배지(`data-size="sm"`, 20px)는 식의 22를 20으로 바꾼다.
배지는 행 높이로 늘어나지 않는다.
**배지 열 폭 고정.** 모든 행의 제목이 같은 x에서 시작하도록 배지 열을 목록 전체에서 하나로 맞춘다. 목록이 열을 정의하고
행은 `subgrid`로 물려받아 가장 긴 배지 폭이 열 폭이 된다. `subgrid`를 못 쓰는 브라우저는 고정 64px 열로 떨어진다.
배지는 열 안에서 왼쪽 정렬(`justify-self: start`)이다.

**2열 변형(`ul.d0-rows.d0-cols`).** 행이 짝수이고 전체 폭에 한 줄 목록이 길게 늘어지면 목록을 2열로 나눈다. 열마다 32em이라 행 설명이 한 줄 50자를 넘지 않는다([shell.md](shell.md) `.d0-cols`).
960px 이상에서만 2열이고, 행은 왼쪽 열부터 차례로 채운다. 행 수가 짝수(4·6)일 때만 쓴다. 3·5행이면 외톨이 행이 생기므로
1열로 두고 문장을 줄인다. 2열에서는 각 열 첫 행의 구분선을 지운다. 글 열은 960px 이상에서 `minmax(0, 32em)` 트랙이다.

```html
<ul class="d0-rows">
  <li><span class="d0-pill" data-tone="orange">중요</span><div><strong>밤사이 실패는 아침에야 알아요</strong><p>알림은 메일로만 가요.</p></div></li>
  <li><span class="d0-pill">참고</span><div><strong>파일은 30일 뒤 지워져요</strong></div></li>
</ul>

<!-- 2열 변형: 짝수 행일 때만 -->
<ul class="d0-rows d0-cols">…</ul>
```

```css
.d0-rows { display: grid; grid-template-columns: max-content 1fr; column-gap: 12px; }
.d0-rows li {
  display: grid; grid-column: 1 / -1;
  grid-template-columns: 64px 1fr; /* subgrid 미지원 폴백 */
  grid-template-columns: subgrid;
  align-items: start; padding: 14px 0; border-top: 1px solid var(--d0-grey-100);
}
.d0-rows .d0-pill { justify-self: start; }
.d0-rows li:first-child { border-top: 0; padding-top: 0; }
.d0-rows .d0-pill { margin-top: calc((15px * var(--d0-leading-body) - 22px) / 2); }
.d0-rows .d0-pill[data-size="sm"] { margin-top: calc((15px * var(--d0-leading-body) - 20px) / 2); }
.d0-rows strong { display: block; font-size: 15px; line-height: var(--d0-leading-body); font-weight: 600; }
.d0-rows p { color: var(--d0-grey-600); font-size: 14px; }
.d0-rows.d0-cols { row-gap: 0; } /* .d0-cols의 row-gap이 행 구분선 사이로 새지 않게 */
.d0-rows[data-badge="head"], .d0-rows[data-badge="head"] li { grid-template-columns: minmax(0, 1fr); } /* 같은 상태: 배지는 섹션 머리에 한 번, 목록은 배지 열 없음(subgrid 폴백 포함) */
@media (min-width: 960px) {
  .d0-rows.d0-cols { grid-template-columns: max-content minmax(0, 32em) max-content minmax(0, 32em); column-gap: 12px; } /* 글 열 32em: shell.md 줄 길이 */
  .d0-rows.d0-cols li { grid-column: span 2; }
  .d0-rows.d0-cols[data-badge="head"] { grid-template-columns: repeat(2, minmax(0, 32em)); } /* 배지 열 없음: 글 열 둘 */
  .d0-rows.d0-cols[data-badge="head"] li { grid-column: span 1; }
  .d0-rows.d0-cols li:nth-child(odd) { margin-right: 36px; } /* 열 사이 48px = 12 + 36 */
  .d0-rows.d0-cols li:nth-child(2) { border-top: 0; padding-top: 0; }
}
```

## 위험 행 변형 (`data-variant="risk"`, report 이슈·위험)

배지 행의 확장이다. 행 = 배지(`위험` orange / `차단` red) → `div`(제목 `strong` = 위험 한 문장 + `dl.d0-risk`).
`dl`은 `영향`(무엇이 늦어지거나 깨지나)과 `대응`(누가 무엇을 하나) 두 쌍을 항상 갖는다. 대응이 아직 없으면 `대응` 칸에
`팀 A가 10월 8일까지 방법 정하기`처럼 대응을 정하는 행동을 쓴다. 칸을 비우거나 `검토 중`만 쓰지 않는다.

- 영향은 숫자나 날짜로 쓴다(`출시가 3일 늦어져요`). `큰 영향`처럼 크기를 말로만 하지 않는다.
- 대응은 주체 + 짧은 구다. 기한·조건까지 다 쓴 할 일은 다음 단계 checklist 행 하나가 정본이고, 여기서는 같은 문장을 되풀이하지 않는다.
- `dt`는 13px/600 grey-600, `dd`는 14px grey-800, 쌍 간격 4px. 한 `dd`는 한 줄(약 40자)이다.
- 행이 여러 줄이라 2열 변형(`.d0-cols`)과 함께 쓰지 않는다. 3행 이내.
- **모든 행이 같은 상태면 행 배지를 빼고 섹션 머리에 한 번만 단다**(`data-badge="head"`, [shell.md](shell.md) 배지 수 규칙). 상태 배지 하나를 h2 옆(`.d0-section-head__title`)에 두고, 목록은 배지 열 없이 제목·`dl`만 둔다.
  상태가 섞이면(`위험`과 `차단`) 행마다 배지를 단다. 배지 행 변형(한계·참고)도 같다.

```html
<!-- 같은 상태면: 섹션 머리 <div class="d0-section-head__title"><h2 …>…</h2><span class="d0-pill" data-tone="orange">위험</span></div> + <ul class="d0-rows" data-variant="risk" data-badge="head">(행에 배지 없음) -->
<ul class="d0-rows" data-variant="risk">
  <li><span class="d0-pill" data-tone="red">차단</span>
    <div><strong>결제 테스트 계정이 아직 안 나왔어요</strong>
      <dl class="d0-risk">
        <div><dt>영향</dt><dd>결제 화면 검수가 3일 밀려요</dd></div>
        <div><dt>대응</dt><dd>팀 B가 발급 요청을 다시 올렸어요</dd></div>
      </dl></div></li>
  <li><span class="d0-pill" data-tone="orange">위험</span>
    <div><strong>번역 문구가 2개 화면에서 넘쳐요</strong>
      <dl class="d0-risk">
        <div><dt>영향</dt><dd>그대로 두면 버튼 글자가 잘려요</dd></div>
        <div><dt>대응</dt><dd>팀 A가 짧은 문구로 바꿔요</dd></div>
      </dl></div></li>
</ul>
```

```css
.d0-risk { display: grid; grid-template-columns: max-content 1fr; gap: 4px 12px; margin: 6px 0 0; }
.d0-risk > div {
  display: grid; grid-column: 1 / -1;
  grid-template-columns: 32px 1fr; /* subgrid 미지원 폴백 */
  grid-template-columns: subgrid;
  align-items: baseline;
}
.d0-risk dt { color: var(--d0-grey-600); font-size: var(--d0-text-compact); font-weight: 600; }
.d0-risk dd { margin: 0; color: var(--d0-grey-800); font-size: 14px; }
```

## 스니펫

```html
<table class="d0-diff">
  <caption>바뀐 항목만 모았어요</caption>
  <thead>
    <tr><th scope="col">항목</th><th scope="col">전</th><th aria-hidden="true"></th><th scope="col">후</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">알림 주기</th><td><del>매주</del></td><td aria-hidden="true">→</td>
      <td><ins>매일</ins><span class="d0-diff__note">아침마다 어제 주문을 받아요</span></td></tr>
    <tr><th scope="row">파일 형식</th><td><del>한 시트</del></td><td aria-hidden="true">→</td><td><ins>두 시트</ins></td></tr>
    <tr><th scope="row">보관 기간</th><td><del><time datetime="P7D">7일</time></del></td><td aria-hidden="true">→</td><td><ins><time datetime="P30D">30일</time></ins></td></tr>
  </tbody>
</table>
```

```css
.d0-diff { width: 100%; max-width: 720px; table-layout: fixed; border-collapse: collapse; } /* 넓은 화면에서 전·후 값이 화살표에서 멀어지지 않게 */
.d0-diff caption { text-align: left; padding-bottom: 8px; color: var(--d0-grey-600); font-size: 14px; }
.d0-diff th, .d0-diff td {
  padding: 12px 8px 12px 0;
  border-top: 1px solid var(--d0-grey-100);
  text-align: left;
  vertical-align: top;
}
.d0-diff thead th {
  border-top: 0;
  color: var(--d0-grey-600);
  font-size: var(--d0-meta);
  font-weight: 600;
}
.d0-diff th[scope="row"] { color: var(--d0-grey-900); font-weight: 600; }
.d0-diff td:nth-child(2) { color: var(--d0-grey-600); }
.d0-diff thead th:nth-child(1) { width: 20%; }
.d0-diff thead th:nth-child(2) { width: 120px; }
.d0-diff td:nth-child(3), .d0-diff thead th:nth-child(3) { width: 28px; color: var(--d0-grey-600); }
@media (max-width: 640px) { /* 후 값 주석이 좁은 열에서 3줄로 접히지 않게 라벨·전 열을 줄인다 */
  .d0-diff thead th:nth-child(1) { width: 72px; }
  .d0-diff thead th:nth-child(2) { width: 104px; }
  .d0-diff td:nth-child(3), .d0-diff thead th:nth-child(3) { width: 20px; }
}
.d0-diff td:last-child { color: var(--d0-blue-dark); font-weight: 600; }
.d0-diff del, .d0-diff ins { text-decoration: none; }
.d0-diff__note {
  display: block;
  color: var(--d0-grey-600);
  font-size: 14px;
  font-weight: 400;
}
```

## 금지

- 바뀌지 않은 항목까지 전체 사양 나열.
- 색만으로 전후 구분(라벨·화살표를 함께 둔다).
- 배지 행을 `div` 나열로 만들기(행 목록은 `ul > li`), 배지 `margin-top`을 줄 높이와 무관한 고정값으로 두기.
- 행마다 `auto` 배지 열을 따로 둬 배지 길이에 따라 제목 시작 위치가 들쭉날쭉한 목록.
- 행 상자·배경, `grey-200` 이상 구분선, 한 줄 50자를 넘는 행 설명을 그대로 두기, 홀수 행 목록에 2열 변형.
- 행 하나에 배지 2개 이상, 페이지 배지 톤 4종류 이상, 모든 행에 같은 배지 되풀이(같은 상태면 `data-badge="head"`, [shell.md](shell.md) 배지 절).
- 위험 행에서 `영향`이나 `대응`을 빼기, `대응` 칸에 `검토 중`·`추후 대응`만 쓰기, 대응 문장을 다음 단계 행에 그대로 되풀이하기.
