---
name: ry-newp
description: "Спроектируй новый Gemini/rldyour project scope. EN: design a new Gemini/rldyour project scope."
---

# Purpose

Design a new project, adapter surface, command, skill, policy, or validation
scope before implementation.

# Native Gemini Boundary

Author designs in Gemini-native terms: TOML commands, Agent Skills, subagents,
hooks JSON protocol, policies, settings, extension manifest, and MCP servers.

# When To Use

Use for new project design, new feature scope, or new adapter capability
planning.

# Inputs

- Owner goals and constraints.
- Existing templates, standards, commands, skills, and contracts.
- Official docs for external technology choices.

# Procedure

1. Ask for missing product constraints when needed.
2. Research current official sources for external dependencies.
3. Propose architecture, native surfaces, validators, release path, and risks.
4. Wait for owner approval before scaffolding or mutation.
5. Keep future or unsupported claims marked `NOT_PROVEN`.

# Evidence Required

Source URLs, local templates, affected contracts, validator plan, and open
questions.

# Forbidden Actions

Do not scaffold, install, publish, or commit before explicit approval.

# Acceptance Checks

The design names source-of-truth files, native Gemini surfaces, and verification
commands.

# Failure Reporting

Report unresolved product/technical decisions and safe options.

