---
name: new-space
description: "Use only when the user explicitly invokes /new-space to create an isolated Orca worktree for a new piece of work. Do not auto-trigger for ordinary branch or workspace discussion."
---

# 새 작업공간 (New Space)

`/new-space`가 호출되면 작업을 확인하고 `<type>/<slug>` branch와 Orca worktree를 만든다.
branch를 요청한 이름으로 보정하고 base를 검증한 뒤에만 agent handoff를 제안한다.

## 1. 무엇을 할 것인가

사용자가 호출과 함께 작업 내용을 적었으면 그대로 사용하고 다시 묻지 않는다. 작업 내용이
없을 때만 한 줄로 묻는다: **“무엇을 할 건가요?”**

## 2. branch를 분류한다

먼저 `scripts/context_cache.py project-get --repo <repo>`로 이 저장소에서 사용자가 기본값으로
확인한 선호를 읽는다. 실제로 사용한 정책 파일이 더 있으면 각각 `--policy-file`로 전달한다.
우선순위는 이번 요청의 명시적 선택, 현재 프로젝트 지침, 저장된 선호 순이다. 메모리가 없거나
정책 hash가 달라 stale이면 필요한 항목을 기존 branch/base 확인에 함께 묻는다. 사용자가
“앞으로 기본값으로 사용”할 뜻을 확인한 값만 `project-set --preferences-json <json>`으로 저장한다.
한 번의 작업 선택을 자동으로 기본값으로 승격하지 않는다.

저장 가능한 항목은 base 정책, branch 규칙, handoff 선호와 model 선호다. current worktree,
worktree id, terminal handle, 현재 세션의 approval policy와 sandbox mode는 저장하거나 권한의
근거로 재사용하지 않고 실행할 때마다 확인한다. 메모리는 저장소 밖 사용자 로컬 state에 두며
Git common directory가 같은 linked worktree끼리 공유한다.

사용자가 branch명을 지정했으면 우선한다. 그렇지 않으면 다음 기준으로 type을 고른다.

| type | 적용할 때 |
| --- | --- |
| `feat` | 없던 기능·화면·동작 추가 |
| `fix` | 잘못 동작하는 것 수정 |
| `refactor` | 동작을 유지하며 구조 개선 |
| `chore` | 의존성·설정·유지보수 작업 |
| `ci` | workflow·pipeline 변경 |
| `docs` | 문서만 변경 |

slug는 작업을 드러내는 영문 kebab-case 2~4단어로 만든다. 저장소가 별도 branch 규칙을 명시하면
그 규칙을 우선한다.

## 3. base를 정하고 한 번 확인한다

사용자가 base를 지정했으면 그대로 사용한다. 그렇지 않으면 저장소의 명시된 base 정책을
우선한다. 별도 정책이 없으면 remote의 기본 branch를 확인하고 같은 remote의 `release/*`를
검사해, 아직 기본 branch에 merge되지 않은 활성 release를 우선한다.

사용자나 저장소 정책이 특정 base를 정했다면 `preflight --base <exact-ref>`로 branch 충돌과
base SHA를 확인한다. 그 밖에는 다음 기본 정책을 적용한다.

1. 필요한 remote를 fetch하고 기본 branch ref를 확인한다. remote 이름이나 `main`을 확인 없이
   가정하지 않는다.
2. 설치된 스킬 디렉터리의 `scripts/new_space.py preflight`에 repo, 완성 branch,
   `--main-ref`와 같은 remote의 `--release-glob`을 전달한다.
3. 활성 release가 0개면 기본 branch, 1개면 그 release를 고른다. 2개 이상이면 release별
   선택지를 보여 주고 사용자가 고르게 한다.

완성된 branch와 base를 Question 계열 도구로 한 번에 확인한다. 추천안을 첫 번째 선택지에 두고
`(추천)`을 표시한다. 예: `feat/search-filter` (base: `release/1.2.0`). type 판단이 애매하면
대안 하나만 함께 제시한다. 사용자가 branch와 base를 이미 명시적으로 확정했다면 같은 확인을
반복하지 않는다.

preflight가 branch 충돌, 잘못된 ref 또는 모호한 base로 실패하면 생성하지 않는다. 출력된
`base_sha`는 생성 뒤 검증할 기준으로 보관한다.

## 4. Orca worktree를 만들고 보정한다

처음 Orca 명령을 쓰기 전에 `orca-cli` 스킬의 resolver로 실행 파일을 하나 선택하고
`references/orca.md`의 캐시 절차를 따른다. 유효한 cache hit이면 해당 version에서 검토해 둔
짧은 recipe를 사용한다. cache miss, 실행 파일·버전·stub·new-space 계약 변경 또는 Orca 명령
오류가 있으면 같은 실행 파일의 `skills get orca-cli --full --json` 원문을 새로 읽고 recipe를
갱신한다. 그 뒤 `status --json`을 확인하고 생성 절차를 따른다.

독립 작업은 `--no-parent`가 기본이다. 사용자가 현재 branch에서 이어지는 stacked 작업이라고
명시한 경우에만 `--parent-worktree active`를 사용한다. 생성 단계에서는 agent나 prompt를
붙이지 않는다.

생성 결과의 exact full worktree id, path와 실제 branch를 한 번 파싱한다. 다음 명령 한 번으로
Orca가 붙인 사용자 prefix와 slash 변환을 보정하고 base까지 검증한다.

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

`finalize`가 exit 0과 `ok: true`를 모두 반환해야 성공이다. dirty worktree, primary checkout,
기존 target branch, base 불일치, Git/Orca readback 불일치 중 하나라도 있으면 handoff로
진행하지 않는다. 실패를 일부 성공 필드로 대체해 해석하거나 reset·강제 삭제하지 않는다.

## 5. 보고하고 handoff를 묻는다

성공하면 먼저 세 줄로 보고한다.

- worktree 경로
- branch, base 이름과 SHA, branch 보정·검증 결과
- 다음에 할 일

그 다음 Question 계열 도구로 묻는다:

> 새 작업 공간에서 현재와 같은 AI 모델을 시작하고, 지금까지의 작업 내용을 넘길까요?

선택지는 **시작하고 핸드오프**와 **작업 공간만 만들기**다. 무응답은 동의가 아니다. 첫 번째를
고르면 `references/orca.md`의 handoff 절차를 따른다. 현재 세션에서 확인된 approval policy와
sandbox mode도 지원되는 Codex CLI 인자로 승계하며, 알 수 없거나 일부만 표현할 수 있으면
그 한계를 첫 handoff 확인에 함께 알리고 새 세션 기본값 사용 여부를 선택받는다. worktree를
다시 만들거나 승인 질문을 반복하지 않는다.

commit, push와 개발 서버 실행은 별도 요청이 있을 때만 한다.

## Orca를 사용할 수 없을 때

Orca 관리 컨텍스트에서는 다른 실행 파일이나 raw Git로 우회하지 않는다. Orca 비관리
저장소에서만, 사용자가 plain Git fallback을 선택하면 기록한 base SHA로 worktree를 만들고
Orca의 정리·terminal·browser 통합을 사용할 수 없음을 알린다.
