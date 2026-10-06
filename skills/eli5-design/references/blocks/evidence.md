# evidence — 주장과 근거

공용 정보 블록이다. **Claim(주장 한 줄) + Proof(근거)**를 한 짝으로 묶는다. 어느 패턴에서나 "그래서 왜 그렇게 말할 수 있나"를 보일 때 쓴다.
예: `B안이 더 적합하다` / `새 요청 10건 중 10건 수용`.

## 해부 구조

- **Claim.** 결론 한 줄(15px/600 grey-900). 주제명이 아니라 주장이다(`처리 시간` ✕ → `처리 시간이 절반으로 줄었다` ○).
- **Proof.** 주장을 받치는 근거 하나. 표현 방식(`data-proof`)은 넷 중 하나다.

  | `data-proof` | 근거 모양 | 마크업 |
  | --- | --- | --- |
  | `number` | 숫자 + 단위 + 기준 한 줄 | `data value` 20px/600 grey-900 `tabular-nums` + 14px grey-600 기준 |
  | `source` | 어디서 확인했나 | 14px grey-700 한 줄 + `small` 출처(12px grey-600) |
  | `before-after` | 바뀌기 전과 후 | [before-after](before-after.md)를 Proof 안에 넣는다 |
  | `example` | 실제 한 건 | 14px grey-700 한 줄, 값은 합성 |

- 형태는 `dl.d0-evidence > div[data-proof]`(짝이 여럿) 또는 `figure.d0-evidence`(근거가 그림 하나: Claim은 `figcaption`을 그림 위에, Proof는 SVG·kpi-cards 막대 변형).
- 짝은 섹션당 1~3개. 여럿이면 세로로, 전체 폭이면 `.d0-cols` 2열. 짝 사이 24px.
- 카드·배경·테두리 상자 금지. 묶음은 여백과 글자 굵기로만 만든다.
- **한 사실은 한 번.** 히어로·요약 행에 있는 숫자를 Proof에 다시 쓰지 않는다. 그 숫자가 정본이면 Proof는 출처나 예시로 받친다.
- 숫자 Proof에는 단위·기간·기준을 붙인다. 예상치는 글자 라벨 `(예상치)`를 단다. 측정값과 섞지 않는다.

## explanation과의 경계

evidence는 "무엇을 근거로"(측정·출처·사례), [explanation](explanation.md)은 "왜·그래서·어떤 조건에서"(이유·뜻·조건)다. 근거 아래 해석이 필요하면 evidence 다음에 explanation `interpretation`을 붙인다. 하나의 블록에 둘을 섞지 않는다.

## 스니펫

```html
<dl class="d0-evidence">
  <div data-proof="number">
    <dt>B안이 새 요청을 다 받는다</dt>
    <dd><data value="10">10건 중 10건</data><span>지난 4주 새 요청 기준</span></dd>
  </div>
  <div data-proof="source">
    <dt>A안은 월말에 느려진다</dt>
    <dd>월말 사흘 동안 대기열이 평소의 세 배였어요.<small>출처: 내부 집계(합성)</small></dd>
  </div>
</dl>

<!-- Proof가 전/후일 때: before-after를 Proof 안에 넣는다 -->
<dl class="d0-evidence">
  <div data-proof="before-after">
    <dt>받을 묶음을 먼저 고르면 다시 받는 일이 줄었다</dt>
    <dd>
      <div class="d0-ba" data-kind="improve">
        <div data-side="before"><span class="d0-ba__label">기존</span><p>전체를 받은 뒤 엑셀에서 지워요.</p></div>
        <span class="d0-ba__arrow" aria-hidden="true"></span>
        <div data-side="after"><span class="d0-ba__label">개선</span><p>필요한 묶음만 받아요.</p></div>
      </div>
    </dd>
  </div>
</dl>
```

```css
.d0-evidence { display: grid; gap: 24px; margin: 0; }
.d0-evidence > div { display: grid; gap: 6px; min-width: 0; }
.d0-evidence dt { color: var(--d0-grey-900); font-size: 15px; font-weight: 600; line-height: var(--d0-leading-title); }
.d0-evidence dd { display: grid; gap: 2px; margin: 0; color: var(--d0-grey-700); font-size: 14px; }
.d0-evidence data { color: var(--d0-grey-900); font-size: 20px; font-weight: 600; font-variant-numeric: tabular-nums; letter-spacing: var(--d0-tracking-title); }
.d0-evidence dd > span, .d0-evidence small { color: var(--d0-grey-600); }
.d0-evidence small { font-size: var(--d0-meta); }
.d0-evidence.d0-cols { column-gap: 48px; }
figure.d0-evidence > figcaption:first-child { color: var(--d0-grey-900); font-size: 15px; font-weight: 600; } /* 그림형: 주장이 그림 위 */
```

## 금지

- 주장 없는 숫자 나열, 근거 없는 주장, 한 짝에 근거 둘 이상.
- 큰 숫자를 blue로 칠하거나 증감 배지 달기(원칙 9번), 히어로 숫자 되풀이.
- 카드·배경 상자, 짝마다 다른 모양.
