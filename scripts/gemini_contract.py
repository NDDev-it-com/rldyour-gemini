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
VERSION = "1.3.2"
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
NATIVE_MCP_KEYS = {
    "command",
    "args",
    "env",
    "cwd",
    "url",
    "httpUrl",
    "headers",
    "timeout",
    "description",
    "includeTools",
    "excludeTools",
}
SECRET_ENV_RE = re.compile(r"\$\{([A-Z0-9_]*(?:TOKEN|KEY|SECRET|PASSWORD)[A-Z0-9_]*)\}")
PROJECTION_FOLDERS = ["commands", "skills", "agents", "hooks", "policies"]
REQUIRED_RY_COMMANDS = {
    "ry:init",
    "ry:start",
    "ry:newp",
    "ry:review",
    "ry:repair",
    "ry:deploy",
    "ry:sync",
}
REQUIRED_LIFECYCLE_SKILLS = {
    "ry-init",
    "ry-start",
    "ry-newp",
    "ry-review",
    "ry-repair",
    "ry-deploy",
    "ry-sync",
}
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
        unsupported = sorted(set(spec) - NATIVE_MCP_KEYS)
        require(not unsupported, f"{source}: unsupported Gemini MCP keys for {alias}: {unsupported}")
        require(spec.get("trust") is not True, f"{source}: trust=true is forbidden for {alias}")
        if "timeout" in spec:
            require(isinstance(spec["timeout"], int) and spec["timeout"] > 0, f"{source}: timeout must be positive milliseconds for {alias}")
        if "command" in spec:
            require(isinstance(spec["command"], str) and spec["command"], f"{source}: command must be a non-empty string for {alias}")
            require(isinstance(spec.get("args", []), list), f"{source}: args must be a list for {alias}")
            require(" " not in spec["command"], f"{source}: command must not shell-concatenate args for {alias}")
        else:
            require("url" in spec or "httpUrl" in spec, f"{source}: MCP spec needs command, url, or httpUrl for {alias}")


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
    validate_extension_secret_settings(manifest)
    validate_mcp_map(manifest["mcpServers"], "gemini-extension.json")


def collect_secret_env_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, str):
        refs.update(SECRET_ENV_RE.findall(value))
    elif isinstance(value, list):
        for item in value:
            refs.update(collect_secret_env_refs(item))
    elif isinstance(value, dict):
        for item in value.values():
            refs.update(collect_secret_env_refs(item))
    return refs


def validate_extension_secret_settings(manifest: dict[str, Any] | None = None) -> None:
    manifest = manifest or load_json(ROOT / "gemini-extension.json")
    settings = manifest.get("settings")
    require(isinstance(settings, list), "extension manifest must declare settings for secret env vars")
    declared: dict[str, dict[str, Any]] = {}
    for item in settings:
        require(isinstance(item, dict), "extension settings entries must be objects")
        env_var = item.get("envVar")
        require(isinstance(env_var, str) and env_var, "extension settings entries must declare envVar")
        declared[env_var] = item
        if re.search(r"TOKEN|KEY|SECRET|PASSWORD", env_var):
            require(item.get("sensitive") is True, f"extension setting {env_var} must be sensitive")

    refs = collect_secret_env_refs(manifest.get("mcpServers", {}))
    missing = sorted(refs - set(declared))
    require(not missing, f"extension secret env refs must be declared in settings: {missing}")


def validate_settings() -> None:
    settings = load_json(ROOT / ".gemini/settings.json")
    require(settings["context"]["fileName"] == "GEMINI.md", "settings context fileName must be GEMINI.md")
    require(settings["general"]["defaultApprovalMode"] == "default", "committed settings must not enable YOLO")
    require(settings["general"]["checkpointing"]["enabled"] is True, "settings general.checkpointing.enabled must be true")
    loading_phrases = settings["ui"].get("loadingPhrases")
    require(
        loading_phrases in {"tips", "witty", "all", "off"},
        "settings ui.loadingPhrases must use Gemini native enum: tips, witty, all, or off",
    )
    require(settings["privacy"]["usageStatisticsEnabled"] is False, "usage statistics must be disabled in template")
    require(settings["hooksConfig"]["enabled"] is True, "hooks must be enabled")
    validate_hook_config(settings.get("hooks"), ".gemini/settings.json hooks", project_settings=True)
    validate_mcp_map(settings["mcpServers"], ".gemini/settings.json")


def validate_hook_config(config: Any, source: str, *, project_settings: bool) -> None:
    require(isinstance(config, dict), f"{source}: hooks must be an event-keyed object")
    expected = {"SessionStart", "BeforeTool", "AfterAgent", "SessionEnd"}
    require(set(config) == expected, f"{source}: hook events must match {sorted(expected)}")
    for event, definitions in config.items():
        require(isinstance(definitions, list) and definitions, f"{source}: {event} must be a non-empty list")
        for definition in definitions:
            require(isinstance(definition, dict), f"{source}: {event} hook definition must be an object")
            require(isinstance(definition.get("matcher"), str), f"{source}: {event} matcher is required")
            hooks = definition.get("hooks")
            require(isinstance(hooks, list) and hooks, f"{source}: {event} hooks array is required")
            for hook in hooks:
                require(isinstance(hook, dict), f"{source}: {event} hook entry must be an object")
                require(hook.get("type") == "command", f"{source}: {event} hook type must be command")
                command = hook.get("command")
                require(isinstance(command, str) and command, f"{source}: {event} hook command is required")
                if project_settings:
                    require(command.startswith("$GEMINI_PROJECT_DIR/.gemini/hooks/"), f"{source}: {event} project hook command must use $GEMINI_PROJECT_DIR")
                else:
                    require(command.startswith("${extensionPath}/hooks/"), f"{source}: {event} extension hook command must use ${'{'}extensionPath{'}'}")
                timeout = hook.get("timeout")
                require(isinstance(timeout, int) and 0 < timeout <= 10000, f"{source}: {event} timeout must be bounded milliseconds")


def command_files() -> list[Path]:
    return sorted((ROOT / ".gemini/commands").glob("**/*.toml"))


def validate_commands() -> None:
    files = command_files()
    require(len(files) >= 8, "at least 8 Gemini commands are required")
    command_names: set[str] = set()
    for path in files:
        data = load_toml(path)
        rel = path.relative_to(ROOT / ".gemini/commands")
        expected = ":".join(rel.with_suffix("").parts)
        command_names.add(str(data.get("name")))
        require(data.get("name") == expected, f"{path}: command name must match path namespace {expected}")
        require("RU:" in data.get("description", "") and "EN:" in data.get("description", ""), f"{path}: description must be RU/EN")
        prompt = data.get("prompt", "")
        require(isinstance(prompt, str) and len(prompt.strip()) > 80, f"{path}: prompt is required")
        require("{{args}}" in prompt, f"{path}: prompt must mention user args")
        require("!{" not in prompt, f"{path}: shell injection syntax is forbidden")
    missing = sorted(REQUIRED_RY_COMMANDS - command_names)
    require(not missing, f"missing required Gemini lifecycle commands: {missing}")


def validate_skills() -> None:
    skills = sorted((ROOT / ".gemini/skills").glob("*/SKILL.md"))
    require(len(skills) >= 8, "at least 8 Gemini skills are required")
    skill_names: set[str] = set()
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
        match = re.search(r"^name:\s*([A-Za-z0-9_-]+)\s*$", text, re.MULTILINE)
        require(match is not None, f"{path}: skill name must be parseable")
        skill_names.add(match.group(1))
        for heading in required:
            require(heading in text, f"{path}: missing heading {heading}")
    missing = sorted(REQUIRED_LIFECYCLE_SKILLS - skill_names)
    require(not missing, f"missing required Gemini lifecycle skills: {missing}")


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
        frontmatter = text.split("---", 2)[1]
        require('"read"' not in frontmatter and '"grep"' not in frontmatter and '"shell"' not in frontmatter, f"{path}: cross-tool shorthand is forbidden")
        require("mcp:" not in frontmatter, f"{path}: MCP shorthand with colon is forbidden")
        tools_match = re.search(r"tools:\s*\[(.*?)\]", frontmatter, re.DOTALL)
        require(tools_match is not None, f"{path}: tools array required")
        tools = [item.strip().strip("'\"") for item in tools_match.group(1).split(",") if item.strip()]
        for tool in tools:
            require(
                tool in {"read_file", "grep_search", "run_shell_command"} or re.fullmatch(r"mcp_[A-Za-z0-9-]+_\*", tool),
                f"{path}: non-native Gemini tool name {tool!r}",
            )
        for heading in required:
            require(heading in text, f"{path}: missing heading {heading}")
        lowered = text.lower()
        require("commit, push" in lowered or "do not tag" in lowered or "do not commit" in lowered, f"{path}: mutation restrictions required")


def validate_hooks() -> None:
    hooks = load_json(ROOT / ".gemini/hooks/hooks.json")
    validate_hook_config(hooks, ".gemini/hooks/hooks.json", project_settings=False)
    source_hooks = load_json(ROOT / "hooks/hooks.json")
    require(source_hooks == hooks, "source hooks and .gemini projection hooks must match")
    for event, definitions in hooks.items():
        for definition in definitions:
            for hook in definition["hooks"]:
                script = ROOT / "hooks" / Path(str(hook["command"])).name
                require(script.exists(), f"hook command missing: {script.relative_to(ROOT)}")
                text = read_text(script)
                require("set -euo pipefail" in text, f"{script}: strict shell mode required")
                require("while true" not in text and "for ((" not in text, f"{script}: unbounded loops forbidden")
                validate_hook_script_json(script, event)


def validate_hook_script_json(script: Path, event: str) -> None:
    payload: dict[str, Any] = {
        "session_id": "validation",
        "cwd": str(ROOT),
        "hook_event_name": event,
        "timestamp": "2026-06-12T00:00:00Z",
    }
    if event == "BeforeTool":
        payload.update({"tool_name": "run_shell_command", "tool_input": {"command": "git status --short"}})
    proc = subprocess.run(
        [str(script)],
        cwd=ROOT,
        input=json.dumps(payload),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5,
        check=False,
    )
    require(proc.returncode == 0, f"{script.relative_to(ROOT)}: hook smoke failed: {proc.stderr.strip()}")
    try:
        decoded = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{script.relative_to(ROOT)}: stdout must be one JSON object: {exc}") from exc
    require(isinstance(decoded, dict), f"{script.relative_to(ROOT)}: stdout JSON must be an object")
    require(proc.stdout.strip().startswith("{") and proc.stdout.strip().endswith("}"), f"{script.relative_to(ROOT)}: stdout must contain only JSON")


def validate_browser_routing() -> None:
    policy = load_json(ROOT / "config/browser-provider-policy.json")
    providers = policy["providers"]
    require(providers["webwright"]["mcp"] is False, "Webwright must not be MCP")
    require(providers["playwright-cli"]["mcp"] is False, "Playwright CLI must not be MCP")
    require(providers["chrome-devtools-mcp"]["mcp"] is True, "Chrome DevTools MCP must remain active")
    browser_agent = policy.get("gemini_builtin_browser_agent") or {}
    require(browser_agent.get("enabled") is False, "Gemini built-in browser_agent must be disabled for this release")
    require(
        set(browser_agent.get("must_not_replace") or []) == {"webwright", "playwright-cli", "chrome-devtools-mcp"},
        "Gemini browser_agent policy must preserve the canonical provider matrix",
    )
    docs = "\n".join(read_text(path) for path in [
        ROOT / "README.md",
        ROOT / "references/browser-provider-routing.md",
        ROOT / "references/gemini-surface-adoption.md",
        ROOT / ".gemini/skills/browser-validation/SKILL.md",
    ])
    for phrase in ["Webwright", "Playwright CLI", "Chrome DevTools MCP"]:
        require(phrase in docs, f"browser docs must mention {phrase}")
    require("browser_agent" in docs and "disabled" in docs.lower(), "browser docs must record disabled Gemini browser_agent policy")


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


def validate_runtime_channel_policy() -> None:
    baseline = load_json(ROOT / "config/gemini-baseline.json")
    priority = baseline.get("source_of_truth_priority") or []
    require(priority and priority[0] == "npm view @google/gemini-cli version", "npm latest must be primary Gemini stable source")
    forbidden = set(baseline.get("forbidden_as_stable") or [])
    required = {
        "github-main-package-json-nightly",
        "github-releases-latest-redirect-when-conflicting",
        "preview-tag",
        "nightly-tag",
    }
    require(required.issubset(forbidden), "Gemini runtime channel policy must reject nightly/preview/latest-redirect drift")


def validate_projection_parity() -> None:
    for folder in PROJECTION_FOLDERS:
        source_dir = ROOT / folder
        projected_dir = ROOT / ".gemini" / folder
        require(source_dir.is_dir(), f"missing source projection folder: {folder}")
        require(projected_dir.is_dir(), f"missing .gemini projection folder: {folder}")
        source_files = sorted(path.relative_to(source_dir) for path in source_dir.rglob("*") if path.is_file())
        projected_files = sorted(path.relative_to(projected_dir) for path in projected_dir.rglob("*") if path.is_file())
        require(source_files == projected_files, f".gemini/{folder} file list must match {folder}")
        for rel in source_files:
            require(
                read_text(source_dir / rel) == read_text(projected_dir / rel),
                f".gemini/{folder}/{rel.as_posix()} must match {folder}/{rel.as_posix()}",
            )


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
    validate_extension_secret_settings()
    validate_commands()
    validate_skills()
    validate_subagents()
    validate_hooks()
    validate_browser_routing()
    validate_runtime_channel_policy()
    validate_projection_parity()
    validate_native_boundaries()
    validate_antigravity_policy()
    validate_instruction_docs()
    validate_serena_memories()
    validate_retired_residue()


VALIDATORS: dict[str, Callable[[bool], None]] = {
    "all": validate_all,
    "config": lambda strict: (validate_version_surfaces(), validate_settings(), validate_manifest(), validate_mcp_inventory()),
    "manifest": lambda strict: validate_manifest(),
    "secret-settings": lambda strict: validate_extension_secret_settings(),
    "commands": lambda strict: validate_commands(),
    "skills": lambda strict: validate_skills(),
    "subagents": lambda strict: validate_subagents(),
    "hooks": lambda strict: validate_hooks(),
    "mcp": lambda strict: validate_mcp_inventory(),
    "browser": lambda strict: validate_browser_routing(),
    "browser-agent": lambda strict: validate_browser_routing(),
    "runtime": lambda strict: validate_runtime_baseline(strict=strict),
    "runtime-channel": lambda strict: validate_runtime_channel_policy(),
    "projection": lambda strict: validate_projection_parity(),
    "instructions": lambda strict: validate_instruction_docs(),
    "memories": lambda strict: validate_serena_memories(),
    "native": lambda strict: validate_native_boundaries(),
    "antigravity": lambda strict: validate_antigravity_policy(),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate rldyour Gemini adapter surfaces.")
    parser.add_argument("target", choices=sorted(VALIDATORS), nargs="?", default="all")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--strict-native-schema", action="store_true")
    parser.add_argument("--strict-native-json", action="store_true")
    parser.add_argument("--strict-native-tools", action="store_true")
    args = parser.parse_args(argv)
    strict = args.strict or args.strict_native_schema or args.strict_native_json or args.strict_native_tools
    try:
        VALIDATORS[args.target](strict)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"ok: Gemini {args.target} validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
