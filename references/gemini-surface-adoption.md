# Gemini Surface Adoption

## Current Baseline

The adapter targets `@google/gemini-cli` `0.46.0` and adopts native Gemini CLI
surfaces: context files, project settings, extension manifest, TOML commands,
Agent Skills, subagents, hooks, policies, MCP servers, model routing, and
headless prompt smoke mode.

## Evidence

- `config/gemini-baseline.json`
- `gemini-extension.json`
- `.gemini/settings.json`
- `.gemini/commands/`
- `.gemini/skills/`
- `.gemini/agents/`
- `.gemini/hooks/hooks.json`

## Operational Rule

Do not represent Gemini runtime configuration through Claude, Codex, or OpenCode
native files.

