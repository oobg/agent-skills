# 분석 리포트 템플릿

요약 다섯 절이 본문이고 상세 분석은 부록이다. 규모에 맞춰 절을 합치거나 지운다. 비어 있는 절을 채우려고 관행을 쓰지 않는다.

## 요약

### 1. 개요

- 분석 대상: (제품명 또는 화면명)
- 입력 형태와 기준: (원본 코드 / 빌드 결과물 / 배포된 서비스 / 정적 스냅샷, 커밋 해시 또는 파일 해시 또는 URL, 분석 시점)
- 작성자, 작성일
- 분석 목적: (예: 프로토타입에서 기능 구조를 복원해 개발 착수 범위를 정한다)
- 검증 방식: 정적 수집만 했는지, 로컬 실행이나 브라우저 관찰을 했는지
- 커버리지: 읽은 파일과 화면, 건너뛴 것과 이유, 열어 보지 못한 것, 실행하지 않은 것, 도구와 스크립트 실패

### 2. 주요 기능과 화면 구성

- 제품 목적과 핵심 사용자 업무 한두 문장
- Product Map (화면 트리)
- 도입 배경: PRD, 티켓, 온톨로지 선례처럼 입력이 있을 때만 쓰고 출처를 적는다. 없으면 절을 지운다.

### 3. 구현 수준과 격차

| ID | Feature | Priority | Level | Confidence | 비고 |
| -- | ------- | -------- | ----- | ---------- | ---- |

이어서 세 묶음으로 나눈다.

- 구현된 것 (L3 이상, CONFIRMED)
- 의도만 있는 것 (L1~L2, 또는 INFERRED)
- 운영 전환에 필요한 것 (L4~L5 요구: persistence, 권한, 동시성, 외부 연동 예외, 감사). 프로토타입에서 판정하지 않기로 한 보안, id 생성, 성능, 경합 항목은 결함이 아니라 여기에 등급 없이 적는다.

### 4. 검증 결과와 예외 처리

- 의도와 구현의 어긋남: 주석이나 명칭이 선언한 규칙을 코드가 지키지 않는 곳. 선언 위치와 위반 위치를 함께 적는다.
- 끊긴 체인: 어디서 끊기는지와 Evidence
- 처리된 edge case
- 처리되지 않은 edge case와 UI 상태
- 누락 (BLOCKING / IMPORTANT / OPTIONAL, 근거 조건 번호)

### 5. 기능 평가와 액션 아이템

P0과 P1 Feature마다 장점, 단점, 바꾸면 좋을 것을 쓴다. 각 항목은 관찰된 사실 하나에 묶이고 근거 유형과 Evidence를 갖는다.

| Feature | 구분 | 내용 | 근거 유형 | Evidence |
| ------- | ---- | ---- | --------- | -------- |

- 구분은 장점, 단점, 변경 제안 세 가지다. 변경 제안에는 (제안)을 붙인다.
- 근거 유형은 다섯 가지로 제한한다. 체인 완결성(끊김 없이 feedback까지 닿는가), 규칙 일관성(같은 개념이 같은 정의를 쓰는가), 워크플로우 단축(사용자 목적까지 단계가 줄거나 늘었는가), 보호 장치(destructive action의 확인·이력·복구), 누락 조건(rubric의 여섯 조건 중 번호).
- 일반 관행이나 취향만으로 단점을 쓰지 않는다. 시각적 완성도는 design-slop-audit, 코드 품질은 code-review의 몫이다.
- 전체 총평은 잘된 점과 아쉬운 점 각각 세 줄 안으로 적는다.
- 액션 아이템: `[등급] 내용 (관련 Feature ID)` 형식. 등급은 누락 등급을 그대로 쓴다.

## 부록

부록은 요약에서 다 설명되지 않은 것만 담는다. 화면 하나짜리 분석이면 부록이 없을 수 있다.

### A. Domain Model

| Entity | Purpose | Key Data | Relations | Evidence |
| ------ | ------- | -------- | --------- | -------- |

### B. Feature Inventory

| ID | Feature | Surface | User Action | System Behavior | Mutation | Priority | Level | Confidence | Evidence |
| -- | ------- | ------- | ----------- | --------------- | -------- | -------- | ----- | ---------- | -------- |

ID는 `RSV-001`, `ORD-002`처럼 도메인 접두어와 번호로 만든다.

### C. Feature Detail (P0, P1)

```text
Feature / Purpose / Trigger / Preconditions / User Flow / Business Rules
Data Read / Data Mutation / State Transition / Side Effects / Feedback
Edge Cases / Audit / Implementation Level / Confidence / Evidence
```

### D. State Model

상태 축별로 분리한다. 업무 상태, UI 상태, 파생 상태를 같은 표에 넣지 않는다. 전이는 From, Trigger, Condition, To, Reversible, Evidence로 적는다.

### E. Business Rules

| ID | Rule | Condition | Result | Related Feature | Confidence | Evidence |
| -- | ---- | --------- | ------ | --------------- | ---------- | -------- |

### F. Core Workflows

```text
Entry → Step → Step → Decision ├→ Branch └→ Branch → Outcome
```

### G. Automation

시스템이 자동으로 수행하는 계산, 판단, 추천, 파생 상태.

### H. Cross-Feature Consistency

같은 개념의 정의가 일치하는지, 갈리는 곳은 어디인지.

### I. Audit & Recovery

destructive action별 Confirmation, Reason, Permission, Audit, Undo, Recovery 유무. 변경 종류별 history 수준.

### J. Missing Capabilities & Production Gap

| 항목 | 근거 조건 | 등급 | 관련 Feature | 필요한 것 |
| ---- | --------- | ---- | ------------ | --------- |

운영 전환 항목은 권한, 동시성과 상태 충돌, 임계치, 외부 연동 예외, 감사 이력 순으로 점검한다.

## 후속 보고서

같은 기능을 출시 후 다시 볼 때는 같은 개요와 기능 절을 유지하고, 3절을 성과 지표(이용률, 전환율, 유지율, 오류율)로, 4절을 사용자 피드백(긍정, 부정, 문의)으로 바꾼다. 이 스킬은 출시 후 모드를 실행하지 않는다. 지표와 피드백은 코드에 없으므로 별도 입력이 있을 때만 사람이 채운다.
