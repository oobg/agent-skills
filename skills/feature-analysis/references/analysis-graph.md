# 분석 그래프

Inventory 뒤의 노드들이다. 각 노드는 앞 노드의 결과를 입력으로 쓰고, 모든 판정에 Evidence를 유지한다.

```text
Inventory
  ├── Interaction ── Domain ── State ── Business Rule
  ▼
Feature → Workflow → Verification → Output
```

예시는 예약 관리와 재고·주문 두 도메인을 섞어 쓴다. 분석 대상의 어휘를 예시 어휘로 바꾸지 않는다.

## Interaction Graph

의미 있는 사용자 액션마다 다음 관계를 추적한다.

```text
Trigger → Handler → Validation/Condition → Mutation → Side Effect → Feedback
```

기록 항목: Trigger, Preconditions, Handler, Data read, Data mutation, State transition, Side effect, Feedback, Failure path, Evidence.

```text
예약 취소 버튼
  → cancelReservation(id)
  → status가 confirmed일 때만 허용
  → reservation.status = cancelled
  → history에 cancel 이벤트 추가
  → 목록 갱신 + toast
```

체인이 끊기면 끊긴 지점을 적는다. 끊긴 지점이 Level을 결정한다. hover와 장식 animation은 낮은 우선순위로 둔다.

## Domain Graph

제품 도메인을 구성하는 entity를 찾는다. entity마다 identifier, 주요 속성, mutable field, derived field, relation, lifecycle, 생성·수정·삭제 지점을 적는다.

```text
Order
 ├─ has many → OrderLines
 ├─ belongs to → Customer
 ├─ has many → Shipments
 └─ relates to → InventoryItem (via OrderLine.sku)
```

코드에 없는 DB 스키마를 만들지 않는다. 데이터 형태에서만 관계가 보이면 INFERRED다.

## State Graph

상태 축을 섞지 않는다. 다음은 서로 다른 축이다.

```text
업무 상태   Reservation Status · Order Status · Item Stock Status · Todo Status
UI 상태     기본 · 로딩 · 빈 상태 · 오류 · 성공 후 후속 액션
파생 상태   저장되지 않고 계산되는 값
```

축마다 가능한 값을 모으고 전이를 복원한다. 전이 기록 항목: From, Trigger, Condition, To, Mutation, Side effect, Reversible 여부, Evidence.

```text
requested ─ 담당자 승인 / 잔여 좌석 > 0 ─→ confirmed
confirmed ─ 고객 취소 / 시작 24시간 전 ──→ cancelled (비가역)
```

파생 상태는 따로 표시한다.

```text
order.status = shipped  +  shipment.delivered_at != null  →  화면 표시 "배송 완료"
```

UI 상태 축은 화면마다 다섯 값이 각각 어떻게 렌더되는지, 렌더되지 않는 값은 무엇인지 적는다. 처리되지 않은 UI 상태는 Validation & Edge Cases로 넘긴다.

## Business Rule Graph

조건문, 계산 함수, validation, 주석에서 규칙을 뽑는다. 우선 대상은 자동 분류, 자동 계산, 추천, 중복 검사, 상태 파생, 종료 조건, 필수 입력, 날짜와 금액 계산, 업무량 계산, eligibility, fallback, 관계 일관성이다.

```text
Input/Context → Condition → Rule → Result

신규 예약 전화번호 → 기존 고객과 일치 → 중복 고객 생성 금지 → 기존 고객에 연결
주문 수량        → 재고 수량 초과   → 확정 차단        → 부족 수량 표시
```

규칙은 코드에서 확인된 것만 CONFIRMED다. 주석에만 있는 규칙은 INFERRED다.

## Feature Graph

앞 노드 결과를 사용자 목적 단위로 묶는다. 버튼 단위로 나누지 않는다.

```text
Feature: 예약 담당자 배정
Capabilities: 담당자 조회 · 담당자별 업무량 확인 · 수동 배정 · 저부하 담당자 추천 · 배정 해제 · 변경 이력
Mutation: reservation.owner
Business Rules: 업무량 기반 추천
Side Effects: history 기록 · UI 갱신
```

담당자 selector, owner mutation, workload 계산, 추천, history, toast가 각각 발견되어도 하나의 Feature다.

## Workflow Graph

Feature를 업무 흐름으로 연결한다. Entry, Action, State/Data Change, Decision, Outcome을 갖는다.

```text
예약 요청 접수
 → 담당자 배정
 → 고객 연락
 → 결과 기록
 → ┌ 확정 가능 → confirmed
   ├ 보류      → 추후 연락 Todo 생성
   └ 이탈      → cancelled
```

확인 항목: Entry point, Required feature, Decision point, State transition, Automation, Exit condition, Failure path, Re-entry path.

## Cross-Feature Rules

같은 개념이 여러 화면에서 쓰이면 정의가 같은지 확인한다.

```text
홈의 "미처리 예약"  ── same definition? ── 목록의 "미처리" 필터
```

같은 계산인가, 같은 source of truth인가, 정의가 갈리는가, 상태 불일치 가능성이 있는가를 적는다. UI의 표시·활성 조건과 handler의 실행 조건은 별도 증거로 대조한다. 한쪽 조건을 다른 쪽에도 적용된 것으로 일반화하지 않는다. 일관되게 공유되면 그것도 명시한다.

P0·P1 흐름이나 같은 값이 여러 곳에서 쓰이는 경우에는 쓰기 경로와 읽기 경로를 함께 추적한다.

- 쓰기: 초기 생성, 이후 갱신, fallback, 기존 값 보존
- 읽기: 화면 표시, 상태 계산, 자동 알림·배치·기한 계산 같은 후속 동작

화면 설명과 저장 기준이 다르거나 쓰기 경로마다 기준 값이 다르면 각 경로를 따로 기록하고, 후속 결과가 어느 값을 읽는지까지 연결한다. 모든 필드를 전수 조사하지 않고 복수 쓰기나 정의 충돌 신호가 있는 값에 집중한다.

## Destructive Action

삭제, 종료, 취소, 관계 해제, 담당 해제, 데이터 초기화는 따로 추적한다. 각 액션에서 Confirmation, Reason required, Permission, Audit trail, Undo, Recovery, Related-data impact를 확인한다. 구현되지 않은 보호 장치를 구현된 것처럼 쓰지 않는다.

## Auditability

업무 데이터 변경에 history가 남는지 본다. 상태 변경, 담당자 변경, 단계 변경, 계약, 관계 연결·해제, Todo 완료·취소, 기록 삭제, 종료를 추적하고 세 수준으로 나눈다.

```text
현재 값만 변경
현재 값 + history
현재 값 + history + undo
```

## Verification

P0과 P1 Feature마다 여덟 질문에 답한다.

1. UI 또는 Trigger가 실제 있는가
2. Handler를 확인했는가
3. Mutation을 확인했는가
4. Business Rule이 해당 폼·액션의 호출 경로에 있는가
5. Side Effect를 확인했는가
6. 다른 Feature와 중복 정의하지 않았는가
7. Workflow에 실제 연결되는가
8. 추론을 사실처럼 쓰지 않았는가

하나라도 아니면 Confidence를 낮추고 rubric의 연결 규칙으로 Level과 Priority를 다시 매긴다.
