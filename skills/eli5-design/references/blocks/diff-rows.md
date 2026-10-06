# diff-rows — 바뀐 행

## 해부 구조

- 바뀐 항목만 행으로 나열한다. 행 = 항목명 | 전 | → | 후.
- 전 값은 `<del>`, 후 값은 `<ins>`로 감싸 바뀜을 마크업으로도 알린다(밑줄·취소선은 CSS로 끈다). 후 값만 블루로 강조한다. 머리 행의 `전`·`후` 라벨과 화살표가 색 없이도 방향을 알려 준다.
- 행 사이는 1px 디바이더.

## 언제 쓰나 / 변형

- compare 전/후 변형, timeline 변경 내역에서 "무엇이 어떻게 바뀌었나"를 보여 줄 때.
- 항목마다 "나에게 달라지는 점"이 필요하면 후 값 아래 한 줄 주석을 둔다(`.d0-diff__note`).

## 배지 행 변형 (한계·위험 목록)

행 목록은 `ul.d0-rows > li`, 행 = 배지(`span.d0-pill`) → `div`(제목 `strong` 15px/600 + 한 줄 `p` 14px grey-600).
배지는 제목 **첫 줄 가운데**에 맞춘다. 행은 `align-items: start`, 배지 위 여백은 줄 높이에서 계산한다:
`margin-top = (제목 글자 15px × --d0-leading-body − 배지 높이 22px) ÷ 2` = (23.25 − 22) ÷ 2 ≈ 0.6px.
고정 `1px`로 두면 반올림 차이로 중심이 어긋난다. 작은 배지(`data-size="sm"`, 20px)는 식의 22를 20으로 바꾼다.
배지는 행 높이로 늘어나지 않는다.
**배지 열 폭 고정.** 모든 행의 제목이 같은 x에서 시작하도록 배지 열을 목록 전체에서 하나로 맞춘다. 목록이 열을 정의하고
행은 `subgrid`로 물려받아 가장 긴 배지 폭이 열 폭이 된다. `subgrid`를 못 쓰는 브라우저는 고정 64px 열로 떨어진다.
배지는 열 안에서 왼쪽 정렬(`justify-self: start`)이다.

```html
<ul class="d0-rows">
  <li><span class="d0-pill" data-tone="orange">중요</span><div><strong>밤사이 실패는 아침에야 알아요</strong><p>알림은 메일로만 가요.</p></div></li>
  <li><span class="d0-pill">참고</span><div><strong>파일은 30일 뒤 지워져요</strong></div></li>
</ul>
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
.d0-diff { width: 100%; table-layout: fixed; border-collapse: collapse; }
.d0-diff caption { text-align: left; padding-bottom: 8px; color: var(--d0-grey-600); }
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
.d0-diff th[scope="row"] { font-weight: 600; }
.d0-diff td:nth-child(2) { color: var(--d0-grey-600); }
.d0-diff td:nth-child(3), .d0-diff thead th:nth-child(3) { width: 28px; color: var(--d0-grey-600); }
.d0-diff td:last-child { color: var(--d0-blue-dark); font-weight: 600; }
.d0-diff del, .d0-diff ins { text-decoration: none; }
.d0-diff__note {
  display: block;
  color: var(--d0-grey-600);
  font-size: var(--d0-text-compact);
  font-weight: 400;
}
```

## 금지

- 바뀌지 않은 항목까지 전체 사양 나열.
- 색만으로 전후 구분(라벨·화살표를 함께 둔다).
- 배지 행을 `div` 나열로 만들기(행 목록은 `ul > li`), 배지 `margin-top`을 줄 높이와 무관한 고정값으로 두기.
- 행마다 `auto` 배지 열을 따로 둬 배지 길이에 따라 제목 시작 위치가 들쭉날쭉한 목록.
