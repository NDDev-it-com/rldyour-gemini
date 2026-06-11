# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and adapter versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
