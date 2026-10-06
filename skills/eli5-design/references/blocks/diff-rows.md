# diff-rows — 바뀐 행

## 해부 구조

- 바뀐 항목만 행으로 나열한다. 행 = 항목명 | 전 | → | 후.
- 후 값만 블루로 강조한다. 머리 행의 `전`·`후` 라벨과 화살표가 색 없이도 방향을 알려 준다.
- 행 사이는 1px 디바이더.

## 언제 쓰나 / 변형

- compare 전/후 변형, timeline 변경 내역에서 "무엇이 어떻게 바뀌었나"를 보여 줄 때.
- 항목마다 "나에게 달라지는 점"이 필요하면 후 값 아래 한 줄 주석을 둔다(`.d0-diff__note`).

## 스니펫

```html
<table class="d0-diff">
  <caption>바뀐 항목만 모았어요</caption>
  <thead>
    <tr><th scope="col">항목</th><th scope="col">전</th><th aria-hidden="true"></th><th scope="col">후</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">알림 주기</th><td>매주</td><td aria-hidden="true">→</td>
      <td>매일<span class="d0-diff__note">아침마다 어제 주문을 받아요</span></td></tr>
    <tr><th scope="row">파일 형식</th><td>한 시트</td><td aria-hidden="true">→</td><td>두 시트</td></tr>
    <tr><th scope="row">보관 기간</th><td>7일</td><td aria-hidden="true">→</td><td>30일</td></tr>
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
