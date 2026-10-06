# 공용 블록

블록을 쓸지는 자유다. 쓰면 해당 파일의 해부 구조와 스니펫을 따른다. 일관성은 블록
모양에서 오고, 자유는 어떤 블록을 고르느냐에서 온다. 이 표로 고른 뒤 쓸 블록 파일만 연다.

공통 규칙:

- 페이지는 [shell.md](blocks/shell.md)에서 시작한다. day0-design의 `tokens.css` 전체를 수정 없이
  `<style>` 맨 앞에 인라인하고, day0-design 위치는 SKILL.md의 탐색 순서를 따른다. 토큰을 외부 `<link>`로 걸지 않는다.
- 색·radius·그림자·모션·자간·행간·글꼴은 `var(--d0-*)`만 쓴다. tokens.css에 없는 이름을 만들지 않는다.
  tokens.css에 없는 간격·폭·제목 크기는 day0-design의 레이아웃·타이포 수치를 px로 쓴다.
- 상태는 `data-*` 속성으로 표현한다(`data-status`, `data-current`, `data-open`, `data-variant`, `data-selected`).
- Card 기본은 plain이다. 리스트는 카드 스택 대신 행 + 1px 디바이더로 나눈다. pill은 배지·탭·토글에만.
- 블록 안 설명 문단은 부모 폭을 그대로 쓴다. 좁히려면 블록 컨테이너를 좁힌다(SKILL.md 개행 규칙).
- 클래스 프리픽스는 `d0-`. 인터랙션은 실제 `<button>`·`<input>`과 aria 속성, 짧은 바닐라 JS로.
- 접근성 하한은 WCAG 2.2 AA다. 글자는 `--d0-blue-dark`·`--d0-grey-600` 이상(4.5:1, `--d0-grey-100`·`--d0-blue-light` 배경 위는 `--d0-grey-700` 이상), 상태는 색과 함께 글자나 모양으로, 클릭 대상은 24px 이상.
- 예시 텍스트는 합성 값만 쓴다(`주문 내보내기`, `팀 A`, `작업-000`).

| 블록 | 언제 쓰나 | 생김새 | 파일 |
| --- | --- | --- | --- |
| shell | 모든 페이지의 골격 | 폰트 + 토큰 + 컨테이너 + 공용 pill | [shell.md](blocks/shell.md) |
| header | 모든 페이지 첫 블록(필수) | 작업 라벨 → h1 → 리드 → 구분선 | [header.md](blocks/header.md) |
| section-head | 구획마다 | h2 + 회색 태그 + 설명 한 줄 | [section-head.md](blocks/section-head.md) |
| flow-line | 전체 흐름 한눈에 | `A → B → C`, 현재만 블루 | [flow-line.md](blocks/flow-line.md) |
| thumb-cards | 무엇이 몇 개 있나 | 3~5장, SVG 도식 + 이름 + 상태 배지 | [thumb-cards.md](blocks/thumb-cards.md) |
| kpi-cards | 근거 숫자 | 큰 숫자 + 증감 + 한 줄 뜻 | [kpi-cards.md](blocks/kpi-cards.md) |
| diagram | 순서·구조 그림 | 번호 상자 3~5 + SVG 화살표, 흐름형·레이어형 | [diagram.md](blocks/diagram.md) |
| step-columns | 단계별 누가·무엇 | 2~4열, 단계 라벨 → 소제목 → 항목 쌍 | [step-columns.md](blocks/step-columns.md) |
| side-by-side | 시안·옵션 비교 | 같은 크기 2~3열, 미니 프로토타입 또는 장점·비용·위험 | [side-by-side.md](blocks/side-by-side.md) |
| diff-rows | 바뀐 점만 | 항목 \| 전 \| → \| 후(블루) | [diff-rows.md](blocks/diff-rows.md) |
| tab-preview | 결과물 모양 | pill 탭 → 파일명 바 → 표 목업 | [tab-preview.md](blocks/tab-preview.md) |
| timeline | 날짜가 있는 순서 | 점 + 날짜 + 제목 + 상태, 오늘 표식 | [timeline.md](blocks/timeline.md) |
| checklist | 직접 따라 하기 | 진행률 + 체크 행 | [checklist.md](blocks/checklist.md) |
| accordion | 질문·용어 | 질문 행 펼침, 용어 카드 변형 | [accordion.md](blocks/accordion.md) |
| callout | 결론·결정 요청·다음 할 일 | soft 블루 상자, 페이지당 2개 이내 | [callout.md](blocks/callout.md) |
