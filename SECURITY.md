# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| `1.3.3` | Yes |

Only the current exact tag `1.3.3` receives security fixes. The `1.3.x` line label tracks only the latest released patch, not every historical patch in the line. Development snapshots and older tags are not supported unless the root control plane explicitly pins them.

## Secrets

Do not commit Gemini API keys, Google API keys, OAuth material, service-account
JSON, Google Cloud ADC files, cookies, browser profile state, or MCP provider
tokens. `.env.example` documents accepted local variable names; real values must
remain local and ignored.

## Runtime Posture

Committed Gemini project settings use the default approval mode. YOLO/full-auto
execution is an owner launcher decision and must not be silently enabled by this
repository.

## Reporting

Report security issues privately through GitHub security advisories for
`NDDev-it-com/rldyour-gemini`.
