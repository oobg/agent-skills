---
name: eli5-design
description: "아무것도 모르는 사람도 그림으로 구조를 먼저 이해하고 짧은 글로 이유와 맥락까지 이해하는 HTML 설명 문서를 Day0 시각 언어로 만든다. 그림 먼저, 라벨 아래 짧은 설명(라벨당 3문장 이내), 용어는 비유로 풀기를 강제하고, 독자 질문을 나눠 질문마다 비교, 절차, 미리보기, 보고, 따라하기·사용 가이드, 일정·변경 내역, 사건·원인, 용어·FAQ 여덟 패턴 중 맞는 것을 섹션 단위로 섞으며(장애 회고·기능 출시 보고·설치 가이드 같은 레시피는 선택), 한 장짜리 페이지(page) 또는 한 장씩 넘기는 발표 덱(deck)으로 출력하고 공용 블록을 골라 조립한다. 토큰은 형제 스킬 day0-design의 tokens.css 전체를 인라인하며, day0-design이 로컬에 없으면 공개 저장소 원본을 읽는다. '/eli5-design', '쉽게 설명하는 시안', '설명 페이지', '설명서 페이지', 'eli5 디자인', '그림으로 쉽게 보여줘', '쉽게 보는 발표 슬라이드' 요청에 사용한다. 설명 페이지가 아닌 Day0 제품 화면은 day0-design, 문구만이면 ux-writing으로 넘긴다. 설명 목적이 없는 일반 화면·랜딩 디자인에는 사용하지 않는다."
---

# ELI5 Design

무엇이든 **처음 보는 사람이 그림으로 구조를 먼저 잡고, 짧은 글로 이유와 맥락까지 이해하는 HTML 설명 문서**를 Day0 시각 언어로 만든다.
시안 문서, 설명서, 보고서, 가이드, 회고가 모두 이 형식이다. 기본은 한 장짜리 페이지(page), 발표용은 한 장씩 넘기는 덱(deck)이다.
세부 규칙은 단계마다 아래 references를 연다.

## 핵심 원칙

> Explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words.

"few words"는 글을 적게 쓰라는 뜻이 아니라 **같은 말을 그림과 글로 두 번 하지 말라**는 뜻이다. 그림이 구조를, 짧은 글이 이유·근거·조건을 맡는다.

원칙의 세부 수치·예외는 정본 파일에만 있다: 2·3·5·9는 [shell](references/blocks/shell.md)(타이포 스케일·본문 축·색)·[diagram](references/blocks/diagram.md)·[hero](references/blocks/hero.md), 4는 [patterns.md](references/patterns.md), 6·8은 [writing.md](references/writing.md), 7·10은 [blocks.md](references/blocks.md#개수-상한-원칙-10번), 판정은 [gates.md](references/gates.md).

1. **독자는 아무것도 모른다.** 배경지식·내부 용어·약어를 가정하지 않는다.
2. **SVG 도식은 필수다.** 첫 화면 안에 주제의 실체를 선과 면으로 그린 인라인 SVG를 1개 이상 둔다. 텍스트 상자 + 화살표는 도식이 아니다.
3. **첫 화면은 보여 준다.** 결과물은 목업으로 보이고 첫 화면에서 그림 면적이 글보다 크다. 그림은 본문 축 폭을 채운다.
4. **섹션은 독자 질문으로 정한다.** 섹션 하나가 질문 하나에 답한다. 그림 없는 섹션도 구조 블록으로 짓는다.
5. **위계가 보인다.** 작은 회색 보조문을 주 콘텐츠로 쓰지 않는다. 섹션 태그 pill은 기본 없음, callout은 상한 안에서 아껴 쓴다.
6. **글은 짧게, 맥락은 남긴다.** 라벨 하나 아래 1~3문장으로 쓰고, 용어는 처음 나올 때 일상 사물 비유로 푼다.
7. **마크업도 뜻을 말한다.** 구조는 시맨틱 태그로 짓고 ARIA는 네이티브로 안 될 때만 쓴다.
8. **한 사실은 한 번.** 같은 숫자·결정은 정본 한 곳에 둔다. 중복 제거는 맥락 제거가 아니다.
9. **결론은 히어로로, 고급스러움은 절제로.** 결론 수치는 히어로 하나, 타이포 스케일은 shell 정본을 따르고, 강조는 크기 → 위치 → 여백 → 무게 → 색, 의미색 글자 금지.
10. **많으면 나눈다.** 카드·단계·옵션·질문·표 열이 많아지면 묶거나 나눈다. 세부 기준은 blocks.md 개수 상한과 gates 정본이다.

**말투.** page는 해요체, deck은 제목·본문·해석을 `-다`체로 쓰고 섞지 않는다. 사용자가 준 문구·인용과 deck 마지막 장 요청(`정해 주세요`)·네비 안내(`←/→로 넘겨요`) 같은 UI 문구는 그대로 둔다.

## 판별 절차

| 단계 | 정할 것 | 세부 |
| --- | --- | --- |
| 1. 독자 질문 | 다 읽고 할 수 있어야 할 것 한 줄 → 질문 한 줄씩. 답할 수 없으면 사용자에게 확인한다 | [patterns.md](references/patterns.md) |
| 2. 패턴 | 복합 질문마다 아래 표에서 고르고 섹션마다 섞는다. 단일 정보 요구는 블록으로 바로 답한다 | 패턴 파일 |
| 3. 레시피(선택) | 장애 회고·출시 보고·설치 가이드·기능 소개·의사결정·상태 보고에 가까우면 출발점 | [recipes.md](references/recipes.md) |
| 4. 출력 | 신호가 없으면 `page`, 발표·화면 공유·"슬라이드로"·"장표"·"덱"이면 `deck`. 패턴 선택은 바뀌지 않는다 | [page](references/output/page.md) · [deck](references/output/deck.md) |

패턴 파일은 섹션에 쓰는 패턴마다 하나씩 연다.

| 패턴 | 이런 질문에 답한다 |
| --- | --- |
| [compare](references/patterns/compare.md) | 무엇과 무엇이 어떻게 다르고, 무엇을 고르나? 바꾸기 전과 후는? |
| [flow](references/patterns/flow.md) | 어떻게 흘러가나? 어떤 부품이 어떻게 이어지나? |
| [preview](references/patterns/preview.md) | 받으면 어떤 모양인가? 무엇을 확인할 수 있나? |
| [report](references/patterns/report.md) | 지금 상태는? 무엇이 달라졌나? 무엇이 위험한가? |
| [guide](references/patterns/guide.md) | 어떻게 하나? 내 상황엔 어떻게 쓰나? |
| [timeline](references/patterns/timeline.md) | 언제 무엇이 되나/바뀌었나? 무엇이 끝나야 다음이 되나? |
| [incident](references/patterns/incident.md) | 무슨 일이 어떤 순서로 왜 일어났나? |
| [faq](references/patterns/faq.md) | 이 용어는 무슨 뜻인가? 내 질문의 답은? |

page와 deck은 Pattern·Block을 공유할 수 있지만, 정보 구조·밀도·구도는 출력 형식에 맞게 다시 구성한다. page는 맥락까지 담고, deck은 한 장 한 주장이며 남는 말은 발표자가 한다.

## 라우팅

| 상황 | 읽을 파일 |
| --- | --- |
| 시각 톤이 불명확하거나 예시가 필요할 때만 | `references/examples/preview-compare.html` |
| 섹션 나누기·헷갈리는 패턴·이름표 | `references/patterns.md` |
| 블록 고르기·개수 상한 | `references/blocks.md` → 쓸 블록 파일만 |
| 골격·프레임과 왼쪽 읽기 축·폭 단계(`data-width`)·넓은 구간(`.d0-wide`)·여백 주석(`.d0-margin`)·2열·타이포·여백·색 | `references/blocks/shell.md` |
| SVG 도식(항상) | `references/blocks/diagram.md` |
| 결론 수치 / 눌러 보는 화면 / 따라하기 / 명령 | `references/blocks/hero.md` / `references/blocks/mockup-frame.md` / `references/blocks/checklist.md` / `references/blocks/code-block.md` |
| 구도·강조·밀도 리듬 | `references/composition.md` |
| 토큰·day0-design 탐색 | `references/day0.md` |
| 문구 확정 | `references/writing.md` |
| page 출력 | `references/output/page.md` |
| deck 출력 | `references/output/deck.md` + `references/blocks/slide-deck.md` |
| 정본 CSS·JS 인라인(열지 않는다) | `scripts/inline_assets.py`(`page` 또는 `deck` 모드, 자리표시자는 shell·slide-deck 스니펫) |
| 출력 게이트(출력 직전) | `references/gates.md` + `references/gates/page.md` 또는 `references/gates/deck.md` |

## 읽기 정책

- **MUST READ.** 선택한 output 파일 1개, 실제 쓰는 pattern 파일, 실제 쓰는 block 파일, 최종 게이트(`references/gates.md` + 현재 출력 형식 파일).
- **READ IF NEEDED.** recipe는 요청이 기존 레시피와 가까울 때, composition은 기본 구도로 해결되지 않을 때, examples는 시각 톤 판단이 어려울 때, day0는 토큰을 찾고 인라인할 때 연다.
- **DO NOT PRELOAD.** 쓰지 않는 pattern·block·recipe·example을 미리 읽지 않는다. 파일 안 링크를 따라 재귀로 열지 않는다.
- **DO NOT READ.** `assets/*.css`·`assets/*.js`는 읽지 않고 그대로 인라인한다(`scripts/inline_assets.py`, 도구가 없으면 파일 내용을 그대로 붙인다). 그 CSS·JS를 고칠 때만 읽는다.
- 마크업 전에 reference를 8개 이상 열려 하면, 선택하지 않은 파일을 미리 읽고 있는지 재검토한다(경고일 뿐 상한은 아니다).

## 작업 순서

독자 질문 → (있으면) Recipe → Pattern → Block → Layout → Output. 용어 계층(개념)과 다르다.
한 단계의 결정을 내린 뒤 다음 정본을 연다. 선택하지 않은 후보 파일은 열지 않는다.

1. **독자 질문.** 할 수 있어야 할 것 한 줄과 질문 목록을 적는다(`references/patterns.md`).
2. **Recipe(선택).** 가까운 레시피가 있으면 출발점으로 쓰고, 맨 위 읽을 파일 표에서 그 레시피 행만 본다(`references/recipes.md`).
3. **Pattern.** 복합 질문마다 판별 표로 고르고 패턴 파일을 연다. 단일 정보 요구는 4번으로 간다.
4. **Block.** `references/blocks.md`에서 고르고, 첫 화면 도식(첫 섹션 패턴의 대표 도식)을 먼저 정한다(`references/blocks/diagram.md`).
5. **Layout.** 주된 패턴으로 폭 단계를 정한다(report·incident·timeline·launch-report·postmortem → `data-width="report"`, guide·install-guide·faq → `"narrow"`, compare·flow·preview → 기본. 섞이면 주된 패턴 기준). 섹션마다 구도(`references/composition.md`)와 섹션 뼈대·읽기 축·2열 자리(`references/blocks/shell.md`)를 정한다.
6. **Output.** page는 `references/output/page.md`, deck은 `references/output/deck.md`를 연다. deck은 독자 질문을 장별 주장으로 배열한 제목 목차부터 쓴다.
7. **토큰.** `references/day0.md` 순서로 찾은 tokens.css 전체를 인라인한다. 못 찾으면 멈춘다.
8. **작성.** shell(덱은 slide-deck) 스니펫에 블록 스니펫을 붙이고, 자리표시자의 tokens·assets는 `scripts/inline_assets.py`(`page` 또는 `deck`)로 채운다(assets는 읽지 않는다). 문구 확정 전 `references/writing.md`로 점검한다.
9. **게이트.** page는 Page Depth Gate를, deck은 Slide Gate를 의미 검사로 먼저 본다(읽을 파일은 마지막 줄).
10. **폰트.** 넘기기 직전 `scripts/subset_font.py`로 서브셋 `@font-face`를 인라인한다.

출력 전 `references/gates.md` 인덱스와 현재 출력 형식 파일(`references/gates/page.md` 또는 `references/gates/deck.md`)만 읽고 HARD 게이트를 모두 확인한다.
