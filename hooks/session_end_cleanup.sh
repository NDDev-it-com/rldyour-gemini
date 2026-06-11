#!/usr/bin/env bash
set -euo pipefail

input="$(cat || true)"
export RLDYOUR_GEMINI_HOOK_INPUT="$input"

markers=""
if command -v find >/dev/null 2>&1; then
  markers="$(find . -path './.git' -prune -o -path './.serena/cache' -prune -o -name '.rldyour-runtime-*' -print 2>/dev/null || true)"
fi
export RLDYOUR_GEMINI_RUNTIME_MARKERS="$markers"

python3 - <<'PY'
import json
import os

_ = os.environ.get("RLDYOUR_GEMINI_HOOK_INPUT", "")
markers = [line for line in os.environ.get("RLDYOUR_GEMINI_RUNTIME_MARKERS", "").splitlines() if line.strip()]
if markers:
    print("rldyour-gemini SessionEnd hook found runtime markers", file=os.sys.stderr)
    message = "Runtime markers remain; cleanup requires explicit owner-approved command."
else:
    message = "No rldyour runtime markers detected by SessionEnd hook."
print(json.dumps({"systemMessage": message, "suppressOutput": True}, separators=(",", ":")))
PY
