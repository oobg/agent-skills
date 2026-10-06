# 공용 블록

블록을 쓸지는 자유다. 쓰면 해당 파일의 해부 구조와 스니펫을 따른다. 일관성은 블록
모양에서 오고, 자유는 어떤 블록을 고르느냐에서 온다. 이 표로 고른 뒤 쓸 블록 파일만 연다.

공통 규칙:

- 페이지는 [shell.md](blocks/shell.md)에서 시작한다. day0-design의 `tokens.css` 전체를 수정 없이
  메인 `<style>` 맨 앞에 인라인하고(폰트 `@font-face` `<style>`은 그 앞 별도 요소), day0-design 위치는 SKILL.md의 탐색 순서를 따른다. 토큰을 외부 `<link>`로 걸지 않는다.
- 색·radius·그림자·모션·자간·행간·글꼴은 `var(--d0-*)`만 쓴다. tokens.css에 없는 이름을 만들지 않는다(표면 `#fff`만 예외).
  tokens.css에 없는 간격·폭·제목 크기는 shell.md의 타이포·여백 스케일을 px로 쓴다.
- **그림이 주인공이다.** 그림 블록은 diagram, thumb-cards, tab-preview, mockup-frame, timeline, kpi-cards 막대 변형
  (`data-variant="bar"`)이다. 막대 없는 kpi-cards는 그림이 아니다. 앞쪽 핵심 섹션(header 다음 첫 1~2개 페이지 섹션,
  `main > section`·`main > .d0-split > section`)은 그림 블록을 먼저 고르고, 위험·한계·할 일 같은 목록 섹션은 그림 없이
  글 블록(diff-rows, checklist, accordion)만 써도 된다. 블록 안 `section`(mockup-frame `.d0-app__body` 등)은 페이지 섹션이 아니다.
  글 블록(step-columns, diff-rows, accordion)은 그림을 거들거나 목록을 담는 데만 쓴다.
- 그림은 컨테이너 폭을 채우거나 옆에 짧은 설명을 붙인다. 폭 절반만 쓰고 옆을 비우지 않는다.
- **그림 무대.** 도식 `figure`의 SVG는 `data-stage` 패널(grey-50 배경, radius card, 패딩 28 / 모바일 20) 위에 놓고,
  figcaption은 패널 밖 아래에 둔다. 값은 SKILL.md 원칙 9번, 스니펫은 [diagram.md](blocks/diagram.md).
- **한 사실은 한 번.** 결론 수치는 [hero.md](blocks/hero.md) 한 곳에 두고 요약 행·섹션 제목·KPI·callout에서 되풀이하지 않는다
  (같은 숫자 문자열 페이지당 2회 이하, SKILL.md 원칙 8번).
- **여백 리듬.** 섹션 사이 64px(모바일 48), 블록 간 24px, 제목↔설명 8px. 디바이더는 섹션 경계 1px grey-100과
  행 목록의 행 구분선만. 블록 안 테두리는 두르지 않는다. 값의 CSS는 [shell.md](blocks/shell.md).
- **줄 길이.** 본문 한 줄이 약 50자를 넘으면 `p`가 아니라 블록 레이아웃(2열 grid, 그림 옆 배치)으로 줄인다.
- **두 섹션 나란히.** 프리셋이 허용하면 [shell.md](blocks/shell.md)의 `.d0-split` 레이아웃을 쓴다.
  한쪽 높이가 다른 쪽의 1.5배를 넘으면 나란히 두지 않는다([shell.md](blocks/shell.md) 높이 기준).
- 상태는 `data-*` 속성으로 표현한다(`data-status`, `data-current`, `data-open`, `data-variant`, `data-selected`).
- Card 기본은 plain이다. 리스트는 카드 스택 대신 행 + 1px 디바이더로 나눈다. pill은 배지·탭·토글에만.
- **색은 섞는다.** Day0 6:3:1, 첫 화면 진한 포인트(채움·선) 1.2% 이상·전체(옅은 면 포함) 3~15%, 넓은 blue-light 무대로 전체만 채우지 않기, 회색만 있는 도식·카드 묶음 금지. blue 단계(blue·blue-dark·blue-light)와
  의미색 2가지까지(green·orange·red, 면·점·선·배지 배경만, 글자 색 금지). 배지는 카드·행마다 1개, 톤 종류 3가지 이하. 정본은 [shell.md](blocks/shell.md) 색 절.
- **배지 높이 고정.** 모든 배지(`.d0-pill`)는 높이 22px(작은 변형 20px), 12px 글자, `flex: none`,
  `align-self: flex-start`, `justify-self: start`. grid·flex 행 안에서 늘어나지 않는다. 행 안 배지는 제목 첫 줄에 맞춘다
  (`align-items: start` + 배지 `margin-top`). 버튼·탭으로 쓰는 pill만 포인터 하한 때문에 32px.
- 배지 색: 글자는 grey-900(시맨틱 톤) 또는 blue-dark(블루 톤), 배경은 해당 `-bg`/`-light`, 시맨틱 톤은 앞에 8px 의미색 점.
  대비 계산표는 shell.md 색 절에 있다. 회색 배지만 늘어놓지 않는다.
- 블록 안 설명 문단은 부모 폭을 그대로 쓴다. 좁히려면 블록 컨테이너를 좁힌다(SKILL.md 개행 규칙).
- **시맨틱 태그.** 구조(`section`·`header`·`figure`·`ol`/`ul`·`dl`·`table`·`time`·`data`·`progress`·`details`·`dialog`·
  `button`/`a`)는 아래 표의 태그로 짓는다. 시맨틱 구조 안의 스타일 훅용 `span`·`div`(배지 `span`, 라벨 `span`)는
  허용하고, 빈 간격용 요소는 금지다. 동작은 `button`, 이동은 `a`로 가른다.
  ARIA는 네이티브 요소로 안 될 때(탭 등)만 쓰고, 네이티브와 겹치는 role(`<nav role="navigation">`)은 금지다.
  헤딩은 h1→h2→h3 순서로 건너뛰지 않고, `main`은 페이지에 하나다.

  | 의미 | 태그 |
  | --- | --- |
  | 페이지 머리·본문·꼬리 | `header` · `main`(1개) · `footer` |
  | 구획 | `section aria-labelledby`(h2 id), 섹션 머리는 섹션 안 `header` |
  | 독립 카드·시안 | `article` |
  | 보조·결정 요청 | `aside` |
  | 섹션 사이 이동 목차·흐름 | `nav aria-label` + `ol` + `a` |
  | 도식·목업·표 + 설명 한 줄 | `figure` + `figcaption` |
  | 순서 있는 단계·흐름 / 순서 없는 목록 | `ol` / `ul` |
  | 라벨-값(요약 행, 키-값, 용어) | `dl`·`dt`·`dd` |
  | 표 | `table` + `caption` + `thead`/`tbody`/`tfoot`(합계 행) + `th scope` |
  | 날짜·기간·소요 시간 | `time datetime`(`2026-03-06`, `PT3M`, `P30D`) |
  | 수치·진행률·비율 | `data value` · `progress` · `meter` |
  | 바뀐 값 전/후, 강조 변경 | `del`/`ins`, `mark` |
  | 약어 | `abbr title` |
  | 펼침(아코디언) | `details`/`summary`(JS 없이, 첫 항목 `open`) |
  | 동작 결과 알림 | `output` 또는 `role="status"` |

- 클래스 프리픽스는 `d0-`. 인터랙션은 실제 `<button>`·`<input>`과 aria 속성, 짧은 바닐라 JS로.
- 접근성 하한은 WCAG 2.2 AA다. 글자는 `--d0-blue-dark`·`--d0-grey-600` 이상(4.5:1, `--d0-grey-100`·`--d0-blue-light` 배경 위는 `--d0-grey-700` 이상), 상태는 색과 함께 글자나 모양으로, 클릭 대상은 24px 이상.
- 예시 텍스트는 합성 값만 쓴다(`주문 내보내기`, `팀 A`, 주제 분류어 `알림 개편`. 티켓 번호는 실제로 있을 때만).

| 블록 | 언제 쓰나 | 생김새 | 파일 |
| --- | --- | --- | --- |
| shell | 모든 페이지의 골격 | 폰트 + 토큰 + 컨테이너 + 타이포·여백 스케일 + 배지 + 나란히 두 섹션 `.d0-split` | [shell.md](blocks/shell.md) |
| header | 모든 페이지 첫 블록(필수) | 작업 라벨 → h1 → (히어로) → 리드(문장형 또는 요약 행) | [header.md](blocks/header.md) |
| hero | report·compare 전/후·incident의 결론 수치 1개(수치 없으면 생략) | h1 바로 아래: 전 값(작게) → 후 값 44px/600 + 단위 + 한 줄 뜻 | [hero.md](blocks/hero.md) |
| section-head | 구획마다 | 위 구분선 + h2 20px + 설명 최대 1문장(제목과 같으면 생략), 태그는 기본 없음 | [section-head.md](blocks/section-head.md) |
| diagram | **그림(필수 1개 이상)** | `data-stage` 패널 위 SVG: 연결 그래프·전/후 막대(비율 `data-variant="ratio"`, 전체 폭 `data-size="wide"`)·미니 격자·화면 와이어프레임 | [diagram.md](blocks/diagram.md) |
| thumb-cards | 무엇이 몇 개, 각각 어떤 모양 | 3~5장, 미니 격자·와이어프레임 SVG + 이름 + 배지 | [thumb-cards.md](blocks/thumb-cards.md) |
| mockup-frame | 결과 화면을 직접 눌러 봄 | 고정 높이 프레임 안 미니 앱: 상단 바·고스트 카드·모달/시트·토스트 | [mockup-frame.md](blocks/mockup-frame.md) |
| tab-preview | 결과물(파일·표) 모양 | pill 탭 → 파일명 바 → 표 목업 | [tab-preview.md](blocks/tab-preview.md) |
| timeline | 날짜가 있는 순서 | 점 + 날짜 + 제목 + 상태, 오늘 표식 | [timeline.md](blocks/timeline.md) |
| kpi-cards | 근거 숫자(막대 변형은 그림) | 라벨 + 큰 숫자 + 막대(`전` 행에만 값, `후` 행은 라벨만, 큰 숫자가 후 값), 증감 배지·문단 없음, 막대 변형 `data-variant="bar"` | [kpi-cards.md](blocks/kpi-cards.md) |
| flow-line | 그림 위 흐름 한 줄(글) | `A → B → C`, 현재만 블루. 단독으로 그림이 아니다 | [flow-line.md](blocks/flow-line.md) |
| step-columns | 그림 아래 단계 주석 | 2~4열, 블루 단계 라벨 → 소제목 → 짧은 항목 | [step-columns.md](blocks/step-columns.md) |
| side-by-side | 옵션 비교 | 같은 크기 2~3열, 장점·비용·위험 또는 작은 mock | [side-by-side.md](blocks/side-by-side.md) |
| diff-rows | 바뀐 점만, 한계 목록 | 항목 \| 전 \| → \| 후(블루), 배지 행 변형 | [diff-rows.md](blocks/diff-rows.md) |
| checklist | 직접 따라 하기·할 일 | 진행률 + 체크 행, 할 일은 담당 변형 `data-variant="owner"`(행 끝 칸 없음 `data-meta="none"`) | [checklist.md](blocks/checklist.md) |
| accordion | 질문·용어 | 질문 행 펼침, 용어 카드 변형 | [accordion.md](blocks/accordion.md) |
| callout | 결정 요청 하나 | soft 블루 상자, **페이지당 최대 1개**, 히어로 결론을 되풀이하지 않음 | [callout.md](blocks/callout.md) |
