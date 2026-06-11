---
name: ry-repair
description: "Запусти rldyour repair для Gemini CLI configuration. EN: repair Gemini CLI adapter."
---

# Purpose

Repair and synchronize this Gemini adapter against repository source of truth.

# Native Gemini Boundary

Use `GEMINI.md`, `.gemini/settings.json`, `gemini-extension.json`, TOML
commands, Gemini Agent Skills, Gemini subagents, hooks, and policies.

# When To Use

Use when adapter docs, runtime baselines, MCP inventory, native surfaces, Serena
memories, or release metadata may be stale.

# Inputs

- User request and scope.
- Current git state.
- `config/rldyour-contract.json`.
- Gemini baseline and native surface files.

# Procedure

1. Read source-of-truth files before editing.
2. Validate native Gemini surfaces.
3. Fix verified drift with the smallest coherent change.
4. Run scope-matching validators and tests.
5. Report exact pass/fail results.

# Evidence Required

File paths, command output summaries, validator names, and `NOT_PROVEN` gaps.

# Forbidden Actions

Do not add Playwright MCP, Semgrep active config, tool-specific tombstone
validators, background orchestrators, or unbounded hooks.

# Acceptance Checks

`python3 scripts/validate_gemini_config.py --strict` and `python3 -m pytest -q`.

# Failure Reporting

Lead with blockers, affected files, and the next acceptance command.
