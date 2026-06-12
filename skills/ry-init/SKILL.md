---
name: ry-init
description: "Инициализируй Gemini adapter scope без изменений. EN: initialize Gemini adapter scope read-only."
---

# Purpose

Build a verified context pack for Gemini adapter work before implementation.

# Native Gemini Boundary

Use Gemini `GEMINI.md`, project settings, TOML commands, Agent Skills,
subagents, hooks, policies, and MCP server config. This skill is not a Claude
slash command, Codex managed agent, OpenCode command, or cmux orchestrator.

# When To Use

Use when the user asks to initialize, inspect, onboard, or prepare for work.

# Inputs

- User scope and constraints.
- `GEMINI.md`, `AGENTS.md`, and `config/rldyour-contract.json`.
- Current git/submodule/fullrepo state.
- Relevant Serena memories and validator entry points.

# Procedure

1. Read source-of-truth files and relevant memories first.
2. Map Gemini native surfaces, runtime baselines, MCP inventory, browser
   routing, cmux boundary, and quality gates.
3. Identify unknowns and mark unsupported claims `NOT_PROVEN`.
4. Do not mutate files, git state, system configs, or fullrepo.
5. Return a compact context pack with exact paths and safe next steps.

# Evidence Required

Git state, source paths, memory names, validator names, and current tuple facts.

# Forbidden Actions

No edits, commits, pushes, branch deletion, fullrepo publication, system
install, or background/headless orchestration.

# Acceptance Checks

Context report names exact source-of-truth files and unresolved gaps.

# Failure Reporting

Report missing context, blocked evidence, and the next read-only command.

