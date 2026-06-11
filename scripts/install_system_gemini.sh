#!/usr/bin/env bash
set -euo pipefail

apply=0
gemini_home="${GEMINI_HOME:-$HOME/.gemini}"

while (($#)); do
  case "$1" in
    --apply) apply=1 ;;
    --gemini-home)
      shift
      gemini_home="${1:?missing --gemini-home value}"
      ;;
    -h|--help)
      printf '%s\n' "usage: scripts/install_system_gemini.sh [--apply] [--gemini-home PATH]"
      exit 0
      ;;
    *)
      printf 'unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
  shift
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
extension_dir="$gemini_home/extensions/rldyour-gemini"

if [[ "$apply" -eq 0 ]]; then
  printf 'dry-run: would install Gemini extension into %s\n' "$extension_dir"
  printf 'dry-run: would copy GEMINI.md, gemini-extension.json, commands, skills, agents, hooks, and policies\n'
  exit 0
fi

mkdir -p "$extension_dir"
cp "$repo_root/GEMINI.md" "$extension_dir/GEMINI.md"
cp "$repo_root/gemini-extension.json" "$extension_dir/gemini-extension.json"
rm -rf "$extension_dir/commands" "$extension_dir/skills" "$extension_dir/agents" "$extension_dir/hooks" "$extension_dir/policies"
cp -R "$repo_root/.gemini/commands" "$extension_dir/commands"
cp -R "$repo_root/.gemini/skills" "$extension_dir/skills"
cp -R "$repo_root/.gemini/agents" "$extension_dir/agents"
cp -R "$repo_root/.gemini/hooks" "$extension_dir/hooks"
cp -R "$repo_root/.gemini/policies" "$extension_dir/policies"
printf 'installed: %s\n' "$extension_dir"

