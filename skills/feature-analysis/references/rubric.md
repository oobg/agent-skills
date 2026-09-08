# 등급 루브릭

네 축을 따로 매기고, 축 사이 연결 규칙으로 서로를 견제한다. 숫자 가중치는 쓰지 않는다.

## Confidence

| 값 | 기준 |
| --- | --- |
| CONFIRMED | 코드에서 동작을 끝까지 확인했다. handler, mutation, 조건 분기, render 결과가 위치와 함께 있다. |
| PARTIAL | 일부는 구현됐지만 완결되지 않았다. UI와 프론트 mutation은 있으나 persistence, API, 실제 업로드가 없다. |
| INFERRED | 구조, 데이터 형태, 명칭, 주석으로 의도가 강하게 추론되지만 동작을 확인하지 못했다. |
| UNKNOWN | 현재 소스만으로 판단할 수 없다. |

UNKNOWN을 일반 관행으로 채우지 않는다. INFERRED를 CONFIRMED처럼 서술하지 않는다.

증거 유형을 구분한다. 실행해야 확인 가능한 동작(비동기 순서, 타이밍, hover·focus, 렌더 결과, 외부 응답 처리, 반응형)은 정적 증거만으로 CONFIRMED하지 않는다. 정적 증거만 있으면 PARTIAL이고, 런타임 증거는 `runtime:` 접두어로 표시한다.

## Implementation Level

| 값 | 기준 |
| --- | --- |
| L0 Absent | 기능을 확인할 수 없다. |
| L1 Surface | UI만 있다. 도달 경로가 없는 정의도 여기다. |
| L2 Interaction | 프론트 interaction이 있다. 클릭하면 무언가 바뀐다. |
| L3 Domain Logic | state mutation, validation, business rule까지 있다. |
| L4 Persistence | 실제 persistence, API, storage가 연결됐다. |
| L5 Operational | 권한, 감사, 실패 처리, 동시성 같은 운영 요구까지 다뤘다. |

UI가 있다고 L3을 주지 않는다. mock 배열 변경은 persistence가 아니므로 L4를 주지 않는다.

## Priority

| 값 | 기준 | 예 |
| --- | --- | --- |
| P0 Core | 없으면 주요 업무 워크플로우가 완료되지 않는다. | 예약 생성, 상태 변경, 담당자 배정, 주문 확정 |
| P1 Operational | 핵심 업무를 운영 가능하게 한다. | 검색, 필터, 할 일, validation, 이력, 일괄 처리 |
| P2 Supporting | 효율과 사용성을 높인다. | 자동 추천, pin, undo, quick filter, download |
| P3 Presentation | 제품 동작에 거의 영향이 없다. | animation, 장식 아이콘, 서체 변형 |

애매하면 그 Feature를 제거했을 때 주요 워크플로우가 깨지는지 본다. 깨지면 높은 Priority다.

## 누락 등급

누락은 다음 여섯 조건 중 하나를 만족할 때만 기록한다. 일반 제품 관행만으로 누락이라 하지 않는다.

1. 기존 워크플로우가 그 기능 없이 끊긴다.
2. 코드에 그 기능을 전제하는 데이터가 있다.
3. UI에는 있지만 handler가 없다.
4. 상태는 있지만 전이 방법이 없다.
5. mutation은 있지만 persistence가 없다.
6. destructive action인데 보호 장치가 없다.

| 값 | 기준 |
| --- | --- |
| BLOCKING | 워크플로우를 완료할 수 없다. |
| IMPORTANT | 운영상 문제가 발생할 가능성이 높다. |
| OPTIONAL | 효율이나 UX 개선이다. |

## 연결 규칙

- Mutation이 CONFIRMED가 아니면 L3 이상을 주지 않는다.
- Persistence 증거(API 호출, storage 쓰기)가 CONFIRMED가 아니면 L4를 주지 않는다.
- Confidence가 INFERRED 이하인 Feature는 P0으로 확정하지 않는다. P0 후보로 두고 오픈 이슈에 올린다.
- 조건 6의 누락은 P0 또는 P1 Feature에 붙을 때 IMPORTANT 이상이다.
- 검증 노드에서 하나라도 확인되지 않으면 Confidence를 한 단계 낮추고 Level을 다시 매긴다.
- 수집 스크립트가 잡은 항목은 그 자체로 어떤 Confidence도 갖지 않는다. 원본 또는 런타임과 대조한 뒤에 매긴다.

## checker에 넘길 때

checker에게는 이 파일과 리포트를 함께 넘기고 다음을 요구한다.

- 각 판정을 파일과 위치로 재확인하고, 짚을 수 없으면 위반으로 세지 않는다.
- 리포트의 주장과 코드가 다르면 코드를 따른다.
- 못 했다는 판정(누락, UNKNOWN)의 사유가 타당한지도 본다. 찾을 수 있었는데 찾지 않은 것은 결함이다.
