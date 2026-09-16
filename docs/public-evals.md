# 공개 합성 평가 fixture

이 저장소는 사적 `/evals/`, 실제 ontology DB, 외부 provider CLI가 없어도 평가 도구의 기본 계약을 확인할 수 있는 작은 공개 smoke baseline을 제공합니다. 정적 계약 입력은 `tests/fixtures/public-evals/static-contracts.json`, trigger 입력은 `tests/fixtures/public-evals/trigger-cases.json`에 둡니다. 두 파일은 실제 자료를 가명화한 사본이 아니라 독립적으로 작성한 합성 fixture입니다.

## 실행

설치된 개발 의존성을 사용하는 저장소 루트에서 다음 순서로 실행합니다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_public_eval_fixtures.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/eval_skill_contracts.py \
  --suite tests/fixtures/public-evals/static-contracts.json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/eval_trigger_cases.py \
  --cases tests/fixtures/public-evals/trigger-cases.json \
  --cwd .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

첫 명령은 공개 fixture의 형식과 제한된 개인정보 패턴을 검사합니다. 두 번째 명령은 현재 `SKILL.md`에 짧은 계약 문구가 있는지 정적으로 검사합니다. 여기서 `execution` kind도 실제 실행 증거가 아니라 문서에 실행 경계가 적혀 있는지를 검사하는 정적 계약입니다.

세 번째 명령은 `--run`이 없는 dry-run입니다. 입력을 로드하고 실행 계획만 보여 주며 agent를 호출하거나 리포트를 만들지 않습니다. 따라서 정적 계약 통과는 규칙이 문서에 있음을, dry-run 통과는 공개 trigger 입력을 읽고 계획할 수 있음을 각각 보여 줍니다. 실제 trigger 실행만이 agent 응답을 채점하지만, 이 baseline은 실제 발동률이나 조회 수행 여부를 입증하지 않습니다.

## 안전 경계

preflight는 고정된 두 fixture만 읽고 JSON 구조, 합성 표식, 대상 경로 이탈, symlink 이탈, 이메일 형식, 사용자 홈 절대경로, PEM private-key header를 검사합니다. 저장소 전체, 사용자 홈, `/evals/`, Git 이력, ontology DB는 탐색하지 않습니다. 작은 정규식 검사이므로 이름·경력·기밀과 모든 secret을 판별하지 못하며, 공개 전 수동 검토가 여전히 필요합니다.

실제 평가 입력·응답·로그·transcript는 공개 fixture로 옮기지 않습니다. 기존 `/evals/` 기본 경로와 ignore 규칙은 그대로 유지하며, 공개 fixture를 쓸 때는 `--suite` 또는 `--cases`로 경로를 명시합니다. 외부 provider 실행, 사용량과 비용, provider transcript 격리는 이 작업에서 검증하지 않습니다.

파일 구성과 설치·전체 검증 절차는 루트 `README.md`를 따릅니다. 공개 smoke baseline 안내를 루트 문서에 연결하는 작업은 별도 통합 범위입니다.
