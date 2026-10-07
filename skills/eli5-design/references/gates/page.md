# gates/page — page 전용 게이트

page 출력은 [gates.md](../gates.md)의 공통 묶음(HARD 공통·접근성·VISUAL 공통)과 이 파일을 함께 본다. 순서는 PAGE DEPTH(의미) → HARD(공통 + page 전용) → 접근성 → VISUAL(공통 + page 전용) → WARNING이다.

## PAGE DEPTH (의미 검사, page만)

글자 수·섹션 수의 하한으로 깊이를 재지 않는다. 완결성으로 잰다. 하나라도 걸리면 섹션 구성부터 고친다.

- [ ] **G-PAGE-01** 페이지가 독자의 핵심 질문에 모두 답한다(질문 목록과 섹션 제목을 한 줄씩 짝지어 검토)
- [ ] **G-PAGE-02** 중요한 결론에는 근거·이유·예시 중 하나 이상이 있다
- [ ] **G-PAGE-03** 변화나 문제를 말하면 원인 또는 영향 중 필요한 맥락이 있다
- [ ] **G-PAGE-04** 조건이 결과를 바꾸면 그 조건이 적혀 있다
- [ ] **G-PAGE-05** 행동이 필요하면 다음 행동·결정이 명확하다
- [ ] **G-PAGE-06** 짧게 만들려고 이해에 필요한 맥락을 지우지 않았다(중복 제거 ≠ 맥락 제거)

## HARD — page 전용 (코드로 확인)

렌더 DOM 기준(JS 실행 후)으로 판정한다. 페이지 섹션은 `main > section`이다.

- [ ] **G-PAGE-07** 설명 `p`와 글 블록(explanation·evidence·faq `dl`, `.d0-cols` 열 칸)에 축·열보다 좁은 `max-width`·`width`·`ch` 제약이 없다
- [ ] **G-PAGE-08** `.d0-page`·축 폭 규칙·`.d0-wide`·`.d0-fig svg`·`.d0-cols`·`.d0-margin`의 CSS가 정본 `assets/page.css` 그대로다(인라인 도구로 채웠으면 통과, 규칙은 [blocks/shell.md](../blocks/shell.md). 프레임 1136px·축 720px, narrow 축 640px, report 프레임 1280px·축 960px·글 720px)
- [ ] **G-PAGE-09** `data-width`가 주된 패턴의 기본값과 맞다(report·incident·timeline·launch-report·postmortem → report, guide·install-guide·faq → narrow, compare·flow·preview → 없음). 다르면 이유가 있다
- [ ] **G-PAGE-10** 2열이 같은 종류끼리 같은 분할이다. 축 안 `.d0-cols`는 6/6이고(`data-split` 없음), 넓은 구간 안 2열은 전부 6/6이거나 전부 7/5다(번호 범례 2열인 pins·annotate·`d0-shot`의 `data-split`도 함께 센다). 대등한 두 덩어리를 `.d0-wide`에 두지 않았다
- [ ] **G-PAGE-11** `.d0-keep`이 페이지당 1개 이하이고 마지막 섹션 끝(closing 앞)에 있다. `.d0-more`는 섹션마다 1개 이하이고 안에 그 섹션의 결정·정본 숫자가 없다
- [ ] **G-PAGE-12** header 다음 첫 페이지 섹션(첫 화면 섹션)에 그림 블록이 있다. checklist linked 변형의 무대 SVG는 그림 블록으로 세고, code-block은 그림으로 세지 않는다
- [ ] **G-PAGE-13** 그림 블록이 없는 페이지 섹션은 구조 블록(`dl.d0-explain`, `.d0-evidence`, `.d0-ba`, `.d0-checkpoint`, `.d0-closing`, faq, diff-rows, checklist, step-columns, accordion, `table`, `dl`·`ol`·`ul` 행 목록) 중 하나 이상을 담고, 섹션 머리 밖 내용이 연속된 일반 `p`만으로 이루어지지 않는다
- [ ] **G-PAGE-14** explanation(`dl.d0-explain > div > dd`) 하나가 4문장 이상이 아니고, 라벨 `dt`가 비어 있지 않으며, 묶음에 배경·테두리·그림자가 없다

## VISUAL — page 전용 (눈으로·측정으로 확인)

측정은 브라우저에서 `getBoundingClientRect()`로 한다. 각 항목 괄호 안이 측정 방법이다.

- [ ] **G-PAGE-15** 1280×800에서 SVG 도식의 bounding box가 첫 화면 안에 전부 보인다(잘리면 FAIL), 375×812에서는 첫 그림 블록 높이의 절반 이상이 첫 화면 안이다(윗부분만 걸치면 FAIL). 320×568은 첫 그림 블록의 위 끝이 첫 화면 안이면 통과다
- [ ] **G-PAGE-16** 첫 화면(1280×800) 안에서 그림·목업 면적이 글 면적보다 크다(그림 = `figure`·`svg`·목업 프레임 box, 글 = `p`·`li`·`dd` 텍스트 블록 box의 첫 화면 안 면적 합. 그림 안 글은 그림으로 센다). 첫 화면 아래 섹션은 이 면적 비교를 하지 않는다
- [ ] **G-PAGE-17** 1366·1440·1920px에서 모든 h2, 축 안 블록, `.d0-wide`, 축 안 2열 첫 열의 왼쪽 끝 x가 하나다(±1px, 프레임 왼쪽). `.d0-wide`의 오른쪽 끝이 프레임 오른쪽 끝이고(±1px) 왼쪽으로 넓어지지 않는다. 축 안 2열은 열마다 300px 이상이거나 세로로 쌓인다. 1024·768px에서는 가로 스크롤 없이 축이 가용 폭을 쓰고 여백 주석이 본문 아래로 내려간다
- [ ] **G-PAGE-18** 도식 `figure.d0-fig`의 SVG 렌더 폭이 놓인 자리(축, 무대 안쪽, 2열 열, `.d0-wide`) 폭의 75% 이상이다(`data-fit="compact"`가 정확히 75%. editorial의 120px 객체, 썸네일·와이어 카드·단계 열 그림 같은 블록 부품은 제외)
- [ ] **G-PAGE-19** 2열(`.d0-cols`, 번호 범례 2열)이 동시 비교·그림 지점과 번호로 대응하는 주석·범례·대등한 두 덩어리 중 하나다(읽어서 확인. "그림 | 그냥 설명 문단", "작은 그림 | 빈자리 채우는 목록"이면 FAIL)
- [ ] **G-PAGE-20** SVG 안 글자의 렌더 크기가 1280px에서 13px 이상 20px 이하, 375·320px에서 11px 이상이다.
  렌더 글자 크기 = font-size × (SVG 렌더 폭 ÷ viewBox 폭)로 잰다(무대가 있으면 무대 안쪽 폭). 글자 박스 높이는 쓰지 않는다(정본: [blocks/diagram.md](../blocks/diagram.md) 라벨 절)
- [ ] **G-PAGE-21** 축 안 글 블록(리드 `p`, explanation·evidence·faq `dl`, 행 목록)의 box 폭이 글 폭과 같다(±1px. 기본·narrow는 축 폭, report는 720px. 2열 열 안이면 그 열 폭). report에서 그림·표·지표·축 안 2열은 축 960px까지 쓴다. 글 블록마다 오른쪽 끝이 다르지 않다(정본: [blocks/shell.md](../blocks/shell.md) 줄 길이 절)
- [ ] **G-PAGE-22** 히어로가 있으면 히어로 수치가 1280×800 첫 화면 상단 1/3(y ≤ 267px) 안에 있다
- [ ] **G-PAGE-23** 페이지 섹션 사이 세로 간격이 64px(모바일 48px)이다(앞 섹션 마지막 블록 아래 끝 ~ 다음 섹션 `header` 위 끝, 오차 ±4px). page Impact(`data-emphasis="impact"`) 앞뒤도 같은 64px(모바일 48px)이다(배경 면 없이 일반 섹션 패딩 그대로)
- [ ] **G-PAGE-24** 섹션마다 그 섹션 패턴의 독자 질문에 답하는 블록이 있다(섹션 `data-pattern`과 패턴 파일의 질문을 짝지어 검토)
- [ ] **G-PAGE-25** explanation이 그림이 이미 말한 내용을 되풀이하지 않는다(그림을 가리고 explanation만 읽어도 새 정보가 있다)

## WARNING (lint, 실패 판정에 포함하지 않음, page)

- [ ] **G-PAGE-26** 1280×800·375×812 첫 화면 진한 포인트 채움 <1%: "강조가 너무 약한지 확인", 1~15%: 정상, >15%: "포인트 색이 배경처럼 쓰이는지 확인". 측정은 [blocks/shell.md](../blocks/shell.md) 색 절을 따르고, 게이트를 맞추려고 색 면적을 늘리지 않는다
- [ ] **G-PAGE-27** 페이지 섹션이 7개를 넘으면 "같은 질문을 나눠 답한 섹션을 묶을 수 있는지 재검토". 섹션 수 자체로 실패시키지 않는다

PAGE DEPTH·HARD·접근성·VISUAL 항목(색 면적 Warning 제외)이 실패하면 고치고 다시 통과시킨다.
