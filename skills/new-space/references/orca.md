# Orca worktree 생성

이 문서는 `orca-cli` 스킬의 resolver로 실행 파일을 선택하고, 그 실행 파일의
`skills get orca-cli` 전체 가이드를 읽은 뒤에만 사용합니다. 아래 명령 형태보다 현재 설치본의
가이드와 `--help`가 우선합니다.

## 대상과 부작용을 확인합니다

- `worktree current --json`과 `repo list --json`에서 현재 repo와 정확한 repo id를 확인합니다.
  현재 Orca worktree 안에서 repo 추론이 명확하면 `--repo`를 생략할 수 있습니다.
- repo의 setup 정책과 기본 terminal을 확인합니다. 생성 시 setup hook이나 terminal 명령이
  실행될 수 있으면 사용자 요청과 충돌하는지 판단합니다.
- 독립 작업에는 `--no-parent`, 현재 worktree에서 이어지는 작업에는
  `--parent-worktree active`를 사용합니다. lineage 옵션은 Git base를 정하지 않습니다.
- 사용자 요청이 없는 한 `--agent`, `--prompt`, `--activate`, setup 강제 실행 옵션을 쓰지
  않습니다. setup을 억제해야 하고 현재 버전이 지원하면 `--setup skip`을 사용합니다.

현재 가이드가 지원하는 명령을 다음 형태로 구성하고 `--json`으로 실행합니다.

```text
<orca-executable> worktree create \
  --repo id:<repo-id> \
  --name <branch-or-display-name> \
  --base-branch <base-ref> \
  --no-parent \
  --json
```

관련 작업이면 마지막 lineage 옵션만 확인된 parent 옵션으로 바꿉니다. 실제 값은 안전한 argv로
전달하며 문서의 자리표시자를 그대로 실행하지 않습니다.

## 결과의 실제 상태를 사용합니다

JSON 전체를 로그나 답변에 복사하지 않습니다. 결과에서 worktree의 full id, path와 branch만
읽고 필요한 후속 명령에 full id를 그대로 사용합니다. 응답 shape는 현재 가이드와 실제 결과로
확인합니다.

Orca가 display name에서 Git branch를 만들면서 합성 예시 `dev/feat-search-filter`처럼 사용자
prefix를 붙이거나 slash를 hyphen으로 바꿀 수 있습니다. 생성 결과의 branch를 반드시 읽고
요청값과 비교합니다. 현재 버전이 정확 branch 지정 또는 Orca metadata를 함께 갱신하는 rename을
지원할 때만 그 기능으로 교정합니다. raw Git rename의 metadata 일관성이 확인되지 않으면 자동
교정하지 않습니다. branch가 달라도 디렉터리명은 그대로 둡니다.

`scripts/new_space.py verify`로 실제 branch와 HEAD를 검사합니다. base 불일치, 예상 밖 branch,
불완전한 JSON 또는 경로가 나오면 reset, force removal, 기존 branch 삭제를 하지 않고 확인된
상태를 보고합니다.

## 생성 후 agent handoff

worktree 생성과 검증이 성공한 뒤에만 다음 질문을 합니다.

```text
새 작업 공간에서 현재와 같은 AI 모델을 시작하고, 지금까지의 작업 내용을 넘길까요?
```

선택지는 `시작하고 핸드오프`와 `작업 공간만 만들기`로 둡니다. 현재 런타임의 Question,
AskUserQuestion 등 구조화된 질문 도구를 우선하고, 사용할 수 없으면 같은 선택을 직접 묻습니다.
사용자가 첫 번째 선택에 명시적으로 동의하기 전에는 terminal을 만들거나 내용을 보내지 않습니다.
무응답이나 시간 경과를 동의로 취급하지 않습니다.

동의하면 새 worktree를 또 만들거나 `worktree create --agent`를 호출하지 않습니다. 생성 결과에서
얻은 exact full worktree id를 대상으로 현재 version-matched 가이드가 안내하는
`terminal create --worktree id:<full-id> --command <agent-command> --json` 흐름을 사용합니다.

- 이 스킬을 실행 중인 현재 대화의 provider와 model을 가용한 session metadata에서 각각
  확인합니다. 해당 provider가 effort 설정을 지원하고 현재 대화에서 사용한다면 effort도
  확인합니다. 같은 provider가 같은 model을 뜻한다고 가정하지 않습니다.
- 필요한 model이나 지원되는 effort 값을 알 수 없으면 누락된 값을 사용자에게 묻습니다. 현재
  CLI나 agent command가 요청한 설정을 지원하지 않으면 다른 model을 몰래 선택하지 말고 제약과
  선택지를 알립니다.
- repo가 만든 기본 terminal이나 setup terminal을 삭제하지 않습니다. 새 agent terminal의 정확한
  handle만 사용합니다.
- agent TUI에는 현재 가이드의 준비 상태 대기를 적용합니다. `tui-idle`을 지원하면 제한된 timeout과
  함께 기다린 뒤 내용을 보냅니다.
- handle이 stale이면 terminal 목록을 다시 읽고 교체된 handle 하나만 사용합니다. 이전 handle과
  새 handle에 같은 내용을 중복 전송하지 않습니다.

handoff 메시지는 새 agent가 대화를 다시 읽지 않아도 이어갈 수 있게 필요한 맥락만 요약합니다.

- 사용자의 목표와 범위
- 확정한 결정과 제약
- 현재 상태와 남은 작업
- 수행한 검증과 결과
- 관련 worktree 경로, branch, base와 commit
- 원래 worktree가 dirty였다면 그 변경과 파일은 새 checkout에 자동 복사되지 않았다는 사실과
  새 agent가 확인할 주의점

원문 대화를 파일로 저장하거나 저장소에 넣지 않습니다. 준비된 terminal의 정확한 handle에 위
요약을 `terminal send`로 한 번만 전송합니다. 성공 후 full handoff로 처리하고 원래 agent는
terminal을 감시하거나 후속 작업을 계속하지 않습니다.
