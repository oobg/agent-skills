# diagram — 상자 도식

## 해부 구조

- 상자 3~5개 + 화살표. 상자 = 번호 → 이름 → 한 줄 역할.
- 상자는 HTML 텍스트, 화살표만 인라인 SVG(`currentColor`)로 그린다. 그림 속 글자는 쓰지 않는다.
- `figcaption`에 "그래서 무엇이 보이는가"를 한 줄로 단다.

## 언제 쓰나 / 변형

- `data-variant="flow"`(기본): 왼쪽에서 오른쪽으로 시간 순서. 모바일에서는 위에서 아래로.
- `data-variant="layers"`: 위아래로 쌓인 구성요소와 그 관계(화면 / 서버 / 저장소).

## 스니펫

```html
<figure class="d0-diagram" data-variant="flow">
  <ol>
    <li><div class="d0-diagram__box"><b>1</b><strong>요청</strong><span>사용자가 내보내기를 눌러요</span></div>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></li>
    <li><div class="d0-diagram__box"><b>2</b><strong>줄 서기</strong><span>번호표를 받고 차례를 기다려요</span></div>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></li>
    <li><div class="d0-diagram__box"><b>3</b><strong>파일 완성</strong><span>다 되면 알림으로 알려 줘요</span></div></li>
  </ol>
  <figcaption>오래 걸리는 일은 줄을 서서 차례대로 처리해요.</figcaption>
</figure>
```

```css
.d0-diagram { margin: 0; display: grid; gap: 12px; }
.d0-diagram ol { display: flex; gap: 8px; }
.d0-diagram li { flex: 1 1 0; min-width: 0; display: flex; align-items: center; gap: 8px; }
.d0-diagram__box {
  flex: 1;
  display: grid;
  gap: 2px;
  padding: 16px;
  border-radius: var(--d0-radius-control);
  background: var(--d0-grey-50);
}
.d0-diagram__box b { color: var(--d0-blue-dark); font-size: var(--d0-text-compact); }
.d0-diagram__box span { color: var(--d0-grey-600); font-size: var(--d0-text-compact); }
.d0-diagram li > svg { flex: none; width: 20px; color: var(--d0-grey-500); }
.d0-diagram figcaption { color: var(--d0-grey-600); }
.d0-diagram[data-variant="layers"] ol,
.d0-diagram[data-variant="layers"] li { flex-direction: column; align-items: stretch; }
.d0-diagram[data-variant="layers"] li > svg { align-self: center; transform: rotate(90deg); }
@media (max-width: 640px) {
  .d0-diagram ol, .d0-diagram li { flex-direction: column; align-items: stretch; }
  .d0-diagram li > svg { align-self: center; transform: rotate(90deg); }
}
```

## 금지

- 정보 없는 장식 그림, 상자 6개 이상.
- SVG `<text>`나 이미지에 글자를 굽기(모바일에서 읽을 수 없다).
