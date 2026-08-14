# Agent Skills

AI 에이전트가 질문을 더 잘 설계하고, 사용자에게 보이는 문장과 변경 이력을 더
정확하게 쓰도록 돕는 스킬 모음입니다.

## 포함된 스킬

### Conventional Commits

실제 diff를 근거로 Conventional Commits 1.0.0 형식의 한국어 커밋 메시지와 커밋
분할안을 만듭니다. 명시적으로 요청받은 경우에만 커밋하며 push 권한은 분리합니다.

자세한 내용은
[`skills/conventional-commits/SKILL.md`](skills/conventional-commits/SKILL.md)에서
확인할 수 있습니다.

### Domain Ontology

회사·개인·공용 지식이나 과거 결정이 답을 바꿀 수 있을 때 온톨로지를 읽기 전용으로
조회합니다. 적재와 수정은 사용자 동의와 tenant 확인이 있을 때만 수행합니다.

### GPT Image Gen

Codex CLI의 gpt-image 플러그인으로 이미지를 생성합니다. 이미지 1장마다 사용량이
차감되므로 사용자가 `/gpt-image-gen`을 직접 입력했을 때만 동작합니다.

자세한 내용은
[`skills/gpt-image-gen/SKILL.md`](skills/gpt-image-gen/SKILL.md)에서 확인할 수 있습니다.

### Question Design

질문과 프롬프트를 다듬거나, 기획안, 전략, 분석 같은 결과물을 여러 관점에서
검토할 때 사용합니다.

- **MODE A — 질문 설계:** 질문의 전제와 범위를 점검하고 더 선명한 질문으로
  고칩니다.
- **MODE B — 리뷰 사이클:** 도메인 검토, 적대적 리뷰, 사고 확장, 흐름 통합을
  거쳐 결과물을 강화합니다.

자세한 내용은
[`skills/question-design/SKILL.md`](skills/question-design/SKILL.md)에서
확인할 수 있습니다.

### UX Writing

제품 UI와 문서의 문구를 명확하고 간결하게 다듬습니다. 버튼, 에러 메시지,
빈 상태, README, 코드 주석 등에 일관된 어투를 적용하고 번역투와 AI 특유의
표현도 함께 점검합니다.

- Clear, Concise, Casual, Respect, Emotional을 기본 기준으로 사용합니다.
- 프로젝트별 용어와 어체를 설정할 수 있습니다.
- 긴 글의 AI 문체, 번역투, 용어와 어체를 검사하는 스크립트를 제공합니다.

자세한 내용은 [`skills/ux-writing/SKILL.md`](skills/ux-writing/SKILL.md)에서
확인할 수 있습니다.


### Day0 Design

Day0 제품 UI(토스형 B2B)와 같은 시각 언어로 화면을 구현합니다. Pretendard,
톤다운 블루, 보더리스(plain 기본), `data-*` 상태 패턴, 바닐라 CSS 토큰을 강제합니다.

자세한 내용은 [`skills/day0-design/SKILL.md`](skills/day0-design/SKILL.md)에서
확인할 수 있습니다.

## 설치

Node.js가 설치된 환경에서 `skills` CLI를 사용합니다. 다음 명령을 실행하면
로컬에 설치된 에이전트를 탐지하고, 설치할 스킬과 대상을 선택할 수 있습니다.

```bash
npx skills add oobg/agent-skills --global
```

모든 스킬을 지원 대상에 바로 설치하려면 에이전트를 지정합니다.

```bash
npx skills add oobg/agent-skills \
  --global \
  --skill '*' \
  --agent claude-code \
  --agent codex \
  --agent gemini-cli \
  --agent grok \
  --yes
```

기본 설치 방식은 심볼릭 링크입니다. 심볼릭 링크를 지원하지 않는 환경에서는
`--copy` 옵션을 추가할 수 있습니다.

설치 상태 확인, 업데이트, 삭제에는 다음 명령을 사용합니다.

```bash
npx skills list --global
npx skills update --global
npx skills remove --global
```

`skills` CLI의 익명 텔레메트리를 끄려면 `DISABLE_TELEMETRY=1` 또는
`DO_NOT_TRACK=1` 환경 변수를 설정합니다.

## 구성

```text
agent-skills/
├── README.md
└── skills/
    ├── conventional-commits/
    │   ├── SKILL.md
    │   ├── README.md
    │   └── references/
    ├── day0-design/
    │   ├── SKILL.md
    │   ├── README.md
    │   └── references/
    ├── domain-ontology/
    │   ├── SKILL.md
    │   └── README.md
    ├── gpt-image-gen/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── references/
    │   └── scripts/
    ├── question-design/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── agents/
    │   └── references/
    └── ux-writing/
        ├── SKILL.md
        ├── README.md
        ├── agents/
        ├── references/
        └── scripts/
```

- `SKILL.md`: 스킬의 진입점과 적용 규칙
- `agents/`: 역할별 에이전트 지침
- `references/`: 조건에 따라 불러오는 상세 지침과 예시
- `scripts/`: 자동 검사 도구

## 온톨로지 보강 (선택)

각 스킬은 온톨로지 없이 완결됩니다. `~/.ontology/ontology.db`가 있으면
`references/ontology-boost.md`가 열려 축적된 지식을 그 스킬의 입력으로 씁니다.

| 스킬 | 온톨로지가 있을 때 달라지는 것 |
| --- | --- |
| Conventional Commits | scope 표기를 개념 이름에 맞추고, 본문의 `왜`를 과거 결정에서 가져옵니다 |
| GPT Image Gen | 프롬프트를 층으로 나누고 브랜드 자산을 회수합니다 |
| Question Design | 이미 판정된 제안을 리뷰가 다시 올리지 않고, 도메인 검토가 KB부터 봅니다 |
| UX Writing | 글로서리가 비었거나 임시 경로일 때 표기와 규칙을 회수합니다 |

보강 모듈은 입력만 바꿉니다. 각 스킬의 게이트, 판정 기준, 실행 권한은 그대로입니다.
회수 결과는 무엇을 봐야 하는지 알려줄 뿐 지금 상태의 증거가 아니므로, 회수한 내용을
근거로 고치기 전에 현재 상태를 확인합니다.

## 스킬 생명주기

`lifecycle.json`은 이 저장소를 스킬 정본으로 두고, 온톨로지의 최근 세션·스킬
관측치를 이용해 승격 후보와 주차 후보를 보여줍니다. 프로바이더 폴더에는 정본을
복사하지 않고 심볼릭 링크만 둡니다.

```bash
python3 scripts/skill_lifecycle.py report
python3 scripts/skill_lifecycle.py doctor
python3 scripts/skill_lifecycle.py sync          # dry-run
python3 scripts/skill_lifecycle.py sync --apply  # 명시적으로 링크 반영
```

자동으로 스킬을 생성하거나 상태를 바꾸지는 않습니다. `report`의 후보를 사람이
검토해 `candidate → active/pinned → parked/retired`로 바꾸고, `sync --apply`로
배포 상태를 맞춥니다. `parked`와 `retired`도 정본은 보존하며, 이 도구가 관리하지
않는 파일이나 외부 심링크는 삭제하지 않습니다.

## 요구 사항

스킬 문서는 별도 런타임 없이 사용할 수 있습니다. UX Writing의 검사 스크립트를
실행하려면 Python 3.8 이상이 필요합니다.

## 검증

스킬 frontmatter, 로컬 참조, README 자산 목록과 전체 회귀 테스트를 실행합니다.

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

## 라이선스

이 프로젝트는 [Apache License 2.0](LICENSE)에 따라 배포됩니다.
