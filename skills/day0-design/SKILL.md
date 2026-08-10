---
name: day0-design
description: "Day0 제품 UI를 동일 톤으로 구현한다. Pretendard, 톤다운 블루(#3d7de5), 보더리스(plain 기본), data-* 상태, 바닐라 CSS 토큰(--d0-*), 스프링 모션을 강제한다. Day0 / d0 UI / @day0/ui / day0-work / /day0-design 요청에 사용한다. 범용 온보딩·관리자·토스 느낌 요청만으로는 자동 호출하지 않는다(Day0 신호 없으면 확인). 카피 윤문은 ux-writing. 슬롭 진단만은 구현 없이 references/anti-patterns.md 게이트만."
---

# Day0 Design

화면·컴포넌트를 **Day0 제품과 같은 시각 언어**로 만든다. 취향 복제가 아니라
토큰·패턴·금지 규칙을 따른다.

## SSOT (역할 분리)

| 맥락 | 정본 |
| --- | --- |
| `day0-work` 등 monorepo 안 제품 작업 | **`packages/ui` 코드** (+ 기존 화면 module.css) |
| monorepo 밖 프로토타입·타 저장소 | 이 스킬 스냅샷 (`references/tokens.css` 등) |

구현 전 monorepo가 있으면 `packages/ui/src/tokens.css`와 쓸 컴포넌트 CSS를 읽고,
스킬과 다르면 **코드베이스를 우선**한다.

**문서 우선순위:** live `packages/ui` > `docs/SPEC-V4.md` / `SPEC-V5.md` >
이 스킬 > `docs/DESIGN-REFRESH.md`.  
`DESIGN-REFRESH.md` §2 토큰·radius 16/12·구 grey는 **v3 초안(폐기)**. 그 값을
다시 쓰지 않는다. 스킬 `references/tokens.css` = live 스냅샷.

## 모듈 라우팅

본문은 항상 로드한다. 아래는 조건이 맞을 때만 연다.

| 언제 | 연다 |
| --- | --- |
| 색·radius·타이포·모션 수치 | `references/tokens.css` |
| 리스트/카드/폼/테이블/레이아웃 레시피 | `references/patterns.md` |
| 슬롭·하드코딩 금지 / 진단만 | `references/anti-patterns.md` |

## 적용 대상

| 산출물 | 적용 |
| --- | --- |
| 제품 화면 (Next/React + `@day0/ui`) | 필수 — 기존 컴포넌트·토큰 재사용 |
| 신규 UI 컴포넌트 (`packages/ui`) | 필수 — `d0-` + data-* + CSS + **styles.css @import + index.ts export** |
| 프로토타입 HTML / 데모 | 필수 — tokens 로드 |
| 카피·에러 문구만 | 범위 밖 → `ux-writing` |
| 슬롭 진단만 (수정 없음) | 구현하지 말고 `references/anti-patterns.md` 게이트만 |

## 한 줄 아이덴티티

**톤다운 블루 + Pretendard 타이트 자간 + 보더리스(여백·타이포·디바이더) + 탄성 인터랙션.**

- 배경 60% · 텍스트 30% · 포인트 10% (6:3:1)
- **면 분리 기본 = 여백·타이포·1px 디바이더.** 카드 박스 보더는 예외(`outlined`)
- 그림자는 **오버레이(모달·플로팅) 위주**. 카드용 두꺼운 shadow 금지
- 회색만 남지 않게 — 주 CTA·활성·링크에 블루 포인트
- 제목 700, 본문 400, 컨트롤 600 (heading h2/h3는 live base 650 허용)

## 스택 규칙

1. **바닐라 CSS + CSS 변수.** Tailwind 유틸로 화면을 짜지 않는다.
2. **클래스 프리픽스 `d0-`.** 화면 전용 CSS Modules, 공용 `@day0/ui`.
3. **상태는 `data-*`.** 조건부 className 스택 대신 CSS 셀렉터.
4. **값은 토큰만.** (`#fff` 표면 예외 허용)
5. **폰트 Pretendard Variable.** Inter / Roboto / system-ui 단독 금지.
6. **라이트 온리.** 다크 팔레트를 임의로 추가하지 않는다.

## 토큰 요약 (정본: `references/tokens.css` = live 스냅샷)

| 역할 | 토큰 | 값 |
| --- | --- | --- |
| 브랜드 | `--d0-blue` | `#3d7de5` |
| hover | `--d0-blue-dark` | `#2f66c4` |
| soft | `--d0-blue-light` | `#eef3fb` |
| 본문 | `--d0-grey-900` | `#1a1f26` |
| 구분선/보더 | `--d0-grey-100` / `200` | — |
| radius | card `14` · control `10` · sm `8` | px |
| shadow | card 흔적(outlined 전용) · overlay 모달 | — |
| ease / dur | `--d0-ease` · `140ms` / `220ms` | — |
| 자간 | body `-0.02em` · title `-0.028em` · display `-0.032em` | — |

구 블루 `#3182f6` / `#1b64da` **금지** (themeColor·confetti·focus ring 포함).

## 타이포 위계

| 역할 | size / weight |
| --- | --- |
| 페이지 제목 | 22–24px / 700 |
| 섹션 | 16–17px / 600~650 |
| 리스트 제목 | 15px / 600 |
| 본문 | 15px / 400 |
| 라벨 | 13px / 500 (본문·온보딩 한글 uppercase 금지) |
| 관리자 compact th | 11px / 600 + **uppercase 허용** (`--d0-label-tracking`) |
| KPI | 26–28px / 700 + tabular-nums |

한글: `word-break: keep-all`, 제목 `text-wrap: balance`.

## 레이아웃

- **폭:** narrow `640` · wide **`1200`** (live `PageEnter`; SPEC-V4 문서 1280은 미반영 — 코드 우선) · content
- **패딩:** 데스크탑 `28×32`, 모바일(≤640) `16×20`
- **브레이크포인트:** ≤640 모바일 · ≤960 컴팩트 · TopBar 높이 전환 ≥901 · BottomSheet ~560
- **TopBar:** sticky, 56/60, blur 12px, 하단 1px grey-200
- **카드 패딩:** sm 20 · md 24 · lg 28
- **관리자 행:** `--d0-density-row` 38px

## 컴포넌트 원칙 (요약)

상세: `references/patterns.md`.

- **Card 기본 = `plain`** (배경·보더·그림자 없음). `soft` = grey-50 블록. `outlined` = 보더 박스 **예외**.
- **리스트:** 항목마다 Card 금지. 기본은 **행 + 디바이더**(또는 plain/soft 래퍼 안 ListRow). outlined 카드 래핑은 레거시.
- **Button:** primary/secondary/ghost/danger × sm·md·lg.  
  **primary fill 목표 1개/주 job.** 기존 화면의 크롬+콘텐츠 공존을 버그로 전면 리팩터하지 말고, 신규 화면은 1 primary 유지.
- **ListRow:** `data-status` installing|done|failed 시각 전이 (pending=기본 무스타일). 자동 설치 시뮬레이션 화면 복원하지 말 것.
- **StatusBadge:** pill 대표. (Toggle·Progress·dot 등 다른 999px 컨트롤은 허용)
- **테이블:** CSS-only `d0-table` / `d0-table-compact` — React 컴포넌트 아님.
- **Input** h52 · **EmptyState** · **Modal/BottomSheet** · **CommandBlock**(터미널 설치) · **FloatingSummary** · **StatStrip**

## 모션

| 종류 | 수단 | 값 |
| --- | --- | --- |
| 진입 / stagger / check pop / 숫자 | motion spring | SPRING 400/32, SOFT 260/30 |
| hover·data-* | CSS | `--d0-dur` + `--d0-ease` |
| Dialog | data-starting/ending-style | 8px + opacity |

이동 8–16px, 일반 scale 0.97–1 (TopBar back 등 시그니처 0.9 예외 허용).  
`prefers-reduced-motion: reduce` 최소화.

## 일러스트

여정 전환점만 150–240px. 제품 자산 `public/images/*` 우선. AI 제네릭 3D 남발 금지.  
작업 밀도 화면(설치 리스트·관리자 테이블) 금지. Confetti는 **완료 축하**만.

## 카피 연동

UI 구조 = 이 스킬. 문구 = `ux-writing`. 기본 `~해요`. 스펙 원문 카피 임의 변경 금지.  
공개 UI: 가운뎃점 사슬·의미 없는 em dash는 AI 티 → 쉼표·문장 분리.

## 작업 방식

### 제품 코드

1. 유사 화면 1개 읽고 패턴 맞춤.
2. `@day0/ui` export 우선.
3. 신규 컴포넌트: `*.tsx` + `*.css` + **`styles.css` @import** + **`index.ts` export**.
4. 화면 스타일 = CSS Modules + 토큰 변수.
5. state → `data-*`.
6. 출력 게이트.

### 프로토타입

1. `references/tokens.css` 로드.  
2. Pretendard Variable.  
3. `d0-` + data-*.  
4. Card 기본 plain.

### 콜드 스타트

2–4개: 표면(온보딩 스텝 check/terminal/install/… / 관리자 / 랜딩 / 기타), 한 화면 vs 플로우, viewport, `@day0/ui` 여부.  
**Day0 제품 신호가 없으면** 이 스킬을 강제하지 말고 확인.

## 출력 게이트

**HARD (코드로 확인)**

- [ ] 토큰 변수만 / 구 블루 없음  
- [ ] 신규 주 job primary fill ≤ 1 (기존 다동선 화면을 전면 리팩터하지 말 것)  
- [ ] 리스트 = 개별 카드 스택 아님 (행+디바이더 또는 plain/soft 래퍼)  
- [ ] 상태 = `data-*`  
- [ ] radius 14/10/8 밖 pill 남용 없음 (badge·dot·toggle 등 허용 제외)  
- [ ] focus-visible 링 (outline:none 단독 금지)  
- [ ] motion 있으면 reduced-motion  
- [ ] 신규 컴포넌트 styles.css + index 등록  

**VISUAL / 제품**

- [ ] 보더리스 톤 (전부 outlined 카드 회귀 아님)  
- [ ] 타이포 위계 보임  
- [ ] 작업 화면 장식 일러스트 과다 아님  

실패 시 수정 후 재통과. 금지 상세: `references/anti-patterns.md`.
