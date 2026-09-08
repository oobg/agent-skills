# Agent Skills

반복해서 쓰는 에이전트 작업 절차를 `SKILL.md`와 조건부 참조 문서로 관리하는
저장소입니다. 각 스킬은 언제 시작하고 멈출지, 어떤 근거를 확인할지, 어디까지
실행할지를 함께 정의합니다.

## 스킬

| 스킬 | 하는 일 |
| --- | --- |
| [conventional-commits](skills/conventional-commits/SKILL.md) | 실제 변경을 확인해 한국어 Conventional Commits 메시지, 커밋 분할안, PR 제목, changelog 항목을 작성합니다. |
| [dark-saas-design](skills/dark-saas-design/SKILL.md) | 다크 히어로와 라이트 본문을 잇는 한국어 B2B SaaS 랜딩, 소개, 요금 페이지를 구현합니다. |
| [day0-design](skills/day0-design/SKILL.md) | Day0의 타이포그래피, 색, 상태, 모션 규칙으로 제품 UI를 구현합니다. |
| [domain-ontology](skills/domain-ontology/SKILL.md) | 회사, 개인, 작업 방식, 과거 결정처럼 축적된 지식이 필요한 요청에서 온톨로지를 읽고 근거를 제시합니다. |
| [engineering-shorts](skills/engineering-shorts/SKILL.md) | 공학 설명 쇼츠를 대본, CLEAN 이미지, INFO 편집, 영상, 최종 검수 순서로 설계합니다. |
| [gpt-image-gen](skills/gpt-image-gen/SKILL.md) | `/gpt-image-gen`을 직접 호출했을 때만 이미지를 생성합니다. |
| [question-design](skills/question-design/SKILL.md) | 질문과 프롬프트의 전제와 범위를 다듬고 기획, 전략, 분석 문서를 여러 관점에서 검토합니다. |
| [resume-assistant](skills/resume-assistant/SKILL.md) | 지원자가 제공한 사실을 보존하면서 이력서와 경력기술서를 작성, 수정, 재구성합니다. |
| [resume-evaluator](skills/resume-evaluator/SKILL.md) | 이력서의 근거를 JD와 대조해 정보의 충분성, 불일치, 확인할 질문을 진단합니다. 채용 여부나 ATS 통과를 판정하지 않습니다. |
| [search-visibility](skills/search-visibility/SKILL.md) | SEO, AEO, GEO, LLMO, NEO 관점에서 검색과 답변 엔진 노출을 진단하고 고칩니다. |
| [ux-writing](skills/ux-writing/SKILL.md) | 제품 UI와 공개 문서의 의미와 보이스를 지키면서 문구를 다듬고 문체 검사를 제공합니다. |

`resume-assistant`는 문서를 만드는 스킬이고 `resume-evaluator`는 제공된 근거의
충분성을 진단하는 스킬입니다. 둘 다 수치나 역할을 지어내지 않으며 평가 결과를
채용 판정으로 바꾸지 않습니다. 동일 지원자의 과거 기록이 필요할 때만 각 스킬의
`references/ontology-boost.md`를 선택해서 입력을 보강할 수 있습니다. 온톨로지
조회는 판정 권한을 넓히거나 새 정보를 자동 저장하지 않습니다.

## 설치

Node.js 환경에서는 [공식 `skills` CLI](https://github.com/vercel-labs/skills)로
저장소의 스킬을 선택해 설치할 수 있습니다.

```bash
npx skills add oobg/agent-skills --global
```

대화형 선택 없이 설치할 때는 스킬과 에이전트를 명시합니다.

```bash
npx skills add oobg/agent-skills \
  --global \
  --skill ux-writing \
  --agent codex \
  --yes
```

`--skill '*'`과 여러 `--agent`를 함께 지정할 수도 있습니다. 설치할 때 심볼릭
링크를 선택하거나 `--copy`로 파일을 복사할 수 있습니다.

```bash
npx skills list --global
npx skills update --global
npx skills remove --global
```

저장소를 clone한 것만으로 에이전트에 스킬이 설치되지는 않습니다. 특히
`resume-assistant`와 `resume-evaluator`는 현재 `lifecycle.json`의 프로바이더
동기화 대상에 등록되어 있지 않으므로, 위 `skills` CLI에서 직접 선택해야 합니다.

## 저장소 구조

각 `skills/<name>/SKILL.md`가 스킬의 진입점입니다. 같은 디렉터리의 `README.md`는
구성과 자산 목록을 설명합니다. 스킬은 필요할 때만 아래 자료를 더 읽습니다.

```text
skills/<name>/
├── SKILL.md       # 발동 조건, 절차, 경계
├── README.md      # 공개 안내와 자산 목록
├── agents/        # 역할별 지침
├── references/    # 조건부 규칙과 예시
└── scripts/       # 검사와 보조 도구
```

일부 스킬에는 선택형 온톨로지 보강 모듈이 있습니다. 온톨로지가 없어도 스킬의
기본 절차는 동작합니다. 조회한 지식은 확인할 대상을 알려 주는 입력이며, 현재
상태를 확인한 증거로 대신 쓸 수 없습니다. 적재나 수정에는 별도의 사용자 동의와
문서별 tenant 확인이 필요합니다.

## 스킬 생명주기

`lifecycle.json`은 이 저장소의 스킬을 프로바이더 디렉터리에 심볼릭 링크로
배치하기 위한 로컬 설정입니다. 현재 등록된 스킬의 상태와 대상만 관리하며,
등록되지 않은 스킬을 자동으로 설치하지 않습니다.

```bash
python3 scripts/skill_lifecycle.py report
python3 scripts/skill_lifecycle.py doctor
python3 scripts/skill_lifecycle.py sync          # 변경 계획만 출력
python3 scripts/skill_lifecycle.py sync --apply  # 링크를 실제 반영
```

`report`와 `doctor`는 상태를 확인합니다. `sync`는 기본적으로 dry-run이며,
`--apply`를 붙인 경우에만 관리 대상 링크를 바꿉니다. 이 도구는 온톨로지를
읽기 전용으로 열고, 저장소 밖의 일반 파일이나 자신이 관리하지 않는 링크를
수정하지 않습니다.

## 검증

공개 clone에서는 구조 검사와 전체 단위 테스트를 실행할 수 있습니다. 구조 검사는
frontmatter, 설치 가능한 스킬 이름, 로컬 참조, 각 스킬 README의 자산 목록을 확인합니다. 로컬 평가 suite가
필요한 테스트는 자료가 없으면 건너뜁니다.

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

정적 계약 suite와 트리거 평가는 로컬 `evals/` 자료가 있을 때만 실행합니다. 이
디렉터리는 git에서 제외되어 있습니다.

```bash
python3 scripts/eval_skill_contracts.py --suite evals/static-contracts.json
```

정적 계약 검사는 규칙이 문서에 적혀 있는지 확인합니다. 실제 에이전트가 그
규칙에 맞춰 스킬을 발동했는지는 별도의 트리거 루프로 확인합니다.

```bash
python3 scripts/trigger_misfire_audit.py --tenant shared \
  --db ~/.ontology/ontology.db \
  --cases evals/trigger-cases.json
python3 scripts/eval_trigger_cases.py --cases evals/trigger-cases.json
python3 scripts/eval_trigger_cases.py --cases evals/trigger-cases.json --run \
  --command-json '["<agent>", "<transcript-isolation-option>", "<prompt-option>", "{request}"]' \
  --output-format text

# Claude CLI 예시
python3 scripts/eval_trigger_cases.py --cases evals/trigger-cases.json --run \
  --command-json '["claude", "-p", "--no-session-persistence", "{request}"]'
python3 scripts/trigger_revisions.py list
python3 scripts/trigger_revisions.py add --skill domain-ontology \
  --reason "트리거 경계를 바로잡는다" \
  --changed "조회 조건을 명확히 한다"
python3 scripts/trigger_revisions.py score \
  --skill domain-ontology --score 3/5
```

- `trigger_misfire_audit.py`는 온톨로지 요청 로그를 읽기 전용으로 확인해 사용자가
  조회를 직접 요청한 빈도를 셉니다. 이 수치만으로 실제 미발동을 증명하거나 전체
  미발동의 하한을 구할 수는 없습니다. 제외할 케이스 파일이 없으면 중단하므로 다른 경로를 지정하거나,
  시험 실행을 함께 세려는 경우에만 `--no-exclude`를 사용합니다.
- `eval_trigger_cases.py`는 기본 실행에서 케이스와 예상 세션 수만 보여 줍니다.
  `--run`은 케이스마다 실제 에이전트 세션을 열어 사용량을 차감합니다.
- 실행기는 특정 provider CLI를 가정하지 않습니다. `--command-json`에 실행 파일과 옵션을
  argv JSON 배열로 넘기고, 요청이 들어갈 `{request}`를 정확히 한 번 둡니다. 사용하는
  provider가 transcript 비저장 옵션을 지원하면 같은 배열에 직접 넣습니다. 외부 훅,
  별도 로그, 온톨로지 적재 여부까지 검증하거나 보장하지는 않습니다. JSON 리포트에는
  응답 원문과 명령 인자를 저장하지 않습니다.
- stdout이 JSON이면 `--output-format json --json-result-field <field>`로 최종 답변이 든
  top-level 문자열 필드를 지정합니다. 지정하지 않은 JSON 객체 전체나 진단 필드는 채점하지 않습니다.
- 채점은 답변의 `근거:` 줄을 조회 흔적으로 보는 대리 지표입니다. 실제 조회를
  독립적으로 증명하지 않으므로 오탐과 누락이 생길 수 있습니다.
- `trigger_revisions.py`의 개정 이력과 `eval_trigger_cases.py`의 실행 리포트는
  기본적으로 ignored `evals/` 아래에 남습니다. `--log`나 `--out`으로 다른 경로를
  지정하면 해당 경로의 공개 여부를 따로 확인해야 합니다.

## 공개 데이터 경계

이 저장소에는 재사용 가능한 지침, 코드, 합성 예시만 둡니다. 실제 이력서,
연락처, 경력, 회사나 고객 기밀, 원문 대화, 평가 입력과 로그는 저장소 밖이나
ignored `evals/`에 보관합니다. 예시는 실자료에서 이름만 바꾸지 않고, 추적 가능한
고유명사와 수치를 제거한 합성 데이터로 작성합니다. 문서의 경로 예시는 `~/...`나
`<placeholder>`를 사용합니다.

## 요구 사항

스킬 문서는 별도 런타임 없이 읽을 수 있습니다. 저장소의 Python 검사 도구는
Python 3.8 이상을 사용하며, 구조 검사는 `requirements-dev.txt`의 PyYAML이 필요합니다.
이미지 생성처럼 외부 도구가 필요한 스킬의 요구 사항은 해당 스킬 문서에서 확인할 수 있습니다.

## 라이선스

이 프로젝트는 [Apache License 2.0](LICENSE)에 따라 배포됩니다.
