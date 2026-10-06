---
name: eli5-design
description: "아무것도 모르는 사람도 그림만 보고 이해하는 한 장짜리 HTML 설명 페이지를 Day0 시각 언어로 만든다. 그림 먼저, 짧은 글, 블록당 설명 3문장 이내, 용어는 비유로 풀기를 강제하고, 시안·옵션 비교, 절차 설명, 결과물 미리보기, 보고서, 따라하기 가이드, 일정·변경 내역, 사건·원인, 용어·FAQ 여덟 프리셋 중 하나를 기준으로 공용 블록을 골라 조립한다. 토큰은 형제 스킬 day0-design의 tokens.css 전체를 인라인하며, day0-design이 로컬에 없으면 공개 저장소 원본을 읽는다. '/eli5-design', '쉽게 설명하는 시안', '설명 페이지', '설명서 페이지', 'eli5 디자인', '그림으로 쉽게 보여줘' 요청에 사용한다. 설명 페이지가 아닌 Day0 제품 화면은 day0-design, 문구만이면 ux-writing으로 넘긴다. 설명 목적이 없는 일반 화면·랜딩 디자인에는 사용하지 않는다."
---

# ELI5 Design

무엇이든 **처음 보는 사람이 그림만 훑어도 이해하는 한 장짜리 HTML 설명 페이지**를
Day0 시각 언어로 만든다. 시안 문서, 설명서, 보고서, 가이드가 모두 이 형식이다.

## ELI5 원칙

출발점은 한 문장이다.

> Explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words.

이것을 다음 규칙으로 푼다.

1. **독자는 아무것도 모른다.** 배경지식·내부 용어·약어를 가정하지 않는다.
2. **그림이 먼저다.** 첫 화면에 그림(도식·흐름·목업)이 보인다. 글은 그림을 거든다.
3. **글은 적게.** 블록당 설명은 3문장 이내. 문단보다 행·라벨·주석을 쓴다.
4. **용어는 비유로 푼다.** 용어를 다른 용어로 설명하지 않고 일상 사물에 빗댄다.
5. **많으면 나눈다.** 아래 상한을 넘으면 묶거나 페이지를 나눈다.

| 항목 | 상한 |
| --- | --- |
| 카드 | 5 |
| 단계 | 5 (guide 체크리스트만 7까지 예외) |
| 옵션 | 3 |
| 질문 | 6 |
| 표 열 | 7 |

## 3층 모델

| 층 | 성격 | 내용 |
| --- | --- | --- |
| 원칙 | 강제 | ELI5 원칙, Day0 토큰·규칙, 개행 규칙, 개수 상한 |
| 프리셋 | 기준 | 독자가 다 읽고 답할 질문, 요청 신호, 권장 구성 예시, 프리셋 안티패턴 |
| 블록 | 선택 | 쓸지는 자유. 쓰면 정해진 해부 구조를 따른다 |

프리셋은 블록 순서를 강제하지 않는다. 권장 구성은 예시일 뿐이고, 판정 기준은
"독자 질문에 답했는가"다. 일관성은 블록 모양에서, 자유는 블록 선택에서 온다.

**복합 요청:** 주 프리셋 하나를 고르고, 다른 프리셋의 블록은 필요한 것만 빌린다.
**어느 프리셋에도 안 맞으면:** 원칙만 지키며 블록으로 자유롭게 구성한다.

## 의존: day0-design

시각 언어는 형제 스킬 `day0-design`이 정본이다. 이 스킬은 토큰 값을 갖지 않는다.

**탐색 순서.** 아래 순서로 찾아 처음 발견한 `day0-design`을 쓴다. 이 순서의 정본은 이 절뿐이다.

1. 로컬 형제 경로 `../day0-design/` (이 스킬 디렉터리 기준).
2. 전역 스킬 디렉터리. 순서대로 확인해 처음 `day0-design/SKILL.md`가 있는 곳을 쓴다.
   `~/.agents/skills/day0-design/` (skills CLI 공용 위치), `~/.claude/skills/day0-design/`,
   `~/.codex/skills/day0-design/`, `~/.gemini/skills/day0-design/`, `~/.grok/skills/day0-design/`.
   예시 목록이며, 현재 호스트의 전역 스킬 디렉터리가 여기 없으면 그것을 우선 포함한다.
3. 공개 저장소 원본. 디렉터리는 https://github.com/oobg/agent-skills/tree/main/skills/day0-design 이고,
   파일은 raw 경로로 읽는다.
   - https://raw.githubusercontent.com/oobg/agent-skills/main/skills/day0-design/SKILL.md
   - https://raw.githubusercontent.com/oobg/agent-skills/main/skills/day0-design/references/tokens.css
   - https://raw.githubusercontent.com/oobg/agent-skills/main/skills/day0-design/references/anti-patterns.md
   - 필요하면 https://raw.githubusercontent.com/oobg/agent-skills/main/skills/day0-design/references/patterns.md
4. 모두 실패하면(경로 없음, 네트워크 불가, 404 등) 토큰을 추측하거나 하드코딩하지 않는다.
   "day0-design을 찾지 못해 진행할 수 없다"고 알리고 멈춘다. 다른 시각 언어로 바꿔 만들지 않는다.

어느 출처를 썼는지(형제 경로, 전역 경로명, 원격 원본) 사용자에게 한 줄 알린다.
어느 출처든 day0-design 디렉터리 기준 같은 상대 경로의 파일을 읽는다.

- 토큰: `day0-design/references/tokens.css` **파일 전체를 수정 없이** HTML `<style>` 맨 앞에 붙여 넣는다.
  토큰을 외부 `<link>`로 걸지 않는다(artifact CSP 차단, 발행 후 소리 없는 변경, 오프라인 깨짐).
- 규칙: day0-design `SKILL.md`의 스택 규칙·타이포 위계·컴포넌트 원칙을 따른다.
- 금지: `day0-design/references/anti-patterns.md`를 함께 적용한다.

## 모듈 라우팅

본문은 항상 로드한다. 아래는 조건이 맞을 때만 연다.

| 언제 | 연다 |
| --- | --- |
| 블록을 고를 때 | `references/blocks.md` (인덱스) → 쓸 블록 파일만 (예: `references/blocks/header.md`) |
| 페이지 골격을 짤 때 | `references/blocks/shell.md` |
| 시안·옵션 비교, 결정 요청, 전후 비교 | `references/formats/compare.md` |
| 절차·흐름·구조·개념 설명 | `references/formats/flow.md` |
| 결과물(파일·표·화면)의 모양 미리보기 | `references/formats/preview.md` |
| 결과·지표 보고 | `references/formats/report.md` |
| 사용자가 직접 따라 하는 가이드 | `references/formats/guide.md` |
| 로드맵·일정·변경 내역 | `references/formats/timeline.md` |
| 장애·사건 경위와 원인 | `references/formats/incident.md` |
| 용어 정리·FAQ | `references/formats/faq.md` |

## 프리셋 판별

헷갈리는 쌍은 이 기준으로 가른다.

| 헷갈리는 쌍 | 기준 |
| --- | --- |
| timeline / flow | 날짜가 있으면 timeline, 순서만 있으면 flow |
| guide / flow | 체크박스가 필요하면 guide, 이해만 하면 flow |
| preview / report | 결과물의 모양이면 preview, 그로부터 알게 된 것이면 report |
| compare 시안 / 결정 | 화면을 눌러 고르면 시안, 숫자·정책을 고르면 결정 |
| incident / report | 사건 하나의 경위면 incident, 결과·지표 정리면 report |

## 개행 규칙

설명 문단이 옆 공간이 남는데도 일찍 줄 바뀌는 버그를 막는다. 원인은 대개 리드나
설명 `p`에 컨테이너보다 좁은 `max-width`(px·`ch`)를 건 것이다.
`day0-design/references/anti-patterns.md`가 슬롭 신호로 꼽는 좁은 부제와 같은 문제다.

- 리드·섹션 설명·블록 설명 문단은 **부모 컨테이너 폭을 그대로 쓴다.**
- 컨테이너보다 좁은 `max-width`·`width`·`ch` 단위를 `p`에 걸지 않는다. 좁혀야 하면 블록 컨테이너를 좁힌다.
- 한글은 `word-break: keep-all`, 본문은 `text-wrap: pretty`.
- `text-wrap: balance`는 제목 셀렉터(h1~h3)에만 쓴다.

## 출력 형식

- **단일 self-contained HTML 파일**을 만든다. 호스트에 artifact 발행 기능이 있으면 발행한다.
- 외부 리소스는 Pretendard Variable 웹폰트(cdn.jsdelivr.net) 하나만. 나머지는 인라인 CSS·SVG·JS.
- **라이트 온리.** `:root { color-scheme: light; }`와 `body` 배경색을 명시해 다크 호스트에서도 깨지지 않게 한다. 다크 팔레트를 추가하지 않는다.
- 모바일 폭에서 좌우 16px 거터, 가로 스크롤 없음.
- 예시 데이터는 전부 합성이다. 실제 회사·제품·사람·티켓 번호처럼 보이는 값을 쓰지 않는다.
- 외부 사이트 링크와 레퍼런스 사이트 이름을 페이지에 넣지 않는다.

## 작업 순서

1. **프리셋 판별.** 요청 신호와 판별 표로 주 프리셋 하나를 고른다. 해당 프리셋 파일을 연다.
2. **독자 질문 확정.** 프리셋의 질문을 이 요청에 맞게 한 줄씩 다시 쓴다. 답할 수 없는 질문은 사용자에게 확인한다.
3. **블록 선택.** `references/blocks.md` 표로 질문마다 답할 블록을 고른다. 첫 화면에 들어갈 그림 블록을 먼저 정한다.
4. **토큰 인라인.** 탐색 순서(의존 절)로 찾은 tokens.css 전체를 수정 없이 `<style>` 맨 앞에 붙인다. 모두 실패하면 멈춘다.
5. **작성.** `references/blocks/shell.md` 스니펫에서 시작해 고른 블록 파일의 스니펫을 붙인다. 블록 해부대로 짓고, 설명은 블록당 3문장 이내, 용어는 비유로 푼다.
6. **게이트.** 아래 출력 게이트를 통과할 때까지 고친다.

## 출력 게이트

**HARD (코드로 확인)**

- [ ] 프리셋의 독자 질문마다 답하는 블록이 있다
- [ ] 설명 `p`에 컨테이너보다 좁은 `max-width`·`width`·`ch` 제약이 없다
- [ ] `text-wrap: balance`가 제목 셀렉터에만 있다
- [ ] 개수 상한(카드 5·단계 5·옵션 3·질문 6·표 열 7)을 넘지 않는다
- [ ] `color-scheme: light`와 `body` 배경이 있다
- [ ] tokens.css 전체가 `<style>`에 인라인되어 있고 토큰용 외부 `<link>`가 없다
- [ ] 외부 리소스는 Pretendard 웹폰트뿐이다
- [ ] day0-design `SKILL.md`의 HARD 게이트(토큰 변수만, 리스트는 행+디바이더, 상태는 `data-*`, focus-visible, reduced-motion)

**접근성 (WCAG 2.2 AA 하한)**

WCAG 3.0은 아직 Working Draft라 방향 참고로만 보고, 판정은 WCAG 2.2 AA로 한다. 3.0이 정식 권고가 되면 이 묶음을 갱신한다.

- [ ] `<html lang="ko">`, header·main·section, h1→h2→h3 순서, 표는 caption과 `th scope`
- [ ] 글자 대비 4.5:1(큰 글자 3:1), UI 경계·포커스 링·정보 그래픽 3:1. tokens.css 실제 값으로 계산한다
- [ ] 상태를 색만으로 구분하지 않는다(배지 글자, 현재 단계 점, 전후 라벨)
- [ ] 포인터 대상 24×24px 이상, 포커스 링이 가려지지 않는다
- [ ] 탭은 tablist/tab/tabpanel + `aria-selected` + 화살표 키, 펼침은 button + `aria-expanded`/`aria-controls`, 체크는 실제 checkbox, 진행률은 `role="progressbar"` + `aria-valuenow`
- [ ] 정보 SVG는 `role="img"`와 이름, 장식 SVG는 `aria-hidden`
- [ ] 320px 폭(400% 확대)에서 페이지 가로 스크롤 없음(표는 자체 스크롤 허용)

**VISUAL (눈으로 확인)**

- [ ] 첫 화면에 그림이 보인다
- [ ] 옆 영역이 남는데 줄이 바뀐 설명 문단이 없다
- [ ] 모바일 폭에서 가로 스크롤이 없다
- [ ] 처음 보는 사람이 그림과 제목만 훑어도 요지를 말할 수 있다

실패하면 고치고 다시 통과시킨다.
