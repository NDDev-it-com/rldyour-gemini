#!/usr/bin/env bash
set -euo pipefail

scripts/validate_fast.sh
python3 scripts/validate_serena_memory_schema.py --strict
python3 scripts/validate_serena_memory_semantics.py --strict
python3 -m py_compile scripts/*.py
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git diff --check
fi
