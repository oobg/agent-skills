# header — 머리 (필수)

## 해부 구조

- 작업 라벨(블루 글자 13px, 예: `알림 개편`, 티켓이 있으면 그 번호) → 제목 h1(32px, 모바일 26px) → [히어로] → 리드 또는 요약 행.
- 작업 라벨은 티켓 번호다. 티켓이 없으면 주제 분류어(예: `알림 개편`)를 쓰거나 라벨을 생략한다. 번호를 지어내지 않는다.
- 상태가 중요하면 라벨 옆에 배지 하나(`.d0-pill[data-tone]`). 배지는 기본 없음. report 상태 배지는 라벨 옆 이 자리에 두고
  `정상`·`완료` green / `위험` orange / `차단` red로 매핑한다(글자 grey-900, 정본 [report.md](../patterns/report.md)).
- 리드는 "이 페이지를 다 읽으면 무엇을 알게 되는가"를 말한다. header 폭을 그대로 쓴다.
- 아래 구분선은 첫 섹션의 `border-top`이 맡는다. header에 따로 긋지 않는다.
- **히어로와의 순서.** 결론 수치가 있으면 h1 바로 아래에 [hero.md](hero.md)를 두고 그 아래 요약 행을 둔다(h1 → 히어로 → 요약 행).
  히어로가 말한 숫자는 리드·요약 행에 다시 쓰지 않는다.

## 언제 쓰나 / 변형

- 모든 페이지의 첫 블록. 하나만 둔다.
- guide는 총 소요 시간을, report는 결론을 리드에 넣는다(결론이 수치면 히어로로 올린다).
- **문장 단위 개행(선택).** 리드가 2문장 이상이고 데스크톱에서 2줄을 넘기거나, 문장마다 역할이 다르면
  (예: "무엇을 바꿨나" / "지금 상태·부탁") 문장마다 `.d0-sentence`로 감싸 줄을 나눈다. 한 문장이 한 줄을
  넘치면 그 안에서는 자연 줄바꿈한다. 기본은 이어 쓰기다.
- **요약 행 변형(`data-variant="summary"`).** 리드 문단 대신 `라벨 | 한 문장` 행 2~3개. 내용이
  "이전 → 현재 → 요청"처럼 역할로 나뉠 때 쓴다. compare 전/후·결정 변형, report, incident, timeline 변경 내역의
  기본 리드다. 그 외 패턴이 첫 섹션이면 문장형 리드가 기본이다.
  - **값은 한 줄.** 각 행 값은 데스크톱에서 한 줄(약 35자 이내)이다. 넘치면 문장을 줄이고, 세부는 아래 섹션으로 보낸다.
  - **용어 풀이는 하나만.** 낯선 용어는 처음 나올 때 한 번, `abbr title` 또는 괄호 중 하나로만 푼다. 둘을 함께 쓰지 않는다.
    괄호 풀이로 한 줄(35자)을 넘기면 `abbr`을 쓴다.
  - **행 라벨.** 사용자가 행 문구를 직접 주면 라벨까지 그대로 쓴다. 스킬이 문구를 정할 때만 기본 `이전 / 현재 / 결정 필요`, 적용 전 제안은 `지금 / 바꾸면 / 결정 필요`를 쓴다.
    report 변형별 기본값(상태 보고 `지금 / 달라진 점 / 결정 필요` 등)은 [report.md](../patterns/report.md)가 정본이다.
  - 라벨 열은 `max-content`(가장 긴 라벨 폭, 라벨은 7자 이내 권장)이고 행들이 `subgrid`로 같은 열을 쓴다. 라벨 13px/600 grey-600, 내용 15px grey-800, 행 간격 8px, 디바이더 없음.
  - 결정·요청 행(`data-tone="decision"`)만 라벨 blue-dark + 행 왼쪽 2px 블루 선. 박스·배경 채우기 금지.
    판정은 라벨 문구가 아니라 `data-tone="decision"`이다. `결정 필요`는 기본 라벨 예시일 뿐 `도움 필요` 등도 쓸 수 있다.
  - 결정·요청 행이 있으면 페이지 아래 결정 요청 callout을 두지 않는다(둘 중 하나만). 결정 본문은 여기 한 곳이고,
    할 일 목록에는 "위 결정 1"처럼 짧게 가리키기만 한다.
  - 결정이 둘이면 결정·요청 행의 `dd` 안에 짧은 `ol`(최대 2개). 셋 이상이면 가장 중요한 1개만 요약 행에 두고
    나머지는 할 일 목록으로 보낸다. 결정 행을 여러 개로 늘리지 않는다(요약 행 최대 3행).
  - **두 번째 결정.** 사용자 문구가 고정이라 `ol`로 합칠 수 없거나, 결정자·시점이 첫 결정과 다르면 `ol`에 넣지 않는다.
    요약 행 바로 아래 보조 줄(`.d0-summary__aside`)에 한 줄로 쓰고, 할 일 목록에는 짧은 참조로만 둔다.
  - 적용 전 변경 제안이면 `예상치`를 페이지에 한 번 쓴다. 히어로가 있으면 히어로 한 줄 뜻에, 없으면 요약 행 수치 옆에.
  - 640px 이하에서는 라벨이 내용 위로 올라간다.

## 스니펫

```html
<header class="d0-header">
  <div class="d0-header__meta">
    <span class="d0-header__label">내보내기 개편</span><!-- 티켓이 있을 때만 번호 -->
    <span class="d0-pill" data-tone="orange">결정 대기</span>
  </div>
  <h1>주문 내보내기 파일은 이렇게 생겼어요</h1>
  <p class="d0-header__lead">
    <span class="d0-sentence">내보내기 파일에 어떤 시트가 있고, 각 칸이 무엇을 뜻하는지 그림으로 보여 드려요.</span>
    <span class="d0-sentence">아래 두 시안은 직접 눌러 볼 수 있어요.</span>
  </p>
</header>

<!-- 요약 행 변형 + 히어로 -->
<header class="d0-header" data-variant="summary">
  <div class="d0-header__meta"><span class="d0-header__label">알림 개편</span></div>
  <h1>알림이 더 빨리 와요</h1>
  <p class="d0-hero"><!-- hero.md 스니펫: 7일 → 1일 --></p>
  <dl class="d0-summary">
    <div><dt>이전</dt><dd>한 주 치를 모아 한 번 보냈어요.</dd></div>
    <div><dt>현재</dt><dd>매일 아침 어제 주문만 모아 보내요.</dd></div>
    <div data-tone="decision"><dt>결정 필요</dt><dd>팀 A에도 켤까요?</dd></div>
  </dl>
  <!-- 결정이 둘이면: <dd><ol class="d0-summary__list"><li>팀 A에도 켤까요?</li><li>보내는 시각을 9시로 할까요?</li></ol></dd> -->
</header>
```

```css
.d0-header { display: grid; gap: 12px; padding-bottom: 32px; }
.d0-header__meta { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.d0-header__label { color: var(--d0-blue-dark); font-size: var(--d0-text-compact); font-weight: 600; }
.d0-header__lead { color: var(--d0-grey-600); }
.d0-summary { display: grid; grid-template-columns: max-content 1fr; gap: 8px 16px; margin-top: 8px; }
.d0-summary > div {
  display: grid; grid-column: 1 / -1;
  grid-template-columns: 76px 1fr; /* subgrid 미지원 폴백 */
  grid-template-columns: subgrid;
  align-items: baseline; padding-left: 12px; border-left: 2px solid transparent;
}
.d0-summary dt { color: var(--d0-grey-600); font-size: var(--d0-text-compact); font-weight: 600; }
.d0-summary dd { color: var(--d0-grey-800); }
.d0-summary > [data-tone="decision"] { border-left-color: var(--d0-blue); }
.d0-summary > [data-tone="decision"] dt { color: var(--d0-blue-dark); }
.d0-summary__list { display: grid; gap: 4px; padding-left: 18px; margin: 0; list-style: decimal; }
.d0-summary__aside { padding-left: 14px; color: var(--d0-grey-600); font-size: 14px; }
.d0-summary abbr[title] { text-decoration: underline dotted var(--d0-grey-500); text-underline-offset: 3px; cursor: help; }
@media (max-width: 640px) {
  .d0-summary > div { grid-template-columns: 1fr; gap: 2px; }
}
```

## 금지

- 그라디언트 히어로, 대문자 eyebrow, 히어로 일러스트. 결론 숫자는 [hero.md](hero.md)의 숫자 블록만 쓴다.
- 리드에 컨테이너보다 좁은 `max-width`·`width`·`ch` 제약, 리드에 `text-wrap: balance`.
- 문장 나누기를 `<br>` 반복으로 하기, 한 문장짜리 리드를 억지로 쪼개기.
- 요약 행에 박스·배경 채우기, 4행 이상, 두 줄로 넘치는 행 값, 결정 행과 결정 callout을 함께 두기, 결정 행 `ol`에 3개 이상.
- 히어로 숫자를 요약 행에 되풀이하기, 같은 용어를 `abbr`과 괄호로 이중 풀이하기.
- 티켓이 없는데 `작업-000` 같은 번호를 지어내기.
