---
name: design-review
description: "Review design implementation with visual evidence and dynamic masks. RU: дизайн/visual review."
---

# Purpose

Evaluate visual implementation against a Figma export, screenshot, image, or spec.

# Native Gemini Boundary

Use Figma and Chrome DevTools MCP where available; use Playwright CLI for
deterministic visual evidence.

# When To Use

Use for Figma-to-code, responsive visual review, typography/color checks, and
layout deviation analysis.

# Inputs

Expected source, target URL or local app, viewport matrix, and masking rules.

# Procedure

1. Capture actual screenshots.
2. Compare against expected source with dynamic masks.
3. Separate pixel, layout, typography, color/token, accessibility, and false positives.
4. Record artifact paths and confidence.

# Evidence Required

Expected source, actual screenshot paths, mask policy, deviation report, and
DOM/ARIA notes.

# Forbidden Actions

Do not approve visual changes without evidence artifacts.

# Acceptance Checks

`python3 scripts/validate_gemini_browser_routing.py --strict`.

# Failure Reporting

Report each mismatch with source, viewport, severity, and evidence path.

