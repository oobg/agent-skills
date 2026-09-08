# 서브에이전트 운영 정책 스냅샷

[`policies/subagent-operation.md`](../policies/subagent-operation.md)는 사람이 검토하는
정본이고, 런타임은 검토된 정본에서 만든 고정 형식 스냅샷만 읽습니다. 컴파일러는
규칙의 의미를 판단하지 않으며 발행 전 의미 검토는 사람 또는 상위 검토 단계가
담당합니다.

정본에는 `<!-- policy:rules:start -->`와 `<!-- policy:rules:end -->`가 정확히 한 쌍,
이 순서로 있어야 합니다. 컴파일 대상은 두 마커 사이뿐입니다. 추출한 구획의 CRLF를
LF로 바꾼 뒤 시작 마커 바로 뒤의 구조용 줄바꿈 한 개와 종료 마커 바로 앞의
구조용 줄바꿈 한 개를 제거합니다. 이어서 각 줄 끝의 ASCII space와 tab을 제거하고
마지막 LF를 정확히 하나 둡니다.
내부 공백, 내부 줄바꿈, 빈 줄, 규칙 순서는 그대로 보존합니다. 이 바이트의 SHA-256이
`source_hash`입니다. 각 규칙은 아래 형태이며 ID는 소문자 kebab-case여야 합니다.

```markdown
- <!-- rule:example-rule -->
  규칙 본문
```

스냅샷 헤더의 키, 순서와 값 형식은 고정됩니다. `snapshot_hash`는 완성된 파일에서
`snapshot_hash:` 헤더 행 전체만 제거한 바이트의 SHA-256입니다. YAML 재직렬화나
placeholder 치환으로 계산하지 않습니다. 검증기는 알 수 없는 키, 중복 키, 순서 변경,
지원하지 않는 버전과 형식, 규칙 변경, 모든 해시 불일치를 거부합니다.

```text
---
snapshot_format: 1
policy: subagent-operation
policy_version: N
source_hash: sha256:<64 lowercase hex>
snapshot_hash: sha256:<64 lowercase hex>
---

<canonical rules>
```

`policy_version`은 앞에 0이 없는 양의 십진 정수입니다. 실행 구획은 최소한
`main-orchestrator`, `min-delegation`, `parent-validation`, `model-routing`,
`model-explicit`, `max-depth`, `redelegation-boundary`, `minimal-context`, `batching`,
`parallel-conflict-check`, `mutation-boundary` ID를 포함해야 하며 정본의 다른 모든 규칙도
순서와 ID를 보존해 스냅샷에 들어갑니다.

기본 런타임 디렉터리는 `~/.ontology/policies/subagent-operation/`이며 다음 명령을
저장소 루트에서 실행합니다.

```bash
python3 scripts/ontology.py policy publish subagent-operation \
  --reviewed-source-hash sha256:<검토한-source-hash>
python3 scripts/ontology.py policy show subagent-operation
python3 scripts/ontology.py policy verify subagent-operation
```

검토할 정본 해시는 저장소 코드와 같은 정규화를 사용해 계산합니다.

```bash
python3 -c 'import importlib.util; from pathlib import Path; p=Path("scripts/ontology.py"); s=importlib.util.spec_from_file_location("policy", p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.sha256(m.canonical_rules(Path("policies/subagent-operation.md").read_bytes())))'
```

기본 경로의 파일 이름은 `snapshot.md`와 `publish.lock`입니다. 테스트와 격리된 검증에서는
`--runtime-dir <directory>`와 `--source <file>`을 사용할 수 있습니다. `publish`는 검토한
해시를 반드시 입력받습니다. 현재 해시와 다르면 실패하며 의미 검토를 자동 수행했다고
간주하지 않습니다. lock을 획득한 임계 구역에서
정본을 다시 읽어 해시를 비교한 뒤 기존 스냅샷도 다시 읽어 검증합니다. 기존 스냅샷이 손상됐으면 덮어쓰지 않습니다. 처음 발행은
버전 1이고, 같은 정본 해시는 버전을 유지하며, 정본 해시가 바뀌면 1을 더합니다.
고정 lock 파일을 삭제하거나 교체하지 않고 OS advisory lock으로 동시 발행을
직렬화합니다. 같은 디렉터리의 임시 파일을 fsync하고 다시 검증한 뒤 atomic replace와
디렉터리 fsync를 수행합니다.

같은 정본 해시를 다시 발행해도 revision은 바뀌지 않습니다. 교체 전 스냅샷의 별도
역사 보관은 이 도구의 범위에 포함되지 않습니다.

`show`는 lock을 잡지 않고 스냅샷을 한 번 열어 한 번 읽은 버퍼만 검증합니다. 검증이
성공한 경우에만 파일 전체를 stdout에 출력하며, 실패하면 stderr와 0이 아닌 종료 코드만
남깁니다. 검색, LLM, fallback, 복구, 재발행은 수행하지 않습니다. `verify`도 스냅샷을
읽기 전용으로 검증합니다.

주 에이전트는 성공한 `show`에서 얻은 정책 버전, 두 해시와 규칙 본문을 한 세션 동안
같은 revision으로 캐시합니다. 같은 지침 문맥에서는 다시 읽지 않으며, 읽기 실패 시
부분 본문이나 이전 본문을 성공한 현재 스냅샷처럼 사용하지 않습니다.
