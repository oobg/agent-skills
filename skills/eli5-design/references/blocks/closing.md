# closing — 마무리 한 문장과 메타 행

공용 정보 블록이다. 문서가 독자에게 남길 일 하나를 큰 한 문장으로 말하고, 구분선 아래 작은 메타 행(담당·기한·다음 등)에 이미 나온 사실만 적는다.
덱의 마지막 장뿐 아니라 page의 마지막 섹션 끝에서도 쓴다. 다음 행동·결정 요청은 [explanation](explanation.md)의 역할이 아니라 이 블록이 맡는다(page의 Next Action).
경계: closing은 독자에게 행동·결정을 요구한다. 영향(`impact`)이나 조건(`constraint`)을 설명하는 문장은 explanation에 두고, closing 문장에 영향 설명을 덧붙이지 않는다.

## 종류 (`data-closing`)

| `data-closing` | 쓰임 | 메타 라벨 예 |
| --- | --- | --- |
| `decision` | 선택지·방안 중 하나를 고르게 한다 | 담당 / 기한 / 다음 |
| `request` | 도움·자원·승인을 요청한다 | 요청 / 기한 / 다음 |
| `action` | 독자가 직접 해 볼 행동을 정한다 | 대상 / 언제 / 다음 |
| `criteria` | 끝났는지 확인할 기준을 남긴다 | 확인할 것 / 통과 기준 / 다음 |
| `takeaway` | 앞으로 지킬 것을 남긴다 | 지킬 것 / 담당 / 다음 |

라벨은 예다. 문서에 나온 사실에 맞게 바꾸고, 없는 담당·날짜를 만들어 채우지 않는다. 메타는 2~3칸이다.
메타는 앞에 나온 사실을 가리키는 자리라 같은 숫자 문자열 반복 셈(SKILL.md 원칙 8번)에서 뺀다. 그래도 숫자보다 담당·행동어(`다음 주 적용`, `운영 팀`)로 쓸 수 있으면 그쪽을 먼저 쓴다.

## 출력별 형태

- **deck.** 마지막 장 `section.d0-slide[data-kind="closing"][data-closing]`. 마크업·CSS·게이트는 [slide-deck](slide-deck.md) 마지막 장 절이 정본이다.
- **page.** 마지막 페이지 섹션 안쪽 끝의 `footer.d0-closing[data-closing]` 하나. 문장(17px/700 grey-900, h2보다 작다) → 12px → 1px grey-200 구분선(진한 구분선 금지의 예외, [shell.md](shell.md) 금지 절) → 12px → `dl.d0-closing__meta`(라벨 12px/600 grey-600, 값 14px grey-800). 960px 이상은 메타 3열, 그 아래는 `라벨 | 값` 행.
  섹션을 새로 만들지 않는다. 배경·테두리 상자·blue 면이 없다.

## 다른 요소와 겹치지 않게

- **결정은 한 곳.** header 요약 행에 결정 행(`data-tone="decision"`)이 있으면 page closing을 `decision`으로 두지 않는다(요약 행이 정본). 이때 closing이 필요하면 `action`·`takeaway`로 짧게 쓰거나 생략한다.
- **문서 끝은 closing.** 문서 끝의 다음 행동·결정은 closing이 맡는다. [callout](callout.md)은 본문 중간용이고, 같은 결정·다음 할 일을 callout과 closing에 함께 두지 않는다.
- **기억할 한 줄(`.d0-keep`)과.** 지킬 행동·결정이면 closing, 기억할 사실 한 문장이면 [shell.md](shell.md)의 `.d0-keep`이다. 둘을 함께 두면 `.d0-keep`이 closing 앞에 오고 같은 문장을 되풀이하지 않는다.
- **checklist 담당 변형과.** 할 일이 여럿이면 [checklist](checklist.md) 담당 변형이 정본이고, closing은 그중 가장 중요한 하나를 문장으로 올린다. 같은 문장을 되풀이하지 않는다.

## 스니펫 (page)

```html
<footer class="d0-closing" data-closing="decision">
  <p class="d0-closing__line">이번 주 안에 발송 주기를 정해 주세요.</p>
  <dl class="d0-closing__meta">
    <div><dt>담당</dt><dd>서비스 운영 팀</dd></div>
    <div><dt>기한</dt><dd><time datetime="2026-10-09">이번 주 금요일</time></dd></div>
    <div><dt>다음</dt><dd>다음 주에 적용해요</dd></div>
  </dl>
</footer>
```

```css
.d0-closing { display: grid; gap: 12px; }
.d0-closing__line { color: var(--d0-grey-900); font-size: 17px; font-weight: 700; line-height: var(--d0-leading-title); letter-spacing: var(--d0-tracking-title); text-wrap: pretty; }
.d0-closing__meta { display: grid; gap: 8px; margin: 0; padding-top: 12px; border-top: 1px solid var(--d0-grey-200); }
.d0-closing__meta > div { display: grid; grid-template-columns: 56px 1fr; gap: 8px; min-width: 0; }
.d0-closing__meta dt { color: var(--d0-grey-600); font-size: var(--d0-meta); font-weight: 600; }
.d0-closing__meta dd { margin: 0; color: var(--d0-grey-800); font-size: 14px; }
@media (min-width: 960px) {
  .d0-closing__meta { grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 24px; }
  .d0-closing__meta > div { grid-template-columns: 1fr; gap: 2px; }
}
```

## 금지

- 문서에 없던 새 사실을 메타에 쓰기, 메타 4칸 이상, 문장과 같은 무게의 불릿 목록.
- 결정 요청을 요약 행·callout·closing 여러 곳에 되풀이하기.
- 배경 상자·blue 면·Impact로 칠하기, page에 closing 둘 이상.
