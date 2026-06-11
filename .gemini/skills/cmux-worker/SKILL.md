---
name: cmux-worker
description: "Operate as a visible cmux Gemini worker terminal. RU: cmux worker для Gemini."
---

# Purpose

Perform a scoped worker task in a visible cmux terminal session.

# Native Gemini Boundary

Gemini subagents are internal delegation and are not cmux worker terminals.

# When To Use

Use only when the owner or visible cmux orchestrator assigns this terminal a
scoped worker task.

# Inputs

Scoped task, allowed paths, reporting contract, and acceptance checks.

# Procedure

1. Confirm scope and restrictions.
2. Work only inside delegated scope.
3. Do not push, publish fullrepo, delete branches, or run system install.
4. Return a concise JSON-compatible report.

# Evidence Required

Files inspected, files changed, commands run, pass/fail results, and blockers.

# Forbidden Actions

No background/headless/daemon orchestrator, no hidden worker jobs, no final sync
unless explicitly delegated.

# Acceptance Checks

Scope-specific checks requested by the orchestrator.

# Failure Reporting

Return blockers with exact command and file evidence.
