# 설명 page 레시피

혼자 읽으며 구조를 이해하는 한 장짜리 문서다. 기능·도구 소개, 흐름·구조 설명, 결과물 미리보기, 사용·설치 가이드, 일정·변경 내역, 용어 풀이가 여기에 든다. 결론을 고르게 하거나 상태·사건을 보고하는 문서는 [decision-report.md](decision-report.md)다.

## 순서

1. **할 수 있어야 할 것.** 독자가 다 읽고 할 수 있어야 할 것 한 줄을 적고, 아래 질문 → 그림 표의 행을 위에서부터 훑어 주제에 해당하는 행마다 거기에 이르려고 답을 얻어야 할 질문을 한 줄씩 적는다.
2. **섹션.** 질문 하나에 섹션 하나가 기본이다. 두 질문을 함께 봐야 이해되면 한 섹션에 묶는다. 같은 질문을 두 섹션에 나눠 답하지 않는다.
3. **그림.** 질문마다 답에 드는 그림을 아래 표에서 고르고, 실제로 고른 것의 상세 문서만 연다. 한 질문에 그림이 여럿일 수 있다(본보기 2번 이미지 속 섹션의 그림은 넷). 글로 충분한 질문에는 그림을 붙이지 않는다.
4. **첫 화면.** 머리 바로 아래 첫 섹션에 주제의 실체를 보여 주는 그림을 둔다. 결과물이 있으면 그 결과를, 주제가 낯선 용어면 그 용어가 일하는 장면(비유 삽화)이나 용어끼리 같은 틀로 견준 그림을 먼저 보여 주고 글에는 출처만 남긴다.
5. **글.** 도식화가 최우선이다. 그림으로 안 되는 이유·조건만 한 줄씩, 복사할 명령은 code-block으로 남긴다. 글에 순서(A→B→C, 요청에서 시작했으면 요청한 쪽이 결과를 받기까지)·비교(이러면 깨짐, 이러면 정상)·구성·연결·자리(경로)·항목의 뜻(필드·옵션)·접근 조건이 남았으면 기존 그림에 얹거나(화살표 위 검문소, 같은 틀의 ✓/✕ 줄, 상자 안 칸, 선 라벨, 자물쇠 라벨, 파일 트리, 번호 핀) 작은 그림으로 올린다.
6. **조립과 검토.** 아래 뼈대로 HTML을 쓰고 `python3 scripts/inline_assets.py page out.html`로 토큰과 정본 CSS·JS를 채운 뒤 [final-review.md](../final-review.md)를 거친다.

## 질문 → 그림

| 질문 | 고를 수 있는 그림 | 상세 |
| --- | --- | --- |
| 어떻게 흘러가나, 무엇이 무엇에 닿나, 누가 누구에게 넘기나 | 단계 도식, 연결 그래프, 주고받기, 진행선 | [diagrams/flow.md](../diagrams/flow.md) |
| 무엇이 어떻게 다른가, 전과 후는 | 같은 틀의 나란한 그림, 전/후 막대, 가로 막대 목록 | [diagrams/comparison.md](../diagrams/comparison.md) |
| 받으면 어떤 모양인가, 화면이나 설정·명령 파일의 줄마다 무엇인가, 어디에 두나 | 와이어프레임, 번호 핀(파일은 실제 줄을 쓴 종이 그림 + 핀), 번호 주석, 파일 트리 | [diagrams/annotation.md](../diagrams/annotation.md) |
| 눌러 봐야 아는 화면 | 미니 앱 목업, 화면 캡처 스포트라이트 | [blocks/mockup-frame.md](../blocks/mockup-frame.md) |
| 결과 파일·표가 어떤 모양인가 | 탭 + 표 목업, 썸네일 카드 | [blocks/tab-preview.md](../blocks/tab-preview.md), [blocks/thumb-cards.md](../blocks/thumb-cards.md) |
| 어떻게 따라 하나, 어디서 받고 어떻게 열어 보나 | 붙여 넣을 명령, 체크리스트 단계 | [blocks/code-block.md](../blocks/code-block.md), [blocks/checklist.md](../blocks/checklist.md) |
| 언제 무엇이 되나, 지금 어디인가 | 시간 막대, 타임라인, 진행 레일 | [blocks/timeline.md](../blocks/timeline.md) |
| 바뀐 항목만 보고 싶다 | 전/후 행 목록, 전과 후 두 쪽 | [blocks/diff-rows.md](../blocks/diff-rows.md), [blocks/before-after.md](../blocks/before-after.md) |
| 이 용어는 무엇인가, 막히면 왜인가 | 질문-답, 접는 용어 목록 | [blocks/faq.md](../blocks/faq.md), [blocks/accordion.md](../blocks/accordion.md) |
| 값 하나하나·분포·이상치 | 점 그래프 | [charts-points.md](../charts-points.md) |

- 그림을 고르기 전 단계에서는 이 표만 보고, 고른 뒤에 상세 문서를 연다. 한 칸의 후보는 순서가 아니라 대안이라 질문에 가장 맞는 것을 고르고, 문서 전체가 한 종류 그림(외곽선 도식)만 되풀이하지 않게 목업·타임라인·숫자 하나 크게·점 그래프도 견준다. 쓰지 않을 문서는 열지 않는다.
- 기능·도구를 소개하면 실제 입력 하나(요청 한 줄, 설정 한 줄)를 정해 문서 끝까지 같은 예제가 결과로 바뀌는 과정을 따라간다. 섹션마다 새 예제나 빈 골격 그림을 꺼내지 않는다.
- 독자에게 써 보라고 권하는 말로 맺거나, 효용을 약속하는 문구를 제목으로 쓰지 않는다. 제목은 사실이고, 끝은 마지막 질문의 답이다.

## 뼈대

질문과 그림을 고른 뒤 본보기 렌더 이미지 세 장([1](../examples/explainer-skills-mcp-1.jpg), [2](../examples/explainer-skills-mcp-2.jpg), [3](../examples/explainer-skills-mcp-3.jpg))을 모두 열어 보고 형식만 맞춘다. 형식은 질문마다 섹션, 섹션마다 그림 먼저, 정의는 그림 라벨, 같은 틀 비교, 글보다 그림이 많은 밀도다. 색·배치·그림 종류·섹션 구성은 주제에 맞게 본보기보다 다채롭게 고르고, 같은 주제여도 제목·눈썹 라벨·문구·예제는 새로 쓴다. 아래 뼈대의 섹션 구성도 한 예다.

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>주문 내보내기 한눈에 보기</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"><!-- 넘기기 전 subset_font.py가 바꾼다 -->
<style>
/* eli5:tokens.css */
/* eli5:page.css */
/* 이 문서만의 작은 CSS가 필요하면 여기. 토큰 변수만 쓴다 */
</style>
</head>
<body>
<main class="d0-page"><!-- 읽고 따라 하는 글이 주인공이면 data-width="narrow" -->
  <header class="d0-header">
    <div class="d0-header__meta"><span class="d0-header__label">내보내기 개편</span></div>
    <h1>주문 내보내기 파일은 이렇게 생겼어요</h1>
    <p class="d0-header__lead">어떤 시트가 있고 각 칸이 무엇을 뜻하는지 그림으로 보여 드려요.</p>
  </header>
  <section class="d0-section" aria-labelledby="s1">
    <header class="d0-section-head"><h2 id="s1">파일에는 시트가 세 장 있어요</h2></header>
    <figure class="d0-fig"><!-- 예: 비유 삽화(뚜껑 연 상자에서 시트 세 장이 나와 있다) -->
      <svg viewBox="0 0 560 280" role="img" aria-labelledby="s1-t s1-d"><title id="s1-t">…</title><desc id="s1-d">…</desc>…</svg>
      <figcaption>그림이 못 보여 주는 조건 한 줄(없으면 생략)</figcaption>
    </figure>
    <figure class="d0-fig" data-variant="pins"><!-- 둘째 그림이 필요하면 예: 시트 한 장의 실제 줄에 번호 핀 -->
      <div class="d0-pins"><svg viewBox="0 0 560 320" role="img" aria-labelledby="s1-p">…</svg><span class="d0-pin" data-pin="1" style="…">1</span>…</div>
      <dl class="d0-pins__key"><div data-pin="1" tabindex="0"><dt><span class="d0-pin">1</span>…</dt><dd>…</dd></div>…</dl>
    </figure>
  </section>
  <!-- 섹션 반복. 섹션마다 질문에 맞는 그림 종류를 고른다. 대상 둘을 견주는 주제이고 앞에서 안 보인 행이 남았을 때만 그 행을 같은 라벨·순서의 카드 두 장으로 둘 수 있다:
  <div class="d0-sbs" data-layout="card"><article class="d0-option"><h3>A</h3><dl class="d0-option__rows"><dt>어디서 구하고 어떻게 여나</dt><dd>…</dd><dt>조심할 점</dt><dd>…</dd></dl></article><article class="d0-option"><h3>B</h3>…같은 행…</article></div>
  남길 행동이 있으면 마지막 섹션 끝에 footer.d0-closing. 출처가 있을 때만 그 섹션 끝에 <p class="d0-note">출처: …</p> -->
</main>
<script>
/* eli5:page.js */
</script>
</body>
</html>
```

## 자주 쓰는 부품

아래 부품의 CSS는 `assets/page.css`에 있어 따로 붙이지 않는다. 질문 → 그림 표의 `blocks/` 파일(목업, 체크리스트 등)은 그 파일의 CSS를 메인 `<style>` 끝에 붙인다.

| 부품 | 마크업 | 쓰는 때 |
| --- | --- | --- |
| 요약 행 | `dl.d0-summary > div > dt + dd` (2~3행) | 리드가 `이전 / 현재 / 요청`처럼 역할로 나뉠 때 |
| 히어로 | `p.d0-hero > span.d0-hero__nums(.d0-hero__before, svg.d0-hero__arrow, .d0-hero__after) + span.d0-hero__note` | 측정된 결론 숫자가 하나 있을 때만. h1 바로 아래 |
| 라벨 설명 | `dl.d0-explain > div > dt + dd` | 그림으로 안 되는 이유·조건만, `dd` 한 줄. 기본은 없음(본보기는 여섯 섹션 중 한 곳). 이러면 X, 저러면 Y는 비교라 그림에 올린다 |
| 주장 + 근거 | `dl.d0-evidence > div > dt + dd` | 주장 한 줄과 그 근거(숫자·출처·예시) |
| 가로 막대 목록 | `ol.d0-barlist > li > .d0-barlist__label + data.d0-barlist__value + .d0-barlist__track > .d0-barlist__fill[style="width:n%"]` | 같은 단위 값 3~6개, 구성비. 강조 행은 `li[data-on]`, 막대 아래 짧은 표기는 `.d0-barlist__note` |
| 비교 표 | `table.d0-table` (아래) | 대상 셋 이상을 같은 기준으로 견줄 때 |
| 몫 막대 | `div.d0-share > div.d0-share__bar > span.d0-share__seg[style="width:n%"]` + `ul.d0-share__keys > li` | 전체 중 몫(구성비). 강조 몫은 `[data-on]` |
| 나란한 두 덩어리 | `div.d0-cols` | 전 \| 후, 완료 \| 남은 것처럼 동시에 봐야 할 때 |
| 넓은 구간 | `.d0-wide` | 기본 축에서 읽히지 않는 넓은 표·긴 띠·차트만 |
| 접기 | `details.d0-more > summary` | 흐름을 끊는 계산 과정·전체 표 |
| 마무리 | `footer.d0-closing[data-closing] > p.d0-closing__line + dl.d0-closing__meta` | 독자가 할 일 하나. `decision`·`request`·`action`·`criteria`·`takeaway` |

```html
<div class="d0-scroll"><!-- 선택지 4개 이상·긴 칸이면 data-stack 없이 표 안에서 가로로 민다. 넓으면 class="d0-wide d0-scroll" -->
  <table class="d0-table" data-stack style="--min-w: 560px"><!-- data-stack: 좁은 화면에서 기준 아래 선택지 칸을 나란히 -->
    <caption>세 배송 방식 비교</caption>
    <thead><tr><th scope="col">기준</th><th scope="col">지금</th><th scope="col" data-on>방식 B(추천)</th><th scope="col">방식 C</th></tr></thead>
    <tbody>
      <tr><th scope="row">하루 처리량</th><td data-num data-label="지금">1,200건</td><td data-num data-on data-label="방식 B">1,800건</td><td data-num data-label="방식 C">1,500건</td></tr>
      <tr><th scope="row">주말 출고</th><td data-label="지금">있음</td><td data-state="pending" data-label="방식 B">없음, 다음 분기 검토(미확정)</td><td data-state="none" data-label="방식 C">없음</td></tr>
    </tbody>
  </table>
</div>
```

- 숫자 칸은 `data-num`, 없음은 `data-state="none"`, 미확정은 `data-state="pending"`을 달고 글자를 꼭 쓴다. 대상이 둘이면 같은 행 라벨·순서의 카드 두 장(`div.d0-sbs[data-layout="card"]`), 셋 이상이면 표로 견준다. 항목 → 설명 두 칸 표는 라벨 설명으로 바꾼다.
- 넓이·여백·글자 크기 같은 구현 수치는 CSS가 갖는다. 배치 규칙이 더 필요하면 [shell/contract.md](../shell/contract.md)를 연다.
