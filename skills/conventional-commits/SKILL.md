---
name: conventional-commits
description: "실제 변경사항을 확인해 Conventional Commits 1.0.0 형식의 한국어 커밋 메시지, 커밋 분할안, PR 제목 또는 changelog 항목을 작성한다. '커밋해줘', '커밋 메시지', 'git commit', 'PR 제목', '릴리즈 노트', 'changelog'처럼 git 변경 이력을 표현하는 요청에 사용한다. 메시지 작성 요청만으로 git commit·push를 실행하지 않는다."
---

# Conventional Commits

변경 의도를 실제 diff에서 확인하고 Conventional Commits 1.0.0 형식으로 표현한다.
메시지 생성과 저장소 변경 권한을 분리한다.

## 먼저 범위를 판정한다

- **메시지 작성·검토**: 읽기 전용으로 diff와 최근 커밋 관례를 확인하고 텍스트만 반환한다.
- **커밋 실행**: 사용자가 현재 요청에서 명시적으로 커밋을 지시한 경우에만 실행한다.
- **PR 제목·릴리즈 노트·changelog**: 같은 헤더 형식을 저장소 관례로 적용할 수 있지만,
  이를 Conventional Commits 규격의 필수 범위라고 표현하지 않는다.
- **push**: 커밋 권한에 포함되지 않는다. 별도 명시가 있을 때만 실행한다.

## 변경을 근거로 메시지를 만든다

1. 저장소 지침과 `git status`를 확인한다.
2. staged diff와 unstaged diff를 구분해 읽는다. 사용자가 지정한 경로·커밋 범위를 우선한다.
3. 최근 커밋에서 scope와 메시지 관례를 확인하되, 실제 변경보다 관례를 우선하지 않는다.
4. type은 요청 문구가 아니라 사용자에게 발생하는 변화로 고른다.
   - 새 기능은 `feat`, 버그 수정은 `fix`, 동작 변화 없는 구조 개선은 `refactor`다.
   - 문서만 바뀌면 `docs`, 테스트만 바뀌면 `test`, 의존성·빌드 설정은 `chore` 또는
     더 구체적인 `build`를 사용한다.
5. scope는 선택 사항이다. 저장소에 안정된 모듈명이 없으면 만들지 않는다.
6. 독립된 의도가 여러 개면 커밋 분할안을 제안한다. 승인 없이 파일을 재배치하거나
   기존 커밋을 rewrite하지 않는다.

## 메시지 규칙

- 헤더는 `<type>[(scope)][!]: <설명>` 형식으로 쓴다. `:` 앞에는 공백을 두지 않고,
  뒤에는 한 칸을 둔다. `!`는 `:` 직전에 둔다.
- 설명은 변경 사항의 짧은 요약으로 쓰고 마침표·이모지를 붙이지 않는다.
- 설명과 본문, 본문과 꼬리말 사이에는 빈 줄을 한 줄 둔다.
- 본문은 필요할 때만 쓰며 무엇을 반복하기보다 왜 바꿨는지 설명한다.
- 꼬리말 토큰의 공백은 `-`로 바꾼다(`Reviewed-by`, `Co-Authored-By`, `Refs`).
  `BREAKING CHANGE`와 동의어 `BREAKING-CHANGE`는 예외다.
- 꼬리말 구분자는 `: ` 또는 ` #`를 사용한다. `Refs:#123`처럼 붙이지 않는다.
- 단절적 변경은 type과 무관하게 `!` 또는 `BREAKING CHANGE: `로 표시한다. `!`만
  쓰면 헤더 설명이 무엇이 깨지는지 직접 드러내야 한다. 둘은 함께 쓸 수 있다.

## 언어 규칙

- subject 설명·본문의 서술·꼬리말 설명은 한국어로 쓴다.
- type, scope, `BREAKING CHANGE` 같은 규격 토큰은 원형을 유지한다.
- 코드 식별자, 제품명, 파일 경로, 명령, SHA, 이슈 번호, 사람 이름과 이메일은
  번역하지 않는다. `Co-Authored-By` 값도 이 예외에 포함된다.

```text
feat(button): 합성 Button과 LinkButton 분리

렌더링 책임이 섞여 확장 시 분기 처리가 늘어나는 문제를 줄인다.

Refs: #123
```

## SemVer와 특수 경우

- `fix`는 PATCH, `feat`는 MINOR다.
- type과 무관하게 `!` 또는 `BREAKING CHANGE`가 있으면 MAJOR다.
- 그 외 type은 Conventional Commits 기준으로 SemVer 증가를 직접 뜻하지 않는다.
- 여러 type을 나눌 수 없으면 `BREAKING > feat > fix > 기타` 순으로 더 큰 영향을
  헤더에 두고 부가 변경은 본문에 적는다.
- revert는 `revert: <한국어 설명>`을 사용하고 되돌리는 SHA를 `Refs: <SHA>`로 남긴다.

## 실제 커밋 실행 가드

- 사용자가 소유하지 않은 변경이나 범위 밖 파일을 stage하지 않는다. `git add -A`를
  기본값으로 사용하지 않는다.
- stage 전후에 대상 경로와 cached diff를 확인한다. pathspec 오류의 stderr를 숨기지 않는다.
- 공유 워킹트리에서 다른 에이전트가 작업 중이거나 pre-commit hook이 stash·restore를
  수행할 수 있으면 커밋을 멈추고 안전한 시점을 확인한다.
- 커밋 직후 `git show --stat --oneline HEAD`와 `git status`를 확인해 의도한 파일과
  변경량만 포함됐는지 검증한다. 예상 밖의 0 insertions/deletions는 사고 신호로 본다.
- amend, rebase, reset, force-push는 사용자가 별도로 명시하지 않으면 실행하지 않는다.

## 출력

- 메시지만 요청받으면 바로 복사할 수 있는 메시지와, type/scope를 고른 근거를 짧게 준다.
- 분할이 필요하면 커밋별 파일 범위와 메시지 초안을 함께 제시한다.
- 실제 커밋을 실행했으면 SHA, 포함 파일, 검증 결과를 보고한다.
