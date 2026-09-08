---
name: new-space
description: "Orca에서 새 작업용 Git worktree를 만들고 요청한 branch와 base에서 정확히 시작했는지 검증한다. '/new-space', '새 작업공간', 'Orca 워크트리 만들어줘', '브랜치 새로 따자'처럼 격리된 작업공간 생성을 명시적으로 요청할 때 사용한다. 단순 브랜치 전환이나 기존 worktree 이동에는 사용하지 않는다."
---

# New Space

새 작업의 branch와 base를 확정하고 Orca 관리 worktree를 만든다. 정책 판단과 사용자 질문은
직접 수행하고, 반복적인 Git 상태 확인과 결과 검증에는 `scripts/new_space.py`를 사용한다.
명령 예시의 script 경로는 현재 저장소가 아니라 설치된 이 스킬 디렉터리를 기준으로 해석한다.

## Orca 정본을 먼저 읽는다

Orca 실행 파일을 `orca-cli` 스킬의 resolver 규칙으로 한 번 선택한다. 같은 실행 파일로
`skills get orca-cli`를 실행해 현재 버전의 전체 가이드를 끝까지 읽고 `status --json`으로
runtime을 확인한다. `references/orca.md`의 생성 절차는 이 확인을 마친 뒤 적용한다. 기억이나
이 문서만으로 CLI 명령과 JSON shape를 추측하지 않는다.

## 작업 이름을 정한다

사용자가 작업 내용을 이미 설명했으면 다시 묻지 않는다. 내용이 없으면 무엇을 할지 한 줄로
묻는다. 저장소의 branch 규칙이 있으면 우선하고, 없으면 작업 성격에 맞는 type과 영문
kebab-case slug를 제안한다. 일반적인 type 후보는 `feat`, `fix`, `refactor`, `chore`, `ci`,
`docs`지만 저장소가 다른 체계를 쓰면 강제하지 않는다.

## base를 정한다

사용자가 명시한 base를 최우선으로 사용한다. 그렇지 않으면 저장소의 `AGENTS.md`, 기여 문서,
Orca repo 설정과 remote ref에서 base 정책을 찾는다. remote 이름이나 기본 branch를 가정하지
않는다.

저장소가 “기본 branch에 아직 merge되지 않은 release branch를 우선한다”는 정책을 실제로
쓸 때는 아래처럼 검사한다. `--main-ref`와 `--release-glob`에는 확인한 remote ref를 전달한다.

```text
python3 scripts/new_space.py preflight \
  --repo <repository> \
  --branch <branch> \
  --main-ref <remote>/<default-branch> \
  --release-glob '<remote>/release/*'
```

활성 release가 0개면 main ref, 1개면 해당 release를 선택한다. 2개 이상이면 자동 추측하지
않고 사용자가 고르게 한다. 이런 release 정책이 없는 저장소에서는 확정한 `--base`를 직접
전달한다. 최신 remote 상태가 필요하면 대상 remote를 특정해 fetch한 뒤 preflight를 다시
실행한다. preflight는 fetch하거나 저장소를 변경하지 않는다.

branch, base와 lineage를 함께 확정한다. 독립 작업은 `--no-parent`, 현재 작업에서 이어지는
stacked 작업은 `--parent-worktree active`다. 명확한 값은 재확인하지 않으며 base나 lineage가
모호해 시작점이 달라질 때만 질문한다.

## 생성하고 검증한다

`references/orca.md`에 따라 Orca로 생성한다. 이 단계에서는 `--agent`와 `--prompt`를 쓰지
않는다. worktree를 먼저 생성하고 검증한 뒤 agent handoff 여부를 별도로 묻는다. 사용자가
요청하지 않은 `--activate`나 강제 setup 실행 옵션도 추가하지 않는다. 저장소의 기본 setup과
terminal 정책은 생성 과정의 일부일 수 있으므로 생성 전에 현재 repo 설정을 확인하고 알려
준다. 자동 실행을 막아야 하고 현재 CLI가 지원하면 `--setup skip`을 사용한다.

생성 전에 원래 worktree의 branch, HEAD와 dirty 여부를 기록한다. dirty 상태여도 stash, stage,
reset, checkout 또는 파일 변경을 하지 않는다. 생성 뒤 같은 값을 다시 확인하며 원래 worktree의
상태를 복원하려고 다른 사용자의 변경을 건드리지 않는다.

Orca 결과에서 실제 worktree path와 branch를 읽는다. Orca가 요청 이름에 사용자 prefix를
붙이거나 slash를 hyphen으로 바꿀 수 있으므로 요청 branch와 같다고 가정하지 않는다.

```text
python3 scripts/new_space.py verify \
  --worktree <created-path> \
  --expected-branch <branch> \
  --base-sha <preflight-base-sha>
```

branch가 달라졌다면 현재 버전 가이드에서 Orca metadata와 Git을 함께 안전하게 갱신하는 방법을
찾는다. 확인된 방법이 있을 때만 요청 branch로 바꾸고 verify를 다시 실행한다. 현재 조회한
가이드에 정확 branch 지정이나 metadata-safe rename이 없다면 raw `git branch -m`을 맹목적으로
실행하지 말고 실제 branch와 원하는 branch의 차이를 보고한다. worktree 디렉터리명은 branch
교정 때문에 바꾸지 않는다.

검증은 생성 직후 HEAD와 preflight에서 기록한 base SHA가 같은지 확인한다. ahead와 behind가
모두 0이어야 한다. 어긋나면 reset으로 맞추거나 생성된 항목을 강제 삭제하지 않는다.

## agent handoff를 선택하게 한다

생성과 검증이 성공하면 `references/orca.md`의 handoff 절차를 읽는다. 런타임이 제공하는
Question 또는 AskUserQuestion 같은 질문 도구로 다음 선택을 한 번 묻는다. 질문 도구가 없으면
같은 내용을 직접 묻는다.

- **시작하고 핸드오프**: 새 작업공간에서 이 스킬을 실행 중인 현재 대화와 같은 AI model과
  effort의 agent를 시작하고 지금까지의 작업 내용을 넘긴다.
- **작업 공간만 만들기**: agent나 terminal을 추가하지 않고 끝낸다.

명시적으로 첫 번째 선택을 받기 전에는 agent를 실행하거나 내용을 전송하지 않는다. 무응답은
승인이 아니다. 동의하면 새 worktree를 다시 만들지 않고 방금 생성한 worktree의 exact full id를
사용한다. 전달을 마치면 full handoff로 처리해 현재 agent는 새 agent를 감시하거나 작업을 계속하지
않는다.

## Orca를 사용할 수 없을 때

Orca 관리 컨텍스트에서 선택한 실행 파일이나 runtime이 실패하면 다른 Orca 실행 파일이나 raw
`git worktree add`로 우회하지 않는다. 오류를 그대로 보고한다. Orca 비관리 저장소에서만,
사용자가 plain Git fallback을 선택하면 확정한 base SHA로 별도 worktree를 만들 수 있다. 이때
Orca의 정리, terminal, browser 통합을 사용할 수 없음을 알리고 기존 branch나 경로를 덮어쓰지
않는다.

## 완료 보고

worktree 경로, 실제 branch, base 이름과 SHA, branch rewrite 여부를 간결하게 보고한다.
handoff를 선택했다면 시작한 model과 전달 성공 여부도 알린다. commit, push와 개발 서버 실행은
별도 요청이 있을 때만 수행한다.
