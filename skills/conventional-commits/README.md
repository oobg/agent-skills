# Conventional Commits

실제 변경사항을 확인해 Conventional Commits 1.0.0 형식의 한국어 커밋 메시지,
커밋 분할안, PR 제목과 changelog 항목을 작성합니다. 메시지 작성과 실제 `git commit`,
`push` 권한을 분리하고 공유 워킹트리의 변경을 보호합니다.

## 사용 시점

- 변경사항에 맞는 한국어 커밋 메시지를 작성할 때
- 커밋을 의미 있는 단위로 나누거나 PR 제목과 changelog 항목을 정리할 때
- 사용자가 명시적으로 요청한 `git commit` 또는 `push`의 범위를 확인할 때

메시지 작성 요청만으로 커밋하거나 푸시하지 않습니다. 실제 실행은 사용자가 요청한
범위에서만 진행합니다.

## 핵심 원칙

- 실제 diff와 저장소 규칙을 먼저 확인합니다.
- Conventional Commits 1.0.0 형식과 한국어 명사형 제목을 사용합니다.
- 공유 워킹트리에서는 다른 사용자의 변경을 섞거나 되돌리지 않습니다.
- 커밋 이유는 확인된 맥락만 사용하며, 온톨로지 보강은 선택 사항입니다.

## 사용 예

```text
현재 변경사항에 맞는 커밋 메시지만 작성해줘.
```

```text
이 변경을 적절히 나눠서 커밋해줘. push는 하지 마.
```

## 구성

```text
conventional-commits/
├── SKILL.md
├── README.md
└── references/
    └── ontology-boost.md
```

- [`SKILL.md`](SKILL.md): 메시지 규칙, 실행 경계와 커밋 안전 가드
- [`references/ontology-boost.md`](references/ontology-boost.md): 온톨로지가 있을 때만 여는
  선택 모듈이며 scope 표기와 변경 이유의 근거를 회수합니다.

설치와 검증 방법은 저장소의 [루트 README](../../README.md)에서 확인할 수 있습니다.
