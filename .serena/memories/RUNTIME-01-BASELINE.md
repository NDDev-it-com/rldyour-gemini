# RUNTIME-01-BASELINE

## Purpose

Record Gemini CLI runtime baseline and source-of-truth policy.

## Current Facts

- Runtime package is `@google/gemini-cli`.
- Target runtime version is `0.46.0`.
- Primary latest source is `npm view @google/gemini-cli version`.
- GitHub tag `v0.46.0` is release provenance.
- Installed runtime smoke requires authentication and is not mandatory for
  source-only validation.

## Evidence

- `config/gemini-baseline.json`
- `README.md`
- `references/gemini-surface-adoption.md`

## Operational Rules

- Do not use unscoped package names such as `gemini-cli` or `gemini/cli`.
- Do not fail source-only validation because preview models are unavailable.

## Last Verified

2026-06-11

