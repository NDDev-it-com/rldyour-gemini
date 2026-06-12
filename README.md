# rldyour Gemini CLI Adapter

`rldyour-gemini` is the Gemini CLI-native configuration adapter for the
rldyour AI CLI control plane. It provides a public, source-validated Gemini CLI
configuration using native Gemini surfaces: `GEMINI.md`, `.gemini/settings.json`,
`gemini-extension.json`, TOML commands, skills, subagents, hooks, policies,
MCP servers, browser-provider routing, Serena memory, and release validation.

## Current Baseline

| Surface | Version |
| --- | ---: |
| Adapter | `1.3.3` |
| Runtime | `@google/gemini-cli` `0.46.0` |
| Runtime channel | `stable/npm-latest` |
| License | `AGPL-3.0-or-later` |

Gemini CLI freshness uses `npm view @google/gemini-cli version` as the primary
source of truth, with the matching GitHub release tag as release provenance.
Only the scoped package `@google/gemini-cli` is valid for this adapter.

## Native Boundaries

This adapter is not a copy of the Claude Code, Codex CLI, or OpenCode adapters.
Gemini CLI configuration is represented through Gemini-native files:

- `GEMINI.md` for repository context.
- `.gemini/settings.json` for project settings and MCP servers.
- `gemini-extension.json` for extension metadata and extension MCP wiring.
- `.gemini/commands/**/*.toml` for custom commands.
- `.gemini/skills/*/SKILL.md` for Agent Skills.
- `.gemini/agents/*.md` for Gemini subagents.
- `.gemini/hooks/hooks.json` plus bounded hook scripts.
- `.gemini/policies/*.toml` for policy extension data.

## Browser Routing

Browser work follows the shared rldyour provider model:

- Webwright: high-level long-horizon browser workflows and reusable evidence scripts.
- Playwright CLI + Skills: low-level UI automation, screenshots, snapshots, traces, and visual evidence.
- Chrome DevTools MCP: console, network, performance, Lighthouse, memory, and live Chrome debugging.

Playwright MCP is retired and must not be active. Webwright is a provider/harness,
not an MCP server.

Gemini built-in `browser_agent` is disabled for this adapter release. The
canonical browser provider matrix remains Webwright, Playwright CLI + Skills,
and Chrome DevTools MCP. If `browser_agent` is enabled later, it must be added
as an explicit provider and must not silently replace Chrome DevTools MCP
inventory.

## MCP Inventory

The active Gemini MCP inventory matches the root positive inventory exactly:

`serena`, `chrome-devtools`, `sequential-thinking`, `shadcn`, `dart-flutter`,
`context7`, `github`, `deepwiki`, `grep`, `figma`, and `openai-docs`.

Semgrep and Playwright MCP are not active MCP servers.

## Access And Antigravity Notice

Gemini CLI adapter `1.3.3` targets enterprise, paid API-key, Vertex AI, Google
Cloud, and explicitly owner-approved authenticated environments. It does not
promise long-term consumer OAuth availability after the Google Antigravity
transition dated June 18, 2026. See
`references/gemini-antigravity-transition.md`.

## Validation

```bash
python3 scripts/validate_gemini_config.py --strict
python3 scripts/validate_gemini_extension_manifest.py --strict
python3 scripts/validate_gemini_commands.py --strict
python3 scripts/validate_gemini_skills.py --strict
python3 scripts/validate_gemini_subagents.py --strict
python3 scripts/validate_gemini_hooks.py --strict
python3 scripts/validate_gemini_mcp_inventory.py --strict
python3 scripts/validate_gemini_browser_routing.py --strict
python3 scripts/validate_gemini_runtime_baseline.py --strict
python3 scripts/validate_instruction_docs.py --strict
python3 scripts/validate_serena_memory_schema.py --strict
python3 scripts/validate_serena_memory_semantics.py --strict
python3 -m pytest -q
```

Installed-runtime smoke checks are optional and require a deliberately
configured owner machine:

```bash
gemini --version
gemini -p 'Return exactly READY.' --output-format json
```
