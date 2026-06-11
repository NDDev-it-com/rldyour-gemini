#!/usr/bin/env bash
set -euo pipefail

input="$(cat || true)"
export RLDYOUR_GEMINI_HOOK_INPUT="$input"

python3 - <<'PY'
import json
import os
import re

raw = os.environ.get("RLDYOUR_GEMINI_HOOK_INPUT", "")
try:
    payload = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    print("rldyour-gemini BeforeTool hook received invalid JSON", file=os.sys.stderr)
    print(json.dumps({
        "decision": "deny",
        "reason": "Invalid Gemini hook JSON input.",
        "suppressOutput": True,
    }, separators=(",", ":")))
    raise SystemExit(0)

tool_name = str(payload.get("tool_name") or payload.get("toolName") or "")
tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
if not isinstance(tool_input, dict):
    tool_input = {"raw": tool_input}
command = str(tool_input.get("command") or tool_input.get("cmd") or tool_input.get("raw") or "")
haystack = f"{tool_name}\n{json.dumps(tool_input, sort_keys=True)}\n{command}"

destructive = re.compile(
    r"rm\s+-rf|git\s+push\s+.*--force|git\s+push\s+--mirror|git\s+branch\s+-D|"
    r"git\s+clean\s+-fdx|git\s+push\s+origin\s+--delete",
    re.IGNORECASE,
)
secret_like = re.compile(r"GEMINI_API_KEY|GOOGLE_API_KEY|service-account|oauth|token", re.IGNORECASE)

if tool_name == "run_shell_command" and destructive.search(command):
    reason = "Blocked destructive shell/git operation by rldyour Gemini policy."
    print(reason, file=os.sys.stderr)
    print(json.dumps({"decision": "deny", "reason": reason, "suppressOutput": True}, separators=(",", ":")))
elif secret_like.search(haystack):
    reason = "Blocked possible secret-bearing operation by rldyour Gemini policy."
    print(reason, file=os.sys.stderr)
    print(json.dumps({"decision": "deny", "reason": reason, "suppressOutput": True}, separators=(",", ":")))
else:
    print(json.dumps({"decision": "allow", "suppressOutput": True}, separators=(",", ":")))
PY
