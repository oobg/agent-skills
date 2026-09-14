---
name: new-space
description: "Use only when the user explicitly invokes /new-space to create an isolated Orca worktree or folder workspace for a new piece of work. Do not auto-trigger for ordinary branch or workspace discussion."
---

# 새 작업공간 (New Space)

`/new-space`가 호출되면 현재 프로젝트를 Git 기반과 Orca folder 기반 중 하나로 먼저 판정한다.
Git 프로젝트에는 branch/base를 검증한 Orca linked worktree를 만들고, folder 또는 non-Git
프로젝트에는 branch 없는 Orca folder workspace를 만든다. 두 경로 모두 생성 결과를 검증한
뒤에만 agent handoff를 제안한다.

## 1. 작업과 프로젝트 종류를 확인한다

사용자가 작업 내용을 적었으면 그대로 사용하고 다시 묻지 않는다. 없을 때만 **“무엇을 할
건가요?”**라고 한 줄로 묻는다. 작업을 드러내는 영문 kebab-case 2~4단어를 task name으로 만든다.

Orca 명령을 처음 쓰기 전에 `orca-cli` 스킬의 resolver로 실행 파일을 하나 선택하고
`references/orca.md`의 캐시 절차를 따른다. 유효한 cache hit이면 version-matched recipe를
사용한다. cache miss, 실행 파일·버전·stub·new-space 계약 변경 또는 명령 오류가 있으면 같은
실행 파일의 `skills get orca-cli --full --json` 원문을 읽고 recipe를 갱신한다. 그 뒤
`status --json`을 확인한다.

현재 프로젝트 절대 경로의 Git top level과 `orca repo list --json`의 exact path 및 repo
`kind`를 확인한다.

- Git top level 안에 있으면 기본 checkout을 포함해 **Git 기반**으로 판정하고 2~4절을 따른다.
- Git 저장소가 아니고 exact path의 repo가 `kind: folder`이면 **folder 기반**으로 판정하고
  5절만 따른다.
- Git 저장소가 아니며 등록되지 않은 경로는 folder 후보로 판정하고 5절에서 등록한다.
- 같은 경로의 종류가 충돌하거나 non-Git 경로가 Orca에서 Git repo로 readback되면 중단한다.

folder 경로에는 branch/base 질문, branch 선호 조회, Git preflight와 Git workspace 생성·변경
명령을 사용하지 않는다. 프로젝트 종류 판정을 위한 읽기 전용 Git 감지만 허용한다.

## 2. Git 프로젝트의 branch를 분류한다

`scripts/context_cache.py project-get --repo <repo>`로 사용자가 기본값으로 확인한 선호를 읽는다.
실제로 사용한 정책 파일은 각각 `--policy-file`로 전달한다. 우선순위는 이번 요청의 명시적 선택,
현재 프로젝트 지침, 저장된 선호 순이다. 메모리가 없거나 정책 hash가 달라 stale이면 필요한
항목을 branch/base 확인에 함께 묻는다. 사용자가 “앞으로 기본값으로 사용”할 뜻을 확인한 값만
`project-set --preferences-json <json>`으로 저장한다. 한 번의 선택을 기본값으로 승격하지 않는다.

저장 가능한 항목은 base 정책, branch 규칙, handoff와 model 선호다. current worktree, worktree
id, terminal handle, approval policy와 sandbox mode는 저장하거나 권한 근거로 재사용하지 않는다.

사용자가 branch명을 지정했으면 우선한다. 그렇지 않으면 다음 기준으로 type을 고른다.

| type | 적용할 때 |
| --- | --- |
| `feat` | 없던 기능·화면·동작 추가 |
| `fix` | 잘못 동작하는 것 수정 |
| `refactor` | 동작을 유지하며 구조 개선 |
| `chore` | 의존성·설정·유지보수 작업 |
| `ci` | workflow·pipeline 변경 |
| `docs` | 문서만 변경 |

slug는 task name을 사용하며 저장소의 별도 branch 규칙이 있으면 우선한다.

## 3. Git 프로젝트의 base를 정하고 한 번 확인한다

사용자가 base를 지정했으면 그대로 사용한다. 아니면 저장소 정책을 우선하고, 별도 정책이 없으면
remote 기본 branch와 같은 remote의 `release/*` 중 아직 기본 branch에 merge되지 않은 활성
release를 확인한다. remote 이름이나 `main`을 확인 없이 가정하지 않는다.

명시된 base에는 `preflight --base <exact-ref>`를 사용한다. 기본 정책에는 완성 branch,
`--main-ref`, 같은 remote의 `--release-glob`을 전달한다. 활성 release가 0개면 기본 branch,
1개면 해당 release를 고르고, 2개 이상이면 선택받는다. 완성 branch와 base를 Question 계열
도구로 한 번에 확인하며 추천안에 `(추천)`을 표시한다. 이미 둘 다 확정했으면 반복하지 않는다.

preflight가 branch 충돌, 잘못된 ref 또는 모호한 base로 실패하면 생성하지 않는다. 출력된
`base_sha`는 생성 뒤 검증 기준으로 보관한다.

## 4. Git Orca worktree를 만들고 보정한다

독립 작업은 `--no-parent`가 기본이다. 사용자가 stacked 작업이라고 명시한 경우에만
`--parent-worktree active`를 사용한다. 확정한 base는 `--base-branch`로 전달하고 생성 단계에는
agent나 prompt를 붙이지 않는다.

생성 결과의 exact full id, path와 실제 branch를 한 번 파싱하고 다음 명령으로 Orca가 붙인
prefix와 slash 변환을 보정하면서 base까지 검증한다.

```text
python3 <skill-directory>/scripts/new_space.py finalize \
  --worktree <created-path> \
  --worktree-id <full-worktree-id> \
  --created-branch <actual-created-branch> \
  --expected-branch <confirmed-branch> \
  --base-sha <preflight-base-sha> \
  --orca-executable <selected-executable> \
  --apply
```

exit 0과 `ok: true`가 모두 필요하다. dirty worktree, primary checkout, 기존 target branch,
base 불일치, Git/Orca readback 불일치가 있으면 handoff로 진행하지 않는다. 실패를 일부 성공
필드로 대체하거나 reset·강제 삭제하지 않는다.

## 5. Orca folder workspace를 만들고 검증한다

`orca repo list --json`에서 현재 프로젝트의 exact absolute path와 `kind: folder`인 repo id를
찾는다. 등록되지 않았으면 한 번 등록한다.

```text
orca repo add --path <absolute-folder> --json
```

응답만 신뢰하지 않고 `orca repo list --json`을 다시 읽어 exact path, `kind: folder`, repo id를
확인한다. folder 등록을 지원하지 않거나 다른 kind로 readback되면 중단한다.

독립 작업은 다음과 같이 생성한다. folder 경로에는 `--base-branch`를 붙이지 않는다.

```text
orca worktree create --repo id:<repo-id> --name <task-name> --no-parent --json
```

사용자가 stacked/parent 작업을 명시한 경우에만 version-matched 가이드에서 확인한 parent 옵션을
`--no-parent` 대신 사용한다. 생성 단계에는 agent나 prompt를 붙이지 않는다. 성공 응답에서
exact full id와 path를 한 번 파싱한 뒤 다음 read-only helper로 검증한다.

```text
python3 <skill-directory>/scripts/new_space.py workspace-verify \
  --worktree <created-path> \
  --repo-id <repo-id> \
  --worktree-id <exact-full-worktree-id> \
  --orca-executable <selected-executable>
```

exit 0, `ok: true`, `workspace_kind: folder`가 모두 필요하다. helper는 같은 Orca 실행 파일로
`repo show`와 `worktree show`를 호출해 exact repo id/path, `kind: folder`, worktree의 exact full
id/path와 `repoId`, `isMainWorktree: false`, 빈 `branch`/`head`와 빈 `git.branch`/`git.head`를
검사한다. Git worktree 상태가 나오거나 하나라도 다르면 handoff로 진행하지 않는다.

기본 `--path-host local`은 helper 실행 호스트에서 workspace path가 실제 디렉터리인지 확인한다.
paired remote host의 경로를 로컬 helper가 볼 수 없다는 사실을 확인한 경우에만 `--path-host remote`를
추가한다. 이때 worktree `hostId`가 문자열이고 `local`이 아닌지 확인한 뒤 로컬 존재 검사를
생략하고 서로 일치하는 repo/worktree readback을 권위로 삼는다.

## 6. 보고하고 handoff를 묻는다

성공하면 workspace 경로와 exact full id, Git이면 branch/base SHA와 보정 결과, folder이면
`kind: folder` 검증 결과, 다음 할 일을 보고한다. 그 뒤 Question 계열 도구로 묻는다.

> 새 작업 공간에서 현재와 같은 AI 모델을 시작하고, 지금까지의 작업 내용을 넘길까요?

선택지는 **시작하고 핸드오프**와 **작업 공간만 만들기**다. 무응답은 동의가 아니다. 첫 번째를
고르면 `references/orca.md`의 절차에 따라 Git과 folder 모두 생성·검증에 사용한 같은 exact
full id로 handoff한다. 확인된 approval policy와 sandbox mode도 지원되는 Codex CLI 인자로
승계하며, 알 수 없거나 일부만 표현할 수 있으면 그 한계를 함께 알리고 새 세션 기본값 사용 여부를
선택받는다. workspace를 다시 만들거나 승인 질문을 반복하지 않는다.

commit, push와 개발 서버 실행은 별도 요청이 있을 때만 한다.

## Orca를 사용할 수 없을 때

프로젝트 종류와 관계없이 다른 실행 파일, raw Git 또는 `git worktree add`로 우회하지 않는다.
Orca가 folder workspace 생성이나 필요한 readback을 지원하지 않으면 외부 상태를 더 바꾸지 않고
중단해 원인을 보고한다.
