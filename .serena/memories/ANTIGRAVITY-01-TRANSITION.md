# ANTIGRAVITY-01-TRANSITION

## Purpose

Record Gemini CLI access risk from the Antigravity transition.

## Current Facts

- Consumer OAuth availability after `2026-06-18` is `NOT_PROVEN`.
- Supported targets are enterprise, paid API-key, Vertex AI, Google Cloud, and
  owner-approved authenticated environments.
- Antigravity CLI is out of scope for adapter `1.3.6`.

## Evidence

- `config/gemini-baseline.json`
- `references/gemini-antigravity-transition.md`
- `references/authentication.md`

## Operational Rules

- Do not promise long-term consumer OAuth support.
- Do not add an Antigravity adapter without verified upstream contracts.

## Last Verified

2026-06-13
