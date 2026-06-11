#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_RE = re.compile(r"uses:\s+([^@\s]+)@([a-f0-9]{40})(?:\s+#\s+.+)?$")


def main() -> int:
    errors: list[str] = []
    for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if not stripped.startswith("uses:"):
                continue
            if stripped.startswith("uses: ./"):
                continue
            if not PIN_RE.match(stripped):
                errors.append(f"{path.relative_to(ROOT)}:{lineno}: action is not full-SHA pinned")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("ok: workflow action pins are full SHAs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

