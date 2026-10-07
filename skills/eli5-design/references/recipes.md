# recipes — 자주 쓰는 Pattern + Block 조합

레시피는 목적별로 자주 나오는 독자 질문 묶음에 Pattern과 공용 Block을 미리 짝지어 둔 **선택 출발점**이다. 규칙 층이 아니고 강제가 아니다.
요청이 레시피에 가까우면 섹션 순서를 빌리고, 독자 질문에 없는 섹션은 빼고 필요한 질문은 더한다. 레시피 없이 만들어도 된다.
섹션 수는 레시피가 아니라 독자 질문이 정한다(SKILL.md 원칙 4번). 레시피를 썼으면 `<main class="d0-page" data-recipe="...">`로 표시한다(선택).

각 섹션은 `질문 → Pattern(섹션 data-pattern) → 추천 Block` 순서로 적는다. Pattern 칸이 `—`이면 단일 정보 요구라 Block으로 바로 답한다.
**표의 첫 행이 첫 화면 섹션이다.** 첫 행에는 첫 화면 규칙(SKILL.md 원칙 2·3번: 도식이 첫 화면 안, 그림 면적 > 글 면적)을 통과할 그림이 있는 질문을 둔다. 순서를 바꿀 때도 이 조건을 지킨다.
높이 12px 비율 막대(`data-variant="ratio"`)만으로는 면적이 모자라므로 첫 화면에서는 전/후 막대·그래프·와이어프레임처럼 면이 있는 그림을 주 그림으로 둔다.
공용 Block: [explanation](blocks/explanation.md) · [evidence](blocks/evidence.md) · [before-after](blocks/before-after.md) · [checkpoint](blocks/checkpoint.md) · [status rail](blocks/timeline.md) · [question-answer](blocks/faq.md) · [closing](blocks/closing.md).

## 장애 회고 `postmortem`

incident + timeline + evidence + before-after + closing.

- **독자·목적.** 사건을 겪지 않은 팀원과 결정권자. 무슨 일이 왜 생겼는지 이해하고, 재발 방지에 동의하거나 맡게 한다.

| 질문 | Pattern | 추천 Block |
| --- | --- | --- |
| 무슨 일이 있었고 지금 어떤가? | `incident` | 첫 화면 영향 그래프, 히어로 또는 요약 행([header](blocks/header.md) 라벨 표), explanation `impact` |
| 무슨 순서로 일어났나? | `timeline` | SVG 시간 막대 + 세로 타임라인, 원인이 확정된 지점에 checkpoint(`여기서 원인 확정`), 인지가 늦은 이유는 explanation `reason` |
| 왜 생겼고 왜 못 막았나? | `incident` | 직접 → 근본 원인 graph, 옆 열에 evidence(어떻게 확인했나), explanation `constraint` |
| 무엇을 고쳤나? | — | before-after `fix`(문제 → 수정) |
| 다음에 무엇을 하나? | — | checklist 담당 변형 + closing `takeaway` |

- **덱으로 낼 때.** `<main class="d0-deck" data-pattern="incident" data-recipe="postmortem">`. [incident](patterns/incident.md)의 회고 덱 스토리라인을 따르고, 대응은 before-after를 `evidence` 슬라이드 한 장으로 낸다.

## 기능 출시 보고 `launch-report`

report + timeline + compare + faq.

- **독자·목적.** 관리자·협업 팀·사용자 대표. 무엇이 나갔고 무엇이 달라졌는지 판단하고, 남은 일정과 자주 묻는 것을 알게 한다.

| 질문 | Pattern | 추천 Block |
| --- | --- | --- |
| 무엇이 나갔고 지금 상태는? | `report` | 첫 화면 전/후 막대(완료 범위 비율 막대는 보조로), 상태 배지, evidence(측정 근거) |
| 일정은 어디쯤인가, 다음은 언제인가? | `timeline` | status rail(준비 · 출시 · 확대), 시간 막대, 밀린 이유는 explanation `reason` |
| 이전과 무엇이 다른가? | `compare` | before-after `improve`(기존 → 개선), 누구에게 달라지는지 explanation `impact` |
| 자주 묻는 것은? | `faq` | question-answer 3~5개 |
| 무엇을 해 주길 바라나? | — | closing `request` 또는 `action` |

- **덱으로 낼 때.** `<main class="d0-deck" data-pattern="report" data-variant="results" data-recipe="launch-report">`. [report](patterns/report.md)의 결과·지표 스토리라인을 따른다. FAQ는 덱에 넣지 않고 page로 둔다. 발표 없이 메일·메신저로 돌려 읽힐 덱이면 장마다 측정 근거·출처를 해석 줄과 출처 줄에 남긴다.

## 설치 가이드 `install-guide`

guide + preview + checklist(단계, 긴 경우 구간) + question-answer.

- **독자·목적.** 처음 설치하는 사용자. 끝나면 무엇이 보이는지 알고, 구간마다 결과를 확인하며 혼자 끝까지 설치하게 한다.

| 질문 | Pattern | 추천 Block |
| --- | --- | --- |
| 끝나면 어떻게 보이나? | `preview` | 첫 화면 완료 화면 와이어프레임 또는 기기 프레임, 범위 고지 |
| 무엇을 준비하나, 왜 필요한가? | — | 준비물 한 줄 행 + explanation `reason`·`constraint` |
| 어떻게 설치하나? | `guide` | checklist linked 변형 + 구간(`data-phased`: 맨 위 `전체 n / N 완료` + 구간 머리 행이 지도와 결과, 현재 구간만 펼침), 단계별 code-block |
| 막히면 왜 그런가? | — | question-answer(`왜 여기서 멈추나요?`), 고친 설정은 before-after `fix` |
| 다 끝나면 무엇을 하나? | — | closing `criteria` 또는 `action` |

- **덱으로 낼 때.** `<main class="d0-deck" data-pattern="guide" data-recipe="install-guide">`. [guide](patterns/guide.md)의 시연 덱을 따른다. 혼자 체크하며 설치하는 용도면 page가 낫다.

## 기능 소개 `feature-intro`

preview + flow + compare + faq.

- **독자·목적.** 기능을 처음 보는 사용자·동료. 무엇이 달라지는지 보고 써 볼지 판단하게 한다.

| 질문 | Pattern | 추천 Block |
| --- | --- | --- |
| 이것은 무엇이고 어떤 모양인가? | `preview` | 첫 화면 기기 프레임 또는 핀 해부도, 범위 고지 |
| 어떻게 쓰나? | `flow` | 단계 도식 + step-columns, 막히는 갈림은 explanation `exception` |
| 지금 방식과 무엇이 다른가? | `compare` | before-after `change`, 왜 바꾸나 explanation `reason` |
| 자주 묻는 것은? | `faq` | question-answer |

- **덱으로 낼 때.** `<main class="d0-deck" data-pattern="preview" data-recipe="feature-intro">`. [preview](patterns/preview.md)의 Demo 스토리라인을 따른다.

## 의사결정 문서 `decision-doc`

compare + context + evidence + trade-off + decision.

- **독자·목적.** 결정권자. 배경과 근거를 보고 트레이드오프를 이해한 뒤 하나를 고르게 한다.

| 질문 | Pattern | 추천 Block |
| --- | --- | --- |
| 무엇과 무엇을 견주나? | `compare` | 첫 화면 결정 변형: side-by-side 와이어 카드(또는 선택지 비교 막대), 같은 비교축, 결정 요약 행([header](blocks/header.md) 라벨 표) |
| 왜 지금 정해야 하나? | — 또는 `report` | explanation `context`. 문제 크기가 숫자면 전/후 막대를 이 섹션에 둔다(첫 화면에 두지 않는다) |
| 근거는? | — | evidence(number·source), 숫자 크기는 kpi-cards 막대 변형 |
| 무엇을 얻고 무엇을 포기하나? | `compare` | 고르면 생기는 일 graph + explanation `constraint`(이 조건이면 답이 바뀐다) |
| 무엇을 결정해 주길 바라나? | — | 요약 행 결정 행 또는 closing `decision` 중 한 곳 |

- **덱으로 낼 때.** `<main class="d0-deck" data-pattern="compare" data-variant="decision" data-recipe="decision-doc">`. [compare](patterns/compare.md)의 Decision 스토리라인을 따른다.

## 상태 보고 `status-report`

report + timeline + risk + next.

- **독자·목적.** 관리자·협업 팀. 지금 상황을 판단하고 필요한 결정·도움을 주게 한다.

| 질문 | Pattern | 추천 Block |
| --- | --- | --- |
| 지금 어떤 상태이고 무엇이 달라졌나? | `report` | 첫 화면 상태 배지 + 전/후 막대 또는 일정 시간 막대(비율 막대는 보조로), evidence, 달라진 이유 explanation `reason` |
| 일정은 어디쯤인가? | `timeline` | status rail 또는 시간 막대(오늘 표식), 밀리면 explanation `impact` |
| 무엇이 위험한가? | `report` | diff-rows 위험 행(영향·대응) |
| 다음에 누가 무엇을 하나? | — | checklist 담당 변형, 가장 중요한 하나는 closing `request` |

- **덱으로 낼 때.** `<main class="d0-deck" data-pattern="report" data-variant="status" data-recipe="status-report">`. [report](patterns/report.md)의 Executive Update 스토리라인을 따른다.

## 레시피 밖

- 요청이 어느 레시피에도 맞지 않으면 레시피 없이 질문별로 Pattern과 Block을 고른다. `data-recipe`는 생략한다.
- 레시피 섹션을 전부 채우려고 없는 질문을 지어내지 않는다.
- 새 조합이 자주 반복되면 새 블록이 아니라 새 레시피로 더한다([blocks.md](blocks.md) 블록 추가 판별).
