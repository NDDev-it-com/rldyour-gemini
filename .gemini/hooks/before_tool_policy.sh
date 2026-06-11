#!/usr/bin/env bash
set -euo pipefail

payload="${GEMINI_TOOL_PAYLOAD:-${1:-}}"

if printf '%s' "$payload" | grep -Eiq 'rm[[:space:]]+-rf|git[[:space:]]+push[[:space:]].*--force|git[[:space:]]+push[[:space:]]+--mirror|git[[:space:]]+branch[[:space:]]+-D|git[[:space:]]+clean[[:space:]]+-fdx|git[[:space:]]+push[[:space:]]+origin[[:space:]]+--delete'; then
  printf '%s\n' "blocked: destructive operation requires explicit owner approval"
  exit 42
fi

if printf '%s' "$payload" | grep -Eiq 'GEMINI_API_KEY|GOOGLE_API_KEY|service-account|oauth|token'; then
  printf '%s\n' "blocked: possible secret-bearing operation requires manual review"
  exit 43
fi

exit 0

