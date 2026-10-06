# header — 머리 (필수)

## 해부 구조

- 작업 라벨(회색 pill, 예: `작업-000`) → 제목 h1 → 리드 1~2줄 → 1px 구분선.
- 리드는 "이 페이지를 다 읽으면 무엇을 알게 되는가"를 한 문장으로 말한다.
- 리드는 header 폭을 그대로 쓴다. 옆 공간이 남는데 줄이 바뀌면 실패다.

## 언제 쓰나 / 변형

- 모든 페이지의 첫 블록. 하나만 둔다.
- 상태가 중요한 페이지(incident)는 라벨 옆에 상태 배지를 하나 더 둔다(`data-tone`).
- guide는 총 소요 시간을, report는 결론을 리드에 넣는다.

## 스니펫

```html
<header class="d0-header">
  <div class="d0-header__meta">
    <span class="d0-pill">작업-000</span>
    <span class="d0-pill" data-tone="green">해결됨</span>
  </div>
  <h1>주문 내보내기 파일은 이렇게 생겼어요</h1>
  <p class="d0-header__lead">이 페이지를 다 읽으면 내보내기 파일에 어떤 시트가 있고, 각 칸이 무엇을 뜻하는지 알 수 있어요.</p>
</header>
```

```css
.d0-header {
  display: grid;
  gap: 12px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--d0-grey-200);
}
.d0-header__meta { display: flex; flex-wrap: wrap; gap: 6px; }
.d0-header h1 {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: var(--d0-tracking-display);
  line-height: var(--d0-leading-display);
}
.d0-header__lead {
  font-size: 17px;
  color: var(--d0-grey-700);
}
@media (max-width: 640px) {
  .d0-header h1 { font-size: 22px; }
  .d0-header__lead { font-size: 15px; }
}
```

## 금지

- 그라디언트 히어로, eyebrow 대문자 라벨, 히어로 일러스트.
- 리드에 컨테이너보다 좁은 `max-width`·`width`·`ch` 제약, 리드에 `text-wrap: balance`.
