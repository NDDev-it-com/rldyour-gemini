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

Hooks use Gemini's native event-keyed schema and must read JSON from stdin,
write exactly one JSON object to stdout, and send diagnostics to stderr.

Claude Code slash-command files, Codex plugin manifests, and OpenCode command
JSON are not Gemini runtime surfaces.

Gemini subagents are internal Gemini CLI delegation and are not cmux worker
terminals. Headless `gemini -p` is allowed for smoke, doctor, and CI checks, not
as a persistent orchestrator.
