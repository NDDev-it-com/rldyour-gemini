#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.1"
RUNTIME_VERSION = "0.46.0"
RUNTIME_PACKAGE = "@google/gemini-cli"
EXPECTED_MCP = [
    "serena",
    "chrome-devtools",
    "sequential-thinking",
    "shadcn",
    "dart-flutter",
    "context7",
    "github",
    "deepwiki",
    "grep",
    "figma",
    "openai-docs",
]
RETIRED_PATTERNS = [
    re.compile(r"@playwright/mcp", re.IGNORECASE),
    re.compile(r"\bplaywright[-_ ]mcp\b", re.IGNORECASE),
    re.compile(r"\bsemgrep\b", re.IGNORECASE),
]
RETIRED_ALLOWED = {
    "README.md",
    "AGENTS.md",
    "GEMINI.md",
    "config/browser-provider-policy.json",
    "config/current-claim-rules.json",
    "config/rldyour-contract.json",
    "references/browser-provider-routing.md",
}
MEMORY_SECTIONS = [
    "## Purpose",
    "## Current Facts",
    "## Evidence",
    "## Operational Rules",
    "## Last Verified",
]


class ValidationError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def version_file() -> str:
    return read_text(ROOT / "VERSION").strip()


def validate_version_surfaces() -> None:
    require(version_file() == VERSION, f"VERSION must be {VERSION}")
    pyproject = load_toml(ROOT / "pyproject.toml")
    require(pyproject["project"]["version"] == VERSION, "pyproject version must match VERSION")
    manifest = load_json(ROOT / "gemini-extension.json")
    require(manifest["version"] == VERSION, "gemini-extension version must match VERSION")
    contract = load_json(ROOT / "config/rldyour-contract.json")
    require(contract["adapter"]["version"] == VERSION, "contract adapter version must match VERSION")


def validate_runtime_baseline(strict: bool = False) -> None:
    baseline = load_json(ROOT / "config/gemini-baseline.json")
    require(baseline["npm_package"] == RUNTIME_PACKAGE, "Gemini runtime package must be @google/gemini-cli")
    require(baseline["target_runtime_version"] == RUNTIME_VERSION, "Gemini runtime baseline must be 0.46.0")
    require(baseline["target_channel"] == "stable/npm-latest", "Gemini target channel must be stable/npm-latest")
    priority = baseline["source_of_truth_priority"]
    require(priority[0] == "npm view @google/gemini-cli version", "npm must be primary Gemini source of truth")
    transition = baseline["antigravity_transition"]
    require(transition["date"] == "2026-06-18", "Antigravity transition date must be recorded")
    require(
        transition["consumer_oauth_long_term_availability"] == "NOT_PROVEN",
        "consumer OAuth longevity must be NOT_PROVEN",
    )
    if strict and os.environ.get("RLDYOUR_VALIDATE_LIVE_GEMINI") == "1":
        proc = subprocess.run(
            ["npm", "view", RUNTIME_PACKAGE, "version"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
        require(proc.returncode == 0, f"npm view failed: {proc.stderr.strip()}")
        require(proc.stdout.strip() == RUNTIME_VERSION, f"npm latest {proc.stdout.strip()} != {RUNTIME_VERSION}")


def validate_mcp_map(mcp: dict[str, Any], source: str) -> None:
    keys = sorted(mcp)
    require(keys == sorted(EXPECTED_MCP), f"{source}: MCP aliases must match expected 11 servers")
    for alias, spec in mcp.items():
        require("_" not in alias, f"{source}: MCP alias must not contain underscore: {alias}")
        require(alias not in {"playwright", "playwright-mcp", "semgrep", "semgrep-mcp"}, f"{source}: retired MCP alias active: {alias}")
        require(isinstance(spec, dict), f"{source}: MCP spec must be an object for {alias}")
        require(spec.get("trust") is not True, f"{source}: trust=true is forbidden for {alias}")
        if "command" in spec:
            require(isinstance(spec["command"], str) and spec["command"], f"{source}: command must be a non-empty string for {alias}")
            require(isinstance(spec.get("args", []), list), f"{source}: args must be a list for {alias}")
            require(" " not in spec["command"], f"{source}: command must not shell-concatenate args for {alias}")
        else:
            require("url" in spec, f"{source}: MCP spec needs command or url for {alias}")


def validate_mcp_inventory() -> None:
    manifest = load_json(ROOT / "gemini-extension.json")
    settings = load_json(ROOT / ".gemini/settings.json")
    contract = load_json(ROOT / "config/rldyour-contract.json")
    validate_mcp_map(manifest["mcpServers"], "gemini-extension.json")
    validate_mcp_map(settings["mcpServers"], ".gemini/settings.json")
    require(sorted(contract["mcp_servers"]) == sorted(EXPECTED_MCP), "contract MCP list must match expected inventory")


def validate_manifest() -> None:
    manifest = load_json(ROOT / "gemini-extension.json")
    require(manifest["name"] == "rldyour-gemini", "extension name must be rldyour-gemini")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", manifest["name"]) is not None, "extension name must be lowercase dash-separated")
    require(manifest["version"] == VERSION, f"extension version must be {VERSION}")
    require(manifest["contextFileName"] == "GEMINI.md", "contextFileName must be GEMINI.md")
    require("mcpServers" in manifest, "extension manifest must define mcpServers")
    require("excludeTools" in manifest and manifest["excludeTools"], "extension manifest must define excludeTools")
    validate_mcp_map(manifest["mcpServers"], "gemini-extension.json")


def validate_settings() -> None:
    settings = load_json(ROOT / ".gemini/settings.json")
    require(settings["context"]["fileName"] == "GEMINI.md", "settings context fileName must be GEMINI.md")
    require(settings["general"]["defaultApprovalMode"] == "default", "committed settings must not enable YOLO")
    require(settings["privacy"]["usageStatisticsEnabled"] is False, "usage statistics must be disabled in template")
    require(settings["hooksConfig"]["enabled"] is True, "hooks must be enabled")
    validate_mcp_map(settings["mcpServers"], ".gemini/settings.json")


def command_files() -> list[Path]:
    return sorted((ROOT / ".gemini/commands").glob("**/*.toml"))


def validate_commands() -> None:
    files = command_files()
    require(len(files) >= 8, "at least 8 Gemini commands are required")
    for path in files:
        data = load_toml(path)
        rel = path.relative_to(ROOT / ".gemini/commands")
        expected = ":".join(rel.with_suffix("").parts)
        require(data.get("name") == expected, f"{path}: command name must match path namespace {expected}")
        require("RU:" in data.get("description", "") and "EN:" in data.get("description", ""), f"{path}: description must be RU/EN")
        prompt = data.get("prompt", "")
        require(isinstance(prompt, str) and len(prompt.strip()) > 80, f"{path}: prompt is required")
        require("{{args}}" in prompt, f"{path}: prompt must mention user args")
        require("!{" not in prompt, f"{path}: shell injection syntax is forbidden")


def validate_skills() -> None:
    skills = sorted((ROOT / ".gemini/skills").glob("*/SKILL.md"))
    require(len(skills) >= 8, "at least 8 Gemini skills are required")
    required = [
        "# Purpose",
        "# Native Gemini Boundary",
        "# When To Use",
        "# Inputs",
        "# Procedure",
        "# Evidence Required",
        "# Forbidden Actions",
        "# Acceptance Checks",
        "# Failure Reporting",
    ]
    for path in skills:
        text = read_text(path)
        require(text.startswith("---\n"), f"{path}: skill frontmatter required")
        require("name:" in text and "description:" in text, f"{path}: name and description required")
        for heading in required:
            require(heading in text, f"{path}: missing heading {heading}")


def validate_subagents() -> None:
    agents = sorted((ROOT / ".gemini/agents").glob("*.md"))
    require(len(agents) >= 7, "at least 7 Gemini subagents are required")
    required = [
        "# Purpose",
        "# Allowed Tools",
        "# MCP Server Access Policy",
        "# Browser Provider Routing",
        "# Report Contract",
        "# Restrictions",
    ]
    for path in agents:
        text = read_text(path)
        require(text.startswith("---\n"), f"{path}: agent frontmatter required")
        require("name:" in text and "description:" in text, f"{path}: name and description required")
        for heading in required:
            require(heading in text, f"{path}: missing heading {heading}")
        lowered = text.lower()
        require("commit, push" in lowered or "do not tag" in lowered or "do not commit" in lowered, f"{path}: mutation restrictions required")


def validate_hooks() -> None:
    hooks = load_json(ROOT / ".gemini/hooks/hooks.json")["hooks"]
    events = {hook["event"] for hook in hooks}
    require(events == {"SessionStart", "BeforeTool", "AfterAgent", "SessionEnd"}, "hook events must match required lifecycle")
    for hook in hooks:
        command = ROOT / hook["command"]
        require(command.exists(), f"hook command missing: {hook['command']}")
        require(hook.get("timeout_seconds", 0) > 0 and hook["timeout_seconds"] <= 10, f"{hook['event']}: hook timeout must be bounded")
        text = read_text(command)
        require("set -euo pipefail" in text, f"{command}: strict shell mode required")
        require("while true" not in text and "for ((" not in text, f"{command}: unbounded loops forbidden")


def validate_browser_routing() -> None:
    policy = load_json(ROOT / "config/browser-provider-policy.json")
    providers = policy["providers"]
    require(providers["webwright"]["mcp"] is False, "Webwright must not be MCP")
    require(providers["playwright-cli"]["mcp"] is False, "Playwright CLI must not be MCP")
    require(providers["chrome-devtools-mcp"]["mcp"] is True, "Chrome DevTools MCP must remain active")
    docs = "\n".join(read_text(path) for path in [
        ROOT / "README.md",
        ROOT / "references/browser-provider-routing.md",
        ROOT / ".gemini/skills/browser-validation/SKILL.md",
    ])
    for phrase in ["Webwright", "Playwright CLI", "Chrome DevTools MCP"]:
        require(phrase in docs, f"browser docs must mention {phrase}")


def validate_native_boundaries() -> None:
    contract = load_json(ROOT / "config/rldyour-contract.json")
    required = {
        "gemini_context",
        "gemini_settings_json",
        "gemini_extension_manifest",
        "gemini_commands_toml",
        "gemini_skills",
        "gemini_subagents",
        "gemini_hooks",
        "gemini_policies",
        "gemini_mcp_servers",
        "gemini_headless_prompt",
    }
    require(required.issubset(set(contract["native_surfaces"])), "contract missing native Gemini surfaces")
    text = read_text(ROOT / "references/gemini-native-boundaries.md")
    require("Claude Code slash-command files" in text, "native boundary doc must reject Claude runtime surfaces")
    require("Codex plugin manifests" in text, "native boundary doc must reject Codex runtime surfaces")
    require("OpenCode" in text and "command" in text and "JSON" in text, "native boundary doc must reject OpenCode runtime surfaces")


def validate_antigravity_policy() -> None:
    baseline = load_json(ROOT / "config/gemini-baseline.json")
    doc = read_text(ROOT / "references/gemini-antigravity-transition.md")
    require("2026-06-18" in doc and baseline["antigravity_transition"]["date"] == "2026-06-18", "transition date required")
    require("NOT_PROVEN" in doc, "Antigravity transition doc must mark future adapter path NOT_PROVEN")
    require("Antigravity CLI is not in scope" in doc, "Antigravity out-of-scope statement required")
    require("enterprise" in doc.lower() and "api-key" in doc.lower() and "vertex" in doc.lower(), "supported access channels required")


def validate_instruction_docs() -> None:
    docs = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "GEMINI.md", ROOT / "SECURITY.md"]
    combined = "\n".join(read_text(path) for path in docs)
    for phrase in [VERSION, RUNTIME_VERSION, RUNTIME_PACKAGE, "Playwright MCP", "Semgrep", "Antigravity"]:
        require(phrase in combined, f"instruction docs must mention {phrase}")
    require("YOLO" in combined and "launcher" in combined, "docs must keep YOLO launcher-only")


def validate_serena_memories() -> None:
    memories = sorted((ROOT / ".serena/memories").glob("*.md"))
    require(len(memories) >= 9, "Gemini adapter must have at least 9 Serena memories")
    for path in memories:
        text = read_text(path)
        for section in MEMORY_SECTIONS:
            require(section in text, f"{path}: missing {section}")
        require(re.search(r"## Last Verified\s+\d{4}-\d{2}-\d{2}", text) is not None, f"{path}: Last Verified date required")
        require("Evidence" in text and "- `" in text, f"{path}: path evidence required")


def validate_retired_residue() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".json", ".toml", ".py", ".sh", ".env"} and path.name not in {"GEMINI.md", "AGENTS.md"}:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == "scripts/gemini_contract.py":
            continue
        if rel.startswith((".gemini/commands/", ".gemini/skills/", ".gemini/agents/", ".gemini/policies/", ".gemini/hooks/", ".serena/memories/", "commands/", "skills/", "agents/", "policies/", "hooks/", "tests/")):
            continue
        text = read_text(path)
        for pattern in RETIRED_PATTERNS:
            if pattern.search(text) and rel not in RETIRED_ALLOWED:
                raise ValidationError(f"{rel}: retired-tool current-doc residue: {pattern.pattern}")


def validate_all(strict: bool = False) -> None:
    validate_version_surfaces()
    validate_runtime_baseline(strict=strict)
    validate_manifest()
    validate_settings()
    validate_mcp_inventory()
    validate_commands()
    validate_skills()
    validate_subagents()
    validate_hooks()
    validate_browser_routing()
    validate_native_boundaries()
    validate_antigravity_policy()
    validate_instruction_docs()
    validate_serena_memories()
    validate_retired_residue()


VALIDATORS: dict[str, Callable[[bool], None]] = {
    "all": validate_all,
    "config": lambda strict: (validate_version_surfaces(), validate_settings(), validate_manifest(), validate_mcp_inventory()),
    "manifest": lambda strict: validate_manifest(),
    "commands": lambda strict: validate_commands(),
    "skills": lambda strict: validate_skills(),
    "subagents": lambda strict: validate_subagents(),
    "hooks": lambda strict: validate_hooks(),
    "mcp": lambda strict: validate_mcp_inventory(),
    "browser": lambda strict: validate_browser_routing(),
    "runtime": lambda strict: validate_runtime_baseline(strict=strict),
    "instructions": lambda strict: validate_instruction_docs(),
    "memories": lambda strict: validate_serena_memories(),
    "native": lambda strict: validate_native_boundaries(),
    "antigravity": lambda strict: validate_antigravity_policy(),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate rldyour Gemini adapter surfaces.")
    parser.add_argument("target", choices=sorted(VALIDATORS), nargs="?", default="all")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        VALIDATORS[args.target](args.strict)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"ok: Gemini {args.target} validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
