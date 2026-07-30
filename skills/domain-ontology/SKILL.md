---
name: domain-ontology
description: Read the personal ontology before answering when accumulated company, personal, or shared knowledge could materially change the answer, or when the user asks to consult prior knowledge or decisions. Also use when substantial durable knowledge arrives and ontology ingestion may be appropriate. Do not trigger for code tasks, simple editing, general facts, casual questions, or requests answerable from the current files alone. Reading is automatic when relevant; ingestion or mutation always requires explicit user consent and tenant confirmation.
---

# Domain Ontology Routing

## Overview
Durable domain knowledge should **compound**, not be re-derived per question. When it arrives, route it through the persistent SQLite knowledge ontology **before proceeding**: ingest → connect it to the graph → then answer grounded in accumulated knowledge (Memex / LLM-Wiki pattern).

**One database, two tenants.** Root `~/.ontology/`, DB at `~/.ontology/ontology.db`.

| | company (회사) | personal (개인) | shared (공용) |
|---|---|---|---|
| tenant key | `company` (1) | `personal` (2) | `shared` (3) |
| 담는 것 | 제품·전략·경쟁·법무 | 삶·자기계발 | **일하는 방식** — 방법론·도구론·에이전트 하네스 |
| raw sources | `tenants/company/sources/` | `tenants/personal/sources/` | `tenants/shared/sources/` |
| session feed | SessionEnd hook + daily distill | 수동(Grok 등) | 없음 |

`shared`는 "회사냐 개인이냐"로 갈리지 않는 문서를 위한 자리다. 루프 엔지니어링,
에이전트 하네스 설계, 검증자 패턴 같은 것 — 회사 업무에도 개인 프로젝트에도 적용되므로
한쪽에 넣으면 반대쪽에서 조회할 때 안 보인다. **주제가 "무엇을 만드는가"가 아니라
"어떻게 일하는가"면 `shared`를 먼저 의심해라.**

`concepts`, `topics`, `concept_topics` are **shared across tenants** — that shared layer is the point: the same concept node links what company work actually built to what personal material says about it. Only `sessions` and `documents` carry `tenant_id`.

`~/.ontology/AGENTS.md` is the authoritative schema + exact commands (`CLAUDE.md` and `GEMINI.md` are symlinks to it). **REQUIRED: read it before ingesting** — do not guess commands from here.

## When to use
- Substantial domain material: reports, research output, market/competitor intel, strategy/legal/product/planning docs, uploaded files (pdf/docx/html/md).
- User says 온톨로지 / 넣어줘 / ingest / add to KB.
- Before answering a domain question the ontology could inform (query first, then answer).

**Not for:** code, task instructions, casual questions, trivial one-line mentions.

## Routing

### Read path — automatic when relevant

Use read-only queries without asking first when accumulated knowledge could materially change the
answer: strategy, product, competition, legal context, personal priorities, prior decisions, or
cross-session history. Prefer the graph views and cite what was found.

Do not query for code tasks, simple editing, general facts, casual questions, or requests fully
answerable from the current files. A forced lookup is not useful evidence and would distort
knowledge-demand counts.

### Write path — explicit consent only

1. **Detect.** Is this durable, reusable domain knowledge (not code/chatter/instructions)? If borderline, propose it as a candidate; do not ingest yet.
2. **Ask before ingesting or mutating (never write silently).** Propose, then confirm:
   - 온톨로지에 적재할까요? (거절 시 → "적재 거절 시" 분기)
   - **회사 / 개인 / 공용** 어느 테넌트? — 성격이 명백하면 근거와 함께 추천하되 사용자가 확정한다. 사용자에게만 떠넘기지 말 것.
     회사 사업·제품·경쟁 → `company` / 개인 삶·자기계발 → `personal` /
     **일하는 방식(방법론·도구론·에이전트 하네스) → `shared`**.
3. **Ingest** (on yes) — follow `AGENTS.md`, all paths under the chosen tenant:
   - Save raw source → `tenants/<tenant>/sources/` (immutable provenance).
   - Extract → `tenants/<tenant>/extractions/docs/<name>.json`. The JSON's `path` must point at that tenant's `sources/`. **Query `concepts` first and reuse existing names** so it merges into the graph instead of fragmenting.
   - Load: `python3 bin/docs.py load <json> --tenant <company|personal>`. **`--tenant` is required** — it is the only boundary left now that both tenants share one DB.
4. **Surface connections.** Query the views — `v_concept_bridge` (coverage/gaps, per-tenant doc counts), `v_topic_bridge` (topic-level rollup), `v_claim_concept` (evidence). What does this connect to, reinforce, contradict, or reveal as a gap?
5. **Proceed.** Continue with the user's actual task, grounded in the KB and citing the graph. Ingesting is the setup, not the whole task.

**적재 거절 시:** 새로 넣지 말고 기존 온톨로지만 읽기전용으로 조회(Step 4의 뷰)한 뒤 Step 5로 바로 — 답은 기존 KB에 근거해 준다.

## Quality gates

`question-design`과 `ux-writing`의 공용 원칙을 온톨로지 적재에 맞게 축약해 적용한다.
원본 스킬 번들은 `shared` 문서로 보존되어 있고, 여기서는 적재 품질을 실제로 바꾸는 규칙만 둔다.

### 1. Frame gate — 질문은 결과가 갈릴 때만

적재 전에 목적, tenant, 출처 상태를 확인한다.

- **반드시 질문:** tenant나 원본 범위에 따라 결과가 달라짐 / 사용자 동의 없음 /
  사용자 직접 진술과 제3자 평가가 섞여 있음 / 회사·개인 경계가 실질적으로 갈림.
- **질문하지 않음:** 앞선 대화에서 이미 답이 나옴 / 사용자가 tenant와 적재를 명시함 /
  파일명·형식 같은 가역적 세부사항.
- 침묵을 동의로 간주하지 않는다. 다만 이미 승인된 적재 작업에 사용자가 같은 목적의
  자료를 이어서 추가하면 그 범위 안에서 진행하고, commentary에 해석을 밝힌다.

### 2. Domain-first gate — 구조보다 실체가 먼저

claim을 예쁘게 구조화하기 전에 도메인 사실·용어·최신성·출처를 확인한다.

- 1차 출처와 사용자 직접 진술을 제3자 요약보다 우선한다.
- 웹 GPT의 장기 메모리처럼 독립 검증되지 않은 회상은 `reported fact`로 취급한다.
- 외부 근거를 검증하지 않았으면 배경 설명 이상으로 승격하지 않는다.
- 기술적으로 그럴듯해도 실제 사용자·업무 흐름의 전제가 틀리면 claim을 확정하지 않는다.

### 3. Claim gate — 확신도와 문장 기능을 보존

추출할 때 다음을 섞지 않는다.

- source가 직접 말한 사실
- 반복 관찰에서 나온 추론
- 작성자나 에이전트의 추천
- 아직 답이 없는 gap

원문의 가능성을 단정으로, 상관을 인과로, 제안을 결정으로 바꾸지 않는다. 시점에 따라 변하는
`현재`·`최근`·`진행 중`에는 기준 날짜를 붙인다. 한 claim에는 가능한 한 한 명제만 둔다.

### 4. Writing gate — 정확 → 명확 → 간결

추출 JSON과 최종 설명은 정확성, 명확성, 간결성 순으로 다듬는다.

- 번역투·AI 상투어·과도한 완곡은 제거하되 의미·확실성·인과·고유명사·수치는 보존한다.
- 근거 없는 중요성 과장, 과도한 칭찬, 기계적 대칭을 추가하지 않는다.
- 원문의 절반 이상을 새로 써야 의미가 통한다면 윤문으로 덮지 말고 source의 한계로 기록한다.
- 법적·보안·결제처럼 고위험 문구는 친근함보다 정확성과 원문 보존이 우선이다.

### 5. Stop gate — 결함 0이 아니라 종료 조건 통과

계속 새 관점을 추가해 추출을 무한히 넓히지 않는다. 아래가 충족되면 적재를 끝낸다.

- tenant·path·원본 provenance가 명확함
- 핵심 claim이 source에 근거하고 확신도가 보존됨
- 기존 concept를 조회하고 중복을 만들지 않음
- lint에서 이번 적재가 만든 구조 오류가 없음
- 남은 불확실성이 gap 또는 주의사항으로 노출됨

문구 취향이나 추가 해석만 남았다면 종료한다. 미해결 구조 위험은 숨기지 말고 사용자에게 알린다.

## Guards
- **Ask before ingesting** — tenant + consent. Never silent.
- **`--tenant` on every `docs.py load`.** Omitting it aborts by design; do not work around it.
- **`sources/` is immutable** raw provenance; DB and extractions are generated.
- **Never run `bin/build.py` full rebuild** — breaks Phase-2 file-id links. Incremental only.
- **Never move a document between tenants by re-loading it** — `docs.py` errors out on tenant change. Company work stays company; personal material stays personal.
- **Honesty:** only claims the source actually states; mark weak/unverified sources as low-confidence in the doc and its claims. Don't fabricate.

## Common mistakes
- Ingesting silently, or not asking which tenant.
- Inventing new concept names for ones that exist → fragments the graph. Reuse.
- Writing the extraction JSON's `path` under the wrong tenant's `sources/` (load warns — don't ignore it).
- Answering a domain question cold without querying the ontology first.
- Stopping after ingest — after loading, proceed with the user's real request.
