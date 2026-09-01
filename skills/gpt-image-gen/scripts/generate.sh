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

# --- 사전 점검: codex CLI 설치와 로그인 여부 ---
if ! command -v codex >/dev/null 2>&1; then
  echo "ERROR: codex CLI를 PATH에서 찾을 수 없습니다." >&2
  echo "       설치 후 'codex login'으로 ChatGPT 계정 로그인이 필요합니다." >&2
  exit 127
fi

# 로그인 여부. 미로그인 상태로 호출하면 codex가 돌다가 죽고 사용자는 로그 tail만 받는다.
# 유료 호출 앞의 검증이므로 실패를 삼키지 않는다. 종료 코드가 유일하게 믿을 만한 신호다
# — codex-cli 0.151.0에서 로그인 상태는 exit 0, 미로그인은 exit 1 + "Not logged in".
# 반대로 exit 0이면 출력 문구를 따지지 않고 통과시킨다. 문구가 바뀌었을 때 정상 설정을
# 막는 쪽이 미로그인을 통과시키는 쪽보다 나쁘다 — 사용자가 손쓸 방법이 없어진다.
if ! codex login status >/dev/null 2>&1; then
  echo "ERROR: codex 로그인이 확인되지 않습니다." >&2
  echo "       'codex login'으로 ChatGPT 계정에 로그인한 뒤 다시 실행하세요." >&2
  exit 1
fi

# image_generation 기능 플래그. 꺼져 있으면 호출이 나가도 이미지가 안 나온다.
# 판정 불가는 통과시키고 알려진 나쁜 상태만 막는다 — 명령이 실패하거나 플래그가 목록에
# 없으면(이름이 바뀌었거나 졸업했을 때) 스킬 전체를 죽이지 않고, 플래그가 있는데 true가 아닐 때만 막는다.
if _FEATURES="$(codex features list 2>/dev/null)"; then
  _IMAGE_FEATURE="$(printf '%s\n' "$_FEATURES" | grep -E '^image_generation[[:space:]]' || true)"
  if [ -n "$_IMAGE_FEATURE" ] && ! printf '%s' "$_IMAGE_FEATURE" | grep -qE '[[:space:]]true[[:space:]]*$'; then
    echo "ERROR: codex의 image_generation 기능이 활성 상태가 아닙니다." >&2
    echo "       현재: ${_IMAGE_FEATURE}" >&2
    echo "       'codex features list'로 확인하고 활성화한 뒤 다시 실행하세요." >&2
    exit 1
  fi
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

# --- 동시성 안전 폴백용 마커: 호출 직전 기준 시각 ---
MARKER="$(mktemp "${TMPDIR:-/tmp}/gpt-image-gen-marker.XXXXXX")"

# --- 실패 원인 분류 -----------------------------------------------------------
# 대처가 갈리는 원인만 구분한다. 원인마다 사용자가 할 일이 다르고("다시 로그인" vs
# "한도 회복 대기"), 로그 tail 20줄만 주면 그 판단을 사용자에게 떠넘기게 된다.
#
# 분류는 추정이므로 결과를 대체하지 않고 덧붙인다 — 분류 문구와 로그 tail을 항상 함께
# 낸다. 상태 코드 숫자는 로그 어디에나 나올 수 있어 문구 패턴을 먼저 보고, 틀리게 짚어도
# 원문이 같이 있어 사용자가 바로잡을 수 있다.
#
# 패턴은 좁게 쓴다. codex exec는 시작 배너에 sandbox 설정을 찍으므로 `sandbox`나 `trust`
# 같은 단어를 그대로 매칭하면 배너 한 줄 때문에 거의 모든 실패가 그 분기로 빨려 들어간다.
# 실제 실패 문구(permission denied, not trusted 등)로만 잡는다.
classify_failure() {
  _hay="$(tr '[:upper:]' '[:lower:]' <"$1" 2>/dev/null || true)"
  case "$_hay" in
    *"not logged in"*|*"missing scopes"*|*unauthorized*|*"token expired"*|*"refresh token"*|*"re-authenticate"*|*"invalid_api_key"*)
      echo "원인 추정: 인증이 거부됨 → 'codex login'으로 다시 로그인하세요." ;;
    *"rate limit"*|*"too many requests"*|*"usage limit"*|*"quota"*|*"429"*)
      echo "원인 추정: 사용량이나 호출 한도 → 한도가 회복된 뒤 다시 시도하세요." ;;
    *"does not have access"*|*"insufficient permission"*|*"not available on your plan"*|*forbidden*)
      echo "원인 추정: 이미지 생성 권한 없음 → ChatGPT 플랜과 'codex features list'의 image_generation을 확인하세요." ;;
    *"timed out"*|*timeout*|*"deadline exceeded"*)
      echo "원인 추정: 시간 초과 → 프롬프트를 짧게 하거나 잠시 후 다시 시도하세요." ;;
    *"not trusted"*|*"permission denied"*|*"read-only file system"*|*"operation not permitted"*|*"sandbox denied"*|*seatbelt*)
      echo "원인 추정: 샌드박스나 쓰기 권한 → 출력 경로(${ABS_OUT_DIR})가 쓰기 가능한지 확인하세요." ;;
    *"connection"*|*"network"*|*"dns"*|*"could not resolve"*|*"tls"*)
      echo "원인 추정: 네트워크 → 연결을 확인하고 다시 시도하세요." ;;
    *)
      echo "원인 추정: 분류하지 못했습니다. 아래 로그를 확인하세요." ;;
  esac
}

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
    echo "ERROR: codex 실행 실패 (label='${LABEL}')." >&2
    classify_failure "$LOG" >&2
    echo "전체 로그: ${LOG}" >&2
    echo "--- 마지막 20줄 ---" >&2
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
