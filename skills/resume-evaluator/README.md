# Resume Evaluator

이력서에 적힌 근거를 JD 요구사항과 대조해 정보의 충분성, 불일치와 확인 질문을 진단합니다. 숫자 점수나 채용 판정을 기본 결과로 만들지 않습니다.

## 역할

작성과 수정은 assistant 또는 resume-assistant가 담당할 수 있고, 평가는 이 스킬이 담당합니다. resume-assistant 설치는 필수가 아닙니다. 평가와 수정을 함께 요청한 경우에만 원문 위치, 관찰, 불확실성과 수정 우선순위를 근거 패킷으로 전달할 수 있습니다.

## 구성

```text
resume-evaluator/
├── SKILL.md
├── README.md
└── references/
    ├── 01_hard_rules.md
    ├── 02_scoring.md
    ├── 03_evaluator_perspectives.md
    ├── 04_bias_defense.md
    ├── 05_output_format.md
    └── ontology-boost.md
```

- [`SKILL.md`](SKILL.md): 문서 근거 진단 원칙과 참조 라우팅
- [`references/01_hard_rules.md`](references/01_hard_rules.md): 근거 제한과 판단 경계
- [`references/02_scoring.md`](references/02_scoring.md): 무점수 상태와 불확실성 규칙
- [`references/03_evaluator_perspectives.md`](references/03_evaluator_perspectives.md): 관점별 종합 기준
- [`references/04_bias_defense.md`](references/04_bias_defense.md): 과대추론과 문체 편향 방어
- [`references/05_output_format.md`](references/05_output_format.md): 요청 규모에 맞춘 출력 구성
- [`references/ontology-boost.md`](references/ontology-boost.md): 동일 지원자의 과거 기록을 입력 후보로 확인하는 선택 모듈

원본 패키지: `resume-evaluator.skill`

실제 이력서, 연락처, 개인 경력, 평가 결과와 로그는 저장소에 보관하지 않습니다. 예시는 합성 데이터만 사용합니다.

설치와 검증 방법은 저장소의 [루트 README](../../README.md)를 참고하세요.
