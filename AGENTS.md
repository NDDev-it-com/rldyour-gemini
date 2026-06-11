# AGENTS.md

## Purpose

This repository is the Gemini CLI-native rldyour adapter. Repository artifacts
are English. Owner-facing conversation in connected agents remains Russian
unless explicitly requested otherwise.

## Source Of Truth

- `VERSION`: adapter product version.
- `GEMINI.md`: Gemini CLI context file.
- `.gemini/settings.json`: project Gemini settings and active MCP inventory.
- `gemini-extension.json`: extension manifest and extension MCP inventory.
- `.gemini/commands/`: Gemini TOML custom commands.
- `.gemini/skills/`: Gemini Agent Skills.
- `.gemini/agents/`: Gemini subagent definitions.
- `.gemini/hooks/`: synchronous bounded Gemini hooks.
- `.gemini/policies/`: policy extension data.
- `config/rldyour-contract.json`: adapter contract consumed by the root control plane.
- `config/gemini-baseline.json`: runtime baseline and source-of-truth policy.
- `references/`: durable native-boundary, browser, release, and auth documentation.
- `.serena/memories/`: fact-only durable adapter memory.

## Native Boundary

Use Gemini CLI-native surfaces. Do not copy Claude slash commands, Codex plugin
manifests, or OpenCode command JSON as runtime surfaces. Comparison notes are
allowed only in documentation when they clarify boundaries.

## MCP Policy

The active MCP inventory is exactly 11 servers: Serena, Chrome DevTools,
Sequential Thinking, shadcn, Dart/Flutter, Context7, GitHub, DeepWiki, Grep,
Figma, and OpenAI Docs. Aliases are dash-separated and must not contain
underscores. Playwright MCP and Semgrep are retired and must not be active.

## Browser Policy

Route browser tasks through Webwright, Playwright CLI + Skills, and Chrome
DevTools MCP according to `references/browser-provider-routing.md`. Keep
Webwright as a non-MCP harness and keep Playwright CLI-only.

## cmux Boundary

Gemini may run as a visible cmux worker terminal or, when explicitly selected by
the owner, as a visible cmux orchestrator terminal. Gemini subagents and
headless `gemini -p` smoke prompts are not cmux orchestration and must not become
background, headless, daemon, or detached orchestrator processes.

## Validation

Run repository-local validators for changed scope. Do not fake green checks.
Installed-runtime checks are optional and require explicit local authentication.
