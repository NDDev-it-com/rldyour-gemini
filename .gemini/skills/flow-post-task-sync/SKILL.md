---
name: flow-post-task-sync
description: "Сделай финальную синхронизацию Gemini adapter: docs, Serena memories, checks, release evidence. EN: post-task sync."
---

# Purpose

Finish a task without leaving semantic drift, runtime markers, or stale memory.

# Native Gemini Boundary

Post-task sync updates Gemini-native files only when verified facts changed.

# When To Use

Use after meaningful code, config, docs, validator, release, or memory changes.

# Inputs

Git diff, changed file list, validation results, and current Serena memories.

# Procedure

1. Confirm changed scope.
2. Update Serena memories from verified facts only.
3. Update durable docs if current facts changed.
4. Run validators matching changed scope.
5. Prepare release evidence without committing local runtime state.

# Evidence Required

Changed files, validator commands, and memory evidence paths.

# Forbidden Actions

Do not store chat logs, speculation, secrets, tokens, caches, or browser evidence.

# Acceptance Checks

Memory schema and semantic validators plus scope-specific Gemini validators.

# Failure Reporting

State remaining blockers and exact commands that still fail.
