# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and adapter versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.2] - 2026-06-12

### Fixed

- Complete `.serena/project.yml` with current Serena project keys so runtime
  MCP smoke checks no longer rewrite the tracked Gemini project configuration.

## [1.3.1] - 2026-06-12

### Fixed

- Stabilize the public 1.3 line with release CI, Context7 MCP freshness, and synchronized four-adapter evidence.

## [1.3.0] - 2026-06-12

### Added

- Add Gemini-native `/ry:init`, `/ry:newp`, `/ry:review`, `/ry:deploy`, and `/ry:sync` TOML commands plus matching Agent Skills so Gemini reaches the root seven-flow lifecycle contract.

### Changed

- Align the Gemini adapter product version with the coordinated four-configuration `1.3.0` stable release contract. This intentionally advances from `1.0.3` to `1.3.0` so Claude, Codex, OpenCode, and Gemini publish the same stable adapter line while retaining Gemini CLI `0.46.0` as the runtime baseline.

## [1.0.3] - 2026-06-12

### Fixed

- Use Gemini CLI native `ui.loadingPhrases = "off"` and enforce the documented enum in settings validation.

## [1.0.2] - 2026-06-12

### Fixed

- Aligned Gemini MCP configuration with native `timeout` milliseconds.
- Converted Gemini hooks to event-keyed native configuration with JSON stdin/stdout contracts.
- Declared sensitive extension environment variables through manifest `settings`.
- Replaced cross-tool subagent shorthand with Gemini-native tool identifiers.
- Added projection parity validation for `.gemini/*` runtime surfaces.
- Documented the disabled Gemini built-in `browser_agent` policy for this release.

## [1.0.1] - 2026-06-12

### Changed

- Updated GitHub Actions dependencies: `actions/checkout` `6.0.3` and
  `github/codeql-action` `4.36.2`.


## [1.0.0] - 2026-06-11

### Added

- Initial public Gemini CLI adapter with native `GEMINI.md`, settings,
  extension manifest, TOML commands, Agent Skills, subagents, hooks, policies,
  MCP inventory, browser-provider routing, Serena memories, validators, and
  tests.
- Runtime baseline for `@google/gemini-cli` `0.46.0`.
- Antigravity transition policy documentation for Gemini CLI access channels.
