# MCP-01-TOOLS

## Purpose

Record the active Gemini MCP inventory.

## Current Facts

- Gemini active MCP inventory has 11 servers.
- Active aliases are `serena`, `chrome-devtools`, `sequential-thinking`,
  `shadcn`, `dart-flutter`, `context7`, `github`, `deepwiki`, `grep`, `figma`,
  and `openai-docs`.
- MCP aliases are dash-separated and contain no underscores.

## Evidence

- `.gemini/settings.json`
- `gemini-extension.json`
- `config/rldyour-contract.json`
- `config/mcp-runtime-versions.env`

## Operational Rules

- Keep Playwright MCP and Semgrep out of active MCP config.
- Keep Chrome DevTools MCP active.

## Last Verified

2026-06-11

