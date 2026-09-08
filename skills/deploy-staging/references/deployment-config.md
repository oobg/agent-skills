# 배포 설정 reference

저장소에 스테이징 배포 규칙이 없거나 흩어져 있을 때 사용하는 간단한 기록 형식입니다. 아래 값은 모두 합성 예시이며 실행 설정이 아닙니다. 실제 값은 저장소 정책, CI 설정과 원격 보호 규칙에서 확인합니다.

```yaml
environment: <staging-environment>
delivery:
  mode: <branch-push | pull-request | workflow-dispatch>
  source_branch: <current-work-branch>
  target_branch: <integration-branch>
  workflow: <workflow-file-or-name>
  inputs:
    environment: <staging-environment>
checks:
  local: [<lint-or-test-command>]
  required_ci: [<required-check-name>]
verification:
  revision_source: <commit-sha-or-deployment-metadata>
  status_source: <ci-run-or-provider-deployment>
```

필요한 필드만 저장소 문서에 추가합니다. 설정값은 다음 근거와 일치해야 합니다.

- `mode`: 실제 CI 트리거와 보호 규칙이 허용하는 반영 방식
- `source_branch`, `target_branch`: 브랜치 패턴과 PR 또는 push 정책
- `workflow`, `inputs`: 저장소에 존재하는 워크플로와 선언된 입력
- `checks`: 로컬에서 실행해야 하는 검사와 원격 필수 검사
- `revision_source`: 어떤 SHA 또는 산출물 식별자가 실제 배포본을 나타내는지
- `status_source`: 성공, 실패, 진행 중 상태를 확인할 권위 있는 위치

예시 placeholder를 실제 명령에 그대로 사용하지 않는다. 문서와 실행 설정이 다르면 실행 설정을 검토하고, 보호 규칙 또는 배포 대상을 바꾸는 수정은 사용자 요청 범위에 포함될 때만 진행한다.
