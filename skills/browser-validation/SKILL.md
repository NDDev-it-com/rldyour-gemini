---
name: browser-validation
description: "Проверь browser/UI поведение через Webwright, Playwright CLI и Chrome DevTools MCP. EN: validate browser behavior."
---

# Purpose

Collect browser evidence for UI flows, screenshots, traces, and runtime defects.

# Native Gemini Boundary

Gemini delegates browser work through documented providers; Playwright and
Webwright are not Gemini MCP servers.

# When To Use

Use for browser flows, UI behavior, screenshots, traces, console/network
diagnostics, and visual evidence.

# Inputs

URL, preconditions, viewport matrix, expected source, and task objective.

# Procedure

1. Route high-level long-horizon tasks to Webwright.
2. Route deterministic screenshots, snapshots, and traces to Playwright CLI.
3. Route console, network, Lighthouse, performance, and memory to Chrome DevTools MCP.
4. Save evidence paths and summarize deviations.

# Evidence Required

Provider used, URL/state, viewport matrix, screenshots/traces/logs, and findings.

# Forbidden Actions

Use only approved active browser providers and do not treat Webwright as MCP.

# Acceptance Checks

`python3 scripts/validate_gemini_browser_routing.py --strict`.

# Failure Reporting

Separate proven defects from `NOT_PROVEN` provider or auth gaps.
