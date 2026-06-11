#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRET_RE = re.compile(r"(AIza[0-9A-Za-z_-]{20,}|-----BEGIN PRIVATE KEY-----|\"private_key\"|GEMINI_API_KEY=.+\S|GOOGLE_API_KEY=.+\S)")
ALLOW = {".env.example", "scripts/scan_text_security.py"}


def main() -> int:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if any(part in {".git", ".pytest_cache", ".ruff_cache", ".serena/cache", "__pycache__"} for part in path.parts):
            continue
        if rel in ALLOW:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SECRET_RE.search(text):
            errors.append(rel)
    if errors:
        for rel in errors:
            print(f"ERROR: possible secret in {rel}", file=sys.stderr)
        return 1
    print("ok: no obvious committed secrets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
