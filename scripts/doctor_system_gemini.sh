#!/usr/bin/env bash
set -euo pipefail

redact=0
while (($#)); do
  case "$1" in
    --redact) redact=1 ;;
    -h|--help)
      printf '%s\n' "usage: scripts/doctor_system_gemini.sh [--redact]"
      exit 0
      ;;
    *)
      printf 'unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
  shift
done

if command -v gemini >/dev/null 2>&1; then
  printf 'gemini: %s\n' "$(gemini --version 2>/dev/null || true)"
else
  printf 'gemini: NOT_INSTALLED\n'
fi

if command -v npm >/dev/null 2>&1; then
  printf 'npm @google/gemini-cli latest: %s\n' "$(npm view @google/gemini-cli version 2>/dev/null || printf NOT_PROVEN)"
else
  printf 'npm: NOT_INSTALLED\n'
fi

for key in GEMINI_API_KEY GOOGLE_API_KEY GOOGLE_GENAI_USE_VERTEXAI GOOGLE_CLOUD_PROJECT GOOGLE_CLOUD_LOCATION; do
  value="${!key-}"
  if [[ -n "$value" ]]; then
    if [[ "$redact" -eq 1 ]]; then
      printf '%s=%s\n' "$key" "REDACTED"
    else
      printf '%s=%s\n' "$key" "$value"
    fi
  else
    printf '%s=UNSET\n' "$key"
  fi
done

