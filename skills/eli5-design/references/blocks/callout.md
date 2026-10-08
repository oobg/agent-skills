# callout — 알림 상자

## 해부 구조

- soft 블루 박스(`--d0-blue-light` 배경, 보더 없음) 하나에 한 가지 목적만 담는다.
- 라벨(목적) → 한두 문장 → 필요하면 `무엇을·누가·언제까지` 행.
- **페이지당 최대 1개.** 결론은 header 리드나 섹션 제목이 말하고, callout은 독자가 행동해야 하는 한 가지(대개 결정 요청)에 쓴다.
- **히어로와 중복 금지.** 히어로가 결론 수치를 말하면 callout에 그 결론·숫자를 다시 쓰지 않는다.

## 언제 쓰나 / 변형

- `data-variant="decision"`: 결정 요청. 무엇을, 누가, 언제까지 정하는지 행으로 적는다.
  header 요약 행에 `결정 필요` 행이 있으면 이 callout을 두지 않는다(둘 중 하나만).
- **문서 끝 다음 행동·결정은 공용 마무리 `footer.d0-closing`이 맡는다. callout은 본문 중간용이다.** 같은 결정·다음 할 일을 callout과 closing에 함께 두지 않는다.
- `data-variant="next"`: 본문 중간의 다음 할 일 한 가지(예: 다음 섹션을 읽기 전에 독자가 먼저 해야 할 일). 자리는 그 할 일이 속한 섹션의 끝, 섹션 안쪽이다(`section` 밖 `main` 직계로 두지 않는다). 문서 끝의 다음 행동은 closing `action`이다.
- `data-variant="conclusion"`: 리드로 결론을 말할 수 없을 때만. 히어로가 있으면 쓰지 않는다.

## 스니펫

CSS는 `assets/page.css`에 들어 있어 따로 붙이지 않는다.

```html
<aside class="d0-callout" data-variant="decision" aria-label="결정 요청">
  <strong class="d0-callout__label">결정이 필요해요</strong>
  <p>알림을 매일 보낼지 매주 보낼지 정해 주세요.</p>
  <dl>
    <div><dt>무엇을</dt><dd>알림 주기</dd></div>
    <div><dt>누가</dt><dd>팀 A 리더</dd></div>
    <div><dt>언제까지</dt><dd>3월 6일</dd></div>
  </dl>
</aside>
```

## 금지

- 페이지에 2개 이상, 결론·경고·장식용 반복, 문단 3개 이상.
- 한 상자에 결론과 결정 요청을 함께 담기.
- 히어로와 결론 callout을 함께 두기, 히어로 숫자를 callout에 되풀이하기.
- header 요약 행의 `결정 필요` 행과 결정 callout을 함께 두기.
