# gates — 출력 게이트 인덱스

결과물 HTML을 넘기기 전에 이 파일(공통 게이트)과 **현재 출력 형식의 게이트 파일 하나**만 읽고, 통과할 때까지 고친다(작업 순서 9번). 다른 출력 형식의 파일은 열지 않는다.

| 출력 | 읽을 파일 | 순서 |
| --- | --- | --- |
| page | 이 파일 + [gates/page.md](gates/page.md) | PAGE DEPTH(의미) → HARD(공통 + page 전용) → 접근성 → VISUAL(공통 + page 전용) → WARNING |
| deck | 이 파일 + [gates/deck.md](gates/deck.md) | [output/deck.md](output/deck.md) Slide Gate(Story 먼저) → 아래 항목 중 deck 출력 예외를 뺀 나머지(공통 항목) |

각 묶음은 **공통**(page·deck 모두)과 **page 전용**([gates/deck.md](gates/deck.md) deck 출력 예외에 해당해 deck에서는 Slide Gate·덱 게이트가 대신하는 항목)으로 나눈다.
page 전용 항목은 [gates/page.md](gates/page.md)에, deck 출력 예외와 덱 게이트 연결은 [gates/deck.md](gates/deck.md)에 있다.

**ID.** 항목마다 짧은 ID를 붙인다. 이 파일의 공통 묶음은 묶음별 접두사(`G-COM` HARD 공통, `G-A11Y` 접근성, `G-VIS` VISUAL 공통), 출력 형식 파일은 파일별 접두사(`G-PAGE`, `G-DECK`)를 쓰고 번호는 파일 안에서 이어진다. 보고·수정 때 ID로 가리킨다.

## HARD (코드로 확인)

렌더 DOM 기준(JS 실행 후)으로 판정한다. 페이지 섹션은 `main > section`이다.
deck 출력의 예외 처리는 [gates/deck.md](gates/deck.md)를 따른다.

**공통**

- [ ] **G-COM-01** `text-wrap: balance`가 제목 셀렉터(h1~h3)에만 있다
- [ ] **G-COM-02** 개수 상한(카드 5·단계 5, guide 체크리스트는 구간 규칙·옵션 3·질문 6·표 열 7 = 데이터 열 6 + 행 번호 열)을 넘지 않는다([blocks.md](blocks.md) 개수 상한)
- [ ] **G-COM-03** `role="img"`와 `<title>`을 가진 인라인 SVG 도식(kpi-cards 막대 변형, Editorial 장르의 SVG 객체 포함)이 1개 이상 있다. Editorial의 숫자는 SVG `<text>`가 아니라 HTML이다(SVG `<text>`로 그린 큰 숫자는 FAIL)
- [ ] **G-COM-04** Editorial(`figure.d0-fig[data-genre="editorial"]`)이 페이지당 1개 이하이고, 큰 글자가 실제 숫자이며(문구 FAIL), SVG 객체가 120px 이하다. 96px 이상 숫자는 Impact 안에만 있고, page Impact는 0~1개이며 안에 editorial이 없다
- [ ] **G-COM-05** 도식 `figure.d0-fig`마다 안에 SVG가 있고, SVG `<text>` 하나가 4어절(공백 3개) 이상이 아니다(넘으면 텍스트 상자 도식으로 보고 FAIL)
- [ ] **G-COM-06** callout이 1개 이하, page `footer.d0-closing`이 1개 이하다. 문서 끝 다음 행동·결정은 closing이 맡고(마지막 섹션 끝에 callout을 두지 않는다), callout은 본문 중간용이며 같은 결정·다음 요청을 둘에 함께 두지 않았다
- [ ] **G-COM-07** header 요약 행에 `data-tone="decision"` 행이 있으면 결정 callout과 closing `decision`이 없다(하나만, 라벨 문구는 `결정 필요`·`도움 필요` 등 무엇이든 같다)
- [ ] **G-COM-08** 모든 h2에 섹션 태그 pill이 붙어 있지 않다(전부 붙어 있으면 FAIL)
- [ ] **G-COM-09** 배지(`.d0-pill`)에 고정 `height`와 `flex: none`이 있다
- [ ] **G-COM-10** 배지 톤 종류(`span.d0-pill`의 `data-tone`, 없으면 회색)가 3가지 이하, 카드·행 하나에 배지가 1개 이하, 의미색(`--d0-green`·`--d0-red`·`--d0-orange`)을 글자 `color`로 쓴 곳이 없다
- [ ] **G-COM-11** 같은 숫자 문자열(숫자+단위, 예 `26분`)이 화면에 보이는 텍스트(`body.innerText` 기준. SVG `<text>`는 이미 포함되므로 따로 더하지 않고, SVG `<title>`·`<desc>`는 제외)에 2회 이하다. closing 메타 `dd`와 덱 제목 목차는 빼고 센다
- [ ] **G-COM-12** 무대를 쓴 도식 `figure.d0-fig[data-stage]`는 SVG가 `.d0-fig__stage` 패널 안에 있고 figcaption은 패널 밖에 있다. 무대 안 SVG에 `<text>`가 없다(글자 있는 도식은 무대 없음, 375px 무대 안쪽에서 라벨이 11px 아래로 준다. 회색 무대는 기본 없음, 쓰는 기준은 [composition.md](composition.md))
- [ ] **G-COM-13** kpi-cards에 증감 배지가 없다
- [ ] **G-COM-14** 화면에 보이는 글(제목·라벨·설명·캡션·SVG `<text>`)에 직역투 표현이 없다(읽어서 확인, [writing.md](writing.md) 점검 목록. 영어식 은유·무생물 주어 + 의지 동사·압축 대구·모호한 조건절이 하나라도 있으면 FAIL)
- [ ] **G-COM-15** `data-pattern` 값이 있으면 패턴 8개 중 하나다
- [ ] **G-COM-16** SVG·CSS 안 모든 `var(--d0-*)`가 tokens.css에 있다
- [ ] **G-COM-17** 구조(`section`·`header`·`figure`·`ol`/`ul`·`dl`·`table`·`time`·`data`·`progress`·`details`·`dialog`·`button`/`a`)를
  시맨틱 태그로 짓는다([blocks.md](blocks.md) 공통 규칙 표). 레이아웃·스타일 훅용 `div`·`span`은 허용, 빈 간격용 요소는 없다
- [ ] **G-COM-18** 헤딩이 h1→h2→h3 순서이고 건너뛰지 않는다, 랜드마크 `main`이 1개다
- [ ] **G-COM-19** 네이티브 시맨틱과 겹치는 role이 없다(`<nav role="navigation">`, `<button role="button">` 금지)
- [ ] **G-COM-20** `color-scheme: light`와 `body` 배경이 있다
- [ ] **G-COM-21** tokens.css 전체가 메인 `<style>` 맨 앞에 인라인되어 있고 토큰용 외부 `<link>`가 없다([day0.md](day0.md))
- [ ] **G-COM-22** 한 artifact 안 여러 페이지를 iframe으로 보여 줄 때 iframe `src`로 같은 artifact 파일을 부르지 않는다(`srcdoc` + `sandbox="allow-scripts"`, `allow-same-origin` 없음)
- [ ] **G-COM-23** 결과물 HTML(파일·artifact 모두)은 외부 요청이 0건이다(서브셋 `@font-face` 인라인). 도구가 없어 Pretendard jsDelivr 링크 하나를 둔 경우만 예외이고 사용자에게 알렸다
- [ ] **G-COM-24** day0-design `SKILL.md`의 HARD 게이트(토큰 변수만, 리스트는 행+디바이더, 상태는 `data-*`, focus-visible, reduced-motion)

page 전용 HARD 항목은 [gates/page.md](gates/page.md)에 있다.

## 접근성 (WCAG 2.2 AA 하한, 공통)

WCAG 3.0은 아직 Working Draft라 방향 참고로만 보고, 판정은 WCAG 2.2 AA로 한다. 3.0이 정식 권고가 되면 이 묶음을 갱신한다.

- [ ] **G-A11Y-01** `<html lang="ko">`, header·main·section, h1→h2→h3 순서, 표는 caption과 `th scope`
- [ ] **G-A11Y-02** 글자 대비 4.5:1(큰 글자 3:1), UI 경계·포커스 링·정보 그래픽 3:1. tokens.css 실제 값으로 계산한다
- [ ] **G-A11Y-03** 상태를 색만으로 구분하지 않는다(배지 글자, 현재 단계 점, 전후 라벨)
- [ ] **G-A11Y-04** 포인터 대상 24×24px 이상, 포커스 링이 가려지지 않는다
- [ ] **G-A11Y-05** 탭은 tablist/tab/tabpanel + `aria-selected` + 화살표 키(네이티브 대안이 없는 경우), 펼침은 `details`/`summary`, 체크는 실제 checkbox, 진행률은 `<progress>`
- [ ] **G-A11Y-06** 정보 SVG는 `role="img"`와 이름, 장식 SVG는 `aria-hidden`
- [ ] **G-A11Y-07** 320px 폭(400% 확대)에서 페이지 가로 스크롤 없음(표는 자체 스크롤 허용)

## VISUAL (눈으로·측정으로 확인)

측정은 브라우저에서 `getBoundingClientRect()`로 한다. 각 항목 괄호 안이 측정 방법이다.

**공통**

- [ ] **G-VIS-01** 옅은 면의 장면 수를 지킨다(blue 무대 1개 이하, deck Impact 20~30%). 색 면적은 아래 Warning으로만 판정한다
- [ ] **G-VIS-02** 회색만 있는 도식이 없다(도식 `svg`마다 blue 계열 또는 의미색 `fill`·`stroke` 요소가 1개 이상)
- [ ] **G-VIS-03** 배지가 세로로 늘어나지 않고 제목 첫 줄에 맞춰져 있다(배지 높이 = 22px 또는 20px, 배지 중심과 제목 첫 줄 중심 차 2px 이하)
- [ ] **G-VIS-04** 옆 영역이 남는데 줄이 바뀐 설명 문단이 없다(문단 폭이 부모의 content box 폭(패딩 제외), grid 안이면 그 열 폭보다 24px 이상 좁은데 2줄 이상이면 FAIL. callout·카드 패딩이나 열 폭을 남는 영역으로 세지 않는다)
- [ ] **G-VIS-05** 모바일 폭에서 가로 스크롤이 없다(375px에서 `scrollWidth` ≤ `clientWidth`)
- [ ] **G-VIS-06** 처음 보는 사람이 그림과 제목만 훑어도 요지를 말할 수 있다(h1·h2·figcaption만 읽고 요지 한 문장을 써 본다)

page 전용 VISUAL 항목과 WARNING은 [gates/page.md](gates/page.md)에 있다.

PAGE DEPTH·HARD·접근성·VISUAL 항목(색 면적 Warning 제외)이 실패하면 고치고 다시 통과시킨다.
