# Resume Assistant

이력서와 경력기술서의 내용을 사실에 맞게 정리하고, 지원 직무에 맞는 표현으로
다듬는 작성 보조 스킬입니다.

## 사용 시점

- 이력서나 경력기술서의 문장을 사실 범위 안에서 다듬을 때
- JD에 맞춰 경력의 순서와 강조점을 다시 구성할 때
- ATS가 읽기 쉬운 구조와 키워드를 정리할 때
- 전문 요약, 경력 bullet과 기술 스택 섹션을 작성할 때

점수나 채용 판정만 요청받으면 적용하지 않습니다. 문서의 근거를 JD와 대조해 진단하는
작업은 [Resume Evaluator](../resume-evaluator/README.md)가 담당합니다. 두 스킬은 서로
자동 호출하거나 설치를 요구하지 않으며, 각각 독립적으로 실행됩니다.

## 핵심 원칙

- 사용자가 주지 않은 수치, 성과, 역할과 의사결정 권한을 만들지 않습니다.
- 확인되지 않은 내용은 `[확인 필요]`로 표시하고, 답이 없으면 같은 질문을 반복하지 않습니다.
- 원본, 개선안과 제출본을 구분해 사용자가 사실관계를 검토할 수 있게 합니다.
- 선택적 온톨로지 보강은 동일 지원자의 과거 경력과 표기 결정을 입력 후보로 회수할 때만
  사용합니다. 회수한 내용은 현재 사용자가 확인하기 전까지 확정 사실로 쓰지 않습니다.

## 사용 예

```text
이 경력기술서를 백엔드 엔지니어 JD에 맞게 다듬어줘. 없는 성과는 만들지 마.
```

```text
이 bullet의 역할이 과장되지 않게 원문과 개선안을 비교해줘.
```

## 개인정보

실제 이력서, 연락처, 개인 경력과 작업 로그는 공개 저장소에 보관하지 않습니다. 문서 예시는
추적 가능한 고유명사와 수치를 제거한 합성 데이터만 사용합니다.

## 구성

```text
resume-assistant/
├── SKILL.md
├── README.md
└── references/
    ├── domain-guide.md
    ├── hard-rules.md
    ├── ontology-boost.md
    ├── quality-check.md
    └── writing-rules.md
```

- [`SKILL.md`](SKILL.md): 이력서 작성 절차와 출력 형식
- [`references/domain-guide.md`](references/domain-guide.md): 직무별 작성 관점
- [`references/hard-rules.md`](references/hard-rules.md): 사실성과 역할 표현의 필수 규칙
- [`references/ontology-boost.md`](references/ontology-boost.md): 동일 지원자의 과거 경력과
  표기 결정을 회수할 때만 여는 선택 모듈
- [`references/quality-check.md`](references/quality-check.md): 결과물 품질 점검 기준
- [`references/writing-rules.md`](references/writing-rules.md): 문장 구성과 표현 규칙

설치와 검증 방법은 저장소의 [루트 README](../../README.md)에서 확인할 수 있습니다.
