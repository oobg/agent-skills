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
