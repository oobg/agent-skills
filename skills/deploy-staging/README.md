# Deploy Staging

저장소의 실제 정책과 CI 설정을 확인해 현재 변경을 스테이징 환경에 배포하고,
배포된 정확한 revision과 최종 상태를 검증합니다.

## 사용 시점

- 현재 변경을 스테이징이나 테스트 환경에 반영할 때
- 저장소가 branch push, PR, 수동 workflow 중 어떤 배포 경로를 쓰는지 확인해 실행할 때
- 이미 요청한 배포의 revision과 성공 여부를 검증할 때

브랜치 이름이나 워크플로를 고정해서 가정하지 않습니다. 저장소 문서, CI 트리거와
원격 보호 규칙을 근거로 경로를 결정하며, 설정 부족이나 충돌이 결과를 바꿀 때만
필요한 값을 확인합니다.

## 핵심 동작

- 작업 트리와 다른 worktree의 변경을 보호합니다.
- 사용자가 요청한 배포 범위 안에서 필요한 commit, push, PR 또는 workflow를 실행합니다.
- force push, 보호 규칙 우회와 타인의 변경 수정을 금지합니다.
- 배포 대상 SHA, CI run과 환경 상태가 연결될 때만 성공으로 보고합니다.
- 결과를 조회할 수 없으면 요청 상태와 확인 불가 사유를 구분합니다.

커밋 메시지와 분할 규칙은 필요한 경우 `conventional-commits` 스킬과 연계합니다.
커밋 메시지 작성만 요청한 경우에는 push나 배포를 실행하지 않습니다.

## 구성

```text
deploy-staging/
├── SKILL.md
├── README.md
├── references/
│   └── deployment-config.md
└── scripts/
    └── preflight.py
```

- [`SKILL.md`](SKILL.md): 정책 탐색, 실행 권한, worktree 보호, 실패 처리와 성공 검증 규칙
- [`deployment-config.md`](references/deployment-config.md): 배포 경로와 검증 근거를 기록하는 합성 설정 예시
- [`preflight.py`](scripts/preflight.py): 확인한 remote 이름을 입력받아 현재 Git 상태, revision과 worktree 점유를 읽기 전용 JSON으로 확인하는 도구. remote-tracking SHA는 마지막 fetch 시점의 로컬 값입니다.

설치와 검증 방법은 저장소의 [루트 README](../../README.md)에서 확인할 수 있습니다.
