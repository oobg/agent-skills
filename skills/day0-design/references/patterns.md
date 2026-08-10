# Day0 UI 패턴 레시피

수치·색은 항상 `tokens.css` 변수. monorepo면 live `packages/ui` CSS를 우선 읽는다.

## 1. 상태 패턴 (`data-*`)

```tsx
<li className="d0-list-row" data-status={item.status} data-interactive="true">
  <span className="d0-badge" data-tone="green">완료</span>
</li>
```

```css
.d0-list-row[data-status="installing"] {
  background: var(--d0-blue-light);
}
.d0-list-row[data-status="done"] .d0-list-row__title {
  color: var(--d0-grey-600);
}
.d0-list-row[data-status="failed"] {
  background: var(--d0-red-bg);
}
```

- 시각 전이: `installing` | `done` | `failed`. `pending` = 기본(무추가 스타일).
- 관례: `data-status`, `data-tone`, `data-variant`, `data-size`, `data-active`,
  `data-current`, `data-disabled`, `data-interactive`, `data-error`, `data-padding`,
  `data-width`.
- Base UI: `data-open` / `data-checked` / `data-starting-style` / `data-ending-style`.

## 2. Button

| variant | 표현 |
| --- | --- |
| primary | fill `--d0-blue`, 흰 텍스트 |
| secondary | 흰 + `1px` grey-200 |
| ghost | 투명, hover grey-100 |
| danger | fill `--d0-red` |

| size | height | font | radius |
| --- | --- | --- | --- |
| lg | 56 | 17 / 600 | control |
| md | 48 | 15 / 600 | control |
| sm | 36 | 14 / 600 | sm |

- focus-visible: soft blue ring 3px  
- disabled: opacity 등 (live Button은 opacity 0.5 — 규범상 grey 처리 권장이지만
  기존 Button 재사용 시 live 동작 유지)  
- **주 job당 primary fill 1개** (기존 다동선 화면은 추가 난립만 막을 것)

## 3. Card + List (보더리스)

**Card 기본 = `plain`.** 항목마다 Card 금지.

| variant | 표현 |
| --- | --- |
| **plain (default)** | 배경·보더·그림자 없음, 패딩만 |
| soft | grey-50, radius control, 보더 없음 |
| outlined | 흰 + 1px grey-200 + shadow-card **예외 컨테이너** |

**리스트 기본 (SPEC-V4):**

```
행 (ListRow 또는 커스텀 행)
────────────────────────  ← Divider / border-top grey-100
행
```

outlined 카드로 리스트를 감싸는 것은 레거시. 온보딩·관리자 밀도 화면은
**래핑 없는 행 + 디바이더** 또는 plain/soft 블록을 우선.

- ListRow padding `14px 16px`, gap 12  
- title 15/600, subtitle 13/400 grey-500  
- interactive hover grey-50  

## 4. StatusBadge

- padding `4px 10px`, radius `999px`, font 12/600  
- tone soft bg + strong fg  
- pill 대표 시그니처. Toggle/Progress/dot 등 다른 999px는 허용.

## 5. IconCircle

| size | box | emoji | radius |
| --- | --- | --- | --- |
| sm | 36 | 18 | control |
| md | 44 | 22 | ~14 / control |
| lg | 56 | 28 | card |

기본 tone grey → `--d0-grey-50`.

## 6. Input

label 13/500 · box h=52 radius control · field 15/500  
focus: border blue + ring `rgba(61,125,229,.2)`  
error: red border/ring  

## 7. 테이블 (관리자, CSS-only)

React 컴포넌트 없음. 화면에서:

```html
<table class="d0-table d0-table-compact">
```

계약 (`table.css`):

- 행 높이 `--d0-density-row` (38)  
- th compact: `--d0-label` 11px / 600 / **`text-transform: uppercase`** /
  `--d0-label-tracking` — **관리자 컬럼 헤더 예외** (본문 한글 라벨 uppercase 금지와 별개)  
- `tr[data-active]` · `td[data-num]` / `data-align="right"`  
- 구분선 grey-100/200  

## 8. 페이지 셸

```tsx
<PageEnter width="narrow">  {/* 640 */}
<PageEnter width="wide">    {/* 1200 live */}
<PageEnter width="content">
```

진입: opacity + y, SPRING_SOFT, stagger ~0.06s.

## 9. TopBar + BottomCTA

- TopBar sticky blur, 뒤로 / 타이틀 / 우측  
- BottomCTA: sticky + **상단 grey 그라데이션 페이드** + safe-area (단순 보더만으로
  대체하지 말 것 — live `bottom-cta.css`)

## 10. Empty / Error

중앙, gap 8, padding 48×24 · 이모지 선택 · title 17/600 · desc 14 grey-500 max 320

## 11. 선택 상태 (설치 카드 등)

선택 = 체크/배지/soft blue-light 위주. **전부 두꺼운 블루 보더** 금지.

## 12. 포커스 링

```css
box-shadow: 0 0 0 3px color-mix(in srgb, var(--d0-blue) 28%, transparent);
/* 또는 rgba(61, 125, 229, 0.2) */
```

`rgba(49, 130, 246, …)` 금지.

## 13. 모션 상수

```ts
export const SPRING = { type: "spring", stiffness: 400, damping: 32 };
export const SPRING_SOFT = { type: "spring", stiffness: 260, damping: 30 };
```

## 14. 신규 컴포넌트 등록 (packages/ui)

1. `src/<name>.tsx` + `src/<name>.css`  
2. `styles.css`에 `@import "./<name>.css"`  
3. `index.ts`에서 export  

빠지면 스타일 없는 컴포넌트가 나간다.

## 15. `@day0/ui` 공개 맵 (index 기준)

**컴포넌트:** Button, Input, Toggle, Checkbox, Select, CodeInput, Card, Divider,
ListRow, IconCircle, StatStrip, StepProgress, ProgressBar, AnimatedNumber,
StatusBadge, CheckPop, Modal, BottomSheet, Kbd, KbdGroup, CommandBlock, Spinner,
Skeleton, Confetti, EmptyState, Toast, FloatingSummary, TopBar, BottomCTA,
PageEnter, StaggerItem, CheckIcon, WarningIcon  

**유틸:** SPRING, SPRING_SOFT, cn, writeClipboard, useCopyFeedback, useCopyKeyFeedback  

**CSS-only:** `d0-table`, `d0-table-compact` (export 없음)
