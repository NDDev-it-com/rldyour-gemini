# Gemini Native Boundaries

Gemini runtime configuration uses:

- `GEMINI.md`
- `.gemini/settings.json`
- `gemini-extension.json`
- `.gemini/commands/**/*.toml`
- `.gemini/skills/*/SKILL.md`
- `.gemini/agents/*.md`
- `.gemini/hooks/hooks.json`
- `.gemini/policies/*.toml`

Claude Code slash-command files, Codex plugin manifests, and OpenCode command
JSON are not Gemini runtime surfaces.

Gemini subagents are internal Gemini CLI delegation and are not cmux worker
terminals. Headless `gemini -p` is allowed for smoke, doctor, and CI checks, not
as a persistent orchestrator.

