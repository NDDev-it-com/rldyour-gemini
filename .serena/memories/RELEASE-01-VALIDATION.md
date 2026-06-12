# RELEASE-01-VALIDATION

## Purpose

Record release validation requirements for the current Gemini adapter release.

## Current Facts

- Current adapter release is `1.0.3`.
- Initial adapter release was `1.0.0`.
- Only exact current numeric tags are supported.
- Public CI must use GitHub-hosted runners and full SHA-pinned actions.
- Source archives must exclude caches, runtime state, secrets, and local browser
  artifacts.

## Evidence

- `VERSION`
- `CHANGELOG.md`
- `SECURITY.md`
- `references/release-version-policy.md`
- `references/public-ci-policy.md`
- `.github/workflows/validate.yml`

## Operational Rules

- Do not certify release without local validators, pytest, GitHub Release
  evidence, and clean archive hygiene.

## Last Verified

2026-06-12
