# rldyour-gemini

`rldyour-gemini` is the Gemini CLI-native configuration adapter for the rldyour AI CLI control plane. It provides a public, source-validated Gemini CLI configuration using native Gemini surfaces: `GEMINI.md`, `.gemini/settings.json`, `gemini-extension.json`, TOML commands, skills, subagents, hooks, policies, MCP servers, browser-provider routing, Serena memory, and release validation.

## Current Baseline

| Surface | Value |
| --- | ---: |
| Adapter version | `1.3.6` |
| Runtime baseline | `@google/gemini-cli` `0.46.0` |
| Runtime channel | `stable/npm-latest` |
| GitHub release tag | `1.3.6` |
| Pinned commit | `001fe7784a1d6cf27eb4cb94f02b84d95316b19b` |

Gemini CLI freshness uses `npm view @google/gemini-cli version` as the primary
source of truth, with the matching GitHub release tag as release provenance.
Only the scoped package `@google/gemini-cli` is valid for this adapter.
The pinned commit and product version are governed by the root control plane
`config/repositories.json`.

## What This Repository Provides

This repository is a configuration package for Gemini CLI, not a fork or copy
of the upstream `@google/gemini-cli` runtime. It wires together the native
Gemini configuration surfaces - context files, project settings, extension
manifest, TOML commands, Agent Skills, subagents, hooks, policies, and MCP
servers - into a coherent, version-controlled, owner-validated setup. The
upstream Gemini CLI binary is installed separately via npm and is not modified
here. All changes in this repository are configuration and adapter logic; runtime
behavior is governed by the installed `@google/gemini-cli` binary version.

## Native Boundaries

Gemini runtime configuration is represented through Gemini-native files only.
Claude Code slash-command files, Codex plugin manifests, and OpenCode command
JSON are not Gemini runtime surfaces and are not present here.

Active native surfaces:

- `GEMINI.md` - repository context injected at session start.
- `.gemini/settings.json` - project settings, hook wiring, and MCP server
  declarations.
- `gemini-extension.json` - extension metadata and extension MCP wiring.
- `.gemini/commands/**/*.toml` - custom commands (13 TOML files across browser,
  flow, release, ry, security, and serena groups).
- `.gemini/skills/*/SKILL.md` - Agent Skills (14 skills).
- `.gemini/agents/*.md` - Gemini subagents (7 agents: browser-reviewer,
  codebase-investigator, design-reviewer, gemini-cli-specialist,
  release-reviewer, security-reviewer, serena-curator).
- `.gemini/hooks/` - native hook scripts for SessionStart, BeforeTool,
  AfterAgent, and SessionEnd events.
- `.gemini/policies/*.toml` - policy extension data.

Hooks use Gemini's native event-keyed schema: read JSON from stdin, write
exactly one JSON object to stdout, and send diagnostics to stderr. Gemini
subagents are internal Gemini CLI delegation and are not cmux worker terminals.
Headless `gemini -p` is allowed for smoke, doctor, and CI checks only.

## Install / Update / ry-repair

Install the upstream Gemini CLI runtime:

```bash
npm install -g @google/gemini-cli
gemini --version
```

Clone or update this adapter:

```bash
# First time
git clone https://github.com/NDDev-it-com/rldyour-gemini.git
cd rldyour-gemini

# Update to latest
git pull origin main
```

Run `/ry-repair` convergence from within a Gemini CLI session to normalize
adapter configuration, validate surface adoption, and sync Serena memories.
For offline or check-only mode, run the static validation lane (see
`## Validation`). Runtime doctor:

```bash
gemini --version
gemini -p 'Return exactly READY.' --output-format json
```

The installed-runtime smoke checks require a deliberately configured owner
machine with valid authentication.

## Active Catalog

| Surface | Count |
| --- | ---: |
| Agent Skills (`.gemini/skills/*/SKILL.md`) | 14 |
| TOML commands (`.gemini/commands/**/*.toml`) | 13 |
| Gemini subagents (`.gemini/agents/*.md`) | 7 |
| Hook scripts (`.gemini/hooks/`) | 4 |
| MCP servers (`.gemini/settings.json`) | 11 |

Active MCP inventory: `serena`, `chrome-devtools`, `sequential-thinking`,
`shadcn`, `dart-flutter`, `context7`, `github`, `deepwiki`, `grep`, `figma`,
and `openai-docs`.

Commands are grouped into: `browser`, `flow`, `release`, `ry`, `security`, and
`serena`. Hooks cover `SessionStart`, `BeforeTool`, `AfterAgent`, and
`SessionEnd` events.

## Browser / Design / DevTools Routing

Browser work follows the shared rldyour provider model with three distinct roles:

- **Webwright** - high-level, long-horizon browser workflows, reusable evidence
  scripts, screenshots, logs, and final-script reproduction. Webwright is a
  provider/harness, not an MCP server.
- **Playwright CLI + Skills** - deterministic UI automation, screenshots,
  snapshots, traces, responsive matrices, and visual evidence.
- **Chrome DevTools MCP** (`chrome-devtools`) - console, network, performance,
  Lighthouse, memory, heap, and live Chrome debugging.

Only providers listed in the approved active inventory may be configured.
Removed or historical tools require an explicit inventory and release-policy
update before reintroduction.

Gemini built-in `browser_agent` is disabled for this adapter release. It is not
a silent replacement for any provider above and must be added as a separately
validated explicit provider with dedicated validators before any future use.

### MCP Inventory Detail

The active MCP inventory matches the root positive inventory. All 11 servers are
declared in `.gemini/settings.json` under `mcpServers`:

| Server | Transport | Role |
| --- | --- | --- |
| `serena` | stdio (`uvx`) | LSP-based code intelligence and Serena memory |
| `chrome-devtools` | stdio (`bunx`) | Live Chrome debugging and DevTools |
| `sequential-thinking` | stdio (`bunx`) | Structured reasoning chains |
| `shadcn` | stdio (`bunx`) | shadcn/ui component registry |
| `dart-flutter` | stdio (`dart`) | Dart/Flutter LSP and pub tools |
| `context7` | stdio (`bunx`) | Library documentation lookup |
| `github` | HTTP/SSE | GitHub repos, issues, pull requests |
| `deepwiki` | HTTP/SSE | AI-powered repository documentation |
| `grep` | HTTP/SSE | Cross-repository code search |
| `figma` | HTTP (local) | Figma design context and code connect |
| `openai-docs` | HTTP/SSE | OpenAI API documentation |

## Memory / Fullrepo Model

Normal `main` history carries source-controlled configuration artifacts:
`.gemini/` surfaces, `config/`, `references/`, `scripts/`, tests, and
`CHANGELOG.md`. Agent-only context files - `AGENTS.md`, `GEMINI.md`,
`.serena/project.yml`, and `.serena/memories/` - are kept on the separate
`fullrepo` overlay branch and are not committed to `main` history once
`fullrepo` is initialized.

Serena memory domains active for this adapter:

- `CORE-01-INDEX` - durable memory index.
- `GEMINI-01-ADAPTER-SURFACE` - native surface facts.
- `RUNTIME-01-BASELINE` - pinned runtime version evidence.
- `MCP-01-TOOLS` - MCP inventory facts.
- `BROWSER-01-VALIDATION` - browser provider routing rules.
- `FLOW-01-SDLC` - SDLC flow rules.
- `SECURITY-01-POSTURE` - security posture facts.
- `RELEASE-01-VALIDATION` - release validation rules.
- `SERENA-01-MEMORY-SYNC` - memory maintenance rules.
- `ANTIGRAVITY-01-TRANSITION` - Antigravity transition notice.

Memories store durable facts only (Purpose, Current Facts, Evidence, Operational
Rules, Last Verified). Chat logs, speculation, secrets, tokens, cookies, and
credentials must not be stored.

Freshness contract: re-verify memories after each adapter release and after any
upstream Gemini CLI version change. The `fullrepo` sync script publishes the
overlay with safe force-with-lease.

## Security Boundary

### Approval Mode and YOLO

Committed `.gemini/settings.json` sets `general.defaultApprovalMode =
"auto_edit"` - the maximal owner-autonomy posture that Gemini CLI accepts in
committed configuration. `auto_edit` auto-approves file edits without prompting.
`security.disableYoloMode = false` and `security.toolSandboxing = false` are set
explicitly to preserve full-auto launcher capability.

Full YOLO (auto-approve every action, including shell commands) is
launcher-only:

```bash
GEMINI_SANDBOX=false gemini --approval-mode=yolo
```

Gemini CLI silently downgrades a committed `yolo` value to the default approval
mode. Writing `yolo` into committed settings has no effect and must not be done.

Permissions are not a sandbox. This adapter is designed for an owner workstation
with owner-trusted tools and reviewed MCP servers. It is not suitable as-is for
untrusted multi-user or production environments.

### Secrets

Do not commit Gemini API keys, Google API keys, OAuth material, service-account
JSON, Google Cloud ADC files, cookies, browser profile state, or MCP provider
tokens. `.env.example` documents accepted local variable names; real values must
remain local and git-ignored.

### MCP Trust Boundary

All 11 active MCP servers are owner-reviewed. HTTP/SSE servers (`github`,
`deepwiki`, `grep`, `openai-docs`) use remote endpoints with env-var tokens
where required. The `figma` server runs locally at `127.0.0.1:3845`. No
unapproved third-party MCP server may be added without an explicit inventory and
release-policy update.

### Access and Antigravity Notice

Gemini CLI adapter `1.3.6` targets enterprise, paid API-key, Vertex AI, Google
Cloud, and explicitly owner-approved authenticated environments. Consumer OAuth
availability after June 18, 2026 is `NOT_PROVEN` for this adapter because
Google announced a transition of unpaid and Google One Gemini CLI users to
Antigravity CLI. Antigravity CLI is out of scope for this adapter release. See
`references/gemini-antigravity-transition.md`.

## Validation

Static validation (no runtime required):

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

Installed-runtime smoke checks (optional; require a deliberately configured
owner machine with valid authentication):

```bash
gemini --version
gemini -p 'Return exactly READY.' --output-format json
```

The `NOT_PROVEN` policy applies to any validation result that cannot be
confirmed through local static analysis alone (e.g., live MCP connectivity,
consumer OAuth availability after June 18, 2026).

## Release / Rollback

Releases follow the root control plane numeric tag policy. A `VERSION` file
alone is not a release: the GitHub Release and the numeric tag must point to the
same commit that the root pins in `config/repositories.json`.

- Default version movement is patch (`+0.0.1`) after any source, config, or
  documentation change post-release.
- Minor (`+0.1.0`) and major (`+1.0.0`) bumps are owner-directed decisions only.
- `CHANGELOG.md` documents all notable changes per release.
- `SECURITY.md` lists the currently supported version.
- Only the current exact numeric tag receives security fixes.

To roll back: check out the prior numeric tag, verify the root control plane
pins it in `expected_head`, and run the static validation lane.

## Support / License

License: `AGPL-3.0-or-later`.

Author: Danil Silantyev (github:rldyourmnd), CEO NDDev.

Repository: <https://github.com/NDDev-it-com/rldyour-gemini>

Report security issues privately through GitHub Security Advisories for
`NDDev-it-com/rldyour-gemini`. Do not open public issues for security
vulnerabilities.
