# 입력 게이트와 Inventory

추론 전에 분석 대상을 분류하고, 코드에 실제로 존재하는 것을 수집한다. 이 단계에서는 제품 기능을 해석하지 않는다.

## 1. 입력 형태 판별

| 형태 | 판별 신호 | 분석 경로 | UNKNOWN으로 고정되는 것 |
| --- | --- | --- | --- |
| 원본 코드: 단일 HTML/CSS/JS | 파일 몇 개, 인라인 스크립트, mock 배열 | 정적 수집 + 필요 시 로컬 실행 | persistence, 권한, 동시성 |
| 원본 코드: 프레임워크 프로젝트 | package.json, 라우터, 상태 관리, API 레이어 | 정적 수집 + 로컬 실행 | 서버 측 규칙, 배포 환경 |
| 빌드 결과물 | minify된 코드, 소스맵 없음 | 정적 수집(토큰·문자열) + 런타임 관찰 | 업무 규칙 대부분, 명칭 기반 추론 |
| 배포된 서비스 | URL만 있음 | 런타임 관찰(DOM, 네트워크, 상태 변화) | 소스맵 없는 코드 전부, 서버 규칙 |
| 정적 스냅샷 | 스크린샷·영상만 | Surface와 Action 기록 | Handler 이하 전부 |

형태와 함께 기준을 적는다. 커밋 해시, 파일 해시, URL 중 확인 가능한 것과 분석 시점이다. `scripts/collect_inventory.py`가 파일 대상의 해시, git 커밋, 생성 시각을 메타에 남긴다.

프레임워크 프로젝트는 진입점을 먼저 잡는다. 라우트 정의, 최상위 상태 저장소, API 클라이언트 세 곳을 찾으면 나머지 수집의 시작점이 된다.

## 1-0. 수집 스크립트

기계적으로 수집 가능한 항목은 스크립트로 모은다. 같은 대상에 다시 돌리면 같은 결과가 나와야 하고, 원본은 읽기만 한다.

```bash
python3 scripts/collect_inventory.py <파일 또는 디렉터리> --json <산출물 경로>/inventory.json --md <산출물 경로>/inventory.md
```

수집 항목: 파일 목록과 규모, 라우트 후보, 이벤트 종류, 위임 속성(data-action 등), 상태 후보(전역 상수·store 호출), API와 네트워크 호출, 부작용(storage, navigation, toast, download), 스텁 마커, destructive로 보이는 함수, 상태 리터럴, CSS 토큰. 항목마다 `파일:줄`이 붙는다.

- 산출물은 원본 밖에 쓴다. 스크래치 디렉터리나 지정한 출력 경로만 쓴다.
- 대상에 맞는 패턴이 더 필요하면 스크립트를 확장한다. 수작업 grep을 반복하지 않는다.
- URL은 가져오지 않는다. 배포된 서비스는 런타임 관찰 경로로 간다.
- 수집 결과는 Inventory다. 패턴 매칭은 오탐과 누락이 있으므로 Feature로 올리기 전에 원본이나 런타임과 대조한다. 어느 절이든 0건은 부재의 증거가 아니다.
- 결과 JSON은 결정적인 `meta`와 항목들, 실행 정보인 `run`(경로, git 커밋, 생성 시각)으로 나뉜다. 같은 입력과 같은 수집기 버전이면 `run`을 뺀 나머지가 같다. 이전 분석과 비교할 때는 `run`을 제외하고 diff한다.
- 스크립트가 실패하거나 어떤 파일을 읽지 못하면 그 사실은 커버리지에 적는다. 제품 결함이 아니다.

## 1-2. 정적 증거와 런타임 증거

정적 수집과 코드 읽기로 확인되는 것과 실행해야 확인되는 것을 나눈다.

| 정적으로 확인 가능 | 실행해야 확인 가능 |
| --- | --- |
| handler 존재, 조건 분기, mutation 대상, 상태 enum, 토큰 값 | 비동기 순서와 경합, 타이밍, hover·focus·drag 표현, 실제 렌더 결과, 외부 응답 처리, 반응형 동작 |

실행해야 확인되는 동작은 정적 증거만으로 CONFIRMED하지 않는다. 로컬 실행이나 브라우저 관찰로 확인했으면 Evidence에 `runtime:` 접두어를 붙여 구분한다. 예: `runtime: 390px에서 상태 탭이 컨테이너를 넘침`. 실행하지 않았으면 PARTIAL로 두고 무엇을 실행해야 확인되는지 적는다.

## 1-1. 프로토타입 판정 규칙

시드 데이터, mock 배열, 자리 표시자 주석처럼 프로토타입임을 직접 보여주는 양성 증거가 하나라도 있으면 프로토타입으로 본다. 프로토타입에서는 판정 대상이 달라진다. 이 규칙은 뒤의 모든 노드와 리포트에 적용된다.

증거의 방향을 섞지 않는다.

```text
mock · seed · stub 증거 있음   → 프로토타입 양성 증거
네트워크 호출 · storage 있음    → persistence/연동 증거
네트워크 호출 0건               → 결론 없음
```

수집기의 API 0건은 정적 사이트, storage 기반 앱, 서버 렌더링 결과, 수집기 패턴이 놓친 클라이언트, worker나 iframe 통신, 프론트에 드러나지 않는 BFF에서도 나온다. 0건은 "현재 패턴이 검출하지 못했다"이고 "네트워크 기능이 없다"가 아니다. 영속성 없음은 storage와 네트워크와 서버 렌더 흔적을 모두 찾아본 뒤에만 쓰고, 그 탐색 범위를 함께 적는다.

판정하지 않는 것

- 데이터 값. 시드의 수량, 날짜, 이름, 금액, 표기가 맞는지 보지 않는다. 시드는 Inventory에 규모(레코드 수, 기준일)만 적는다.
- 시드가 노출한 결함을 시드 값으로 서술하는 것. 월 정밀도 비교 같은 규칙 결함은 규칙으로 적고, 어느 레코드가 어떤 값으로 뜨는지는 근거로 쓰지 않는다.
- 스텁과 자리 표시자의 정확도. 주석이나 명칭으로 자리 표시자임이 드러난 함수는 입력, 출력, 남기는 기록만 적고 L2 placeholder로 표시한다. 정규식 추출기의 오독, 가짜 API의 응답 형태를 결함으로 세지 않는다.
- 영속성이 없을 때 의미 없는 것. id 생성 충돌, 메모리 해제, 성능 수치, XSS와 인젝션, 동시성, 경합. 이들은 결함이 아니라 리포트 3절의 운영 전환에 필요한 것으로 옮긴다. 등급을 붙이지 않는다.
- 선언되지 않은 범위. 반응형 뷰포트, 다크 모드, 접근성, 브라우저 호환은 프로토타입이 그 범위를 대상으로 선언했을 때만 판정한다. 선언이 없으면 범위 밖으로 기록만 한다.
- 시각 규칙과 디자인 시스템 대조. 디자인 명세 요청이 있을 때만 한다.

프로토타입에서 유효한 것

- 체인 완결성. 어디까지 동작하고 어디서 끊기는가.
- 상태 전이 일관성. 한 경로에서 바꾼 상태를 다른 경로가 되돌리지 못하거나 잔존시키는가.
- 정의 일관성. 같은 개념이 화면마다 다른 수를 말하는가.
- 규칙의 존재와 적용 범위. 규칙이 있는데 일부 경로가 우회하는가.
- destructive action 보호. 확인, 사유, 이력, 복구.
- 의도와 구현의 어긋남. 주석이나 명칭이 선언한 규칙을 코드가 지키지 않는 곳. 프로토타입에서 가장 값진 발견이므로 따로 모아 적는다.
- 워크플로우 연결과 도달 불가 경로.

결함을 위치순 목록으로 내지 않는다. Feature 단위로 묶고, 위치는 Evidence 열에만 둔다.

## 2. 수집 대상

### Structure

화면, page, section, tab, panel, modal, dialog, drawer, popover, form, list, table, card

### Interaction

button, link, input, select, checkbox, radio, toggle, tab, filter, search, sort, pagination, drag/drop

### Code

event listener와 handler, render 함수, mutation 함수, validation 함수, 계산 함수, filtering/sorting 함수, navigation 함수

### State

전역 상태, 지역 상태, UI state, business state, filter state, selection state

### Data

array, object, mock database, entity, enum, constant, relation

### Side Effect

API 호출, storage, download, upload, navigation, toast, notification, history 기록

## 3. 수집 형식

스크립트 결과를 기본으로 하고, 스크립트가 잡지 못한 항목은 같은 형식으로 손으로 보탠다. 항목마다 위치를 함께 적는다. 위치가 없는 항목은 Inventory에 넣지 않는다.

```text
[Structure] 예약 목록 화면 — pages/reservations.js:12
[Interaction] 예약 취소 버튼 — components/ReservationRow.js:48
[Code] cancelReservation(id) — services/reservation.js:80
[State] reservation.status — store/reservations.js:5 (enum: requested|confirmed|cancelled|completed)
[Side Effect] toast('취소되었습니다') — services/reservation.js:91
```

## 4. 커버리지 기록

Inventory를 닫을 때 다음을 적는다.

- 읽은 파일과 화면 목록
- 건너뛴 파일과 이유 (예: 벤더 코드, 테스트, 스타일 전용)
- 열어 보지 못한 것 (예: 서버 코드 없음, 환경 변수 참조)
- 실행하지 않은 것과 그 이유. 런타임 검증을 하지 않았으면 어떤 항목이 PARTIAL로 남았는지
- 도구와 스크립트의 실패. 읽지 못한 파일, 실행 오류, 타임아웃. 제품 결함 목록에 넣지 않는다.

이 기록은 리포트의 커버리지 절로 그대로 옮긴다. 조사 결과는 본 것만 말하므로, 못 본 범위는 여기서 적지 않으면 어디에도 나타나지 않는다.

## 5. 우선순위

hover, 장식 animation, typography variation 같은 표현 요소는 수집하되 낮은 우선순위로 표시한다. 뒤 노드에서 제품 동작과 연결되지 않으면 P3으로 내려간다.
