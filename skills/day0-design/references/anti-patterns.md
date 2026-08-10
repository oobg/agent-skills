# Day0 안티패턴 (하지 말 것)

게이트에서 막는다. 발견 시 토큰·patterns로 되돌린다.

## 브랜드 / 토큰

| 금지 | 대신 |
| --- | --- |
| `#3182f6`, `#1b64da` (구 토스 블루) | `--d0-blue` `#3d7de5` |
| DESIGN-REFRESH §2 구 토큰·radius 16/12·옛 grey | live / 스킬 tokens.css (14/10/8) |
| hex 하드코딩 남발 | semantic 토큰 |
| 카드 glow·두꺼운 컬러 shadow | 보더리스 plain 또는 outlined 1px + shadow-card 흔적 |
| Inter / Roboto / system만 | Pretendard Variable |
| 그라데이션 타이틀·glassmorphism 남용 | solid surface; blur는 TopBar 정도 |
| 임의 다크 테마 발명 | light-only |

## 레이아웃 / 컴포넌트

| 금지 | 대신 |
| --- | --- |
| 리스트 항목마다 개별 Card | 행 + 디바이더 / plain·soft 래퍼 |
| 온보딩·밀도 화면을 전부 outlined 카드로 | **plain 기본**, outlined는 예외 |
| 신규 주 job에 primary fill 2개+ | primary 1 (기존 다동선 화면 전면 리팩터 금지) |
| 선택 카드 전원 두꺼운 블루 보더 | 체크 / soft bg |
| disabled primary를 “활성처럼” 연한 블루 fill로 위장 | grey+opacity 또는 live Button opacity |
| pill을 일반 버튼·카드에 남용 | badge·dot·toggle·progress 등 허용 범위 안 |
| 본문·온보딩 한글 라벨 uppercase + 넓은 자간 | 11–13px, tracking 토큰 |
| **관리자 compact th uppercase를 지우는 것** | table-compact 헤더는 **의도된** uppercase |
| 작업 화면 히어로 일러스트 | 전환점만 |
| hover lift y −4px+ / 과장 scale | ≤1px, 일반 0.97–1 |
| styles.css / index 미등록 신규 컴포넌트 | 3단 등록 |
| BottomCTA를 “상단 보더만”으로 대충 | live 그라데이션 페이드 + safe-area |

## 상태 / 코드

| 금지 | 대신 |
| --- | --- |
| className 삼항으로 색·상태 스택 | `data-*` + CSS |
| `outline: none`만 | focus-visible soft blue ring |
| Tailwind 유틸 화면 | 토큰 CSS / CSS Modules |
| 스펙 원문 카피 임의 윤문 | 구조만; 문구는 ux-writing |
| 삭제된 자동 설치 시뮬레이션 UI 복원 | terminal/guided 현 플로우 |

## 슬롭 형식 신호

- 앱 화면의 큰 그라데이션 hero + EYEBROW + 60ch 부제  
- 균일 아이콘 카드 그리드 + 가짜 지표  
- 전부 Bold 700  
- `#0000FF` / indigo / rounded-full 버튼  
- 의미 없는 confetti 루프 (완료 축하 제외)  
- generic empty ("No data yet") 반복  

**오탐 가드 (지우지 말 것)**

- `~해요` 상태 서술 톤  
- IconCircle + 의미 있는 이모지  
- 랜딩 **PC 가로 타임라인** (의도된 레이아웃)  
- 관리자 compact 테이블 uppercase 헤더  

## 빠른 시각 검사 (30초)

1. 회색뿐이면 실패 → 블루 포인트  
2. 전부 떠 보이는 보더 카드 스택이면 실패 → 보더리스/행 구조  
3. 알약 버튼 남용이면 실패  
4. 같은 위계 primary 난립이면 실패 (신규)  
5. 리스트가 카드 스택이면 실패  

## 진단만 모드

사용자가 수정 없이 슬롭/안티패턴 검사만 요청하면 구현하지 않는다.  
이 파일 + 출력 게이트로 PASS/주의 목록만 보고한다.  
(별도 `design-slop-audit` 스킬이 워크스페이스에 없으면 여기로 끝낸다.)
