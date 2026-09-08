# New Space

Orca에서 새 작업용 Git worktree를 만들고 요청한 branch와 base에서 정확히 시작했는지 확인하는
스킬입니다. Orca의 repo, lineage, setup 정책을 존중하면서 기존 작업공간과 분리된 공간을
만듭니다.

## 사용 시점

`/new-space`, “새 작업공간”, “Orca 워크트리 만들어줘”처럼 새 공간 생성을 명시적으로 요청할
때 사용합니다. 단순 브랜치 전환이나 기존 worktree 이동에는 사용하지 않습니다.

사용자가 지정한 base와 branch를 우선합니다. 별도 지정이 없으면 저장소의 실제 정책과 remote
ref를 확인합니다. 활성 release 우선 정책이 있는 저장소에서는 아직 기본 branch에 merge되지
않은 release를 찾고, 여러 개면 사용자가 선택하도록 합니다.

## 핵심 동작

- 현재 설치된 Orca CLI에서 version-matched `orca-cli` 가이드를 읽습니다.
- 독립 작업과 현재 작업에서 이어지는 lineage를 구분합니다.
- Orca가 Git branch에 prefix를 붙이거나 이름을 바꾼 결과를 감지합니다.
- 생성 전 기록한 base SHA와 생성 직후 HEAD의 양방향 차이를 검사합니다.
- 기존 branch, 경로와 작업 내용을 덮어쓰거나 강제 정리하지 않습니다.

Git 상태 확인과 검증은 Python 표준 라이브러리만 사용하는 보조 스크립트로 반복할 수 있습니다.
스크립트는 읽기 전용이며 fetch, worktree 생성, branch rename, reset 또는 삭제를 수행하지
않습니다. 실제 생성은 agent가 현재 Orca 가이드와 사용자 선택을 확인한 뒤 수행합니다.

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
