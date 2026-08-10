# Day0 Design

Day0 제품 UI와 같은 시각 언어로 화면을 구현하는 에이전트 스킬입니다.
토큰·보더리스 문법·컴포넌트 패턴을 고정해, 설명 없이 같은 디자인을 재현합니다.
온톨로지·제품 기획 문서 없이도 스킬만으로 동작한다.

## 언제 사용하나요?

- Day0 / `@day0/ui` / day0-work UI를 구현·추가할 때
- `/day0-design` 으로 명시 호출할 때
- Day0 프로토타입 HTML을 토큰 문법으로 그릴 때

Day0 신호가 없는 범용 “온보딩·관리자·토스 느낌” 요청만으로는 자동 적용하지
않습니다. 카피만은 `ux-writing`, 진단만은 `references/anti-patterns.md` 게이트.

## 핵심 요약

- **브랜드:** `#3d7de5` (구 `#3182f6` 금지)
- **폰트:** Pretendard Variable, 타이트 한글 자간
- **면:** **보더리스 기본** (Card `plain`) — outlined·1px 박스는 예외
- **상태:** `data-*` + CSS 전이
- **CSS:** 바닐라 + `--d0-*`, Tailwind 유틸 화면 금지
- **CTA:** 주 job primary fill 1개
- **리스트:** 행 + 디바이더 (항목별 카드 금지)
- **정본:** monorepo면 `packages/ui` > 이 스킬 스냅샷

## 사용 예

```text
@day0/ui 패턴으로 관리자 진행현황 테이블을 추가해줘.
```

```text
이 HTML을 Day0 토큰·보더리스 문법으로 다시 그려줘.
```

## 구성

```text
day0-design/
├── SKILL.md
├── README.md
└── references/
    ├── tokens.css
    ├── patterns.md
    └── anti-patterns.md
```

- [`SKILL.md`](SKILL.md): 트리거, SSOT, 아이덴티티, 게이트
- [`references/tokens.css`](references/tokens.css): live 토큰 스냅샷
- [`references/patterns.md`](references/patterns.md): 컴포넌트·테이블 레시피
- [`references/anti-patterns.md`](references/anti-patterns.md): 금지·진단 게이트

운영 자산: `tokens.css`, `patterns.md`, `anti-patterns.md`

`DESIGN-REFRESH.md` §2 구 토큰은 폐기 초안입니다. live `packages/ui`를 따릅니다.

설치 방법은 저장소의 [루트 README](../../README.md)를 참고하세요.
