# patterns — 패턴 판별 세부

SKILL.md 판별 표(독자 질문 → 패턴 → 레시피 → 출력)로 고른 뒤, 섹션을 나누거나 패턴이 헷갈리거나 이름표를 달 때 이 파일을 연다. 패턴마다의 규칙은 [patterns/](patterns/compare.md) 아래 패턴 파일이 정본이다.

## 섹션은 독자 질문으로 정한다 (원칙 4번)

- 섹션 하나는 독자 질문 하나에 답한다. 다른 질문은 별도 섹션으로 나누고, 같은 질문에 답하는 블록은 한 섹션에 합친다.
- 섹션 수에 목표나 하한은 없다. 핵심 질문에 답하지 못하면 실패이고, 7개를 넘으면 묶을 수 있는 질문이 있는지 재검토한다(경고).
- 구도 다양화·Editorial·Impact는 섹션을 늘리지 않는다. 기존 섹션을 **대체**할 때만 쓴다.
- **그림 없는 섹션**은 허용한다. 단 구조를 가진다: 질문→답, 라벨→설명, 주장→근거, 조건→영향, 단계→설명 중 하나 이상
  (explanation·evidence·before-after·checkpoint·question-answer·diff-rows·checklist·step-columns·accordion·표 같은 구조 블록). 연속된 일반 문단만으로 섹션을 채우지 않는다.
- **페이지 섹션**은 `main > section`이다. 섹션은 나란히 두지 않고 축을 따라 쌓는다. 블록 안 `section`(mockup-frame의 `.d0-app__body` 등)은 세지 않는다.
- 패턴 문서의 권장 블록을 전부 채우지 않고 그 질문에 필요한 블록만 쓴다.
- 섹션 뼈대(제목 → 그림 → 해석 한 줄 → 필요할 때만 "왜" 한 줄), 접기 `.d0-more`, 기억할 한 줄 `.d0-keep`은 [blocks/shell.md](blocks/shell.md) 섹션 뼈대 절이 정본이다.

## 독자가 알아야 할 것 나누기

먼저 독자가 다 읽고 나서 무엇을 할 수 있어야 하는지 한 줄로 정한다. 그 행동에 이르려면 독자가 답을 얻어야 할 질문을 한 줄씩 적는다
(예: "무슨 일이 있었나", "왜 생겼나", "어떤 대안을 견줬나", "다음에 무엇을 하나"). 답할 수 없는 질문은 사용자에게 확인한다.
다른 질문은 다른 섹션이다. 같은 질문을 두 섹션에 나눠 답하지 않는다.

## 섞는 것이 기본이다

- 페이지 전체를 지배하는 주 패턴은 없다. 장애 회고에 비교·타임라인이 필요하면 섹션마다 그 패턴을 쓴다.
- 첫 화면 도식은 첫 섹션 패턴의 대표 도식이다. 패턴 문서의 블록 목록은 "추천 블록"이고 순서를 강제하지 않는다. 판정 기준은 "그 섹션이 독자 질문에 답했는가"다.
- 일관성은 블록 모양에서, 자유는 패턴·블록 선택에서 온다.
- **어느 패턴에도 안 맞는 질문:** 원칙만 지키며 공용 블록으로 구성한다.
- **새 블록이 필요해 보이면:** 기존 공용 블록으로 표현할 수 있으면 만들지 않는다. 판별 순서는 [blocks.md](blocks.md) 블록 추가 판별 절.

## 단일 정보 요구는 블록으로 바로

단일 정보 요구(지금 어디인가, 근거는, 조건·예외는 등)는 패턴 없이 블록으로 바로 답한다([blocks.md](blocks.md)).

- 지금 어디인가 → status rail, 근거는 → evidence, 조건·예외는 → explanation `constraint`·`exception`, 왜 필요한가 → explanation `reason`,
  여기까지 하면 무엇이 되나 → checkpoint, 설치 방법 → checklist 단계, 막히는 이유 → question-answer, 수정 전후 → before-after, 무엇을 결정해 주나 → closing.
- 복합 질문 → Pattern을 거쳐: 두 선택지 중 무엇이 나은가 → compare → evidence + before-after + closing. 무슨 일이 있었고 왜 → incident → status rail·timeline + evidence + explanation + checkpoint.

## 레시피 출발점

요청이 자주 쓰는 조합에 가까우면 [recipes.md](recipes.md)의 레시피를 출발점으로 쓴다:
장애 회고(`postmortem`), 기능 출시 보고(`launch-report`), 설치 가이드(`install-guide`), 기능 소개(`feature-intro`), 의사결정 문서(`decision-doc`), 상태 보고(`status-report`).
레시피는 Pattern + Block 조합 추천일 뿐 규칙이 아니다. 독자 질문에 없는 섹션은 빼고, 필요한 질문은 더한다. 레시피 없이 만들어도 된다.

## 패턴이 남기는 것

SKILL.md 판별 표의 질문에 답한 섹션이 독자에게 남기는 것이다. 섹션이 이것을 남겼는지로 패턴 선택을 검토한다.

| 패턴 | 섹션이 남기는 것 |
| --- | --- |
| compare | 판단 |
| flow | 흐름·구조 이해, 다음 행동 |
| preview | 모양 파악, 관심 여부 |
| report | 현재 상황 판단 |
| guide | 올바른 실행·사용 |
| timeline | 시간·의존성 공유 |
| incident | 원인 이해, 재발 방지 |
| faq | 특정 질문 해결 |

## 자연스러운 깊이

패턴마다 자연스러운 섹션 깊이 참고값이 있다(목표가 아니라 참고다. 그 패턴이 페이지 대부분을 차지할 때의 흔한 섹션 수다).

| 패턴 | 비교 | 절차 | 미리보기 | 보고 | 가이드 | 일정 | 사건 | FAQ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 자연스러운 깊이 | 3~5 | 4~6 | 3~5 | 4~6 | 4~7 | 4~5 | 4~6 | 질문 수만큼 |

## 헷갈리는 쌍

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

## 이름표

- **page.** 섹션마다 `data-pattern`, 변형은 같은 섹션의 `data-variant`, 레시피는 루트 `data-recipe`(선택). 정본은 [output/page.md](output/page.md) 루트 마크업.
- **deck.** 루트에 주 패턴 하나를 단다(`<main class="d0-deck" data-pattern="..." data-variant="...">`, 필수). 정본은 [output/deck.md](output/deck.md) 루트 마크업.
- 이름표일 뿐 스타일은 바꾸지 않는다(덱 표지 비율처럼 정본 파일이 정한 예외만).
- 변형 이름표 목록(정본): compare (생략 = 개념 비교)·`prototype`(시안)·`decision`(결정)·`before-after`(전/후), guide `practice`(사용 가이드, 따라하기는 생략), timeline `roadmap`·`changelog`, report `status`(기본)·`results`·`executive`·`proposal`. flow·preview·incident·faq는 변형이 없다.
- 예전 이름표는 이렇게 옮긴다: 페이지 루트의 옛 변형 이름표 `data-variant` → 해당 섹션의 `data-pattern` + `data-variant`, 덱 루트의 옛 `data-preset` → `data-pattern`. 예전 slides 변형의 대응은 [output/deck.md](output/deck.md).
