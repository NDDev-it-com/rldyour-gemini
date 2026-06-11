#!/usr/bin/env bash
set -euo pipefail

if find . -path './.git' -prune -o -path './.serena/cache' -prune -o -name '.rldyour-runtime-*' -print | grep -q .; then
  printf '%s\n' "warning: runtime marker remains; cleanup requires explicit owner-approved command"
fi

exit 0

