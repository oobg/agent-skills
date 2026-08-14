#!/usr/bin/env bash
#
# gpt-image-gen :: Codex CLI(gpt-image 플러그인)로 이미지를 생성한다.
# 사용법: generate.sh [--label NAME] <이미지 프롬프트>
#
# 이 스크립트만 동작 로직을 담는다. SKILL.md 본문에서 모델이 명령을
# 직접 조립하면 $(...) 치환이 어긋날 수 있으므로, 파싱/실행은 전부 여기서 한다.
#
# 동시 실행 안전(concurrency-safe): 여러 서브에이전트가 병렬로 호출해도
# 파일명/로그가 충돌하지 않고, 폴백이 남의 결과를 잘못 집지 않는다.

set -euo pipefail

# --- 인자 파싱: 선택적 --label NAME ---
LABEL=""
if [ "${1:-}" = "--label" ]; then
  # shift 2 실패를 삼키면 "--label"이 그대로 프롬프트가 되어 유료 호출이 나간다.
  if [ "$#" -lt 3 ]; then
    echo "ERROR: --label 뒤에는 라벨 값과 프롬프트가 모두 필요합니다." >&2
    echo "Usage: generate.sh [--label NAME] <image prompt>" >&2
    exit 1
  fi
  LABEL="$2"
  shift 2
fi

PROMPT="${*:-}"
if [ -z "$PROMPT" ]; then
  echo "ERROR: 프롬프트가 비어 있습니다." >&2
  echo "Usage: generate.sh [--label NAME] <image prompt>" >&2
  exit 1
fi

# --- 출력 위치 + 호출별 고유 식별자 ---
OUT_DIR="./generated-images"
mkdir -p "$OUT_DIR"                       # mkdir -p는 병렬 호출에도 안전
ABS_OUT_DIR="$(cd "$OUT_DIR" && pwd)"

TS="$(date +%Y%m%d-%H%M%S)"
UNIQ="$$-${RANDOM}"                        # PID+난수 → 같은 초에 병렬 호출돼도 파일명 충돌 없음
SAFE_LABEL="$(printf '%s' "$LABEL" | tr ' /' '__' | tr -cd '[:alnum:]_-')"
BASENAME="img${SAFE_LABEL:+-$SAFE_LABEL}-${TS}-${UNIQ}.png"
ABS_OUT="${ABS_OUT_DIR}/${BASENAME}"
LOG="/tmp/gpt-image-gen-${UNIQ}.log"       # 호출별 로그 → 병렬 실행끼리 안 덮어씀

# --- 사전 점검: codex CLI 설치 및 로그인 여부 ---
if ! command -v codex >/dev/null 2>&1; then
  echo "ERROR: codex CLI를 PATH에서 찾을 수 없습니다." >&2
  echo "       설치 후 'codex login'으로 ChatGPT 계정 로그인이 필요합니다." >&2
  exit 127
fi

# --- 동시성 안전 폴백용 마커: 호출 직전 기준 시각 ---
MARKER="$(mktemp "${TMPDIR:-/tmp}/gpt-image-gen-marker.XXXXXX")"

# --- 이미지 생성 호출 ---------------------------------------------------------
# Codex의 gpt-image 플러그인 스킬(@imagegen)에 위임한다. 이미지 생성 지능은
# Codex 쪽 플러그인이 담당하고, 여기서는 프롬프트와 저장 경로만 넘긴다.
#
#
# 샌드박스는 workspace-write다. 프롬프트가 그대로 에이전트 지시문에 들어가므로
# 붙여넣은 텍스트 안의 주입 문구도 이 권한으로 실행된다 — 쓰기 범위를 작업 폴더와
# --add-dir로 한정한다. danger-full-access는 --add-dir을 무의미하게 만들고
# 주입에 머신 전체를 내준다.
#
# ▼▼▼ 플러그인 진입점이 다르면(@imagegen 외) 이 한 줄만 바꾸면 된다 ▼▼▼
codex exec \
  --skip-git-repo-check \
  --sandbox workspace-write \
  --cd "$(pwd)" \
  --add-dir "$ABS_OUT_DIR" \
  "@imagegen ${PROMPT}. Save the generated image to exactly: ${ABS_OUT} . Print only the final saved absolute path." \
  >"$LOG" 2>&1 || {
    echo "ERROR: codex 실행 실패 (label='${LABEL}'). 로그:" >&2
    tail -n 20 "$LOG" >&2
    rm -f "$MARKER"
    exit 1
  }
# ▲▲▲ ----------------------------------------------------------------------- ▲▲▲

# --- 결과 확인 및 보고 (동시성 안전) ---
# 1순위: 우리가 지정한 정확한 경로. 병렬이어도 호출마다 고유하므로 안전.
if [ -f "$ABS_OUT" ]; then
  echo "SAVED ${ABS_OUT}"
  rm -f "$MARKER"
  exit 0
fi

# 폴백: 마커 이후 새로 생긴 png만 본다. 새 파일이 '정확히 1개'일 때만 채택하고,
# 모호하면 차라리 실패한다. 다만 병렬 호출에서 이웃이 아직 저장 전이면 그 1개가
# 남의 결과일 수 있다 — 이 경로는 최선 추정이지 오집 방지 보장이 아니다.
# bash 4 전용 배열 읽기 내장 대신 while read를 쓴다. macOS 기본 bash는 3.2다.
NEW_FILES=()
while IFS= read -r found; do
  [ -n "$found" ] && NEW_FILES+=("$found")
done < <(find "$ABS_OUT_DIR" -maxdepth 1 -name '*.png' -newer "$MARKER" 2>/dev/null || true)
rm -f "$MARKER"

if [ "${#NEW_FILES[@]}" -eq 1 ]; then
  echo "SAVED ${NEW_FILES[0]}"
elif [ "${#NEW_FILES[@]}" -gt 1 ]; then
  echo "ERROR: 지정 경로(${ABS_OUT})에 저장되지 않았고, 동시에 여러 새 이미지가 생겨" >&2
  echo "       이번 호출의 결과를 확정할 수 없습니다. 로그 확인: ${LOG}" >&2
  exit 1
else
  echo "ERROR: codex는 실행됐지만 생성된 이미지를 찾지 못했습니다. 로그 확인: ${LOG}" >&2
  exit 1
fi
