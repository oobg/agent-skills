---
name: eli5-design
description: "아무것도 모르는 사람도 그림으로 구조를 먼저 이해하고 짧은 글로 이유와 맥락까지 이해하는 HTML 설명 문서를 Day0 시각 언어로 만든다. 그림 먼저, 라벨 아래 짧은 설명(라벨당 3문장 이내), 용어는 비유로 풀기를 강제하고, 독자 질문을 나눠 질문마다 비교, 절차, 미리보기, 보고, 따라하기·사용 가이드, 일정·변경 내역, 사건·원인, 용어·FAQ 여덟 패턴 중 맞는 것을 섹션 단위로 섞으며(장애 회고·기능 출시 보고·설치 가이드 같은 레시피는 선택), 한 장짜리 페이지(page) 또는 한 장씩 넘기는 발표 덱(deck)으로 출력하고 공용 블록을 골라 조립한다. 토큰은 형제 스킬 day0-design의 tokens.css 전체를 인라인하며, day0-design이 로컬에 없으면 공개 저장소 원본을 읽는다. '/eli5-design', '쉽게 설명하는 시안', '설명 페이지', '설명서 페이지', 'eli5 디자인', '그림으로 쉽게 보여줘', '쉽게 보는 발표 슬라이드' 요청에 사용한다. 설명 페이지가 아닌 Day0 제품 화면은 day0-design, 문구만이면 ux-writing으로 넘긴다. 설명 목적이 없는 일반 화면·랜딩 디자인에는 사용하지 않는다."
---

# ELI5 Design

무엇이든 **처음 보는 사람이 그림으로 구조를 먼저 잡고, 짧은 글로 이유와 맥락까지 이해하는 HTML 설명 문서**를
Day0 시각 언어로 만든다. 시안 문서, 설명서, 보고서, 가이드, 회고가 모두 이 형식이다.
기본은 혼자 읽어도 이해되는 한 장짜리 페이지(page)이고, 같은 내용을 발표용으로 한 장씩 넘기는 덱(deck)으로도 낸다(출력 형식 판별 절).

## ELI5 원칙

출발점은 한 문장이다.

> Explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words.

"few words"는 글을 적게 쓰라는 뜻이 아니라 **같은 말을 그림과 글로 두 번 하지 말라**는 뜻으로 읽는다.
이 스킬이 만드는 것은 글이 적은 페이지가 아니라, 그림이 구조를 설명하고 짧은 글이 이유·근거·조건을 보완하는 페이지다.

> **그림으로 구조를 먼저 이해하고, 짧은 글로 이유와 맥락까지 이해하게 만든다.** 같은 내용을 그림과 글로 중복하지 않는다.

이것을 다음 규칙으로 푼다.

1. **독자는 아무것도 모른다.** 배경지식·내부 용어·약어를 가정하지 않는다.
2. **SVG 도식은 필수다.** 페이지마다 그 주제의 실체를 그린 인라인 SVG 도식이 최소 1개, 첫 화면 안에 있다.
   도식은 대상의 모양(표 격자, 화면 와이어프레임, 연결 그래프, 시간 막대, 전/후 크기 비교)을 선과 면으로 그리고,
   라벨은 짧은 명사만 단다. **텍스트 상자를 화살표로 이은 것은 도식이 아니다(금지).**
   Editorial 장르(`data-genre="editorial"`)도 도식이다. 숫자는 HTML(56px/600, 모바일 40)로 쓰고 그 뜻을 받치는 SVG 객체 하나(최대 120px, 원의 몫·막대 하나)를 그린다.
   페이지당 최대 1개이고 **실제 숫자일 때만** 쓴다(문구·대답 금지). 96px 이상 숫자는 Impact 안에서만 쓴다. 정본: `references/blocks/diagram.md` 장르 절.
   kpi-cards 막대 변형(`data-variant="bar"`)은 도식으로 인정한다. 막대 없는 kpi-cards는 그림이 아니다.
   **첫 화면**은 1280×800 뷰포트에서 도식의 bounding box가 전부 보이는 것(잘리면 실패), 375×812에서는
   첫 그림 블록 높이의 절반 이상이 첫 화면 안에 보이는 것이다(윗부분만 걸치면 실패). 320×568은 첫 그림 블록의 위 끝이 첫 화면 안에 들어오면 충분하다(면적 규칙은 1280×800에만 적용).
3. **첫 화면은 보여 준다.** 결과물·화면·데이터가 있으면 설명하지 말고 목업이나 눌러 보는 프로토타입으로 보인다.
   **첫 화면(1280×800) 안에서** 그림·목업 면적이 글 면적보다 크다. 이 면적 규칙은 첫 화면에만 적용한다.
   그 아래 섹션은 그림이 필수가 아니다. 핵심 구조(관계·순서·크기·모양)가 있는 섹션은 그림을 권장하고, 구조를 글로 길게 풀지 않는다.
   **한 줄 읽기 축을 따라 그림을 크게 보여 준다.** 모든 섹션은 본문 축(안쪽 720px, `data-width="narrow"` 640px)의 같은 왼쪽 시작선에서 시작한다.
   그림은 축 폭의 75~100%를 쓰고(단순 도식만 `data-fit="compact"` 75%), 옆에 남는 폭은 채우지 않는다. 여백은 덩어리를 묶어 준다. 설명은 그림 아래에 둔다.
   2열은 동시 비교(A안 | B안, 전 | 후), 그림 지점과 번호로 대응하는 주석·범례 열, 대등한 두 덩어리(완료 | 남은 것, 문제 | 해결)일 때만 `.d0-wide` 구간 안 `.d0-cols`로 쓰고,
   분할선은 문서 전체에서 하나(12열 중 6/6 또는 7/5)다. 정본: `references/blocks/shell.md` 본문 축·2열 절.
4. **섹션은 독자 질문으로 정한다.** 섹션 하나는 독자 질문 하나에 답한다. 다른 질문은 별도 섹션으로 나누고, 같은 질문에 답하는 블록은 한 섹션에 합친다.
   섹션 수에 목표나 하한은 없다. 핵심 질문에 답하지 못하면 실패이고, 7개를 넘으면 묶을 수 있는 질문이 있는지 재검토한다(경고).
   구도 다양화·Editorial·Impact는 섹션을 늘리지 않는다. 기존 섹션을 **대체**할 때만 쓴다.
   **그림 없는 섹션**은 허용한다. 단 구조를 가진다: 질문→답, 라벨→설명, 주장→근거, 조건→영향, 단계→설명 중 하나 이상
   (explanation·evidence·before-after·checkpoint·question-answer·diff-rows·checklist·step-columns·accordion·표 같은 구조 블록). 연속된 일반 문단만으로 섹션을 채우지 않는다.
   **페이지 섹션**은 `main > section`이다. 섹션은 나란히 두지 않고 축을 따라 쌓는다. 블록 안 `section`(mockup-frame의 `.d0-app__body` 등)은 세지 않는다.
   패턴 문서의 권장 블록을 전부 채우지 않고 그 질문에 필요한 블록만 쓴다.
   **섹션 뼈대(원칙).** 제목(h2) → 그림 → 해석 한 줄 → 필요할 때만 "왜" 한 줄. 라벨 글 블록·표·목록은 이해에 필요한 만큼만 본 흐름에 두고, 흐름을 끊는 세부는 `details.d0-more` 접기로 보낸다.
   페이지 끝에 "기억할 한 줄" 상자(`aside.d0-keep`, blue-light 면, 라벨 + 한 문장)를 하나 둘 수 있다(선택).
5. **위계가 보인다.** 13px 회색 문장을 주 콘텐츠로 쓰지 않는다. 섹션 태그 pill은 기본 없음, callout은 페이지당 최대 1개.
   섹션 머리 설명 `p`는 최대 1문장이고 제목과 같은 말이면 생략한다. 스케일 값은 아래 9번이 정본이다.
6. **글은 짧게, 맥락은 남긴다.** 본문 설명은 라벨을 단 explanation 블록으로 쓰고 **한 라벨 아래 1~3문장**이다(4문장 이상이면 질문을 나눈다).
   라벨 없는 문단을 늘어놓지 않고, 용어는 일상 사물에 빗댄다. explanation 역할은 배경(context)·이유(reason)·뜻(interpretation)·영향(impact)·조건(constraint)·예외(exception)다.
   주장과 근거의 짝은 evidence 블록, 다음 행동·결정 요청은 closing 블록(또는 checklist 담당 변형·요약 행 결정 행)이 맡는다.
   용어는 **처음 나오는 곳**(대개 header 요약 행이나 리드)에서 `<abbr title>` 또는 괄호 속 짧은 비유로 푼다. 뒤 섹션에서만 풀지 않는다.
7. **마크업도 뜻을 말한다.** 구조는 시맨틱 태그로 짓는다(`section`·`header`·`figure`·`ol`/`ul`·`dl`·`table`·
   `time`·`data`·`progress`·`details`·`dialog`·`button`/`a`). 레이아웃·스타일 훅용 `div`·`span`
   (배지, 라벨, 그리드 묶음)은 허용한다. 빈 간격용 요소는 금지다. 블록별 태그는 `references/blocks.md`
   공통 규칙을 따르고, ARIA는 네이티브 요소로 안 될 때(탭 등)만 쓴다.
8. **한 사실은 한 번.** 숫자·결정은 정본 위치 하나에만 본문으로 둔다. 같은 숫자 문자열(예 `26분`)은 화면에 보이는 텍스트에
   페이지당 2회 이하다. 세는 범위는 `body.innerText`다(SVG `<text>`는 이미 들어 있으므로 따로 더하지 않고, SVG `<title>`·`<desc>`는 들어 있지 않아 세지 않는다).
   closing 메타(`dl.d0-closing__meta`·`dl.d0-slide__meta`)와 덱 제목 목차는 앞 사실을 가리키는 자리라 빼고 센다. 결정은 요약 행 또는 할 일 중 한 곳에 두고 다른 곳은 짧은 참조만 쓴다.
   요약 행 값은 데스크톱 한 줄(약 35자 이내), 용어 풀이는 `abbr` 또는 괄호 중 하나만 처음 등장 시 1회.
   **중복 제거는 맥락 제거가 아니다.** 같은 숫자·결정을 되풀이하지 말라는 규칙이지, 그 숫자가 왜 나왔는지·무엇을 뜻하는지·어떤 조건에서 달라지는지를 지우라는 규칙이 아니다.
   그림이 이미 보여 준 모양은 글로 반복하지 않고, 그림이 보여 줄 수 없는 이유·조건·영향은 explanation, 근거는 evidence로 남긴다.
9. **결론은 히어로로, 고급스러움은 절제로.**
   - **결론 히어로.** 결론 수치가 있는 보고·전/후 비교·사건 페이지는 h1 바로 아래(요약 행 위)에 결론 수치 1개를
     `d0-hero`로 둔다. 전 값(작게, grey-600, 취소선 없음) → 후 값(44px/600, 모바일 36, 단위는 숫자와 같은 크기) + 단위 + 한 줄 뜻(15px grey-600).
     수치가 없으면 생략한다. 정본: `references/blocks/hero.md`.
   - **줄 길이는 축으로.** 본문 한 줄의 길이는 본문 축(720px, 15px 본문 공백 포함 약 68~75자)이 정한다. 글 블록은 축(또는 놓인 `.d0-wide` 열) 폭을 그대로 쓰고 `p`·`dd`·글 블록에 따로 폭 상한을 두지 않는다.
     더 짧은 줄이 필요하면 페이지 전체를 `data-width="narrow"`로 둔다. 개행 규칙의 `p` `max-width` 금지는 그대로다. 정본은 `references/blocks/shell.md` 줄 길이 절이다.
   - **타이포 대비.** h1 32px/700(display 자간·행간), h2 20px/700(title 자간), 본문 15px/400 grey-800(`p` 행간 1.65, 토큰 규칙의 예외로 `references/blocks/shell.md` 행간 예외),
     보조 14px/400 grey-600, 라벨 12px/600 grey-600(대문자 변환 없음; grey-500은 선·화살표 같은 그래픽에만). 숫자는 전부 `tabular-nums`.
     explanation은 라벨 14px/600 grey-900 + 설명 15px grey-700이다. 모바일(≤640px) h1 26, h2 18, 히어로 숫자 36.
   - **여백 리듬.** 섹션 사이 64px(모바일 48), 섹션 안 블록 간 24px, 제목↔설명 8px, 페이지 상단 패딩 64.
     page Impact는 선택이고 페이지당 0~1개다. 배경 면·풀블리드 띠 없이 큰 글자와 여백만 쓰고 섹션 사이는 일반과 같은 64px(모바일 48)이다(덱 Impact 슬라이드는 그대로 blue-light 면). 안에는 문장 하나(32/700, 모바일 24) 또는 숫자 하나(64, 모바일 48)만 두고 editorial을 넣지 않는다(`references/blocks/shell.md` 강조 절).
     디바이더는 섹션 경계 1px grey-100과 행 목록의 행 구분선만 쓴다. closing 문장 아래·checkpoint 뒤 1px grey-200 한 줄은 블록 부품이라 예외다(`references/blocks/shell.md` 금지 절).
   - **그림 무대.** 회색 무대는 기본 없음이다. 무대 패딩 때문에 렌더 라벨이 하한 아래로 내려가면 무대를 쓰지 않는다(글자 있는 도식은 무대 없음). 무대가 필요할 때만 도식 SVG를 `figure.d0-fig[data-stage]` 안 `div.d0-fig__stage` 패널(grey-50 배경, radius card, 패딩 28 / 모바일 20) 위에 놓고,
     figcaption은 그림(무대) 밖 아래 13px grey-600. 쓰는 기준은 `references/composition.md`. SVG 선은 기본 1.5·강조 2.5, round cap/join, 노드 그림자 없음.
   - **강조 순서.** 크기 → 위치 → 여백 → 무게 → 색. 색은 마지막 수단이다. 구도·강조 3단계·밀도 리듬은 `references/composition.md`가 정본이다.
   - **색 면적은 lint Warning이다.** 첫 화면(1280×800·375×812) 진한 포인트 채움이 1% 미만이면 "강조가 너무 약한지 확인", 1~15%는 정상, 15% 초과면 "포인트 색이 배경처럼 쓰이는지 확인" 경고를 낸다. 게이트를 맞추려고 색 면적을 늘리지 않는다. 대비·WCAG 2.2 AA·의미색 글자 금지는 Hard로 유지한다. 옅은 채움은 경고 비율에서 빼고 면 단위 옅은 표면은 장면 수로 관리한다: page는 blue 무대 최대 1개와 기억할 한 줄 상자 `.d0-keep` 최대 1개(page Impact는 면이 없다), deck은 Impact 슬라이드 20~30%(`references/blocks/shell.md` 색 절). 회색만으로 된 도식·카드 묶음 금지는 유지한다.
     blue는 단계(blue 선·채움 / blue-dark 글자·번호 / blue-light 옅은 면)로, 의미색(green 가능·완료, orange 주의·준비, red 위험·실패)은
     면·점·선·배지 배경으로만 쓰고 글자 색으로 쓰지 않는다. 페이지당 의미색 2가지 + blue. 정본: `references/blocks/shell.md` 색 절.
     KPI는 숫자 + 막대(`전` 행에만 값, `후` 행은 라벨만)만 두고 증감 배지를 달지 않는다.
   - 그라디언트·글래스·두꺼운 그림자·장식 3D는 금지다. 모션·정렬 세부는 `references/blocks/shell.md`가 정본이다.
10. **많으면 나눈다.** 아래 상한을 넘으면 묶거나 페이지를 나눈다. 페이지 섹션 수는 상한이 아니라 원칙 4번(독자 질문)으로 정한다.

| 항목 | 상한 |
| --- | --- |
| 카드 | 5 |
| 단계 | 5 (guide 체크리스트는 총 단계 수 대신 구간 하나에 보통 3~5단계, `references/blocks/checklist.md` 구간 절) |
| 옵션 | 3 |
| 질문 | 6 |
| 표 열 | 7 (데이터 열 6 + 행 번호 열 1) |
| explanation 한 라벨 아래 문장 | 3 |
| callout | 1 |
| 상태 배지(`span.d0-pill`) 카드·행 하나에 | 1 |
| 배지 톤 종류(`data-tone`, 없으면 회색) / 의미색 종류, 페이지당 | 3 / 2 |

## 용어 계층

여섯 층은 **개념 계층**이다. 작업 순서가 아니다(작업 순서는 아래 작업 순서 절).

| 층 | 성격 | 내용 |
| --- | --- | --- |
| Principle | 강제 | 변하지 않는 원칙: ELI5 원칙, Day0 토큰·규칙, 개행 규칙, 개수 상한 |
| Pattern | 기준 | 정보를 설명하는 방식 8개(compare·flow·preview·report·guide·timeline·incident·faq). 독자 질문 하나에 답하는 섹션 단위로 고르고, 한 페이지에 여러 패턴을 섞는다 |
| Block | 선택 | 공용 부품(explanation·evidence·before-after·checkpoint·status rail·question-answer·closing과 그림·목록 블록). 패턴이 소유하지 않고 어느 패턴에서나 빌려 쓴다. 쓰면 해부 구조를 따른다 |
| Layout | 기준 | 배치 = 구도(`references/composition.md`) |
| Recipe | 선택 | 목적별 Pattern + Block 조합(`references/recipes.md`). 규칙 층이 아니라 출발점 조합이다 |
| Output | 별도 축 | page는 혼자 읽는 시각 문서, deck은 발표자와 함께 보는 자료. **같은 Block을 쓰고 밀도 규칙만 다르다** |

Pattern은 어떻게 설명할지, Block은 무엇으로 표현할지, Layout은 어디에 놓을지, Recipe는 무엇을 함께 쓰면 좋은지를 정한다.

**섞는 것이 기본이다.** 페이지 전체를 지배하는 주 패턴은 없다. 장애 회고에 비교·타임라인이 필요하면 섹션마다 그 패턴을 쓴다.
첫 화면 도식은 첫 섹션 패턴의 대표 도식이다. 패턴 문서의 블록 목록은 "추천 블록"이고 순서를 강제하지 않는다. 판정 기준은 "그 섹션이 독자 질문에 답했는가"다.
일관성은 블록 모양에서, 자유는 패턴·블록 선택에서 온다.
**어느 패턴에도 안 맞는 질문:** 원칙만 지키며 공용 블록으로 구성한다.
**새 블록이 필요해 보이면:** 기존 공용 블록으로 표현할 수 있으면 만들지 않는다. 판별 순서는 `references/blocks.md` 블록 추가 판별 절.

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
  파일 머리 주석(출처 경로·메모)도 원문 그대로 둔다. 예시 데이터의 "실제 회사·제품 이름 금지"는 페이지 내용에 대한 규칙이라 이 주석에는 적용하지 않는다.
- 규칙: day0-design `SKILL.md`의 스택 규칙·컴포넌트 원칙을 따른다.
- **우선순위.** 설명 페이지의 타이포 스케일(h1 32 / h2 20 / 본문 15, 설명 문단 행간 1.65, 원칙 9번)과 페이지 여백은 이 스킬 값이
  day0-design보다 우선한다. 색·radius·모션·컴포넌트 규칙은 day0-design을 따른다.
- 금지: `day0-design/references/anti-patterns.md`를 함께 적용한다.

## 모듈 라우팅

본문은 항상 로드한다. 아래는 조건이 맞을 때만 연다.

| 언제 | 연다 |
| --- | --- |
| 처음 만들 때 톤 기준으로 | `references/examples/preview-compare.html` (완성 예시: 흐름+격자 카드 → 결과물 목업 → 눌러 보는 A/B 프레임, 섹션마다 `data-pattern`) |
| 질문별 패턴을 고른 뒤 | 아래 패턴 판별 §3 표의 패턴 파일(섹션에 쓰는 패턴마다 하나) |
| 요청이 장애 회고·기능 출시 보고·설치 가이드·기능 소개·의사결정·상태 보고에 가까울 때 | `references/recipes.md` (Pattern + Block 조합 출발점, 선택) |
| 블록을 고를 때 | `references/blocks.md` (인덱스) → 쓸 블록 파일만 (예: `references/blocks/header.md`) |
| 라벨 단 짧은 설명(배경·이유·뜻·영향·조건·예외)을 쓸 때 | `references/blocks/explanation.md` |
| 주장에 근거(숫자·출처·전/후·예시)를 붙일 때 | `references/blocks/evidence.md` |
| 전과 후(문제→수정, 기존→개선, 예상→실제)를 보일 때 | `references/blocks/before-after.md` |
| 지금 위치(완료·진행·예정)를 보일 때 / 여기까지 하면 완성되는 결과를 남길 때 | `references/blocks/timeline.md` status rail 절 / `references/blocks/checkpoint.md` |
| 문서 끝에 결정·요청·행동·기준·지킬 것을 남길 때(page·deck) | `references/blocks/closing.md` |
| 페이지 골격·타이포·배지·본문 축과 넓은 구간(`.d0-wide`)·2열(`.d0-cols`)·섹션 뼈대·접기(`.d0-more`)·기억할 한 줄(`.d0-keep`)·줄 길이·첫 화면 높이 예산 | `references/blocks/shell.md` |
| SVG 도식을 그릴 때(항상; 라벨 크기 표·viewBox 폭 560, 작게 `data-fit="compact"`, 비율 `data-variant="ratio"`) | `references/blocks/diagram.md` |
| 보고·전/후 비교·사건에 결론 수치가 있을 때 | `references/blocks/hero.md` |
| 화면을 눌러 보게 할 때 | `references/blocks/mockup-frame.md` |
| 따라하기 단계를 그림과 함께 보일 때(왼쪽 단계 화면이 행에 따라 바뀜, `data-variant="linked"`), 긴 따라하기를 구간으로 나눌 때(`data-phased`) | `references/blocks/checklist.md` |
| 붙여 넣을 명령·설정이 있을 때(복사 버튼, 그림 블록 아님, 줄 길이 예외) | `references/blocks/code-block.md` |
| 섹션·슬라이드를 구성할 때(구도, 강조 3단계 `data-emphasis`, 밀도 리듬, 회색 무대를 쓰는 기준) | `references/composition.md` |
| 출력 형식이 deck일 때(덱 구성, 슬라이드 종류, Impact 비율, Slide Gate) | `references/output/deck.md` |
| 출력 형식이 deck일 때 마크업·CSS·JS(16:9 한 장 보기, 네비, 키보드, 인쇄, 덱 게이트) | `references/blocks/slide-deck.md` |
| 문구를 확정하기 전(page·deck 공통, 직역투 점검 목록과 예시 쌍) | `references/writing.md` |
| 결과물 HTML을 넘기기 직전(폰트 인라인, 발행 여부와 무관) | `scripts/subset_font.py` (Pretendard 서브셋 `@font-face` 생성) |

## 패턴 판별

### 1. 독자가 알아야 할 것 나누기

먼저 독자가 다 읽고 나서 무엇을 할 수 있어야 하는지 한 줄로 정한다. 그 행동에 이르려면 독자가 답을 얻어야 할 질문을 한 줄씩 적는다
(예: "무슨 일이 있었나", "왜 생겼나", "어떤 대안을 견줬나", "다음에 무엇을 하나"). 답할 수 없는 질문은 사용자에게 확인한다.
다른 질문은 다른 섹션이다. 같은 질문을 두 섹션에 나눠 답하지 않는다.

### 2. (있으면) 레시피 출발점

요청이 자주 쓰는 조합에 가까우면 `references/recipes.md`의 레시피를 출발점으로 쓴다:
장애 회고(`postmortem`), 기능 출시 보고(`launch-report`), 설치 가이드(`install-guide`), 기능 소개(`feature-intro`), 의사결정 문서(`decision-doc`), 상태 보고(`status-report`).
레시피는 Pattern + Block 조합 추천일 뿐 규칙이 아니다. 독자 질문에 없는 섹션은 빼고, 필요한 질문은 더한다. 레시피 없이 만들어도 된다.

### 3. 질문별 패턴 고르기

복합 질문마다 아래 표에서 답하기 좋은 패턴을 고른다. 한 페이지에 여러 패턴이 섞이는 것이 정상이다.
**예외:** 단일 정보 요구(지금 어디인가, 근거는, 조건·예외는 등)는 패턴 없이 블록으로 바로 답한다(작업 순서 4번).

| 패턴 | 이런 질문에 답한다 | 섹션이 남기는 것 | 연다 |
| --- | --- | --- | --- |
| compare | 무엇과 무엇이 어떻게 다르고, 무엇을 고르나? 바꾸기 전과 후는? | 판단 | `references/patterns/compare.md` |
| flow | 어떻게 흘러가나? 어떤 부품이 어떻게 이어지나? | 흐름·구조 이해, 다음 행동 | `references/patterns/flow.md` |
| preview | 받으면 어떤 모양인가? 무엇을 확인할 수 있나? | 모양 파악, 관심 여부 | `references/patterns/preview.md` |
| report | 지금 상태는? 무엇이 달라졌나? 무엇이 위험한가? | 현재 상황 판단 | `references/patterns/report.md` |
| guide | 어떻게 하나? 내 상황엔 어떻게 쓰나? | 올바른 실행·사용 | `references/patterns/guide.md` |
| timeline | 언제 무엇이 되나/바뀌었나? 무엇이 끝나야 다음이 되나? | 시간·의존성 공유 | `references/patterns/timeline.md` |
| incident | 무슨 일이 어떤 순서로 왜 일어났나? | 원인 이해, 재발 방지 | `references/patterns/incident.md` |
| faq | 이 용어는 무슨 뜻인가? 내 질문의 답은? | 특정 질문 해결 | `references/patterns/faq.md` |

패턴마다 자연스러운 섹션 깊이 참고값이 있다(목표가 아니라 참고다. 그 패턴이 페이지 대부분을 차지할 때의 흔한 섹션 수다).

| 패턴 | 비교 | 절차 | 미리보기 | 보고 | 가이드 | 일정 | 사건 | FAQ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 자연스러운 깊이 | 3~5 | 4~6 | 3~5 | 4~6 | 4~7 | 4~5 | 4~6 | 질문 수만큼 |

헷갈리는 쌍은 이 기준으로 가른다.

| 헷갈리는 쌍 | 기준 |
| --- | --- |
| timeline / flow | 날짜가 있으면 timeline, 순서만 있으면 flow |
| guide / flow | 체크박스로 직접 실행하면 guide 따라하기, 흐름 이해가 목적이면 flow, 잘 쓰는 법·선택 기준이면 guide 사용 가이드 |
| preview / report | 결과물의 모양이면 preview, 그로부터 알게 된 것이면 report |
| compare 시안 / 결정 | 화면을 눌러 고르면 시안, 숫자·정책을 고르면 결정 |
| timeline / report | 날짜 순서가 주인공이면 timeline, 지금 상태와 다음 행동이 주인공이면 report |
| incident / report | 사건 하나의 경위면 incident, 진행 상태·결과·지표 정리면 report(한 페이지에 둘 다 필요하면 섹션마다 나눠 쓴다) |
| 적용 전 변경 제안 | report 제안 변형 + 요약 행 헤더, 수치는 `예상치`로 표기(측정값과 섞지 않는다) |
| page / deck | 혼자 읽는 문서면 page, 발표·화면 공유로 한 장씩 넘기며 설득하면 deck. 출력 형식은 패턴 선택을 바꾸지 않는다 |

### 이름표

- **page.** 섹션마다 `data-pattern="compare|flow|preview|report|guide|timeline|incident|faq"`를 단다(`main > section`).
  패턴 변형은 같은 섹션의 `data-variant`로 단다. 레시피를 썼으면 `<main class="d0-page" data-recipe="...">`(선택). 패턴이 없는 섹션은 `data-pattern`을 생략한다.
- **deck.** 덱은 스토리라인 하나가 필요하므로 루트에 주 패턴 하나를 단다: `<main class="d0-deck" data-pattern="..." data-variant="...">`(필수). 레시피로 짠 덱이면 `data-recipe`를 더한다.
  루트 `data-pattern`은 스토리라인을 이끄는 주 패턴의 이름표일 뿐이다. 다른 패턴의 내용도 장 단위로 섞어 넣는다(`references/output/deck.md` 루트 마크업).
- 이름표일 뿐 스타일은 바꾸지 않는다(덱 표지 비율처럼 정본 파일이 정한 예외만).
- 변형 이름표 목록(정본): compare (생략 = 개념 비교)·`prototype`(시안)·`decision`(결정)·`before-after`(전/후), guide `practice`(사용 가이드, 따라하기는 생략), timeline `roadmap`·`changelog`, report `status`(기본)·`results`·`executive`·`proposal`. flow·preview·incident·faq는 변형이 없다.
- 예전 이름표는 이렇게 옮긴다: 페이지 루트의 옛 변형 이름표 `data-variant` → 해당 섹션의 `data-pattern` + `data-variant`, 덱 루트의 옛 `data-preset` → `data-pattern`. 예전 slides 변형의 대응은 `references/output/deck.md`.

## 출력 형식 판별 (page | deck)

질문과 패턴을 정한 뒤 출력 형식을 하나 고른다.

| 출력 형식 | 무엇인가 | 언제 | 연다 |
| --- | --- | --- | --- |
| `page`(기본) | 혼자 읽어도 이해되는 시각 문서. 구조 + 맥락 + 근거 + 조건 + 해석을 담는다 | 혼자 읽는 한 장짜리 문서. 신호가 없으면 page다 | 이 본문, 패턴 파일, `references/blocks/explanation.md` |
| `deck` | 발표자와 함께 보는 자료. 한 장 한 주장, 최소한의 글 | 발표·화면 공유·한 장씩 넘기기 요청 신호("발표 자료", "슬라이드로", "장표", "덱", "화면 공유용") | `references/output/deck.md`(구성·Slide Gate) + `references/blocks/slide-deck.md`(마크업) + 주 패턴 파일의 "덱으로 낼 때" 절 |

page와 deck은 같은 Pattern·Block을 쓴다. 다른 것은 밀도다: page는 explanation·evidence로 맥락까지 담고, deck은 한 장 한 주장으로 같은 블록을 줄여 쓰며(예: evidence는 `evidence` 슬라이드, closing은 마지막 장) 남는 말은 발표자가 한다.

**말투.** page는 해요체, deck은 제목·본문·해석을 `-다`체로 쓴다. 한 출력 안에서 섞지 않는다. 사용자가 준 문구와 인용, deck의 마지막 장 요청 문장(`정해 주세요`)과 네비 안내(`←/→로 넘겨요`)처럼 독자에게 직접 말하는 UI 문구는 그대로 둔다.

혼자 읽히는 게 주목적이면 page를 쓴다. 발표자 없이 전달될 덱이면 필요한 맥락과 출처를 덱 안에 남긴다(별도 모드 아님).
Audience × Purpose를 정한 뒤 `references/output/deck.md`의 Story Gate부터 통과하고 Slide·Visual·Ending과 구현 게이트를 본다.

**deck 출력 예외.** deck은 한 장짜리 문서가 아니라 16:9 슬라이드 5~12장(표지·제목 목차 포함)을 한 장씩 넘기는 덱이다. 원칙 4번 섹션 규칙, 원칙 2·3번 첫 화면 규칙, 원칙 6번 explanation 설명,
원칙 9번 히어로·h1 32/h2 20 고정 타이포·섹션 사이 64px·첫 화면 색 비중, 본문 축·2열·줄 길이 규칙, 720px 프레임, page 도식 라벨 렌더 13~20px 게이트, Page Depth Gate 대신
`references/output/deck.md`의 덱 구성·Slide Gate(한 장 한 주장, 결론 제목, 그림 면적·본문 밀도, 근거 밀도(제목이 주장하는 비교 기준·분모·관계가 화면에 있다, `stat`은 숫자 + 근거 그림이 기본), Impact 20~30%, 마지막 장(closing: decision·request·action·criteria·takeaway))와 `references/blocks/slide-deck.md` 덱 게이트를 따른다.
결론 수치는 히어로 대신 `stat` 슬라이드에 둔다. 나머지 원칙(글은 적게, 한 사실은 한 번(제목 목차·closing 메타 반복은 빼고 센다), 시맨틱, 토큰, 색, 접근성)은 그대로다.

## 개행 규칙

설명 문단이 옆 공간이 남는데도 일찍 줄 바뀌는 버그를 막는다. 원인은 대개 리드나
설명 `p`에 컨테이너보다 좁은 `max-width`(px·`ch`)를 건 것이다.
`day0-design/references/anti-patterns.md`가 슬롭 신호로 꼽는 좁은 부제와 같은 문제다.

- 리드·섹션 설명·블록 설명 문단(explanation `dd` 포함)은 **부모 컨테이너 폭을 그대로 쓴다.**
- 컨테이너보다 좁은 `max-width`·`width`·`ch` 단위를 `p`에 걸지 않는다. 좁혀야 하면 블록 컨테이너를 좁힌다.
- 한글은 `word-break: keep-all`, 본문은 `text-wrap: pretty`.
- `text-wrap: balance`는 제목 셀렉터(h1~h3)에만 쓴다.
- **문장 단위 개행(선택).** 기본은 이어 쓰기다. 리드·설명이 2문장 이상이고 데스크톱 폭에서 2줄을 넘기거나,
  문장마다 역할이 다르면(예: "무엇을 바꿨나" / "지금 상태·부탁") 온점 단위로 문장마다 줄을 나눈다.
  문장마다 `<span class="d0-sentence">`(`display: block`) 또는 별도 `<p>`를 쓰고 `<br>`을 늘어놓지 않는다.
  한 문장이 한 줄을 넘치면 그 안에서는 자연 줄바꿈한다.
- **요약 행.** 리드 내용이 "이전 → 현재 → 요청"처럼 역할로 나뉘면 문단 대신 header 요약 행(`라벨 | 한 문장` 2~3행)을 쓴다.
  compare 전/후·결정 변형, report, incident, timeline 변경 내역이 첫 섹션일 때의 기본 리드다. 결정·요청 행(`data-tone="decision"`)이 있으면 결정 callout과 closing `decision`을 두지 않는다.
  결정이 둘 이상이면 `결정 필요` 칸에 짧은 `ol`(최대 2개), 셋 이상이면 가장 중요한 1개만 요약 행에 두고 나머지는
  할 일 목록으로 보낸다. 요약 행은 최대 3행이다. 행 라벨·두 번째 결정의 세부 규칙은 `references/blocks/header.md`가 정본이다.

## 출력 형식

- **단일 self-contained HTML 파일**을 만든다. 호스트에 artifact 발행 기능이 있으면 발행한다.
- **폰트.** 결과물 HTML을 넘기는 모든 경우(파일 전달, artifact 발행)의 기본은 `scripts/subset_font.py`로 페이지 글자만 담은 Pretendard 서브셋 `@font-face`를 인라인해 외부 요청을 0건으로 만드는 것이다. 발행 여부와 무관하다.
  도구를 못 쓸 때(파이썬·원본 폰트 없음)만 Pretendard Variable jsDelivr `<link>` 하나를 두고, 외부 요청이 1건 남으며 artifact에서는 링크가 막혀 시스템 폰트로 대체된다고 사용자에게 알린다.
  그 밖의 외부 리소스는 없다. CSS·SVG·JS는 인라인이다.
- 인라인 `@font-face`는 메인 `<style>` **앞**의 별도 `<style>`이다. "tokens.css는 메인 `<style>` 맨 앞" 규칙과 충돌하지 않는다.
- **라이트 온리.** `:root { color-scheme: light; }`와 `body` 배경색을 명시해 다크 호스트에서도 깨지지 않게 한다. 다크 팔레트를 추가하지 않는다.
  예외는 덱의 장면 전환 장뿐이다: 표지·섹션·마무리 장(`data-kind="cover|section|closing"`)에만 `data-surface="dark"`(blue-dark 풀블리드 면 + 흰 글자, 덱당 1~3장)를 쓸 수 있다. 본문 장·Impact·page에는 쓰지 않는다(`references/blocks/slide-deck.md` 진한 면 절).
- 모바일 폭에서 좌우 16px 거터, 가로 스크롤 없음.
- **높이 720px 프레임.** 갤러리 iframe처럼 높이 약 720px 프레임(1280×720)에 넣을 페이지는 첫 SVG 도식의 위쪽 절반 이상이 720px 안에 든다(1280×800에서는 원칙 2번대로 전부 보인다). 머리 260 + 첫 그림 렌더 높이 390이 합계 기준이다(정본: `references/blocks/shell.md` 첫 화면 높이 예산).
- **한 artifact 안 여러 페이지.** 탭으로 고른 페이지를 iframe으로 보여 줄 때 같은 artifact의 다른 파일을 `src`로 부르지 않는다(뷰어 샌드박스에서 연결이 끊긴다).
  각 페이지 HTML을 base64 JSON으로 내장하고, 탭을 고르면 `TextDecoder`로 풀어 `iframe.srcdoc`에 넣는다. iframe은 `sandbox="allow-scripts"`이고 `allow-same-origin`은 주지 않는다.
  새 탭 열기는 같은 HTML로 만든 Blob URL을 쓰고, 막히면 "새 탭을 열 수 없어요. 이 화면에서 보세요" 같은 안내 문구를 보여 준다.
- 예시 데이터는 전부 합성이다. 실제 회사·제품·사람·티켓 번호처럼 보이는 값을 쓰지 않는다.
- 외부 사이트 링크와 레퍼런스 사이트 이름을 페이지에 넣지 않는다.

## 작업 순서

실제 작업 흐름은 용어 계층과 다르다: **독자가 알아야 할 것 → (있으면) Recipe를 출발점으로 → 필요한 Pattern 결정 → Block 선택 → Layout 구성 → Output에 맞게 조정.**

1. **독자가 알아야 할 것 나누기.** 독자가 다 읽고 나서 할 수 있어야 하는 것을 한 줄로 정하고, 거기에 필요한 질문을 한 줄씩 적는다. 답할 수 없는 질문은 사용자에게 확인한다.
2. **(있으면) Recipe.** 조합이 레시피에 가까우면 `references/recipes.md`를 출발점으로 쓴다. 없으면 건너뛴다.
3. **Pattern 결정.** 복합 질문마다 패턴 판별 표로 패턴을 고르고 그 패턴 파일을 연다. 단일 정보 요구는 패턴을 거치지 않고 4번으로 간다.
4. **Block 선택.** 알아야 할 것마다 블록을 고른다(`references/blocks.md`).
   - 단일 정보 요구 → Block으로 바로: 지금 어디인가 → status rail, 근거는 → evidence, 조건·예외는 → explanation `constraint`·`exception`, 왜 필요한가 → explanation `reason`,
     여기까지 하면 무엇이 되나 → checkpoint, 설치 방법 → checklist 단계, 막히는 이유 → question-answer, 수정 전후 → before-after, 무엇을 결정해 주나 → closing.
   - 복합 질문 → Pattern을 거쳐: 두 선택지 중 무엇이 나은가 → compare → evidence + before-after + closing. 무슨 일이 있었고 왜 → incident → status rail·timeline + evidence + explanation + checkpoint.
   첫 화면에 들어갈 SVG 도식을 먼저 정하고(첫 섹션 패턴의 대표 도식), 핵심 구조가 있는 섹션마다 그림을 고른다. 그림이 보여 줄 수 없는 이유·조건·영향은 explanation, 근거는 evidence로 붙인다.
   리드가 역할로 나뉘면 header 요약 행을 쓴다. 결론 수치가 있으면 히어로에 두고, 다른 곳은 그 숫자를 되풀이하지 않는다. 처음이면 예시 HTML로 톤을 맞춘다.
5. **Layout 구성.** 섹션마다 구도를 고르고(`references/composition.md`), 섹션 뼈대(제목 → 그림 → 해석 한 줄 → 필요할 때 "왜" 한 줄)를 따른다. 그림은 축 폭을 채우고 옆 빈자리는 그대로 둔다. 2열은 세 경우에만 `.d0-wide` 안에 두고(5칸 이상 단계 줄·긴 타임라인처럼 축 폭에서 칸·라벨 하한을 못 지키는 가로 순서 띠도 `.d0-wide` 한 블록으로 둘 수 있다), 문서의 분할선(6/6 또는 7/5)을 하나로 정한다.
6. **Output 조정.** 신호가 없으면 page. 발표·화면 공유 신호가 있으면 deck으로 정하고 `references/output/deck.md`를 연다. deck은 주 패턴 하나의 스토리라인으로 제목 목차를 먼저 쓰고 같은 블록을 덱 밀도로 줄인다.
7. **토큰 인라인.** 탐색 순서(의존 절)로 찾은 tokens.css 전체를 수정 없이 메인 `<style>` 맨 앞에 붙인다. 모두 실패하면 멈춘다.
8. **작성.** `references/blocks/shell.md` 스니펫에서 시작해 고른 블록 파일의 스니펫을 붙인다. 블록 해부대로 짓고, 섹션마다 `data-pattern`을 단다.
   설명은 한 라벨 아래 3문장 이내, 용어는 비유로 푼다.
   **문구 확정 전 직역투 점검.** page·deck 모두 제목·리드·라벨·설명·캡션·해석 줄·SVG `<text>`까지 `references/writing.md` 목록(영어식 은유, 무생물 주어 + 의지 동사, 압축 대구, 분열문, 번역 조사, 명사 나열 압축, 모호한 조건절)으로 읽고 누가·무엇을·어떻게를 원인 → 결과 순서의 일상 문장으로 고친다.
9. **게이트.** 아래 출력 게이트를 통과할 때까지 고친다. page는 Page Depth Gate를, deck은 Slide Gate를 의미 검사로 먼저 본다.
10. **넘기기 직전 폰트 인라인.** 결과물 HTML을 넘기면(파일·artifact 모두) 글자를 다 고친 뒤 `scripts/subset_font.py`로 서브셋 `@font-face`를 만들어
    jsDelivr `<link>` 자리에 넣는다(글자가 바뀌면 다시 만든다). 도구가 없으면 링크를 두고 외부 요청과 시스템 폰트 대체 가능성을 알린다.

## 출력 게이트

순서: page는 PAGE DEPTH(의미) → HARD → 접근성 → VISUAL → WARNING. deck은 `references/output/deck.md` Slide Gate(Story 먼저) → 아래 항목 중 deck 예외를 뺀 나머지.

**PAGE DEPTH (의미 검사, page만)**

글자 수·섹션 수의 하한으로 깊이를 재지 않는다. 완결성으로 잰다. 하나라도 걸리면 섹션 구성부터 고친다.

- [ ] 페이지가 독자의 핵심 질문에 모두 답한다(질문 목록과 섹션 제목을 한 줄씩 짝지어 검토)
- [ ] 중요한 결론에는 근거·이유·예시 중 하나 이상이 있다
- [ ] 변화나 문제를 말하면 원인 또는 영향 중 필요한 맥락이 있다
- [ ] 조건이 결과를 바꾸면 그 조건이 적혀 있다
- [ ] 행동이 필요하면 다음 행동·결정이 명확하다
- [ ] 짧게 만들려고 이해에 필요한 맥락을 지우지 않았다(중복 제거 ≠ 맥락 제거)

**HARD (코드로 확인)**

렌더 DOM 기준(JS 실행 후)으로 판정한다. 페이지 섹션은 `main > section`이다.
deck 출력은 위 deck 출력 예외에 적힌 항목 대신 `references/output/deck.md` Slide Gate(Story 먼저, 이어서 Slide·Visual·Ending)와 `references/blocks/slide-deck.md` 덱 게이트로 판정하고, 나머지 항목은 그대로 적용한다.

- [ ] 설명 `p`와 글 블록(explanation·evidence·faq `dl`, `.d0-cols` 열 칸)에 축·열보다 좁은 `max-width`·`width`·`ch` 제약이 없다
- [ ] `.d0-page`·`.d0-wide`·`.d0-fig svg`·`.d0-cols`의 CSS가 `references/blocks/shell.md` 정본 CSS 그대로다(안쪽 폭 720px, narrow 640px)
- [ ] `.d0-cols`가 `.d0-wide` 안에만 있고, 문서의 모든 2열이 같은 분할이다(`data-split="7-5"`가 전부 있거나 전부 없다. 번호 범례 2열인 pins·annotate·`d0-shot`의 `data-split`도 함께 센다)
- [ ] `.d0-keep`이 페이지당 1개 이하이고 마지막 섹션 끝(closing 앞)에 있다. `.d0-more`는 섹션마다 1개 이하이고 안에 그 섹션의 결정·정본 숫자가 없다
- [ ] `text-wrap: balance`가 제목 셀렉터(h1~h3)에만 있다
- [ ] 개수 상한(카드 5·단계 5, guide 체크리스트는 구간 규칙·옵션 3·질문 6·표 열 7 = 데이터 열 6 + 행 번호 열)을 넘지 않는다
- [ ] `role="img"`와 `<title>`을 가진 인라인 SVG 도식(kpi-cards 막대 변형, Editorial 장르의 SVG 객체 포함)이 1개 이상 있다. Editorial의 숫자는 SVG `<text>`가 아니라 HTML이다(SVG `<text>`로 그린 큰 숫자는 FAIL)
- [ ] Editorial(`figure.d0-fig[data-genre="editorial"]`)이 페이지당 1개 이하이고, 큰 글자가 실제 숫자이며(문구 FAIL), SVG 객체가 120px 이하다. 96px 이상 숫자는 Impact 안에만 있고, page Impact는 0~1개이며 안에 editorial이 없다
- [ ] header 다음 첫 페이지 섹션(첫 화면 섹션)에 그림 블록이 있다. checklist linked 변형의 무대 SVG는 그림 블록으로 세고, code-block은 그림으로 세지 않는다
- [ ] 그림 블록이 없는 페이지 섹션은 구조 블록(`dl.d0-explain`, `.d0-evidence`, `.d0-ba`, `.d0-checkpoint`, `.d0-closing`, faq, diff-rows, checklist, step-columns, accordion, `table`, `dl`·`ol`·`ul` 행 목록) 중 하나 이상을 담고, 섹션 머리 밖 내용이 연속된 일반 `p`만으로 이루어지지 않는다
- [ ] explanation(`dl.d0-explain > div > dd`) 하나가 4문장 이상이 아니고, 라벨 `dt`가 비어 있지 않으며, 묶음에 배경·테두리·그림자가 없다
- [ ] 도식 `figure.d0-fig`마다 안에 SVG가 있고, SVG `<text>` 하나가 4어절(공백 3개) 이상이 아니다(넘으면 텍스트 상자 도식으로 보고 FAIL)
- [ ] callout이 1개 이하, page `footer.d0-closing`이 1개 이하다. 문서 끝 다음 행동·결정은 closing이 맡고(마지막 섹션 끝에 callout을 두지 않는다), callout은 본문 중간용이며 같은 결정·다음 요청을 둘에 함께 두지 않았다
- [ ] header 요약 행에 `data-tone="decision"` 행이 있으면 결정 callout과 closing `decision`이 없다(하나만, 라벨 문구는 `결정 필요`·`도움 필요` 등 무엇이든 같다)
- [ ] 모든 h2에 섹션 태그 pill이 붙어 있지 않다(전부 붙어 있으면 FAIL)
- [ ] 배지(`.d0-pill`)에 고정 `height`와 `flex: none`이 있다
- [ ] 배지 톤 종류(`span.d0-pill`의 `data-tone`, 없으면 회색)가 3가지 이하, 카드·행 하나에 배지가 1개 이하, 의미색(`--d0-green`·`--d0-red`·`--d0-orange`)을 글자 `color`로 쓴 곳이 없다
- [ ] 같은 숫자 문자열(숫자+단위, 예 `26분`)이 화면에 보이는 텍스트(`body.innerText` 기준. SVG `<text>`는 이미 포함되므로 따로 더하지 않고, SVG `<title>`·`<desc>`는 제외)에 2회 이하다. closing 메타 `dd`와 덱 제목 목차는 빼고 센다
- [ ] 무대를 쓴 도식 `figure.d0-fig[data-stage]`는 SVG가 `.d0-fig__stage` 패널 안에 있고 figcaption은 패널 밖에 있다. 무대 안 SVG에 `<text>`가 없다(글자 있는 도식은 무대 없음, 375px 무대 안쪽에서 라벨이 11px 아래로 준다. 회색 무대는 기본 없음, 쓰는 기준은 `references/composition.md`)
- [ ] kpi-cards에 증감 배지가 없다
- [ ] 화면에 보이는 글(제목·라벨·설명·캡션·SVG `<text>`)에 직역투 표현이 없다(읽어서 확인, `references/writing.md` 점검 목록. 영어식 은유·무생물 주어 + 의지 동사·압축 대구·모호한 조건절이 하나라도 있으면 FAIL)
- [ ] `data-pattern` 값이 있으면 패턴 8개 중 하나다
- [ ] SVG·CSS 안 모든 `var(--d0-*)`가 tokens.css에 있다
- [ ] 구조(`section`·`header`·`figure`·`ol`/`ul`·`dl`·`table`·`time`·`data`·`progress`·`details`·`dialog`·`button`/`a`)를
  시맨틱 태그로 짓는다(blocks.md 공통 규칙 표). 레이아웃·스타일 훅용 `div`·`span`은 허용, 빈 간격용 요소는 없다
- [ ] 헤딩이 h1→h2→h3 순서이고 건너뛰지 않는다, 랜드마크 `main`이 1개다
- [ ] 네이티브 시맨틱과 겹치는 role이 없다(`<nav role="navigation">`, `<button role="button">` 금지)
- [ ] `color-scheme: light`와 `body` 배경이 있다
- [ ] tokens.css 전체가 메인 `<style>` 맨 앞에 인라인되어 있고 토큰용 외부 `<link>`가 없다
- [ ] 한 artifact 안 여러 페이지를 iframe으로 보여 줄 때 iframe `src`로 같은 artifact 파일을 부르지 않는다(`srcdoc` + `sandbox="allow-scripts"`, `allow-same-origin` 없음)
- [ ] 결과물 HTML(파일·artifact 모두)은 외부 요청이 0건이다(서브셋 `@font-face` 인라인). 도구가 없어 Pretendard jsDelivr 링크 하나를 둔 경우만 예외이고 사용자에게 알렸다
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

- [ ] 1280×800에서 SVG 도식의 bounding box가 첫 화면 안에 전부 보인다(잘리면 FAIL), 375×812에서는 첫 그림 블록 높이의 절반 이상이 첫 화면 안이다(윗부분만 걸치면 FAIL). 320×568은 첫 그림 블록의 위 끝이 첫 화면 안이면 통과다
- [ ] 첫 화면(1280×800) 안에서 그림·목업 면적이 글 면적보다 크다(그림 = `figure`·`svg`·목업 프레임 box, 글 = `p`·`li`·`dd` 텍스트 블록 box의 첫 화면 안 면적 합. 그림 안 글은 그림으로 센다). 첫 화면 아래 섹션은 이 면적 비교를 하지 않는다
- [ ] 1280px에서 모든 페이지 섹션의 h2 왼쪽 끝 x가 같다(±1px, 하나의 축). 축 밖으로 넓어진 것은 `.d0-wide` 블록(2열, 또는 축 폭에서 칸·라벨 하한을 못 지키는 가로 순서 띠)뿐이고, 그 안 2열 분할선(두 열 사이 틈의 가운데 x)이 문서 전체에서 하나다(±1px)
- [ ] 도식 `figure.d0-fig`의 SVG 렌더 폭이 놓인 자리(축, 무대 안쪽, `.d0-wide` 열) 폭의 75% 이상이다(`data-fit="compact"`가 정확히 75%. editorial의 120px 객체, 썸네일·와이어 카드·단계 열 그림 같은 블록 부품은 제외)
- [ ] 2열(`.d0-cols`, 번호 범례 2열)이 동시 비교·그림 지점과 번호로 대응하는 주석·범례·대등한 두 덩어리 중 하나다(읽어서 확인. "그림 | 그냥 설명 문단", "작은 그림 | 빈자리 채우는 목록"이면 FAIL)
- [ ] 옅은 면의 장면 수를 지킨다(blue 무대 1개 이하, deck Impact 20~30%). 색 면적은 아래 Warning으로만 판정한다
- [ ] 회색만 있는 도식이 없다(도식 `svg`마다 blue 계열 또는 의미색 `fill`·`stroke` 요소가 1개 이상)
- [ ] 배지가 세로로 늘어나지 않고 제목 첫 줄에 맞춰져 있다(배지 높이 = 22px 또는 20px, 배지 중심과 제목 첫 줄 중심 차 2px 이하)
- [ ] SVG 안 글자의 렌더 크기가 1280px에서 13px 이상 20px 이하, 375·320px에서 11px 이상이다.
  렌더 글자 크기 = font-size × (SVG 렌더 폭 ÷ viewBox 폭)로 잰다(무대가 있으면 무대 안쪽 폭). 글자 박스 높이는 쓰지 않는다(정본: `references/blocks/diagram.md` 라벨 절)
- [ ] 축 안 글 블록(리드 `p`, explanation·evidence·faq `dl`, 행 목록)의 box 폭이 축 폭과 같다(±1px. `.d0-wide` 열 안이면 그 열 폭). 글 블록마다 오른쪽 끝이 다르지 않다(정본: `references/blocks/shell.md` 줄 길이 절)
- [ ] 히어로가 있으면 히어로 수치가 1280×800 첫 화면 상단 1/3(y ≤ 267px) 안에 있다
- [ ] 페이지 섹션 사이 세로 간격이 64px(모바일 48px)이다(앞 섹션 마지막 블록 아래 끝 ~ 다음 섹션 `header` 위 끝, 오차 ±4px). page Impact(`data-emphasis="impact"`) 앞뒤도 같은 64px(모바일 48px)이다(배경 면 없이 일반 섹션 패딩 그대로)
- [ ] 옆 영역이 남는데 줄이 바뀐 설명 문단이 없다(문단 폭이 부모의 content box 폭(패딩 제외), grid 안이면 그 열 폭보다 24px 이상 좁은데 2줄 이상이면 FAIL. callout·카드 패딩이나 열 폭을 남는 영역으로 세지 않는다)
- [ ] 모바일 폭에서 가로 스크롤이 없다(375px에서 `scrollWidth` ≤ `clientWidth`)
- [ ] 섹션마다 그 섹션 패턴의 독자 질문에 답하는 블록이 있다(섹션 `data-pattern`과 패턴 파일의 질문을 짝지어 검토)
- [ ] explanation이 그림이 이미 말한 내용을 되풀이하지 않는다(그림을 가리고 explanation만 읽어도 새 정보가 있다)
- [ ] 처음 보는 사람이 그림과 제목만 훑어도 요지를 말할 수 있다(h1·h2·figcaption만 읽고 요지 한 문장을 써 본다)

**WARNING (lint, 실패 판정에 포함하지 않음)**

- [ ] 1280×800·375×812 첫 화면 진한 포인트 채움 <1%: "강조가 너무 약한지 확인", 1~15%: 정상, >15%: "포인트 색이 배경처럼 쓰이는지 확인". 측정은 `references/blocks/shell.md` 색 절을 따르고, 게이트를 맞추려고 색 면적을 늘리지 않는다
- [ ] 페이지 섹션이 7개를 넘으면 "같은 질문을 나눠 답한 섹션을 묶을 수 있는지 재검토". 섹션 수 자체로 실패시키지 않는다

PAGE DEPTH·HARD·접근성·VISUAL 항목(색 면적 Warning 제외)이 실패하면 고치고 다시 통과시킨다.
