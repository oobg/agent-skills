# Orca 생성과 handoff

`orca-cli` resolver로 실행 파일을 선택하고 그 실행 파일의 version-matched 전체 가이드를 읽은
뒤 적용합니다. 현재 세션에서 확인한 명령과 JSON schema는 다시 탐색하지 않고 재사용합니다.

## worktree 생성

`worktree current --json` 또는 `repo list --json`에서 정확한 repo를 확인합니다. 독립 작업은
`--no-parent`, 명시된 stacked 작업은 `--parent-worktree active`로 생성합니다. 확정한 base를
`--base-branch`로 전달하고 `--json`을 사용합니다. agent handoff는 생성 뒤 선택받으므로
`--agent`와 `--prompt`를 넣지 않습니다.

응답 전체를 반복해서 읽지 않습니다. 성공 envelope인지 확인한 뒤 worktree의 exact full id,
path, branch를 한 번 파싱해 `scripts/new_space.py finalize --apply`에 전달합니다.

현재 Orca에는 공식 Git branch rename 명령이 없습니다. `finalize`는 생성 결과와 일치하는 새
linked worktree가 clean이고 base가 정확하며 target branch가 없을 때만 `git branch -m`을
수행합니다. 디렉터리명과 Orca display name은 바꾸지 않습니다. 이후 `worktree show`의
`branch`/`git.branch`와 `head`/`git.head`를 Git 결과와 대조합니다. 이 readback까지 통과해야
생성이 성공한 것으로 봅니다.

## 동의 후 handoff

Question에서 **시작하고 핸드오프**를 선택한 경우에만 생성된 worktree의 exact full id에 새
terminal을 만듭니다. 새 worktree를 다시 만들지 않고 기본 terminal도 삭제하지 않습니다.

이 스킬을 실행 중인 현재 대화의 provider와 model을 session metadata에서 확인해 같은 설정의
agent command를 사용합니다. provider가 effort를 지원하고 현재 값이 알려져 있으면 그대로
유지합니다. 현재 세션의 실효 metadata에서 `approval_policy`와 `sandbox_mode`도 확인하고,
Codex CLI가 지원하는 값이면 각각 `-a <approval_policy>`와 `-s <sandbox_mode>`로 전달합니다.
`never`, `danger-full-access`처럼 특정 값을 고정하거나 확인되지 않은 값을 추측하지 않습니다.
effort만 알 수 없다면 첫 Question에 “effort는 확인되지 않아 새 세션 기본값을 사용한다”는
사실을 함께 표시하고 두 선택지 중 하나를 받습니다. approval policy 또는 sandbox mode를 알
수 없거나 CLI가 해당 인자를 지원하지 않으면 그 사실을 handoff 확인에 함께 표시하고, 새
세션의 기본값을 사용할지 선택받습니다. 예를 들어
`workspace-write`만 전달할 수 있고 네트워크 허용이나 추가 쓰기 경로 같은 별도 제한을 표현할
수 없다면 mode만으로 완전한 권한 승계를 주장하지 않습니다. model 자체를 알 수 없으면 같은
model이라고 주장하지 말고 필요한 값만 묻습니다. 동의 뒤 같은 확인을 반복하지 않습니다.

현재 가이드에서 확인한 `terminal create --worktree id:<full-id> --command ... --json`을 실행하고
응답을 한 번 파싱해 정확한 새 handle을 얻습니다. `terminal wait --for tui-idle`이 성공하면
추가 `terminal read`로 준비 상태를 반복 추측하지 않고 같은 handle에 `terminal send`를 한 번만
실행합니다. stale handle이면 한 번 다시 조회해 교체된 handle만 사용하며 중복 전송하지 않습니다.

전달문에는 목표, 결정, 현재 상태, 남은 작업, 검증 결과, worktree·branch·base·commit을
요약합니다. 원래 worktree가 dirty였다면 그 변경이 새 checkout에 자동 복사되지 않았다는 점도
알립니다. 원문 대화를 파일로 저장하지 않습니다. 전송이 성공하면 full handoff로 처리하고 원래
agent는 새 agent를 감시하지 않고 종료합니다.
