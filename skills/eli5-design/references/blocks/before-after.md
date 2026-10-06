# before-after — 전과 후

공용 정보 블록이다. 같은 대상의 전과 후를 같은 축으로 나란히 놓는다. compare 패턴 전용이 아니라 보고·사건·가이드·일정 어디서나 빌려 쓴다.
[evidence](evidence.md)의 Proof로 안에 넣을 수도 있다(경쟁이 아니라 근거 모양 하나다).

## 해부 구조

- `div.d0-ba[data-kind] > div[data-side="before"] + div[data-side="after"]`. 각 쪽 = 라벨 `span.d0-ba__label`(12px/600) + 내용(한 줄 `p`, 또는 작은 SVG·와이어 하나).
- 두 쪽은 같은 크기·같은 구도다. 전 라벨 grey-600, 후 라벨 blue-dark. 두 쪽 사이 가운데에 `→`(grey-500, `aria-hidden`)를 둔다. 상태를 색만으로 말하지 않고 라벨 글자가 늘 붙는다.
- 960px 미만에서는 위아래로 쌓고 화살표는 `↓`로 바뀐다.
- 카드·배경·테두리 상자 없음. 작은 그림을 넣을 때만 각 쪽에 grey-50 무대를 쓸 수 있다(그림 무대 규칙과 같다).

### 종류 (`data-kind`, 라벨 문구)

| `data-kind` | 전 라벨 / 후 라벨 | 예 |
| --- | --- | --- |
| `change`(기본) | `전` / `후` | 이미 정한 변경 |
| `fix` | `문제` / `수정` | 사건의 대응, 가이드의 막힘 해결 |
| `improve` | `기존` / `개선` | 보고의 달라진 점 |
| `forecast` | `예상` / `실제` | 계획 대비 결과, 일정 회고 |

라벨은 이름표의 기본 문구다. 사용자가 다른 말을 주면 그 말을 쓴다.

## 어느 모양을 쓰나

| 바뀐 것 | 쓰는 것 |
| --- | --- |
| 한두 가지 상태·방식 | 이 블록(`.d0-ba`) |
| 여러 항목의 값 | [diff-rows](diff-rows.md) 행(항목 \| 전 \| → \| 후) |
| 숫자 크기 | [diagram](diagram.md) 전/후 막대 또는 [kpi-cards](kpi-cards.md) 막대 변형 |
| 화면 배치 | 와이어프레임 두 장([diagram](diagram.md) (d)) 또는 [side-by-side](side-by-side.md) 와이어 카드 |

패턴별 예:
- report: `improve` — `기존 전체 받기` → `개선 묶음 골라 받기`, 아래 explanation `reason`.
- incident: `fix` — `문제 재시도 1번` → `수정 재시도 3번 + 알림`.
- guide: `fix` — 자주 막히는 설정의 `문제` 화면 → `수정` 화면.
- timeline: `forecast` — `예상 3월 둘째 주` → `실제 3월 넷째 주`, 아래 explanation `reason`.

## 스니펫

```html
<div class="d0-ba" data-kind="fix">
  <div data-side="before"><span class="d0-ba__label">문제</span><p>연결이 끊기면 한 번만 다시 보내요.</p></div>
  <span class="d0-ba__arrow" aria-hidden="true"></span>
  <div data-side="after"><span class="d0-ba__label">수정</span><p>세 번까지 다시 보내고 실패하면 알려요.</p></div>
</div>
```

```css
.d0-ba { display: grid; gap: 12px; align-items: start; }
.d0-ba > [data-side] { display: grid; gap: 4px; min-width: 0; }
.d0-ba__label { color: var(--d0-grey-600); font-size: var(--d0-meta); font-weight: 600; }
.d0-ba [data-side="after"] .d0-ba__label { color: var(--d0-blue-dark); }
.d0-ba [data-side] p { color: var(--d0-grey-800); }
.d0-ba [data-side="before"] p { color: var(--d0-grey-600); }
.d0-ba__arrow::before { content: "↓"; color: var(--d0-grey-500); }
@media (min-width: 960px) {
  .d0-ba { grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); column-gap: 24px; }
  .d0-ba__arrow { align-self: center; }
  .d0-ba__arrow::before { content: "→"; }
}
```

화살표 `span.d0-ba__arrow`는 필수다(evidence Proof 안에서도). 960px 이상 3열 grid가 전·화살표·후 세 자식을 전제로 한다.

## 금지

- 전과 후의 축이 다름(전은 화면, 후는 숫자), 두 쪽 크기·정보량 불균형.
- 취소선으로 전 값을 지우기(전 값은 작게 grey-600으로만), 색만으로 전/후 구분.
- 카드 상자, 의미색 글자.
