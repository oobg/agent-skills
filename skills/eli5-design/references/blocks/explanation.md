# explanation — 라벨 단 짧은 설명

공용 정보 블록이다. 그림이 구조를 보여 준 뒤, 그림이 보여 줄 수 없는 배경·이유·뜻·영향·조건·예외를 라벨 아래 1~3문장으로 보완한다.
page 본문 설명의 기본 그릇이고 어느 패턴에서나 쓴다. 그림 블록이 아니다.

## 해부 구조

- 묶음 `dl.d0-explain` > 항목 `div[data-role]` > `dt` 라벨 + `dd` 설명.
- **라벨**은 14px/600 grey-900, 화면 문구는 자연어다(`왜 늦어졌나`, `영향`, `조건`, `그래서`). 역할 이름표를 화면에 그대로 쓰지 않는다.
- **설명**은 15px grey-700, 행간 1.65([shell.md](shell.md) 행간 예외), **1~3문장**이다. 블록당 3문장 상한은 이 블록에서 "한 라벨 아래 3문장"으로 센다.
- 묶음당 항목은 보통 2~3개이고 최대 3개다. 넷 이상이면 그 섹션은 질문 둘이다. 섹션을 나눈다.
- 항목 사이 24px. 카드·배경·테두리·그림자 상자로 감싸지 않는다. 묶음은 여백과 라벨 굵기로만 만든다.
- **놓는 곳은 그림 아래다.** 섹션 뼈대(제목 → 그림 → 해석 한 줄 → 필요할 때 "왜" 한 줄, [shell.md](shell.md))에서 해석은 `interpretation`, "왜"는 `reason` 한 항목이다. 묶음은 축 폭을 그대로 쓰고 따로 폭 상한을 두지 않는다(정본: [shell.md](shell.md) 줄 길이 절).
- 그림 옆 열에 두지 않고, 항목이 짝수라도 2열로 나누지 않는다. 그림 옆 열은 그림 지점과 번호로 대응하는 주석·범례만 쓴다(`.d0-wide` 안 `.d0-cols[data-split="7-5"]`, [shell.md](shell.md) 2열 절). 없어도 이해되는 용어 풀이 한 줄은 여백 주석 `.d0-margin`(선택)으로 둘 수 있지만 explanation 항목을 옮기지 않는다.
  대등한 두 덩어리(문제 | 해결 등)를 견주는 2열의 한 열 안에 explanation 묶음이 들어가는 것은 된다.

### 역할 (`data-role`)

| `data-role` | 답하는 것 | 라벨 예 |
| --- | --- | --- |
| `context` | 어떤 배경에서 생긴 일인가, 왜 지금인가 | `배경`, `왜 지금인가` |
| `reason` | 왜 그렇게 했나, 왜 그렇게 되나 | `왜 늦어졌나`, `왜 B안인가` |
| `interpretation` | 그림·숫자가 무엇을 뜻하나 | `그래서`, `읽는 법` |
| `impact` | 누구에게 무엇이 달라지나 | `영향`, `나에게 달라지는 점` |
| `constraint` | 어떤 조건에서 결과가 바뀌나 | `조건`, `이럴 때만` |
| `exception` | 규칙이 통하지 않는 경우는 | `예외`, `이 경우는 다르다` |

역할 이름표는 검토용이다. 스타일은 역할과 무관하다.

**여기 넣지 않는 것.** 주장과 측정 근거의 짝(숫자·출처·전/후·예시)은 [evidence](evidence.md)가 맡는다. 다음 행동·결정 요청은 explanation 역할이 아니다(그래서 `next` 역할이 없다).
문서가 남길 일 하나는 공용 [closing](closing.md)(page는 마지막 섹션 끝 `footer.d0-closing`, deck은 마지막 장)이 맡고, 할 일이 여럿이면 [checklist](checklist.md) 담당 변형의 메타 행(주체 + 기한·조건), 결정 하나는 header 요약 행의 결정 행으로 쓴다.
경계: explanation `impact`는 "무엇이 달라지나", `constraint`는 "어떤 조건에서 바뀌나"를 설명할 뿐 독자에게 행동을 요구하지 않는다. 행동을 요구하는 문장이면 closing으로 옮긴다.

## 언제 쓰나

- 그림이 모양을 보였지만 독자가 "왜?", "그래서?", "언제나 그런가?"를 다시 물을 때.
- 그림 없는 섹션을 라벨→설명·조건→영향 구조로 지을 때(원칙 4번, 주장→근거는 [evidence](evidence.md)).

## 다른 글 블록과의 경계

| 블록 | 차이 |
| --- | --- |
| 섹션 머리 설명 `p` | 섹션 제목 아래 1문장. 섹션의 한 줄 요지다 |
| 섹션 리드 `p.d0-section-lead`([section-head](section-head.md)) | 라벨 없는 결론 방향 2~3문장, 페이지당 1개. compare의 핵심 차이처럼 표·그림 앞에 둔다 |
| header 요약 행([header](header.md)) | 페이지 전체 상태 `라벨 \| 한 문장`. explanation은 섹션 안 설명이다 |
| [evidence](evidence.md) | 주장 + 측정 근거(숫자·출처·전/후·예시)의 짝. explanation은 근거 없는 설명이 아니라 그림·근거 옆의 이유·뜻·조건이다 |
| diff-rows 위험 행 `영향`/`대응`([diff-rows](diff-rows.md)) | 위험 행마다 붙는 짧은 dl. 섹션 전체의 맥락은 explanation이 맡는다 |
| step-columns([step-columns](step-columns.md)) | 순서가 있는 단계 주석. 순서가 없는 이유·조건은 explanation이다 |
| figcaption | 그림 아래 13px 한 줄 읽는 법. 두 문장 이상이면 explanation으로 옮긴다 |

## 스니펫

```html
<!-- 그림 아래 세로 -->
<dl class="d0-explain">
  <div data-role="reason">
    <dt>왜 늦어졌나</dt>
    <dd>내보내기 요청이 한 줄로 몰려 앞 작업이 끝나야 다음이 시작됐어요. 월말에는 줄이 평소보다 길어요.</dd>
  </div>
  <div data-role="constraint">
    <dt>조건</dt>
    <dd>팀 × 일자 묶음처럼 칸이 많은 파일만 기다려요.</dd>
  </div>
</dl>
```

```css
.d0-explain { display: grid; gap: 24px; margin: 0; }
.d0-explain > div { display: grid; gap: 4px; min-width: 0; }
.d0-explain dt { font-size: 14px; font-weight: 600; color: var(--d0-grey-900); line-height: var(--d0-leading-title); letter-spacing: var(--d0-tracking-title); }
.d0-explain dd { margin: 0; font-size: 15px; color: var(--d0-grey-700); line-height: 1.65; text-wrap: pretty; } /* 1.65: shell.md 행간 예외 */
```

grey-700은 흰 바탕에서 글자 대비 4.5:1을 넘는다([shell.md](shell.md) 대비 계산표). 묶음은 축 폭을 끝까지 쓰고, 줄 길이는 축이 정한다.

## 금지

- 그림이 이미 말한 내용을 글로 되풀이하기(그림을 가리고 explanation만 읽어도 새 정보가 있어야 한다).
- 라벨 없이 문단만 두기, 한 라벨 아래 4문장 이상, 한 묶음에 항목 4개 이상.
- 카드·배경·테두리·그림자 상자로 감싸기, 역할마다 다른 색 칠하기, 의미색 글자.
- 히어로·요약 행에 있는 숫자를 되풀이하기(원칙 8번). 숫자는 정본 위치를 가리키고 이유·조건만 쓴다.
- 그림 옆 빈자리를 채우려고 explanation을 그림 옆 열에 두기, 묶음을 2열로 나누기.
- `dd`나 묶음 `dl`에 `max-width`를 걸어 좁히기(SKILL.md 개행 규칙). 줄을 줄이려면 페이지 전체를 `data-width="narrow"`로 둔다.
