#!/usr/bin/env bash
set -euo pipefail

input="$(cat || true)"
export RLDYOUR_GEMINI_HOOK_INPUT="$input"
printf '%s\n' "rldyour-gemini SessionStart hook received input" >&2

python3 - <<'PY'
import json
import os

_ = os.environ.get("RLDYOUR_GEMINI_HOOK_INPUT", "")
message = (
    "rldyour-gemini adapter=1.3.4 runtime=@google/gemini-cli@0.46.0; "
    "standard mode is owner-led; cmux orchestration is visible-terminal-only; "
    "browser routing is Webwright, Playwright CLI, and Chrome DevTools MCP; "
    "no Playwright MCP or Semgrep active config; supported auth is enterprise, "
    "API-key, Vertex, Google Cloud, or owner-approved."
)
print(json.dumps({"systemMessage": message, "suppressOutput": True}, separators=(",", ":")))
PY
