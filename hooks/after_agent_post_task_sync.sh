#!/usr/bin/env bash
set -euo pipefail

input="$(cat || true)"
export RLDYOUR_GEMINI_HOOK_INPUT="$input"

status_output=""
if git rev-parse --show-toplevel >/dev/null 2>&1; then
  root="$(git rev-parse --show-toplevel)"
  status_output="$(git -C "$root" status --short 2>/dev/null || true)"
fi
export RLDYOUR_GEMINI_STATUS_OUTPUT="$status_output"

python3 - <<'PY'
import json
import os

_ = os.environ.get("RLDYOUR_GEMINI_HOOK_INPUT", "")
status = os.environ.get("RLDYOUR_GEMINI_STATUS_OUTPUT", "").strip()
if status:
    print("rldyour-gemini AfterAgent hook observed working-tree changes", file=os.sys.stderr)
    message = "Working tree has changes; run scoped validation and Serena sync before final delivery."
else:
    message = "Working tree clean or unavailable to hook; no post-task mutation was performed."
print(json.dumps({"systemMessage": message, "suppressOutput": True}, separators=(",", ":")))
PY
