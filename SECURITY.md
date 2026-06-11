# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| `1.0.0` | Yes |

Only the exact current numeric release is supported. Development snapshots and
older tags are not supported unless the root control plane explicitly pins them.

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

