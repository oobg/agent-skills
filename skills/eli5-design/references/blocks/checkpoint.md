# checkpoint — 여기까지 하면

공용 정보 블록이다. 단계·경위 사이에 **여기까지 하면 무엇이 완성되는가**를 얇은 선과 결과 한 줄로 남긴다.
절차 단계 도식 뒤(`여기까지 하면 초안 완성`), 사건 경위(`여기서 원인 확정`), 일정(`여기까지 설계 완료`)에서 쓴다.
[checklist](checklist.md) 구간에서는 쓰지 않는다. 구간 결과는 구간 머리 행의 결과 한 줄이 맡는다(같은 결과를 두 번 쓰지 않는다).

## status rail과의 역할 구분

| 블록 | 답하는 질문 | 자리 |
| --- | --- | --- |
| [status rail](timeline.md) `ol.d0-rail` | 지금 어디에 있는가(완료·진행·예정) | 목록·섹션 위, 전체를 한 줄로 |
| checkpoint `p.d0-checkpoint` | 여기까지 하면 무엇이 완성되는가 | 단계 묶음의 끝, 결과가 생기는 지점 |

rail은 위치를, checkpoint는 결과를 말한다. 같은 말을 둘에 쓰지 않는다(rail 이름은 짧은 구간 이름, checkpoint는 결과 문장).

## 해부 구조

- `p.d0-checkpoint` = 앞 라벨 `span.d0-checkpoint__label`(`여기까지 하면`, 12px/600 grey-600) + 결과 한 줄(14px/600 grey-900) + 뒤로 이어지는 1px grey-200 선.
- 결과는 상태가 아니라 얻는 것이다(`설정 끝` ✕ → `내보내기 메뉴를 쓸 수 있어요` ○). 한 줄(약 40자 이내)이다.
- 완료가 확인되면 `data-status="done"`으로 앞에 green 점 + `✓`를 붙인다. 글자는 grey-900 그대로다.
- 카드·배경·굵은 구분선 없음. 뒤 1px grey-200 선은 블록 안 표식이라 진한 구분선 금지의 예외다([shell/contract.md](../shell/contract.md) 금지 절).
- **자리.** 섹션 경계선(1px grey-100)과 겹치지 않게 섹션 맨 끝 대신 단계 묶음 안쪽 끝에 둔다. flow 단계 도식, 세로 timeline처럼 묶음이 없으면 그 단계 블록 바로 뒤에 둔다.

## 스니펫

```html
<p class="d0-checkpoint"><span class="d0-checkpoint__label">여기까지 하면</span>초안이 완성돼요.</p>
<p class="d0-checkpoint" data-status="done"><span class="d0-checkpoint__label">여기서</span>원인이 확정됐어요.</p>
```

```css
.d0-checkpoint { display: flex; align-items: center; gap: 8px; margin: 0; padding: 12px 0; color: var(--d0-grey-900); font-size: 14px; font-weight: 600; }
.d0-checkpoint::after { content: ""; flex: 1 1 24px; height: 1px; margin-left: 8px; background: var(--d0-grey-200); }
.d0-checkpoint__label { flex: none; color: var(--d0-grey-600); font-size: var(--d0-meta); font-weight: 600; }
.d0-checkpoint[data-status="done"]::before { content: "✓"; display: inline-grid; place-content: center; flex: none; width: 18px; height: 18px; border-radius: 999px; background: var(--d0-green); color: #fff; font-size: 11px; }
```

green 원 위 흰 체크선은 checklist와 같은 3.47:1(그래픽 3:1)이다. 완료 여부는 `✓` 모양이 함께 말한다.

## 금지

- 상태 단어만 쓴 결과(`완료`, `끝`), 두 줄 넘는 결과, 구간마다 반복되는 같은 문장.
- 카드·배경 상자로 감싸기, 섹션 구분선처럼 굵게 긋기, 섹션 사이에 두어 섹션 간격(64px)을 바꾸기.
