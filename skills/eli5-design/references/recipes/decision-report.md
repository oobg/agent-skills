# 결정·보고 page 레시피

결론과 그 결론을 믿을 근거를 전하는 한 장짜리 문서다. 선택지 중 하나를 고르게 하는 결정 문서, 진행 상태·결과 보고, 장애 회고, 출시 보고, 적용 전 제안이 여기에 든다. 구조를 이해시키는 문서는 [explainer-page.md](explainer-page.md)다.

## 순서

1. **결론 한 줄.** 독자가 다 읽고 내릴 결정이나 알아야 할 결론을 한 줄로 적고, 그 결론을 바꿀 수 있는 근거가 무엇인지 적는다.
2. **첫 화면.** 제목은 결론이나 추천을 말해도 되고, 근거의 범위(인원·기간·시범 여부)를 제목 안에 함께 쓴다(`8명·5일 시범에서는 자동 배정이 예약 시간을 줄였어요`). 머리에 요약 행을 두고, 첫 섹션에는 결론을 가르는 실제 값·상태를 견주는 그림이나 표를 둔다. 한 결정에 두 지표가 함께 걸리면(예약 시간과 다시 고른 횟수) 같은 문법으로 나란히 첫 화면에 둔다.
3. **근거.** 결정에 필요한 근거는 바로 보이게 두고, 검증용 상세(계산 과정, 전체 표, 로그, 코드 위치)는 뒤로 보내거나 `details.d0-more`에 접는다.
4. **조건과 영향.** 조건이 바뀌면 답이 바뀌는 지점은 라벨 설명(`이럴 때는 달라져요`)으로 붙인다. 영향은 독립 섹션으로 만들지 않고 관련 근거나 결정 바로 곁에 둔다.
5. **결정 요청.** 결정·요청은 한 곳에만 둔다. 요약 행의 결정 행(`div[data-tone="decision"]`)이나 마지막 `footer.d0-closing` 중 하나다. 사용자가 마지막에 요청하라고 하면 closing에 둔다.
6. **조립과 검토.** `main.d0-page`로 뼈대를 쓰고(레이아웃은 설명 page와 같다. 결정·보고 문서임을 표시하려면 `data-width="report"`, 폭은 바뀌지 않는다) `python3 scripts/inline_assets.py page out.html`로 채운 뒤 [final-review.md](../final-review.md)를 거친다.

## 문서 종류별 출발점

출발점일 뿐이다. 독자 질문에 없는 섹션은 빼고, 필요한 질문은 더한다.

| 문서 | 첫 화면 | 이어지는 질문 |
| --- | --- | --- |
| 결정 | 선택지를 같은 축으로 견준 막대나 비교 표 + 요약 행(`문제 / 추천 / 결정 필요`) | 무엇을 얻고 무엇을 포기하나(조건 설명), 근거는(근거 + 출처), 결정 요청 |
| 상태 보고 | 지금 상태와 달라진 값(전/후 막대, 일정 막대) + 요약 행(`지금 / 달라진 점 / 결정 필요`) | 일정은 어디쯤인가, 무엇이 위험한가(위험 행), 다음에 누가 무엇을 하나(담당 목록) |
| 결과·출시 보고 | 전/후 값 또는 히어로 숫자 하나 + 요약 행(`이전 / 현재 / 결정 필요`) | 이전과 무엇이 다른가, 남은 일정, 자주 묻는 것 |
| 장애 회고 | 영향 그래프나 히어로 + 요약 행(`발생 / 복구 / 영향`) | 무슨 순서로 일어났나(시간 막대), 왜 생겼고 왜 못 막았나(원인 그래프 + 근거), 무엇을 고쳤나(전과 후), 다시 지킬 것 |
| 적용 전 제안 | 지금과 바꾸면을 같은 틀로 + 요약 행(`지금 / 바꾸면 / 결정 필요`) | 수치는 `예상치`로 표시하고 측정값과 섞지 않는다 |

- 고른 그림의 상세 문서만 연다: 흐름·원인 그래프 [diagrams/flow.md](../diagrams/flow.md), 같은 틀 비교·막대 [diagrams/comparison.md](../diagrams/comparison.md), 화면 짚기 [diagrams/annotation.md](../diagrams/annotation.md), 시간 막대 [blocks/timeline.md](../blocks/timeline.md), 위험 행 [blocks/diff-rows.md](../blocks/diff-rows.md), 담당 목록 [blocks/checklist.md](../blocks/checklist.md), 전과 후 [blocks/before-after.md](../blocks/before-after.md), 점 그래프 [charts-points.md](../charts-points.md).
- 히어로는 이미 측정된 결론 숫자가 하나일 때만 쓴다. 선택지마다 다른 추정 숫자는 히어로가 아니라 비교 막대다.

## 근거를 놓는 법

결정 근거와 검증용 상세를 나누는 한 가지 예다. 매번 이 세 층을 다 채울 필요는 없다.

1. 본문: 결론을 바꿀 수 있는 핵심 근거(값·비교·사례).
2. 근거 곁 한 줄: 다음 행동에 필요할 때만 출처나 기준(`지난 분기 기록 기준`).
3. 접힌 상세: 여러 경로, 로그, 원시 측정값, 보조 계산.

## 비교의 모양

- 선택지 값은 같은 트랙·같은 축의 막대(`ol.d0-barlist` 또는 SVG 막대)로 견준다. 추천안이 있으면 그 행만 강조한다. 막대 길이는 값에서 계산한다.
- 기능·조건 비교는 `table.d0-table`이다. 선택지가 3개까지면 `data-stack`을 달고 칸마다 `data-label`(선택지 이름)을 적어 좁은 화면에서도 세 선택지가 한 줄에 보이게 한다(`<table class="d0-table" data-stack>` … `<td data-label="자동 배정">1.5분</td>`). 추천 열은 `data-on`, 숫자 칸은 `data-num`, 없음은 `data-state="none"`, 미확정은 `data-state="pending"`이고 글자(`없음`, `미확정`)를 칸에 꼭 쓴다.
- 구조가 다른 두 방식(상태 흐름, 처리 경로)은 같은 틀에 나란히 그리고 차이 나는 자리만 다르게 그린다. 한쪽에 없는 상태는 대응 자리를 비우고 `없음` 라벨을 단다. 상세는 [diagrams/comparison.md](../diagrams/comparison.md)다.

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>좌석 배정 방식 결정</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"><!-- 넘기기 전 subset_font.py가 바꾼다 -->
<style>
/* eli5:tokens.css */
/* eli5:page.css */
</style>
</head>
<body>
<main class="d0-page" data-width="report">
<header class="d0-header">
  <div class="d0-header__meta"><span class="d0-header__label">좌석 배정 방식 결정</span></div>
  <h1>8명·5일 시범에서는 자동 배정이 예약 시간을 줄였어요</h1>
  <dl class="d0-summary">
    <div><dt>문제</dt><dd>자리를 고르는 데 시간이 걸려요.</dd></div>
    <div><dt>추천</dt><dd>자동 배정, 다만 창가 자리 고르기는 아직 없어요.</dd></div>
  </dl>
</header>
<!-- 첫 섹션: 결론을 가르는 값 두 개를 같은 문법으로 나란히 -->
<section class="d0-section" aria-labelledby="s1">
  <header class="d0-section-head"><h2 id="s1">예약 시간은 줄고 다시 고르는 일은 그대로예요</h2></header>
  <div class="d0-cols">
    <figure class="d0-evidence"><figcaption>한 번 예약에 걸린 시간</figcaption>
      <ol class="d0-barlist">
        <li><span class="d0-barlist__label">지금(수동)</span><data class="d0-barlist__value" value="4">4분</data><span class="d0-barlist__track" aria-hidden="true"><span class="d0-barlist__fill" style="width: 100%"></span></span></li>
        <li data-on><span class="d0-barlist__label">자동 배정</span><data class="d0-barlist__value" value="1.5">1.5분</data><span class="d0-barlist__track" aria-hidden="true"><span class="d0-barlist__fill" style="width: 37.5%"></span></span></li>
      </ol>
    </figure>
    <figure class="d0-evidence"><figcaption>하루에 자리를 다시 고른 횟수</figcaption>
      <ol class="d0-barlist">
        <li><span class="d0-barlist__label">지금(수동)</span><data class="d0-barlist__value" value="6">6번</data><span class="d0-barlist__track" aria-hidden="true"><span class="d0-barlist__fill" style="width: 100%"></span></span></li>
        <li data-on><span class="d0-barlist__label">자동 배정</span><data class="d0-barlist__value" value="6">6번</data><span class="d0-barlist__track" aria-hidden="true"><span class="d0-barlist__fill" style="width: 100%"></span></span><span class="d0-barlist__note">8명·5일 시범 기준</span></li>
      </ol>
    </figure>
  </div>
  <!-- 이 섹션이 마지막이면 끝에 closing. 요약 행에 결정 행을 두었다면 closing은 action·takeaway로 짧게 쓰거나 생략 -->
  <footer class="d0-closing" data-closing="request">
    <p class="d0-closing__line">다음 주 금요일까지 회신해 주세요.</p>
    <dl class="d0-closing__meta"><div><dt>요청</dt><dd>자동 배정으로 바꿀지 회신</dd></div><div><dt>다음</dt><dd>바꾸면 첫 주는 한 층만 바꿔요</dd></div></dl>
  </footer>
</section>
</main>
<script>
/* eli5:page.js */
</script>
</body>
</html>
```

- 이 레시피의 부품 CSS는 `assets/page.css`에 있다. `blocks/` 파일의 특수 블록(타임라인, 위험 행, 체크리스트 등)만 그 파일의 CSS를 붙인다. 부품 목록(라벨 설명 `dl.d0-explain`, 주장 + 근거 `dl.d0-evidence`, 지표 카드, 옵션 나란히, 접기)과 배치 규칙은 [shell/contract.md](../shell/contract.md)에 있다.
- 요약 행은 2~3행이고 행 값은 한 줄이다. 결정이 둘이면 결정 행 `dd` 안에 짧은 `ol.d0-summary__list`를 둔다.
- 할 일이 여럿이면 담당 목록([blocks/checklist.md](../blocks/checklist.md) 담당 변형)에 두고, closing에는 가장 중요한 하나만 문장으로 올린다.
- 발표로 결정을 받으면 [deck.md](deck.md)다.
