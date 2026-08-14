# GPT Image Gen

Codex CLI의 gpt-image 플러그인으로 이미지를 생성하는 얇은 래퍼 스킬입니다. 생성 지능은
플러그인이 담당하고, 이 스킬은 호출 게이트와 저장 경로, 결과 보고만 맡습니다.

## 명시 호출 전용

이미지 1장마다 사용자의 ChatGPT/Codex 사용량이 차감됩니다. 그래서 이 스킬은 사용자가
`/gpt-image-gen <이미지 설명>`을 직접 입력했을 때만 동작합니다.

- 동작합니다: `/gpt-image-gen 프랜차이즈 대시보드 히어로 배너`
- 동작하지 않습니다: "이미지 만들어줘", "여기 그림 넣자", 문서 작업 중 이미지가 있으면
  좋아 보이는 경우

프롬프트 없이 명령만 입력하면 추측해서 생성하지 않고 어떤 이미지를 원하는지 되묻습니다.

## 출력

- 위치: 현재 작업 디렉터리의 `./generated-images/`
- 파일명: `img[-라벨]-<타임스탬프>-<고유ID>.png`
- 배경: 사용자가 배경을 지정하지 않으면 배경을 제거한 이미지로 생성합니다.
- 성공하면 마지막 줄에 `SAVED <절대경로>`를 출력합니다.

여러 장이 필요하면 서브에이전트가 `--label`을 다르게 주어 병렬로 호출해도 됩니다.
호출마다 PID와 난수로 만든 고유 ID가 붙어 파일명과 로그가 겹치지 않습니다. 다만 병렬
N건이면 사용량도 약 N배이므로 대량 생성 전에 규모를 확인하세요.

## 요구 사항

- Codex CLI 설치와 `codex login`(ChatGPT 계정)
- `codex features list`에서 `image_generation`이 `stable true`
- Bash 3.2 이상. macOS 기본 `/bin/bash`(3.2)에서 정상 경로와 폴백 경로 모두 확인했습니다.

## 프롬프트가 실행 권한을 만납니다

프롬프트는 codex 에이전트의 지시문에 그대로 들어갑니다. 붙여넣은 텍스트 안에 지시문처럼
읽히는 문장이 있으면 그것도 에이전트가 읽습니다. 쓰기 범위는 `--sandbox workspace-write`와
`--add-dir`로 작업 폴더에 한정했지만, 출처를 모르는 텍스트를 그대로 넘기지 마세요.

## 온톨로지 보강 (선택)

`~/.ontology/ontology.db`가 있으면 프롬프트를 층으로 나누는 방법과 브랜드 자산을
회수할 수 있습니다. 온톨로지가 없어도 스킬은 그대로 동작하며, 보강 모듈이 비용 게이트나
출력 규약을 바꾸지 않습니다.

## 구성

```text
gpt-image-gen/
├── SKILL.md
├── README.md
├── references/
│   └── ontology-boost.md
└── scripts/
    └── generate.sh
```

- [`SKILL.md`](SKILL.md): 호출 게이트, 동작 순서, 출력 규약, 문제 해결
- [`references/ontology-boost.md`](references/ontology-boost.md): 온톨로지가 있을 때만 여는
  프롬프트 계층 설계와 브랜드 자산 회수
- [`scripts/generate.sh`](scripts/generate.sh): 프롬프트 파싱, codex 호출, 결과 확인

설치 방법은 저장소의 [루트 README](../../README.md)를 참고하세요.
