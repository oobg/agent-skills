# Resume Evaluator

이력서에 적힌 근거를 JD 요구사항과 대조해 정보의 충분성, 불일치와 확인 질문을
진단합니다. 숫자 점수나 채용 판정을 기본 결과로 만들지 않습니다.

## 사용 시점

- 이력서가 JD 요구사항을 얼마나 뒷받침하는지 확인할 때
- ATS, 리크루터, 실무자와 임원 관점의 근거 차이를 점검할 때
- 모순, 정보 부족과 면접에서 확인할 항목을 분리할 때
- 문서를 수정하기 전에 보완 우선순위를 정할 때

이력서 작성과 수정만 필요한 작업에는 적용하지 않습니다. 해당 작업은
[Resume Assistant](../resume-assistant/README.md)가 담당합니다.

## 역할 경계

평가와 작성은 서로 자동 호출하거나 의존하지 않습니다. 평가와 수정을 함께 요청한 경우에만
원문 위치, 관찰, 불확실성, 확인 상태와 수정 우선순위를 근거 패킷으로 전달합니다.

## 핵심 원칙

- JD 요구사항마다 이력서 원문과 위치를 연결합니다.
- JD가 없으면 가독성, 구체성, 문서 내부 일관성과 면접에서 확인할 항목만 진단합니다.
- 상태는 `근거 충분`, `보완 필요`, `판단 불가`로 구분하며, 경험 미기재를 역량 없음으로
  해석하지 않습니다.
- 관찰과 추론을 분리하고, 실제 불일치와 정보 부족을 구분합니다.
- 직무 적합성, 시장 순위와 채용 가능성을 문서만으로 단정하지 않습니다.
- 온톨로지 보강은 동일 지원자의 과거 기록을 입력 후보로 확인할 때만 사용하며, 현재 입력을
  덮어쓰지 않습니다.

## 사용 예

```text
이 이력서의 근거를 JD 요구사항별로 대조하고, 판단할 수 없는 항목을 구분해줘.
```

```text
점수는 빼고 리크루터와 실무자 관점에서 확인 질문만 정리해줘.
```

## 개인정보

실제 이력서, 연락처, 개인 경력, 평가 결과와 로그는 공개 저장소에 보관하지 않습니다.
문서 예시는 추적 가능한 고유명사와 수치를 제거한 합성 데이터만 사용합니다.

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

설치와 검증 방법은 저장소의 [루트 README](../../README.md)에서 확인할 수 있습니다.
