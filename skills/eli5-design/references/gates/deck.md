# gates/deck — deck 전용 게이트

deck 출력은 [gates.md](../gates.md)의 공통 묶음 중 아래 deck 출력 예외를 뺀 나머지와 이 파일을 함께 본다. Slide Gate와 덱 게이트의 항목 정본은 [output/deck.md](../output/deck.md)와 [blocks/slide-deck.md](../blocks/slide-deck.md)이고, 이 파일은 순서와 위치만 가리킨다.

## deck 출력 예외

deck은 한 장짜리 문서가 아니라 16:9 슬라이드 5~12장(표지·제목 목차 포함)을 한 장씩 넘기는 덱이다. 원칙 4번 섹션 규칙, 원칙 2·3번 첫 화면 규칙, 원칙 6번 explanation 설명,
원칙 9번 히어로·h1 32/h2 20 고정 타이포·섹션 사이 64px·첫 화면 색 비중, 본문 축·2열·줄 길이 규칙, 720px 프레임, page 도식 라벨 렌더 13~20px 게이트, Page Depth Gate 대신
[output/deck.md](../output/deck.md)의 덱 구성·Slide Gate(한 장 한 주장, 결론 제목, 그림 면적·본문 밀도, 근거 밀도(제목이 주장하는 비교 기준·분모·관계가 화면에 있다, `stat`은 숫자 + 근거 그림이 기본), Impact 20~30%, 마지막 장(closing: decision·request·action·criteria·takeaway))와 [blocks/slide-deck.md](../blocks/slide-deck.md) 덱 게이트를 따른다.
결론 수치는 히어로 대신 `stat` 슬라이드에 둔다. 나머지 원칙(글은 적게, 한 사실은 한 번(제목 목차·closing 메타 반복은 빼고 센다), 시맨틱, 토큰, 색, 접근성)은 그대로다.

deck 출력은 위 deck 출력 예외에 적힌 항목 대신 [output/deck.md](../output/deck.md) Slide Gate(Story 먼저, 이어서 Slide·Visual·Ending)와 [blocks/slide-deck.md](../blocks/slide-deck.md) 덱 게이트로 판정하고, 나머지 항목은 그대로 적용한다.

## 순서와 위치

- [ ] **G-DECK-01** Slide Gate [Story]: [output/deck.md](../output/deck.md#story) (먼저 본다)
- [ ] **G-DECK-02** Slide Gate [Slide]: [output/deck.md](../output/deck.md#slide)
- [ ] **G-DECK-03** Slide Gate [Visual]: [output/deck.md](../output/deck.md#visual)
- [ ] **G-DECK-04** Slide Gate [Evidence] 근거 밀도: [output/deck.md](../output/deck.md#evidence-근거-밀도)
- [ ] **G-DECK-05** Slide Gate [Ending]: [output/deck.md](../output/deck.md#ending)
- [ ] **G-DECK-06** 덱 게이트(마크업·타이포·키보드·인쇄): [blocks/slide-deck.md](../blocks/slide-deck.md#덱-게이트-구현)
- [ ] **G-DECK-07** 그림 글자 렌더 크기: [blocks/slide-deck.md](../blocks/slide-deck.md#그림-글자)
- [ ] **G-DECK-08** 나머지 공통 항목(G-COM·G-A11Y·G-VIS): [gates.md](../gates.md)

Slide Gate의 전체 절은 [output/deck.md](../output/deck.md#slide-gate-의미-검사-우선)에 있다.
