# New Space

Orca에서 새 작업용 Git worktree를 빠르게 만들고 요청한 branch와 base에서 정확히 시작했는지
확인하는 스킬입니다. 작업을 6개 type 중 하나로 분류하고 영문 kebab-case slug를 만든 뒤,
branch와 base를 한 번 확인해 기존 작업공간과 분리된 공간을 만듭니다.

## 사용 시점

사용자가 `/new-space`를 직접 호출할 때 사용합니다. 일반적인 branch 대화, 단순 브랜치 전환이나
기존 worktree 이동에는 자동으로 적용하지 않습니다.

사용자가 지정한 base와 branch를 우선합니다. 별도 지정이 없으면 저장소의 실제 정책과 remote
ref를 확인합니다. 활성 release 우선 정책이 있는 저장소에서는 아직 기본 branch에 merge되지
않은 release를 찾고, 여러 개면 사용자가 선택하도록 합니다.

## 핵심 동작

- 현재 설치된 Orca CLI에서 version-matched `orca-cli` 가이드를 읽습니다.
- `feat`, `fix`, `refactor`, `chore`, `ci`, `docs` 기준과 2~4단어 slug로 branch를 제안합니다.
- 완성된 branch와 base를 Question에서 한 번에 확인합니다.
- 독립 작업과 현재 작업에서 이어지는 lineage를 구분합니다.
- Orca가 Git branch에 붙인 prefix와 이름 변환을 안전한 조건에서 보정합니다.
- 생성 전 기록한 base SHA와 생성 직후 HEAD의 양방향 차이를 검사합니다.
- 기존 branch, 경로와 작업 내용을 덮어쓰거나 강제 정리하지 않습니다.
- 생성과 검증 뒤 같은 AI model과 effort, 확인된 approval policy와 sandbox mode의 Codex CLI
  agent를 시작해 현재 내용을 넘길지 묻습니다. CLI가 일부 설정을 표현하지 못하면 그 한계를
  알리고 새 세션 기본값 사용 여부를 선택받습니다.

Git 상태 확인과 검증은 Python 표준 라이브러리만 사용하는 보조 스크립트로 반복할 수 있습니다.
`preflight`와 `verify`는 읽기 전용입니다. `finalize`는 기본적으로 보정 계획만 보여 주며,
`--apply`를 명시했을 때 새로 생성된 clean linked worktree의 branch만 보정합니다. 기존 branch,
primary checkout, dirty worktree, base가 다른 worktree에는 적용하지 않습니다.

handoff를 선택하면 새 worktree를 다시 만들지 않고 생성된 공간의 exact full id에 terminal을
추가합니다. 현재 model과 확인된 approval policy, sandbox mode는 같은 설정을 사용하며 알 수
없으면 사용자에게 묻습니다. 지원되는 effort 값만 알 수 없는 경우에는 첫 Question에서 새
세션 기본값을 쓴다는 사실을 함께 알립니다. sandbox mode로 표현할 수 없는 네트워크 허용이나
추가 쓰기 경로 같은 제한은 완전히 승계되었다고 주장하지 않습니다.
준비된 agent에 필요한 작업 맥락을 한 번 전달한 뒤 원래 agent는 감시하지 않고 작업을 넘긴 뒤
종료합니다. 작업 공간만 만들기를 선택하거나 응답하지 않으면 agent와 terminal을 추가하지 않습니다.

## 사용 예

```text
/new-space 검색 필터를 추가할 작업공간을 만들어줘.
```

```text
새 Orca 작업공간을 만들어줘. base는 upstream/develop이고 독립 작업이야.
```

## 도구 요구 사항

Orca 관리 작업공간 생성에는 현재 환경에 설치된 Orca CLI가 필요합니다. 검사 스크립트는 Git과
Python 3.8 이상을 사용합니다. plain Git fallback은 Orca 비관리 저장소에서 사용자가 직접
선택한 경우에만 적용합니다.

## 구성

```text
new-space/
├── SKILL.md
├── README.md
├── references/
│   └── orca.md
└── scripts/
    └── new_space.py
```

- [`SKILL.md`](SKILL.md): 이름, base, lineage 결정과 실행 경계를 설명합니다.
- [`references/orca.md`](references/orca.md): 현재 Orca 가이드에 맞춘 생성과 결과 처리 규칙입니다.
- [`scripts/new_space.py`](scripts/new_space.py): preflight와 생성 결과 검증을 수행합니다.

설치 방법은 [루트 README의 설치 안내](../../README.md#설치), 검사 방법은
[검증 안내](../../README.md#검증)에서 확인할 수 있습니다.
