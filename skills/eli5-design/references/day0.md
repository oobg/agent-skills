# day0 — day0-design 의존

시각 언어는 형제 스킬 `day0-design`이 정본이다. 이 스킬은 토큰 값을 갖지 않는다. 토큰을 인라인할 때(작업 순서 7번) 이 파일을 연다.

## 탐색 순서

아래 순서로 찾아 처음 발견한 `day0-design`을 쓴다. 이 순서의 정본은 이 절뿐이다.

1. 로컬 형제 경로 `../day0-design/` (이 스킬 디렉터리 기준).
2. 전역 스킬 디렉터리. 순서대로 확인해 처음 `day0-design/SKILL.md`가 있는 곳을 쓴다.
   `~/.agents/skills/day0-design/` (skills CLI 공용 위치), `~/.claude/skills/day0-design/`,
   `~/.codex/skills/day0-design/`, `~/.gemini/skills/day0-design/`, `~/.grok/skills/day0-design/`.
   예시 목록이며, 현재 호스트의 전역 스킬 디렉터리가 여기 없으면 그것을 우선 포함한다.
3. 공개 저장소 원본. 디렉터리는 https://github.com/oobg/agent-skills/tree/main/skills/day0-design 이고,
   파일은 raw 경로로 읽는다.
   - https://raw.githubusercontent.com/oobg/agent-skills/main/skills/day0-design/SKILL.md
   - https://raw.githubusercontent.com/oobg/agent-skills/main/skills/day0-design/references/tokens.css
   - https://raw.githubusercontent.com/oobg/agent-skills/main/skills/day0-design/references/anti-patterns.md
   - 필요하면 https://raw.githubusercontent.com/oobg/agent-skills/main/skills/day0-design/references/patterns.md
4. 모두 실패하면(경로 없음, 네트워크 불가, 404 등) 토큰을 추측하거나 하드코딩하지 않는다.
   "day0-design을 찾지 못해 진행할 수 없다"고 알리고 멈춘다. 다른 시각 언어로 바꿔 만들지 않는다.

어느 출처를 썼는지(형제 경로, 전역 경로명, 원격 원본) 사용자에게 한 줄 알린다.
어느 출처든 day0-design 디렉터리 기준 같은 상대 경로의 파일을 읽는다.

## 쓰는 법

- 토큰: `day0-design/references/tokens.css` **파일 전체를 수정 없이** 메인 `<style>` 맨 앞에 붙여 넣는다.
  토큰을 외부 `<link>`로 걸지 않는다(artifact CSP 차단, 발행 후 소리 없는 변경, 오프라인 깨짐).
  파일 머리 주석(출처 경로·메모)도 원문 그대로 둔다. 예시 데이터의 "실제 회사·제품 이름 금지"는 페이지 내용에 대한 규칙이라 이 주석에는 적용하지 않는다.
- 규칙: day0-design `SKILL.md`의 스택 규칙·컴포넌트 원칙을 따른다.
- **우선순위.** 설명 페이지의 타이포 스케일(h1 32 / h2 20 / 본문 15, 설명 문단 행간 1.65, 원칙 9번·[blocks/shell.md](blocks/shell.md) 타이포 스케일)과 페이지 여백은 이 스킬 값이
  day0-design보다 우선한다. 색·radius·모션·컴포넌트 규칙은 day0-design을 따른다.
- 금지: `day0-design/references/anti-patterns.md`를 함께 적용한다.
