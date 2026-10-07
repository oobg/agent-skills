# 공용 블록

블록을 쓸지는 자유다. 쓰면 해당 파일의 해부 구조와 스니펫을 따른다. 일관성은 블록
모양에서 오고, 자유는 어떤 블록을 고르느냐에서 온다. 이 표로 고른 뒤 쓸 블록 파일만 연다.

## 용어 계층 (개념 계층, 작업 순서 아님)

| 층 | 뜻 | 어디 |
| --- | --- | --- |
| Principle | 변하지 않는 원칙 | SKILL.md ELI5 원칙 |
| Pattern | 정보를 설명하는 방식(compare·flow·preview·report·guide·timeline·incident·faq) | [patterns/](patterns/compare.md) |
| Block | 공용 부품(explanation·evidence·checkpoint·…) | 이 파일 |
| Layout | 배치 = 구도 | [composition.md](composition.md) |
| Recipe | 목적별 Pattern + Block 조합(선택 출발점) | [recipes.md](recipes.md) |
| Output | page · deck | SKILL.md 출력 형식 판별, [output/deck.md](output/deck.md) |

Pattern은 어떻게 설명할지, Block은 무엇으로 표현할지, Layout은 어디에 놓을지, Recipe는 무엇을 함께 쓰면 좋은지를 정한다.

**블록은 패턴이 소유하지 않는다.** 패턴 문서의 블록 목록은 "추천 블록"일 뿐이고, 어느 패턴에서나 아래 모든 블록을 빌려 쓴다. page와 deck도 같은 블록을 쓰고 밀도 규칙만 다르다.

## 공용 정보 블록

어느 패턴·출력에서나 자주 빌려 쓰는 의미 단위 블록이다. 먼저 이 묶음으로 표현할 수 있는지 본다.

| 블록 | 답하는 것 | 파일 |
| --- | --- | --- |
| explanation | 배경·이유·뜻·영향·조건·예외(라벨 + 1~3문장) | [explanation.md](blocks/explanation.md) |
| evidence | 주장 + 근거(숫자·출처·전/후·예시) | [evidence.md](blocks/evidence.md) |
| before-after | 같은 대상의 전과 후(문제→수정, 기존→개선, 예상→실제) | [before-after.md](blocks/before-after.md) |
| checkpoint | 여기까지 하면 무엇이 완성되나 | [checkpoint.md](blocks/checkpoint.md) |
| status rail | 지금 어디에 있나(완료·진행·예정) | [timeline.md](blocks/timeline.md) status rail 절 |
| question-answer | 독자가 실제로 가질 질문과 답 | [faq.md](blocks/faq.md) |
| closing | 남길 일 하나(결정·요청·행동·기준·지킬 것) + 메타 행 | [closing.md](blocks/closing.md) |

## 블록 추가 판별

기존 공용 블록으로 표현할 수 있으면 새 블록을 만들지 않는다. 새로 필요해 보이면 이 순서로 가른다.

| 새로 필요한 것 | 어디에 더하나 |
| --- | --- |
| 새 모양 | 기존 블록의 `data-variant` |
| 기존 블록에 클래스 하나(도식 표식, 상태 하나) | 새 블록이 아니라 variant 범주다. 그 블록 파일의 공용 CSS에 토큰만 쓰는 클래스로 더한다(예: [diagram.md](blocks/diagram.md) 흔한 표식 표) |
| 새 배치 | Layout(구도, [composition.md](composition.md)) |
| 새 조합 | Recipe([recipes.md](recipes.md)) |
| 새 의미 구조가 둘 이상 패턴에서 반복해 필요 | 그때만 새 공용 블록 |

## 공통 규칙

- 페이지는 [shell.md](blocks/shell.md)에서 시작한다. day0-design의 `tokens.css` 전체를 수정 없이
  메인 `<style>` 맨 앞에 인라인하고(폰트 `@font-face` `<style>`은 그 앞 별도 요소), day0-design 위치는 SKILL.md의 탐색 순서를 따른다. 토큰을 외부 `<link>`로 걸지 않는다.
- 색·radius·그림자·모션·자간·행간·글꼴은 `var(--d0-*)`만 쓴다. tokens.css에 없는 이름을 만들지 않는다(표면 `#fff`만 예외).
  글(본문) 행간의 예외는 설명 문단(`p`, explanation `dd`)의 1.65다([shell.md](blocks/shell.md) 행간 예외).
  tokens.css에 없는 간격·폭·제목 크기는 shell.md의 타이포·여백 스케일을 px로 쓴다.
- **그림이 주인공이다.** 그림 블록은 diagram(핀 오버레이 `pins` 포함), thumb-cards, tab-preview, mockup-frame, timeline의 SVG 시간 막대(`data-variant="timebar"`),
  kpi-cards 막대 변형(`data-variant="bar"`), side-by-side 와이어 카드(`.d0-option__wire`), step-columns 그림 변형(`data-variant="figure"`),
  checklist 연동 그림 변형(`data-variant="linked"`, 무대 SVG를 diagram으로 센다), evidence 근거 변형 중 metric-list(작은 차트)·bar-list다.
  evidence tiles는 막대 없는 kpi-cards처럼 그림이 아니다.
  막대 없는 kpi-cards, CSS 타임라인(가로·세로), status rail, code-block은 그림이 아니다. 첫 화면 섹션(header 다음 첫 페이지 섹션)은 그림 블록을 먼저 고르고,
  그 아래 섹션은 핵심 구조가 있으면 그림을 권장한다. 그림 없는 섹션은 구조 블록(explanation, evidence, before-after, checkpoint, question-answer, diff-rows, checklist, step-columns, accordion, 표)으로 짓고
  연속된 일반 문단만으로 채우지 않는다(정본: SKILL.md 원칙 4번). 블록 안 `section`(mockup-frame `.d0-app__body` 등)은 페이지 섹션이 아니다.
  글 블록은 그림이 이미 보여 준 모양을 되풀이하지 않고 이유·근거·조건을 더한다.
- **본문 축.** 섹션은 모두 본문 축(720px, narrow 640px)의 같은 왼쪽 시작선을 쓴다. 그림은 축 폭의 75~100%를 채우고(단순 도식만 `data-fit="compact"`), 옆에 남는 폭은 채우지 않는다. 설명은 그림 아래에 둔다. 정본은 [shell.md](blocks/shell.md) 본문 축 절.
- **그림 무대.** 회색 무대는 기본 없음이다. 필요할 때만 도식 `figure.d0-fig[data-stage]`의 SVG를 `div.d0-fig__stage` 패널(grey-50 배경, radius card, 패딩 28 / 모바일 20) 위에 놓고,
  figcaption은 패널 밖 아래에 둔다. 쓰는 기준은 [composition.md](composition.md), 값은 SKILL.md 원칙 9번, 스니펫은 [diagram.md](blocks/diagram.md).
- **구도와 강조.** 섹션·슬라이드의 구도(`data-composition`), 강조 3단계(`data-emphasis="quiet|impact"`), 밀도 리듬, 강조 순서(크기 → 위치 → 여백 → 무게 → 색)는
  [composition.md](composition.md)가 정본이다. 블록 고르기 전에 섹션마다 구도를 먼저 정한다.
- **한 사실은 한 번.** 결론 수치는 [hero.md](blocks/hero.md) 한 곳에 두고 요약 행·섹션 제목·KPI·callout에서 되풀이하지 않는다
  (같은 숫자 문자열 페이지당 2회 이하, SKILL.md 원칙 8번).
- **여백 리듬.** 섹션 사이 64px(모바일 48), 블록 간 24px, 제목↔설명 8px. 디바이더는 섹션 경계 1px grey-100과
  행 목록의 행 구분선만(closing 문장 아래·checkpoint 뒤 grey-200 한 줄은 블록 부품 예외, [shell.md](blocks/shell.md) 금지 절). 블록 안 테두리는 두르지 않는다. 값의 CSS는 [shell.md](blocks/shell.md).
- **줄 길이.** 본문 한 줄의 길이는 축이 정한다. 글 블록은 축(또는 놓인 열) 폭을 그대로 쓰고 따로 폭 상한을 두지 않는다(`code`·`pre`·명령어 줄·[code-block](blocks/code-block.md)은 규칙 밖). 줄을 줄이려면 페이지 전체를 `data-width="narrow"`로 둔다. 정본은 [shell.md](blocks/shell.md) 줄 길이 절이다.
- **2열은 세 경우만.** 동시 비교(A안 | B안, 전 | 후), 그림 지점과 번호로 대응하는 주석·범례, 대등한 두 덩어리(완료 | 남은 것)일 때만 `.d0-wide` 구간 안 `.d0-cols`로 쓴다.
  분할선은 문서 전체에서 하나(6/6 또는 7/5)다. 섹션은 나란히 두지 않고 축을 따라 쌓는다. 정본은 [shell.md](blocks/shell.md) 2열 절.
- **섹션 뼈대.** 제목(h2) → 그림 → 해석 한 줄 → 필요할 때만 "왜" 한 줄. 흐름을 끊는 세부는 `.d0-more` 접기로, 페이지 끝 기억할 사실 한 문장은 `.d0-keep`(선택)으로 둔다.
- 상태는 `data-*` 속성으로 표현한다(`data-status`, `data-current`, `data-open`, `data-variant`, `data-selected`).
- Card 기본은 plain이다. 리스트는 카드 스택 대신 행 + 1px 디바이더로 나눈다. pill은 배지·탭·토글에만.
- **색은 섞는다.** Day0 6:3:1, 첫 화면 진한 포인트 채움 면적은 1% 미만·15% 초과일 때만 경고(Warning, [shell.md](blocks/shell.md) 색 절), 넓은 blue-light 무대로 전체만 채우지 않기, 회색만 있는 도식·카드 묶음 금지. blue 단계(blue·blue-dark·blue-light)와
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

## 블록 표

| 블록 | 언제 쓰나 | 생김새 | 파일 |
| --- | --- | --- | --- |
| shell | 모든 페이지의 골격 | 폰트 + 토큰 + 본문 축(720px, narrow 640px) + 넓은 구간 `.d0-wide` + 2열 `.d0-cols`(6/6·7/5, 문서에 하나) + 섹션 뼈대 + 접기 `details.d0-more` + 기억할 한 줄 `aside.d0-keep` + 타이포·여백 스케일 + 배지 | [shell.md](blocks/shell.md) |
| header | 모든 페이지 첫 블록(필수) | 작업 라벨 → h1 → (히어로) → 리드(문장형 또는 요약 행) | [header.md](blocks/header.md) |
| hero | report·compare 전/후·incident의 결론 수치 1개(수치 없으면 생략) | h1 바로 아래: 전 값(작게) → 후 값 44px/600 + 단위 + 한 줄 뜻 | [hero.md](blocks/hero.md) |
| section-head | 구획마다 | 위 구분선 + h2 20px + 설명 최대 1문장(제목과 같으면 생략), 태그는 기본 없음 | [section-head.md](blocks/section-head.md) |
| diagram | **그림(필수 1개 이상)** | 축 폭을 채우는 SVG(글자 있으면 viewBox 폭 560, 단순 도식은 `data-fit="compact"`, 무대는 글자 없는 그림에만): 연결 그래프·전/후 막대(비율 `data-variant="ratio"`)·미니 격자·화면 와이어프레임·번호 핀 오버레이 `data-variant="pins"`(preview 해부도, faq 용어 핀). 장르 `data-genre`(`structural`·`narrative`·`editorial`, 생략=structural, editorial은 선 거의 없이 숫자·문구·객체 하나를 크게). 모으기 (h) converge(문제 여럿 → 해결 하나 곡선), 번호 주석 (i) `data-variant="annotate"`(기존 그림 위 번호 2~4개 + 한 줄 주석 `ol.d0-annot__notes`, page·deck 공용) | [diagram.md](blocks/diagram.md) |
| thumb-cards | 무엇이 몇 개, 각각 어떤 모양 | 3~5장, 미니 격자·와이어프레임 SVG + 이름 + 배지 | [thumb-cards.md](blocks/thumb-cards.md) |
| mockup-frame | 결과 화면을 직접 눌러 봄 | 고정 높이 프레임 안 미니 앱: 상단 바·고스트 카드·모달/시트·토스트. 별도 페이지는 `srcdoc` 내장(`src` 금지), 여러 페이지는 `data-variant="gallery"`(뷰포트 높이 노트북 창 + 탭), 기기 프레임 `data-device="desktop|mobile"`(PC 화면은 노트북 창, 모바일 화면은 375px 폰, 둘 다면 PC/모바일 토글). 화면 캡처 spotlight `figure.d0-shot`(화면 + `.d0-shot__spot` 위치 표시 + 바깥 흐림 + 번호 주석 `.d0-shot__note`, deck의 `screenshot` 슬라이드) | [mockup-frame.md](blocks/mockup-frame.md) |
| tab-preview | 결과물(파일·표) 모양 | pill 탭 → 파일명 바 → 표 목업 | [tab-preview.md](blocks/tab-preview.md) |
| timeline | 날짜가 있는 순서, 지금 위치 | 점 + 날짜 + 제목 + 상태, 오늘 표식(CSS, 그림 아님). SVG 시간 막대 `data-variant="timebar"`는 그림. 공용 status rail `ol.d0-rail`(지금 어디, 그림 아님) | [timeline.md](blocks/timeline.md) |
| kpi-cards | 근거 숫자(막대 변형은 그림) | 라벨 + 큰 숫자 + 막대(`전` 행에만 값, `후` 행은 라벨만, 큰 숫자가 후 값), 증감 배지·문단 없음, 막대 변형 `data-variant="bar"` | [kpi-cards.md](blocks/kpi-cards.md) |
| flow-line | 그림 위 흐름 한 줄(글) | `A → B → C`, 현재만 블루. 단독으로 그림이 아니다 | [flow-line.md](blocks/flow-line.md) |
| step-columns | 그림 아래 단계 주석 | 2~5열, 블루 단계 라벨 → 소제목 → 짧은 항목. 그림+설명 변형 `data-variant="figure"`는 그림 | [step-columns.md](blocks/step-columns.md) |
| side-by-side | 옵션 비교 | 같은 크기 2~3열, 장점·비용·위험 또는 작은 mock, 와이어 카드 `.d0-option__wire`(수치 없는 결정의 대표 도식). 기본은 카드 없는 split-plain, 독립된 선택지 2~3개는 `data-layout="card"`(split-card) | [side-by-side.md](blocks/side-by-side.md) |
| diff-rows | 바뀐 점만, 한계 목록 | 항목 \| 전 \| → \| 후(블루), 배지 행 변형, 위험 행 변형 `data-variant="risk"`(배지 + 위험 한 문장 + dl 영향/대응) | [diff-rows.md](blocks/diff-rows.md) |
| checklist | 직접 따라 하기·할 일 | 진행률 + 체크 행, 긴 따라하기는 구간(`data-phased`: 맨 위 전체 진행률 + 구간 머리 행이 지도와 결과, 현재 구간만 펼침), 할 일은 담당 변형 `data-variant="owner"`(행 끝 칸 없음 `data-meta="none"`), owner 메타 슬롯 `.d0-check__owner` + `<time>` 또는 `.d0-check__when`(조건). 연동 그림 변형 `data-variant="linked"`(왼쪽 sticky 단계 화면이 행 호버·포커스·클릭·체크로 바뀜, 그림) | [checklist.md](blocks/checklist.md) |
| code-block | 붙여 넣을 명령·설정(그림 아님, 줄 길이 예외) | 어두운 코드 면 + 라벨·복사 버튼 바, 클립보드 실패 시 선택 + 단축키 안내. checklist·accordion 행 `<details>` 안에 둔다 | [code-block.md](blocks/code-block.md) |
| accordion | 선택 보조 정보, 용어 목록 | `details` 선택 펼침, 용어 목록 변형 | [accordion.md](blocks/accordion.md) |
| faq (question-answer, 공용) | 독자가 실제로 가질 질문: faq 패턴, guide 막혔을 때, 보고·사건 끝 질문 | 항상 노출하는 답글형(들여쓴 답 + 꺾인 연결선 `.d0-faq`), 끝 한 줄 `.d0-faq__more` | [faq.md](blocks/faq.md) |
| callout | 본문 중간의 결정 요청·다음 할 일 하나 | soft 블루 상자, **페이지당 최대 1개**, 히어로 결론을 되풀이하지 않음. 문서 끝 맺음은 closing이 맡는다 | [callout.md](blocks/callout.md) |
| explanation (공용) | 그림이 보여 줄 수 없는 배경·이유·뜻·영향·조건·예외 | `dl.d0-explain > div[data-role] > dt + dd`, 라벨 14px/600 + 1~3문장 15px grey-700, 상자 없음. 그림 아래에 두고 축 폭을 그대로 쓴다 | [explanation.md](blocks/explanation.md) |
| evidence (공용) | 주장과 근거의 짝 | `dl.d0-evidence > div[data-proof]` 주장 한 줄 + 근거(number·source·before-after·example), 그림형 `figure.d0-evidence`, 근거 변형 `data-variant="metric-list|bar-list|tiles"`(`.d0-mlist`·`.d0-barlist`·`.d0-tiles`, 덱 evidence 장 그림 자리에도) | [evidence.md](blocks/evidence.md) |
| before-after (공용) | 같은 대상의 전과 후 | `div.d0-ba[data-kind="change|fix|improve|forecast"]` 두 쪽 + 화살표. 여러 항목은 diff-rows, 숫자는 막대 | [before-after.md](blocks/before-after.md) |
| checkpoint (공용) | 여기까지 하면 완성되는 결과 | `p.d0-checkpoint` 라벨 + 결과 한 줄 + 얇은 선, 완료면 green ✓ | [checkpoint.md](blocks/checkpoint.md) |
| closing (공용) | 문서가 남길 일 하나 | 큰 한 문장 + 구분선 + 메타 2~3칸, `data-closing`: decision·request·action·criteria·takeaway. page는 `footer.d0-closing`, deck은 마지막 장 | [closing.md](blocks/closing.md) |
| slide-deck | 출력 형식이 deck일 때의 덱 골격(page의 `d0-page` 대신, 어느 패턴이든). 구성·Slide Gate는 [output/deck.md](output/deck.md) | `main.d0-deck[data-pattern][data-variant]` + 16:9 `section.d0-slide`(`data-kind`로 종류, cqi 타이포)를 한 장씩 보기: 결론 제목 → 근거 그림 하나 → 해석 한 줄 → 쪽수, 표지 다음 제목 목차, 네비·←/→ 키 이동, 인쇄 한 장씩, 좁은 화면은 비율 해제. 제목 결론어 `b.d0-slide__key`, 크롬(섹션 태그 `p.d0-slide__tag`·쪽번호·얇은 푸터), 비대칭 구도 `data-layout="asym"`, 섹션 장 `data-kind="section"`, 표지·섹션·마무리의 진한 면 `data-surface="dark"` | [slide-deck.md](blocks/slide-deck.md) |
