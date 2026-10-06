---
name: eli5-design
description: "아무것도 모르는 사람도 그림만 보고 이해하는 한 장짜리 HTML 설명 페이지를 Day0 시각 언어로 만든다. 그림 먼저, 짧은 글, 블록당 설명 3문장 이내, 용어는 비유로 풀기를 강제하고, 시안·옵션 비교, 절차 설명, 결과물 미리보기, 보고서, 따라하기·사용 가이드, 일정·변경 내역, 사건·원인, 용어·FAQ, 발표용 슬라이드 아홉 프리셋 중 하나를 기준으로 공용 블록을 골라 조립한다. 토큰은 형제 스킬 day0-design의 tokens.css 전체를 인라인하며, day0-design이 로컬에 없으면 공개 저장소 원본을 읽는다. '/eli5-design', '쉽게 설명하는 시안', '설명 페이지', '설명서 페이지', 'eli5 디자인', '그림으로 쉽게 보여줘', '쉽게 보는 발표 슬라이드' 요청에 사용한다. 설명 페이지가 아닌 Day0 제품 화면은 day0-design, 문구만이면 ux-writing으로 넘긴다. 설명 목적이 없는 일반 화면·랜딩 디자인에는 사용하지 않는다."
---

# ELI5 Design

무엇이든 **처음 보는 사람이 그림만 훑어도 이해하는 한 장짜리 HTML 설명 페이지**를
Day0 시각 언어로 만든다. 시안 문서, 설명서, 보고서, 가이드가 모두 이 형식이다.

## ELI5 원칙

출발점은 한 문장이다.

> Explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words.

이것을 다음 규칙으로 푼다.

1. **독자는 아무것도 모른다.** 배경지식·내부 용어·약어를 가정하지 않는다.
2. **SVG 도식은 필수다.** 페이지마다 그 주제의 실체를 그린 인라인 SVG 도식이 최소 1개, 첫 화면 안에 있다.
   도식은 대상의 모양(표 격자, 화면 와이어프레임, 연결 그래프, 시간 막대, 전/후 크기 비교)을 선과 면으로 그리고,
   라벨은 짧은 명사만 단다. **텍스트 상자를 화살표로 이은 것은 도식이 아니다(금지).**
   kpi-cards 막대 변형(`data-variant="bar"`)은 도식으로 인정한다. 막대 없는 kpi-cards는 그림이 아니다.
   **첫 화면**은 1280×800 뷰포트에서 도식의 bounding box가 전부 보이는 것(잘리면 실패), 375×812에서는
   첫 그림 블록 높이의 절반 이상이 첫 화면 안에 보이는 것이다(윗부분만 걸치면 실패).
3. **보여 준다.** 결과물·화면·데이터가 있으면 설명하지 말고 목업이나 눌러 보는 프로토타입으로 보인다.
   첫 화면(1280×800) 안에서 그림·목업 면적이 글 면적보다 크다. 글은 그림 옆 주석이다.
   그림이 컨테이너 폭의 절반만 쓰고 옆을 비우지 않는다. 폭을 채우거나 옆에 짧은 설명을 붙인다.
4. **섹션은 2~4개(기본 3~4개), 섹션마다 한 가지 일.** 앞쪽 핵심 섹션(header 다음 첫 1~2개 페이지 섹션)은 그림이 필수다.
   위험·한계·할 일 같은 목록 섹션(diff-rows·checklist·accordion만 담은 섹션)은 그림 없이 둘 수 있다.
   **그림 없는 목록 섹션**은 섹션 머리 + 목록 블록 하나 + 마무리 한 줄 `p`(배운 점·다음 행동 한 줄) 1개까지다. 다른 블록이나 문단을 더하면 그림이 필요하다.
   **페이지 섹션**은 `main > section`과 `main > .d0-split > section`이다. 블록 안 `section`(mockup-frame의 `.d0-app__body` 등)은 세지 않는다. 프리셋 권장 구성을 전부 채우지 않고 독자 질문에 필요한 블록만 쓴다.
5. **위계가 보인다.** 13px 회색 문장을 주 콘텐츠로 쓰지 않는다. 섹션 태그 pill은 기본 없음, callout은 페이지당 최대 1개.
   섹션 설명 `p`는 최대 1문장이고 제목과 같은 말이면 생략한다. 스케일 값은 아래 9번이 정본이다.
6. **글은 적게, 용어는 비유로.** 블록당 설명은 3문장 이내. 문단보다 라벨·주석을 쓰고, 용어는 일상 사물에 빗댄다.
   용어는 **처음 나오는 곳**(대개 header 요약 행이나 리드)에서 `<abbr title>` 또는 괄호 속 짧은 비유로 푼다. 뒤 섹션에서만 풀지 않는다.
7. **마크업도 뜻을 말한다.** 구조는 시맨틱 태그로 짓는다(`section`·`header`·`figure`·`ol`/`ul`·`dl`·`table`·
   `time`·`data`·`progress`·`details`·`dialog`·`button`/`a`). 레이아웃·스타일 훅용 `div`·`span`
   (배지, 라벨, 그리드 묶음)은 허용한다. 빈 간격용 요소는 금지다. 블록별 태그는 `references/blocks.md`
   공통 규칙을 따르고, ARIA는 네이티브 요소로 안 될 때(탭 등)만 쓴다.
8. **한 사실은 한 번.** 숫자·결정은 정본 위치 하나에만 본문으로 둔다. 같은 숫자 문자열(예 `26분`)은 렌더 텍스트에
   페이지당 2회 이하. 결정은 요약 행 또는 할 일 중 한 곳에 두고 다른 곳은 짧은 참조만 쓴다.
   요약 행 값은 데스크톱 한 줄(약 35자 이내), 용어 풀이는 `abbr` 또는 괄호 중 하나만 처음 등장 시 1회.
9. **결론은 히어로로, 고급스러움은 절제로.**
   - **결론 히어로.** report·compare 전/후·incident는 수치가 있으면 h1 바로 아래(요약 행 위)에 결론 수치 1개를
     `d0-hero`로 둔다. 전 값(작게, grey-600, 취소선 없음) → 후 값(44px/600, 모바일 36, 단위는 숫자와 같은 크기) + 단위 + 한 줄 뜻(15px grey-600).
     수치가 없으면 생략한다. 정본: `references/blocks/hero.md`.
   - **줄 길이는 레이아웃으로.** 본문 텍스트 블록 한 줄이 약 50자를 넘으면(`code`·`pre`·명령어 줄·code-block은 제외) `p`를 좁히지 않고 블록 레이아웃으로 줄인다
     (2열 grid로 행 나누기, 그림 옆 배치). 개행 규칙의 `max-width` 금지는 그대로다.
   - **타이포 대비.** h1 32px/700(display 자간·행간), h2 20px/700(title 자간), 본문 15px/400 grey-800(`p` 행간 1.65),
     보조 14px/400 grey-600, 라벨 12px/600 grey-600(대문자 변환 없음; grey-500은 선·화살표 같은 그래픽에만). 숫자는 전부 `tabular-nums`.
     모바일(≤640px) h1 26, h2 18, 히어로 숫자 36.
   - **여백 리듬.** 섹션 사이 64px(모바일 48), 섹션 안 블록 간 24px, 제목↔설명 8px, 페이지 상단 패딩 64.
     디바이더는 섹션 경계 1px grey-100과 행 목록의 행 구분선만 쓴다.
   - **그림 무대.** 도식 `figure`는 `data-stage` 패널(grey-50 배경, radius card, 패딩 28 / 모바일 20) 위에 놓고
     figcaption은 패널 밖 아래 13px grey-600. SVG 선은 기본 1.5·강조 2.5, round cap/join, 노드 그림자 없음.
   - **색은 6:3:1로 섞는다.** 첫 화면(1280×800) 진한 포인트(채움 면적) 1.2% 이상·전체(옅은 면 포함) 3~15%, 375×812 첫 화면 진한 포인트 0.8% 이상, 넓은 blue-light 무대로 전체만 채우지 않는다. 회색만으로 된 도식·카드 묶음 금지.
     blue는 단계(blue 선·채움 / blue-dark 글자·번호 / blue-light 옅은 면)로, 의미색(green 가능·완료, orange 주의·준비, red 위험·실패)은
     면·점·선·배지 배경으로만 쓰고 글자 색으로 쓰지 않는다. 페이지당 의미색 2가지 + blue. 정본: `references/blocks/shell.md` 색 절.
     KPI는 숫자 + 막대(`전` 행에만 값, `후` 행은 라벨만)만 두고 증감 배지를 달지 않는다.
   - 그라디언트·글래스·두꺼운 그림자·장식 3D는 금지다. 모션·정렬 세부는 `references/blocks/shell.md`가 정본이다.
10. **많으면 나눈다.** 아래 상한을 넘으면 묶거나 페이지를 나눈다.

| 항목 | 상한 |
| --- | --- |
| 카드 | 5 |
| 단계 | 5 (guide 체크리스트만 7까지 예외) |
| 옵션 | 3 |
| 질문 | 6 |
| 표 열 | 7 (데이터 열 6 + 행 번호 열 1) |
| 페이지 섹션(`main > section`, `main > .d0-split > section`) | 4 |
| callout | 1 |
| 상태 배지(`span.d0-pill`) 카드·행 하나에 | 1 |
| 배지 톤 종류(`data-tone`, 없으면 회색) / 의미색 종류, 페이지당 | 3 / 2 |

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

- 토큰: `day0-design/references/tokens.css` **파일 전체를 수정 없이** 메인 `<style>` 맨 앞에 붙여 넣는다.
  토큰을 외부 `<link>`로 걸지 않는다(artifact CSP 차단, 발행 후 소리 없는 변경, 오프라인 깨짐).
- 규칙: day0-design `SKILL.md`의 스택 규칙·컴포넌트 원칙을 따른다.
- **우선순위.** 설명 페이지의 타이포 스케일(h1 32 / h2 20 / 본문 15, 원칙 9번)과 페이지 여백은 이 스킬 값이
  day0-design보다 우선한다. 색·radius·모션·컴포넌트 규칙은 day0-design을 따른다.
- 금지: `day0-design/references/anti-patterns.md`를 함께 적용한다.

## 모듈 라우팅

본문은 항상 로드한다. 아래는 조건이 맞을 때만 연다.

| 언제 | 연다 |
| --- | --- |
| 처음 만들 때 톤 기준으로 | `references/examples/preview-compare.html` (완성 예시: 흐름+격자 카드 → 결과물 목업 → 눌러 보는 A/B 프레임) |
| 블록을 고를 때 | `references/blocks.md` (인덱스) → 쓸 블록 파일만 (예: `references/blocks/header.md`) |
| 페이지 골격·타이포·배지·나란히 두 섹션(`.d0-split`, 그림 둘이면 무대 정렬 `data-align="stage"`)·첫 화면 높이 예산 | `references/blocks/shell.md` |
| SVG 도식을 그릴 때(항상; 비율 `data-variant="ratio"`, 폭 `data-size="wide"`) | `references/blocks/diagram.md` |
| report·compare 전/후·incident에 결론 수치가 있을 때 | `references/blocks/hero.md` |
| 화면을 눌러 보게 할 때 | `references/blocks/mockup-frame.md` |
| 따라하기 단계를 그림과 함께 보일 때(왼쪽 단계 화면이 행에 따라 바뀜, `data-variant="linked"`) | `references/blocks/checklist.md` |
| 붙여 넣을 명령·설정이 있을 때(복사 버튼, 그림 블록 아님, 줄 길이 예외) | `references/blocks/code-block.md` |
| slides 프리셋으로 발표 덱을 만들 때(16:9 슬라이드, 제목 목차, 키보드 이동, 덱 게이트) | `references/blocks/slide-deck.md` |
| artifact로 발행하기 직전(폰트 인라인) | `scripts/subset_font.py` (Pretendard 서브셋 `@font-face` 생성) |
| 프리셋을 고른 뒤 | 아래 프리셋 판별 표의 프리셋 파일 하나 |

## 프리셋 판별

먼저 독자가 읽고 나서 무엇을 할 수 있어야 하는지 한 줄로 정한다. 그 행동이 프리셋을 정한다.

| 프리셋 | 언제 | 읽고 나서 할 수 있어야 하는 것 | 연다 |
| --- | --- | --- | --- |
| compare | 시안·옵션 비교, 결정 요청, 전후 비교 | 판단한다 | `references/formats/compare.md` |
| flow | 절차·흐름·구조·개념 설명 | 흐름을 이해하고 다음 행동을 알게 한다(시작 조건 → 단계 → 성공 확인 → 막히면 → 다음, 개념·구조 설명 포함) | `references/formats/flow.md` |
| preview | 결과물(파일·표·화면)의 모양 미리보기 | 관심 여부를 판단한다 | `references/formats/preview.md` |
| report | 상태·진행 보고, 결과·지표 보고, 상위 보고 요약, 아직 적용 전인 변경 제안·설명 | 판단하거나 행동한다 | `references/formats/report.md` |
| guide | 사용자가 직접 따라 하는 가이드, 도구·규칙을 잘 쓰는 사용 가이드 | 올바르게 실행하거나 사용하게 한다 — 따라하기(기본)·사용 가이드(`data-variant="practice"`) | `references/formats/guide.md` |
| timeline | 로드맵·일정·변경 내역 | 시간과 의존성을 공유한다 | `references/formats/timeline.md` |
| incident | 장애·사건 경위와 원인 | 이해하고 재발을 막는다 | `references/formats/incident.md` |
| faq | 용어 정리·FAQ | 특정 질문을 바로 해결한다 | `references/formats/faq.md` |
| slides | 발표·화면 공유용 슬라이드(업무 보고·제안·전략·기술 발표) | 한 장씩 따라오며 결론에 동의하고 결정·행동한다 | `references/formats/slides.md` |

guide는 두 변형으로 나뉜다. 순서대로 실행하면 따라하기, 목적·원칙·상황별 추천으로 잘 쓰게 하면 사용 가이드다.
프리셋 변형은 `<main class="d0-page" data-variant="...">`로 표시한다(slides만 `<main class="d0-deck" data-variant="...">`). 이름표일 뿐 스타일은 바꾸지 않는다.
이름표 목록(정본): compare `prototype`(시안)·`decision`(결정)·`before-after`(전/후), guide `practice`(사용 가이드, 따라하기는 생략), timeline `roadmap`·`changelog`, report `status`(기본)·`results`·`executive`·`proposal`, slides `report`·`proposal`·`strategy`·`tech`. flow·preview·incident·faq는 변형이 없다.

**slides 예외.** slides는 한 장짜리 문서가 아니라 16:9 슬라이드 5~12장(표지·제목 목차 포함)을 나열한 덱이다. 원칙 4번 섹션 상한(2~4개)·앞쪽 핵심 섹션 그림, 원칙 2·3번 첫 화면 규칙,
원칙 9번 히어로·h1 32/h2 20 고정 타이포·섹션 사이 64px·첫 화면 색 비중, 줄 길이 50자, 720px 프레임, 도식 라벨 데스크톱 16px 상한 대신
`references/blocks/slide-deck.md`의 덱 규칙과 덱 게이트(액션 타이틀, 슬라이드당 그림 1개(표지·목차·요약 예외), 본문 3줄·불릿 3개, 슬라이드 5~12장, 제목 목차, 16:9, 강조 계열 하나만 blue)를 따른다.
결론 수치는 히어로 대신 핵심 수치 슬라이드에 둔다. 나머지 원칙(글은 적게, 한 사실은 한 번(제목 목차 반복은 빼고 센다), 시맨틱, 토큰, 색, 접근성)은 그대로다.

헷갈리는 쌍은 이 기준으로 가른다.

| 헷갈리는 쌍 | 기준 |
| --- | --- |
| timeline / flow | 날짜가 있으면 timeline, 순서만 있으면 flow |
| guide / flow | 체크박스로 직접 실행하면 guide 따라하기, 흐름 이해가 목적이면 flow, 잘 쓰는 법·선택 기준이면 guide 사용 가이드 |
| preview / report | 결과물의 모양이면 preview, 그로부터 알게 된 것이면 report |
| compare 시안 / 결정 | 화면을 눌러 고르면 시안, 숫자·정책을 고르면 결정 |
| timeline / report | 날짜 순서가 주인공이면 timeline, 지금 상태와 다음 행동이 주인공이면 report |
| incident / report | 사건 하나의 경위면 incident, 진행 상태·결과·지표 정리면 report |
| 적용 전 변경 제안 | report + 요약 행 헤더, 수치는 `예상치`로 표기(측정값과 섞지 않는다) |
| slides / report | 발표·화면 공유로 한 장씩 넘기며 설득하면 slides, 혼자 읽는 문서면 report |
| slides / compare·flow | 옵션을 나란히 놓고 고르는 문서면 compare, 흐름을 이해시키는 한 장이면 flow, 그것을 근거로 무엇을 하자고 발표하면 slides |

## 개행 규칙

설명 문단이 옆 공간이 남는데도 일찍 줄 바뀌는 버그를 막는다. 원인은 대개 리드나
설명 `p`에 컨테이너보다 좁은 `max-width`(px·`ch`)를 건 것이다.
`day0-design/references/anti-patterns.md`가 슬롭 신호로 꼽는 좁은 부제와 같은 문제다.

- 리드·섹션 설명·블록 설명 문단은 **부모 컨테이너 폭을 그대로 쓴다.**
- 컨테이너보다 좁은 `max-width`·`width`·`ch` 단위를 `p`에 걸지 않는다. 좁혀야 하면 블록 컨테이너를 좁힌다.
- 한글은 `word-break: keep-all`, 본문은 `text-wrap: pretty`.
- `text-wrap: balance`는 제목 셀렉터(h1~h3)에만 쓴다.
- **문장 단위 개행(선택).** 기본은 이어 쓰기다. 리드·설명이 2문장 이상이고 데스크톱 폭에서 2줄을 넘기거나,
  문장마다 역할이 다르면(예: "무엇을 바꿨나" / "지금 상태·부탁") 온점 단위로 문장마다 줄을 나눈다.
  문장마다 `<span class="d0-sentence">`(`display: block`) 또는 별도 `<p>`를 쓰고 `<br>`을 늘어놓지 않는다.
  한 문장이 한 줄을 넘치면 그 안에서는 자연 줄바꿈한다.
- **요약 행.** 리드 내용이 "이전 → 현재 → 요청"처럼 역할로 나뉘면 문단 대신 header 요약 행(`라벨 | 한 문장` 2~3행)을 쓴다.
  compare 전/후·결정 변형, report, incident, timeline 변경 내역의 기본 리드다. 결정·요청 행(`data-tone="decision"`)이 있으면 결정 callout을 두지 않는다.
  결정이 둘 이상이면 `결정 필요` 칸에 짧은 `ol`(최대 2개), 셋 이상이면 가장 중요한 1개만 요약 행에 두고 나머지는
  할 일 목록으로 보낸다. 요약 행은 최대 3행이다. 행 라벨·두 번째 결정의 세부 규칙은 `references/blocks/header.md`가 정본이다.

## 출력 형식

- **단일 self-contained HTML 파일**을 만든다. 호스트에 artifact 발행 기능이 있으면 발행한다.
- **폰트.** artifact로 발행할 때는 `scripts/subset_font.py`로 페이지 글자만 담은 Pretendard 서브셋 `@font-face`를 인라인해 외부 요청을 0건으로 만든다.
  일반 HTML 파일은 Pretendard Variable jsDelivr `<link>` 하나를 허용한다. 도구를 못 쓰면(파이썬·원본 폰트 없음) 링크를 유지하고,
  artifact에서는 링크가 막혀 시스템 폰트로 대체된다고 사용자에게 알린다. 그 밖의 외부 리소스는 없다. CSS·SVG·JS는 인라인이다.
- 인라인 `@font-face`는 메인 `<style>` **앞**의 별도 `<style>`이다. "tokens.css는 메인 `<style>` 맨 앞" 규칙과 충돌하지 않는다.
- **라이트 온리.** `:root { color-scheme: light; }`와 `body` 배경색을 명시해 다크 호스트에서도 깨지지 않게 한다. 다크 팔레트를 추가하지 않는다.
- 모바일 폭에서 좌우 16px 거터, 가로 스크롤 없음.
- **높이 720px 프레임.** 갤러리 iframe처럼 높이 약 720px 프레임에 넣을 페이지는 첫 SVG 도식의 아래 끝이 720px 안에 든다. 머리 260 + 첫 무대 300은 합계 기준이다(정본: `references/blocks/shell.md` 첫 화면 높이 예산).
- **한 artifact 안 여러 페이지.** 탭으로 고른 페이지를 iframe으로 보여 줄 때 같은 artifact의 다른 파일을 `src`로 부르지 않는다(뷰어 샌드박스에서 연결이 끊긴다).
  각 페이지 HTML을 base64 JSON으로 내장하고, 탭을 고르면 `TextDecoder`로 풀어 `iframe.srcdoc`에 넣는다. iframe은 `sandbox="allow-scripts"`이고 `allow-same-origin`은 주지 않는다.
  새 탭 열기는 같은 HTML로 만든 Blob URL을 쓰고, 막히면 "새 탭을 열 수 없어요. 이 화면에서 보세요" 같은 안내 문구를 보여 준다.
- 예시 데이터는 전부 합성이다. 실제 회사·제품·사람·티켓 번호처럼 보이는 값을 쓰지 않는다.
- 외부 사이트 링크와 레퍼런스 사이트 이름을 페이지에 넣지 않는다.

## 작업 순서

1. **프리셋 판별.** 먼저 독자가 읽고 나서 무엇을 할 수 있어야 하는지 한 줄로 정한다. 그 행동과 요청 신호, 판별 표로 주 프리셋 하나를 고른다. 해당 프리셋 파일을 연다.
2. **독자 질문 확정.** 프리셋의 질문을 이 요청에 맞게 한 줄씩 다시 쓴다. 답할 수 없는 질문은 사용자에게 확인한다.
3. **그림 먼저, 섹션 2~4개(기본 3~4개, slides는 제목 목차 먼저 쓰고 슬라이드마다 그림 하나).** 첫 화면에 들어갈 SVG 도식을 먼저 정하고(프리셋의 대표 도식), 앞쪽 핵심 섹션 1~2개에
   그림을 고른 뒤 남은 질문(위험·할 일 등)에만 글 블록을 붙인다. `references/blocks.md` 표로 고른다. 처음이면 예시 HTML로 톤을 맞춘다.
   리드가 역할로 나뉘면 header 요약 행을 쓴다. 결론 수치가 있으면 히어로에 두고, 다른 곳은 그 숫자를 되풀이하지 않는다.
4. **토큰 인라인.** 탐색 순서(의존 절)로 찾은 tokens.css 전체를 수정 없이 메인 `<style>` 맨 앞에 붙인다. 모두 실패하면 멈춘다.
5. **작성.** `references/blocks/shell.md` 스니펫에서 시작해 고른 블록 파일의 스니펫을 붙인다. 블록 해부대로 짓고, 설명은 블록당 3문장 이내, 용어는 비유로 푼다.
6. **게이트.** 아래 출력 게이트를 통과할 때까지 고친다.
7. **발행 직전 폰트 인라인.** artifact로 발행하면 글자를 다 고친 뒤 `scripts/subset_font.py`로 서브셋 `@font-face`를 만들어
   jsDelivr `<link>` 자리에 넣는다(글자가 바뀌면 다시 만든다). 도구가 없으면 링크를 두고 시스템 폰트 대체를 알린다.

## 출력 게이트

**HARD (코드로 확인)**

렌더 DOM 기준(JS 실행 후)으로 판정한다. 페이지 섹션은 `main > section, main > .d0-split > section`이다.
slides 덱은 위 slides 예외에 적힌 항목 대신 `references/blocks/slide-deck.md` 덱 게이트로 판정하고, 나머지 항목은 그대로 적용한다.

- [ ] 설명 `p`에 컨테이너보다 좁은 `max-width`·`width`·`ch` 제약이 없다
- [ ] `text-wrap: balance`가 제목 셀렉터(h1~h3)에만 있다
- [ ] 개수 상한(카드 5·단계 5, guide 체크리스트만 7·옵션 3·질문 6·표 열 7 = 데이터 열 6 + 행 번호 열)을 넘지 않는다
- [ ] `role="img"`와 `<title>`을 가진 인라인 SVG 도식(kpi-cards 막대 변형 포함)이 1개 이상 있다
- [ ] header 다음 첫 1~2개 페이지 섹션(앞쪽 핵심 섹션)마다 그림 블록이 있다. 그림 블록이 없는 페이지 섹션은 diff-rows·checklist·accordion 블록 하나(+ 마무리 한 줄 `p` 1개까지)만 담은 섹션이어야 한다. checklist linked 변형의 무대 SVG는 그림 블록으로 세고, code-block은 그림으로 세지 않는다(행 `<details>` 안 code-block은 그 목록 블록의 일부다)
- [ ] 도식 `figure.d0-fig`마다 안에 SVG가 있고, SVG `<text>` 하나가 4어절(공백 3개) 이상이 아니다(넘으면 텍스트 상자 도식으로 보고 FAIL)
- [ ] 페이지 섹션(`main > section, main > .d0-split > section`)이 4개 이하, callout이 1개 이하다. mockup-frame 안 `section` 등 블록 안 `section`은 세지 않는다
- [ ] header 요약 행에 `data-tone="decision"` 행이 있으면 결정 callout이 없다(둘 중 하나만, 라벨 문구는 `결정 필요`·`도움 필요` 등 무엇이든 같다)
- [ ] 모든 h2에 섹션 태그 pill이 붙어 있지 않다(전부 붙어 있으면 FAIL)
- [ ] 배지(`.d0-pill`)에 고정 `height`와 `flex: none`이 있다
- [ ] 배지 톤 종류(`span.d0-pill`의 `data-tone`, 없으면 회색)가 3가지 이하, 카드·행 하나에 배지가 1개 이하, 의미색(`--d0-green`·`--d0-red`·`--d0-orange`)을 글자 `color`로 쓴 곳이 없다
- [ ] 같은 숫자 문자열(숫자+단위, 예 `26분`)이 렌더 텍스트(`body.innerText`, SVG `<text>` 포함)에 2회 이하다
- [ ] 도식 `figure.d0-fig`마다 SVG가 `[data-stage]` 패널 안에 있고 figcaption은 패널 밖에 있다(전체 폭 비율 막대 `figure.d0-fig[data-variant="ratio"]`는 무대 없이 섹션 폭에 두는 예외)
- [ ] kpi-cards에 증감 배지가 없다
- [ ] SVG·CSS 안 모든 `var(--d0-*)`가 tokens.css에 있다
- [ ] 구조(`section`·`header`·`figure`·`ol`/`ul`·`dl`·`table`·`time`·`data`·`progress`·`details`·`dialog`·`button`/`a`)를
  시맨틱 태그로 짓는다(blocks.md 공통 규칙 표). 레이아웃·스타일 훅용 `div`·`span`은 허용, 빈 간격용 요소는 없다
- [ ] 헤딩이 h1→h2→h3 순서이고 건너뛰지 않는다, 랜드마크 `main`이 1개다
- [ ] 네이티브 시맨틱과 겹치는 role이 없다(`<nav role="navigation">`, `<button role="button">` 금지)
- [ ] `color-scheme: light`와 `body` 배경이 있다
- [ ] tokens.css 전체가 메인 `<style>` 맨 앞에 인라인되어 있고 토큰용 외부 `<link>`가 없다
- [ ] 한 artifact 안 여러 페이지를 iframe으로 보여 줄 때 iframe `src`로 같은 artifact 파일을 부르지 않는다(`srcdoc` + `sandbox="allow-scripts"`, `allow-same-origin` 없음)
- [ ] artifact 발행본은 외부 요청이 0건이다(서브셋 `@font-face` 인라인, 도구가 없어 링크를 둔 경우만 예외이고 사용자에게 알렸다). 일반 HTML 파일은 외부 리소스가 Pretendard jsDelivr 링크뿐이다
- [ ] day0-design `SKILL.md`의 HARD 게이트(토큰 변수만, 리스트는 행+디바이더, 상태는 `data-*`, focus-visible, reduced-motion)

**접근성 (WCAG 2.2 AA 하한)**

WCAG 3.0은 아직 Working Draft라 방향 참고로만 보고, 판정은 WCAG 2.2 AA로 한다. 3.0이 정식 권고가 되면 이 묶음을 갱신한다.

- [ ] `<html lang="ko">`, header·main·section, h1→h2→h3 순서, 표는 caption과 `th scope`
- [ ] 글자 대비 4.5:1(큰 글자 3:1), UI 경계·포커스 링·정보 그래픽 3:1. tokens.css 실제 값으로 계산한다
- [ ] 상태를 색만으로 구분하지 않는다(배지 글자, 현재 단계 점, 전후 라벨)
- [ ] 포인터 대상 24×24px 이상, 포커스 링이 가려지지 않는다
- [ ] 탭은 tablist/tab/tabpanel + `aria-selected` + 화살표 키(네이티브 대안이 없는 경우), 펼침은 `details`/`summary`, 체크는 실제 checkbox, 진행률은 `<progress>`
- [ ] 정보 SVG는 `role="img"`와 이름, 장식 SVG는 `aria-hidden`
- [ ] 320px 폭(400% 확대)에서 페이지 가로 스크롤 없음(표는 자체 스크롤 허용)

**VISUAL (눈으로·측정으로 확인)**

측정은 브라우저에서 `getBoundingClientRect()`로 한다. 각 항목 괄호 안이 측정 방법이다.

- [ ] 1280×800에서 SVG 도식의 bounding box가 첫 화면 안에 전부 보인다(잘리면 FAIL), 375×812에서는 첫 그림 블록 높이의 절반 이상이 첫 화면 안이다(윗부분만 걸치면 FAIL)
- [ ] 첫 화면(1280×800) 안에서 그림·목업 면적이 글 면적보다 크다(그림 = `figure`·`svg`·목업 프레임 box, 글 = `p`·`li`·`dd` 텍스트 블록 box의 첫 화면 안 면적 합. 그림 안 글은 그림으로 센다)
- [ ] 그림이 컨테이너 폭의 절반만 쓰고 옆이 빈 배치가 없다(그림 폭이 부모 폭의 60% 미만이고 같은 줄 옆에 내용이 없으면 FAIL)
- [ ] 1280×800 첫 화면에서 진한 포인트(`blue`·`blue-dark`·`green`·`orange`·`red` 채움)가 1.2% 이상, 375×812 첫 화면에서 0.8% 이상, 전체(옅은 면 포함)가 1280에서 3~15%이고 blue와 의미색 1가지 이상이 보인다. 넓은 blue-light 무대로 전체 비율만 채우지 않는다(측정: 해당 색이 `background-color`·SVG `fill`인 요소의 보이는 bbox 합 ÷ 뷰포트 면적, `stroke`·`border`만 그 색인 요소는 세지 않음, 센 요소의 자손은 제외. 정본 `references/blocks/shell.md` 색 절)
- [ ] 회색만 있는 도식이 없다(도식 `svg`마다 blue 계열 또는 의미색 `fill`·`stroke` 요소가 1개 이상)
- [ ] 배지가 세로로 늘어나지 않고 제목 첫 줄에 맞춰져 있다(배지 높이 = 22px 또는 20px, 배지 중심과 제목 첫 줄 중심 차 2px 이하)
- [ ] SVG 안 글자의 렌더 크기가 11px 이상 16px 이하다(375px과 1280px 모두). 데스크톱에서 h2 18px보다 작다.
  렌더 글자 크기 = font-size × (SVG 렌더 폭 ÷ viewBox 폭)로 잰다. 글자 박스 높이는 쓰지 않는다(정본: `references/blocks/diagram.md` 라벨 절)
- [ ] `.d0-split`으로 나란히 둔 두 섹션의 높이 비(긴 쪽 ÷ 짧은 쪽)가 1.5 이하다(1280px에서 두 `section` 높이. 무대 정렬 변형은 두 무대 안 SVG 높이로 잰다. 정본: `references/blocks/shell.md`)
- [ ] 나란히 둔 두 섹션이 모두 무대 위 그림이면 `data-align="stage"`이고, 1280px에서 좌우 h2 위 끝·무대 위 끝·무대 높이·figcaption 위 끝의 차가 각각 2px 이하다. 375px에서는 1열로 쌓인다
- [ ] 본문 텍스트 블록 한 줄이 50자 이하다(실제 줄 글자 수, 또는 텍스트 블록 폭 ÷ (15px × 0.95) 근사. `code`·`pre`·명령어 줄은 제외)
- [ ] 히어로가 있으면 히어로 수치가 1280×800 첫 화면 상단 1/3(y ≤ 267px) 안에 있다
- [ ] 페이지 섹션 사이 세로 간격이 64px(모바일 48px)이다(앞 섹션 마지막 블록 아래 끝 ~ 다음 섹션 `header` 위 끝, 오차 ±4px)
- [ ] 옆 영역이 남는데 줄이 바뀐 설명 문단이 없다(문단 폭이 부모의 content box 폭(패딩 제외), grid 안이면 그 열 폭보다 24px 이상 좁은데 2줄 이상이면 FAIL. callout·카드 패딩이나 열 폭을 남는 영역으로 세지 않는다)
- [ ] 모바일 폭에서 가로 스크롤이 없다(375px에서 `scrollWidth` ≤ `clientWidth`)
- [ ] 프리셋의 독자 질문마다 답하는 블록이 있다(질문 목록과 섹션 제목을 한 줄씩 짝지어 검토)
- [ ] 처음 보는 사람이 그림과 제목만 훑어도 요지를 말할 수 있다(h1·h2·figcaption만 읽고 요지 한 문장을 써 본다)

실패하면 고치고 다시 통과시킨다.
