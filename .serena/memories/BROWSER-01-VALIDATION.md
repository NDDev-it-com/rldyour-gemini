# BROWSER-01-VALIDATION

## Purpose

Record browser-provider routing for Gemini workflows.

## Current Facts

- Webwright handles high-level long-horizon browser workflows.
- Playwright CLI handles low-level UI automation, screenshots, snapshots,
  traces, and visual evidence.
- Chrome DevTools MCP handles console, network, performance, Lighthouse,
  memory, and live debugging.

## Evidence

- `config/browser-provider-policy.json`
- `references/browser-provider-routing.md`
- `.gemini/skills/browser-validation/SKILL.md`

## Operational Rules

- Do not activate Playwright MCP.
- Do not represent Webwright as an MCP server.

## Last Verified

2026-06-11

