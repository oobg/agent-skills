# New Space

Orca에서 새 작업용 공간을 만들고 생성 결과를 정확히 검증하는 스킬입니다. Git 프로젝트에는
요청한 branch와 base의 linked worktree를 만들고, folder 또는 non-Git 프로젝트에는 branch가
없는 Orca folder workspace를 만듭니다.

## 사용 시점

사용자가 `/new-space`를 직접 호출할 때 사용합니다. 일반적인 branch 대화, 단순 브랜치 전환이나
기존 worktree 이동에는 자동으로 적용하지 않습니다.

먼저 현재 프로젝트가 Git 기반인지 Orca folder 기반인지 판정합니다. Git 기반에서만 사용자가
지정한 base와 branch를 우선하고 저장소 정책과 remote ref를 확인합니다. folder 기반에서는
branch/base를 묻거나 Git preflight를 실행하지 않습니다.

## 핵심 동작

- 첫 사용과 cache 무효화 때 현재 Orca CLI의 version-matched `orca-cli` 원문을 확인합니다.
- Git 프로젝트와 folder 또는 non-Git 프로젝트의 생성 절차를 처음부터 분리합니다.
- 실행 파일·버전·stub·스킬 계약이 같으면 검토된 Orca recipe를 사용자 cache에서 재사용합니다.
- 사용자가 앞으로의 기본값으로 확인한 프로젝트 선호를 저장소 밖 로컬 state에 저장합니다.
- `feat`, `fix`, `refactor`, `chore`, `ci`, `docs` 기준과 2~4단어 slug로 branch를 제안합니다.
- 완성된 branch와 base를 Question에서 한 번에 확인합니다.
- 독립 작업과 현재 작업에서 이어지는 lineage를 구분합니다.
- Orca가 Git branch에 붙인 prefix와 이름 변환을 안전한 조건에서 보정합니다.
- 생성 전 기록한 base SHA와 생성 직후 HEAD의 양방향 차이를 검사합니다.
- folder 프로젝트가 미등록이면 Orca에 등록하고 exact path, `kind: folder`, repo id를 다시
  확인한 뒤 branch/base 없이 workspace를 생성합니다.
- folder workspace의 repo id/path와 `kind: folder`, exact full id/path, `repoId`, non-main 상태와
  빈 Git 필드를 `repo show`와 `worktree show` readback으로 검증합니다.
- 기존 branch, 경로와 작업 내용을 덮어쓰거나 강제 정리하지 않습니다.
- 생성과 검증 뒤 같은 AI model과 effort, 확인된 approval policy와 sandbox mode의 Codex CLI
  agent를 시작해 현재 내용을 넘길지 묻습니다. CLI가 일부 설정을 표현하지 못하면 그 한계를
  알리고 새 세션 기본값 사용 여부를 선택받습니다.

검증은 Python 표준 라이브러리만 사용하는 보조 스크립트로 반복할 수 있습니다. Git 전용
`preflight`와 `verify`, folder 전용 `workspace-verify`는 읽기 전용입니다. `workspace-verify`는
Git 명령을 호출하지 않으며 기본적으로 helper 실행 호스트의 디렉터리 존재도 확인합니다. paired
remote 경로는 명시적 remote 모드에서 일치하는 Orca repo/worktree readback으로 확인합니다.
이 모드는 worktree `hostId`가 문자열이고 `local`이 아닌 경우에만 허용합니다.
`finalize`는 기본적으로 보정 계획만 보여 주며,
`--apply`를 명시했을 때 새로 생성된 clean linked worktree의 branch만 보정합니다. 기존 branch,
primary checkout, dirty worktree, base가 다른 worktree에는 적용하지 않습니다.

프로젝트 메모리는 현재 요청, 현재 프로젝트 지침보다 낮은 우선순위로 적용합니다. 이번 한 번의
base나 model 선택은 자동 저장하지 않습니다. 프로젝트 정책 파일의 내용이 바뀌면 stale로
처리해 다시 확인합니다. worktree id, terminal handle과 현재 세션의 실효 권한은 저장하지
않습니다. 기본 저장 위치는 `~/.local/state/new-space`와 `~/.cache/new-space`이며 각각
`XDG_STATE_HOME`, `XDG_CACHE_HOME`으로 바꿀 수 있습니다. Orca recipe도 최초 원문을 검토해 hash로 연결한 뒤에만 재사용하며, 실행 오류가 나면
원문을 새로 받아 갱신합니다.

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

```text
/new-space 이 non-Git 폴더에서 실험용 문서 공간을 만들어줘.
```

## 도구 요구 사항

작업공간 생성에는 folder workspace를 지원하는 현재 환경의 Orca CLI가 필요합니다. 검사
스크립트는 Python 3.8 이상을 사용하며 Git 경로의 검사에만 Git이 필요합니다. Orca를 사용할 수
없거나 folder readback이 일치하지 않으면 생성을 중단하며 raw Git으로 우회하지 않습니다.

## 구성

```text
new-space/
├── SKILL.md
├── README.md
├── references/
│   └── orca.md
└── scripts/
    ├── context_cache.py
    └── new_space.py
```

- [`SKILL.md`](SKILL.md): 이름, base, lineage 결정과 실행 경계를 설명합니다.
- [`references/orca.md`](references/orca.md): 현재 Orca 가이드에 맞춘 생성과 결과 처리 규칙입니다.
- [`scripts/new_space.py`](scripts/new_space.py): Git preflight/finalize와 folder workspace의
  read-only 검증을 수행합니다.
- [`scripts/context_cache.py`](scripts/context_cache.py): 저장소 밖 프로젝트 선호와 검증된 Orca
  recipe cache의 유효성을 관리합니다.

설치 방법은 [루트 README의 설치 안내](../../README.md#설치), 검사 방법은
[검증 안내](../../README.md#검증)에서 확인할 수 있습니다.
