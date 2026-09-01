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

스크립트가 유료 호출을 내보내기 **전에** 이 세 가지를 직접 점검합니다. 점검에서 막히면 아직
사용량이 차감되지 않은 상태이므로, 안내대로 고친 뒤 다시 실행하면 됩니다. 단 `image_generation`
점검은 알려진 나쁜 상태만 막습니다 — 목록에 플래그가 없거나 명령이 실패하면 판정 불가로 보고
통과시킵니다.

호출이 실패하면 출력에 `원인 추정` 한 줄이 붙습니다. 인증, 사용량 한도, 권한, 시간 초과,
샌드박스, 네트워크로 갈립니다. 로그를 훑은 추측이므로 함께 표시되는 로그 원문이 우선입니다.

## 왜 REST API가 아니라 codex exec인가

`~/.codex/auth.json`의 ChatGPT OAuth 액세스 토큰으로는 OpenAI REST API를 직접 부를 수 없습니다.
토큰이 유효하지 않아서가 아니라 이미지 스코프가 없어서입니다 — `POST /v1/images/generations`는
`Missing scopes: api.model.images.request`로 거부됩니다(codex-cli 0.151.0, 2026-09-01 실측).
상태 코드는 엔드포인트마다 401과 403으로 갈리므로 코드가 아니라 스코프 부재가 사실입니다.

그래서 이 스킬은 `codex exec`를 경유합니다. `OPENAI_API_KEY`가 있으면 REST 경로가 열리지만
그건 구독이 아니라 API 과금이라 이 스킬의 과금 모델과 다릅니다.

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
