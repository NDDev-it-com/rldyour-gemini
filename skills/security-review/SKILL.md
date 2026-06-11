---
name: security-review
description: "Проверь безопасность Gemini adapter: hooks, MCP, secrets, auth. EN: security review."
---

# Purpose

Find safety, secrets, auth, hook, MCP, and release risks before they ship.

# Native Gemini Boundary

Gemini committed settings use default approval mode; YOLO is launcher-only.

# When To Use

Use for hook changes, MCP changes, workflow changes, auth docs, release scripts,
and security-sensitive config.

# Inputs

Git diff, config files, hooks, workflows, and policy files.

# Procedure

1. Inspect high-risk shell/git/file operations.
2. Check secrets and token handling.
3. Verify MCP env boundaries.
4. Check workflow permissions and action pins.
5. Report findings before summaries.

# Evidence Required

File/line references, risk impact, and remediation.

# Forbidden Actions

Do not expose secrets or normalize unsafe auto-approval in committed config.

# Acceptance Checks

Security review plus relevant validators and tests.

# Failure Reporting

Order findings by severity and include exact fix guidance.
