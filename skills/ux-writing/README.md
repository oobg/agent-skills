# UX Writing

제품 UI와 사용자에게 공개되는 문장을 명확하고 자연스럽게 다듬는 에이전트
스킬입니다. AI 티를 지우는 것보다 원문의 의미와 프로젝트 보이스를 보존하는 일을
먼저 봅니다.

## 언제 사용하나요?

- 버튼, 라벨, 에러 메시지, 빈 상태 문구를 다듬을 때
- README, 가이드, 릴리스 노트의 어체를 정리할 때
- 번역투나 기계적인 AI 문체를 줄이고 싶을 때
- 프로젝트 용어와 브랜드 보이스를 일관되게 적용할 때
- 결제, 삭제, 보안처럼 위험이 큰 문구를 별도로 검증할 때

## 적용 강도

| 강도 | 대상 | 적용 범위 |
| --- | --- | --- |
| 경량 | 내부 문서, 코드 주석 | 정확성과 명확성 |
| 표준 | 제품 UI, 외부 README와 가이드 | 체크리스트와 출력 게이트 |
| 고위험 | 결제, 삭제, 보안, 법률, 접근성 | 정확성 우선, fresh-eyes 감사 추가 |

프로젝트의 glossary, register, 브랜드 규칙이 기본 `~해요`체보다 우선합니다.

## 핵심 원칙

충돌할 때는 다음 순서를 따릅니다.

```text
정확 → 명확 → 간결 → 감정
```

- 확실성, 인과, 행위자, 수치, 긍정·부정을 바꾸지 않습니다.
- 멀쩡한 문장은 고치지 않습니다.
- 과윤문과 장르 이탈도 실패로 봅니다.
- 관점이나 실제 경험을 지어내지 않습니다.
- 이모지, 곱슬따옴표, 대시 같은 스타일 신호는 문맥으로 판단합니다.
- lint의 HARD 0은 좋은 글을 보증하지 않습니다.

## 사용 예

```text
이 결제 실패 메시지를 더 명확하게 다듬어줘. 의미와 오류 코드는 유지해줘.
```

```text
이 README의 프로젝트 어체는 유지하면서 번역투와 AI 티만 줄여줘.
```

정서까지 보강하려면 `/ux-writing:deep` 또는 “정서까지 살려줘”라고 요청합니다.

## 검사 도구

Python 3.8 이상에서 실행합니다.

```bash
python3 scripts/ai_lint.py <파일>
python3 scripts/glossary_check.py <파일>
python3 scripts/register_check.py <파일>
```

- `ai_lint.py`: 결정적인 문법 오류와 스타일 신호 검사
- `glossary_check.py`: 프로젝트 고정 표기 검사
- `register_check.py`: 목표 어체 일관성 검사

HARD 항목은 출력을 막지만 ADVISORY는 문맥을 확인하라는 신호입니다.

## 구성

```text
ux-writing/
├── SKILL.md
├── agents/
│   └── copy-auditor.md
├── references/
│   ├── ai-tells.md
│   ├── deep-mode.md
│   ├── glossary.md
│   ├── register.md
│   ├── translation-ese.md
│   └── worked-examples.md
└── scripts/
    ├── ai_lint.py
    ├── glossary_check.py
    └── register_check.py
```

- [`SKILL.md`](SKILL.md): 적용 범위, 원칙, 출력 게이트
- [`references/`](references): 필요할 때만 여는 상세 규칙과 예시
- [`agents/copy-auditor.md`](agents/copy-auditor.md): 배치·고위험 문구의 fresh-eyes 점검
- [`scripts/`](scripts): 기계적으로 판정할 수 있는 검사

설치 방법은 저장소의 [루트 README](../../README.md)를 참고하세요.
