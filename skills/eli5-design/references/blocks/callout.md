# callout — 알림 상자

## 해부 구조

- soft 블루 박스(`--d0-blue-light` 배경, 보더 없음) 하나에 한 가지 목적만 담는다.
- 라벨(목적) → 한두 문장 → 필요하면 `무엇을·누가·언제까지` 행.
- **페이지당 최대 1개.** 결론은 header 리드나 섹션 제목이 말하고, callout은 독자가 행동해야 하는 한 가지(대개 결정 요청)에 쓴다.
- **히어로와 중복 금지.** 히어로가 결론 수치를 말하면 callout에 그 결론·숫자를 다시 쓰지 않는다.

## 언제 쓰나 / 변형

- `data-variant="decision"`: 결정 요청. 무엇을, 누가, 언제까지 정하는지 행으로 적는다.
  header 요약 행에 `결정 필요` 행이 있으면 이 callout을 두지 않는다(둘 중 하나만).
- `data-variant="next"`: 결정이 없는 페이지의 다음 할 일 한 가지.
- `data-variant="conclusion"`: 리드로 결론을 말할 수 없을 때만. 히어로가 있으면 쓰지 않는다.

## 스니펫

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

```css
.d0-callout {
  display: grid;
  gap: 8px;
  padding: 20px 24px;
  border-radius: var(--d0-radius-card);
  background: var(--d0-blue-light);
}
.d0-callout__label { color: var(--d0-blue-dark); font-size: var(--d0-text-compact); font-weight: 600; }
.d0-callout p { color: var(--d0-grey-900); }
.d0-callout dl { display: flex; flex-wrap: wrap; gap: 8px 24px; margin-top: 4px; }
.d0-callout dt { color: var(--d0-grey-700); font-size: var(--d0-meta); }
.d0-callout dd { font-weight: 600; }
@media (max-width: 640px) { .d0-callout { padding: 16px; } }
```

## 금지

- 페이지에 2개 이상, 결론·경고·장식용 반복, 문단 3개 이상.
- 한 상자에 결론과 결정 요청을 함께 담기.
- 히어로와 결론 callout을 함께 두기, 히어로 숫자를 callout에 되풀이하기.
- header 요약 행의 `결정 필요` 행과 결정 callout을 함께 두기.
