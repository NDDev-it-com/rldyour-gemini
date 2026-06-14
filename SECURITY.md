# Security Policy

## Supported Versions

Only the current exact numeric product release tag receives security fixes. The
`1.3.x` line label tracks only the latest released patch, not every historical
patch in the line. Development snapshots and older tags are not supported unless
the root control plane explicitly pins them.

| Version | Supported |
| --- | --- |
| Current exact tag `1.3.6` | yes |
| Older minor / major lines | no |

## Secrets

Do not commit Gemini API keys, Google API keys, OAuth material, service-account
JSON, Google Cloud ADC files, cookies, browser profile state, or MCP provider
tokens. `.env.example` documents accepted local variable names; real values must
remain local and ignored.

## Runtime Posture

Committed Gemini project settings use the `auto_edit` approval mode: the maximal
owner-autonomy posture that Gemini CLI accepts in committed config (it
auto-approves edits without prompting). Full YOLO (auto-approve every action,
including shell) can only be enabled through the launcher
(`gemini --approval-mode=yolo`); Gemini CLI silently downgrades a committed
`yolo` value to default, so YOLO must never be written into committed settings.

## Reporting

Report security issues privately through GitHub security advisories for
`NDDev-it-com/rldyour-gemini`.
