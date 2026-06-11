# Browser Provider Routing

Use the shared rldyour provider model:

- Webwright: high-level long-horizon web workflows, reusable scripts,
  screenshots/logs/evidence, and final-script reproduction.
- Playwright CLI + Skills: deterministic UI automation, screenshots, snapshots,
  traces, responsive matrices, and visual evidence.
- Chrome DevTools MCP: console, network, performance, Lighthouse, memory, heap,
  and live Chrome debugging.

Gemini built-in `browser_agent` is disabled for this release. It is not a silent
replacement for any provider above and must be added as a separately validated
provider before use.

Forbidden current state:

- Active Playwright MCP.
- Webwright as MCP.
- Semgrep as an active MCP or provider.
