# ELI5 Design

아무것도 모르는 사람도 그림만 훑어 이해할 수 있는 한 장짜리 HTML 설명 페이지를
Day0 시각 언어로 만드는 에이전트 스킬입니다. 시안 비교, 절차 설명, 보고서,
따라하기 가이드처럼 누군가에게 무언가를 쉽게 보여 줘야 하는 문서에 씁니다.

## 사용 시점

- 시안이나 옵션을 나란히 놓고 결정을 받아야 할 때
- 절차, 구조, 결과물의 모양을 처음 보는 사람에게 설명할 때
- 보고서, 가이드, 일정, 사건 경위, 용어 정리를 한 장으로 보여 줄 때
- `/eli5-design` 으로 명시 호출할 때

설명 페이지가 아닌 Day0 제품 화면은 `day0-design`, 문구만 다듬는 작업은
`ux-writing`을 사용합니다.

## 핵심 동작

"아무것도 모르는 사람에게, 큰 그림과 적은 글로 된 HTML로 설명하라"는 원칙을
강제합니다. 첫 화면에 그림을 두고, 블록당 설명을 3문장 이내로 줄이고, 용어는
비유로 풉니다. 카드, 단계, 옵션, 질문, 표 열에는 개수 상한이 있고 넘으면
페이지를 나눕니다.

구성은 세 층으로 나뉩니다.

| 층 | 성격 | 내용 |
| --- | --- | --- |
| 원칙 | 강제 | 위 원칙, Day0 토큰과 규칙, 개행 규칙, 개수 상한 |
| 프리셋 | 기준 | 독자가 다 읽고 답할 수 있어야 할 질문과 권장 구성 예시 |
| 블록 | 선택 | 쓸지는 자유지만 쓰면 정해진 모양을 따릅니다 |

프리셋은 비교, 절차, 미리보기, 보고서, 가이드, 일정, 사건, FAQ 여덟 가지입니다.
블록 순서는 강제하지 않으며, 어느 프리셋에도 맞지 않는 요청은 원칙만 지키며
블록을 자유롭게 조립합니다.

설명 문단이 옆 공간을 남긴 채 일찍 줄 바뀌지 않도록, 설명 문단은 부모 폭을 그대로
쓰고 `text-wrap: balance`는 제목에만 둡니다. 결과는 단일 HTML 파일이며, 라이트
전용으로 다크 환경에서도 깨지지 않게 배경을 명시합니다. 호스트에 artifact 발행
기능이 있으면 발행합니다.

## 사용 예

```text
/eli5-design 알림 주기를 매일로 할지 매주로 할지 결정 페이지 만들어줘.
```

```text
주문 내보내기 파일이 어떻게 생겼는지 쉽게 설명하는 페이지 만들어줘.
```

```text
팀 A 신규 입사자용 설정 따라하기 가이드를 설명 페이지로.
```

## 요구 사항

`day0-design` 스킬을 함께 설치하는 것을 권장합니다. 이 스킬은 토큰 값을 갖지 않고
`day0-design`의 `tokens.css` 파일 전체를 HTML `<style>`에 그대로 인라인합니다.
`day0-design`을 어디서 찾는지는 `SKILL.md`의 탐색 순서를 따릅니다. 로컬에 없으면 공개
저장소 원본을 읽으므로 네트워크가 필요하고, 그마저 실패하면 토큰을 추측하지 않고 멈춥니다.
페이지의 외부 리소스는 Pretendard Variable 웹폰트만 사용합니다.

## 구성

| 파일 | 내용 |
| --- | --- |
| `SKILL.md` | 원칙, 3층 모델, day0-design 탐색 순서, 모듈 라우팅, 프리셋 판별, 개행 규칙, 작업 순서, 출력 게이트 |
| `references/blocks.md` | 블록 인덱스: 공통 규칙과 블록 표(언제 쓰나, 생김새, 파일) |
| `references/blocks/shell.md` | 페이지 골격 스니펫: 웹폰트, 토큰 인라인 자리, 컨테이너, 개행·포커스·모션 축소 기본값 |
| `references/blocks/header.md` | 작업 라벨, 제목, 리드, 구분선 |
| `references/blocks/section-head.md` | 섹션 제목, 회색 태그, 설명 한 줄 |
| `references/blocks/flow-line.md` | 한 줄 흐름과 현재 단계 표시 |
| `references/blocks/thumb-cards.md` | SVG 도식 썸네일 카드와 상태 배지 |
| `references/blocks/kpi-cards.md` | 지표 숫자, 증감, 한 줄 해석 |
| `references/blocks/diagram.md` | 번호 상자와 SVG 화살표 도식 (흐름형, 레이어형) |
| `references/blocks/step-columns.md` | 단계별 열 |
| `references/blocks/side-by-side.md` | 시안 미니 프로토타입과 결정 비교 열, 선택 전환 JS |
| `references/blocks/diff-rows.md` | 바뀐 항목만 전후로 보여 주는 행 |
| `references/blocks/tab-preview.md` | 시트 탭, 파일명 바, 표 목업, 탭 전환 JS |
| `references/blocks/timeline.md` | 가로 마일스톤과 세로 기록, 오늘 표식 |
| `references/blocks/checklist.md` | 진행률과 체크 행, 체크 JS |
| `references/blocks/accordion.md` | 질문 펼침과 용어 카드, 펼침 JS |
| `references/blocks/callout.md` | 결론, 결정 요청, 다음 할 일 상자 |
| `references/formats/compare.md` | 시안·옵션 비교 (시안, 결정, 전/후 변형) |
| `references/formats/flow.md` | 절차·구조 설명 (흐름형, 레이어형 도식) |
| `references/formats/preview.md` | 결과물 미리보기 |
| `references/formats/report.md` | 보고서 |
| `references/formats/guide.md` | 따라하기 가이드 |
| `references/formats/timeline.md` | 로드맵과 변경 내역 |
| `references/formats/incident.md` | 사건 경위와 원인 |
| `references/formats/faq.md` | 용어 카드와 FAQ |

설치와 검증 방법은 저장소의 [루트 README](../../README.md)에서 확인할 수 있습니다.
