---
name: ry-review
description: "Проведи read-only Gemini rldyour review. EN: read-only Gemini rldyour review."
---

# Purpose

Review a requested scope for bugs, drift, release risk, security issues, and
native-boundary violations.

# Native Gemini Boundary

Use Gemini-native evidence gathering. Subagents may analyze when policy allows,
but they must not mutate source or act as cmux orchestrators.

# When To Use

Use only for explicit review, audit, security review, or rules review requests.

# Inputs

- Review scope and baseline commit.
- Source diff, validators, docs, memories, and live evidence where requested.

# Procedure

1. Stay read-only.
2. Inspect source, configs, docs, tests, and generated surfaces.
3. Prioritize findings by severity with exact file/path evidence.
4. Separate confirmed bugs from `NOT_PROVEN` gaps.
5. Report tests or validators that would prove resolution.

# Evidence Required

File paths, command outputs, validator names, release/GitHub evidence, and
source-backed external facts.

# Forbidden Actions

No edits, commits, pushes, fullrepo publication, branch deletion, or system
install.

# Acceptance Checks

Findings are actionable, severity-ordered, and grounded in exact evidence.

# Failure Reporting

Report blocked evidence sources and the effect on confidence.

