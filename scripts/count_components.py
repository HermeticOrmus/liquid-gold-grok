#!/usr/bin/env python3
"""Count the components Grok can load from one plugin folder.

Usage: python3 scripts/count_components.py <plugin dir> [--json]

Reads the manifest the way Grok does (plugin.json at the plugin root, then
.grok-plugin/plugin.json, then .claude-plugin/plugin.json; see manifest.rs in
xai-org/grok-build) and honors its skills, agents,
commands, hooks and mcpServers fields. Without a field, the standard folder is
used (skills/, agents/, commands/, hooks/hooks.json, .mcp.json).

Prints one line: skills=N agents=N commands=N hooks=N mcp=N
hooks counts hook events (SessionStart, PreToolUse, ...); mcp counts servers.
"""
import json
import sys
from pathlib import Path

MANIFESTS = ("plugin.json", ".grok-plugin/plugin.json", ".claude-plugin/plugin.json")


def manifest(root: Path) -> dict:
    for rel in MANIFESTS:
        p = root / rel
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except ValueError:
                return {}
    return {}


def paths(value, default):
    if value is None:
        return [default]
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str)]
    return [default]


def count_skills(root: Path, value) -> int:
    n = 0
    for rel in paths(value, "skills"):
        d = (root / rel).resolve()
        if (d / "SKILL.md").is_file():
            n += 1
        elif d.is_dir():
            n += sum(1 for s in d.iterdir() if (s / "SKILL.md").is_file())
    return n


def count_md(root: Path, value, default: str) -> int:
    n = 0
    for rel in paths(value, default):
        p = (root / rel).resolve()
        if p.is_file() and p.suffix == ".md":
            n += 1
        elif p.is_dir():
            n += sum(1 for f in p.glob("*.md") if f.name.lower() != "readme.md")
    return n


def load_json(root: Path, value, default: str):
    if isinstance(value, dict):
        return value
    for rel in paths(value, default):
        p = root / rel
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except ValueError:
                return {}
    return {}


def count(root: Path) -> dict:
    m = manifest(root)
    hooks = load_json(root, m.get("hooks"), "hooks/hooks.json")
    hooks = hooks.get("hooks", hooks) if isinstance(hooks, dict) else {}
    mcp = load_json(root, m.get("mcpServers"), ".mcp.json")
    mcp = mcp.get("mcpServers", mcp) if isinstance(mcp, dict) else {}
    return {
        "skills": count_skills(root, m.get("skills")),
        "agents": count_md(root, m.get("agents"), "agents"),
        "commands": count_md(root, m.get("commands"), "commands"),
        "hooks": len([k for k, v in hooks.items() if isinstance(v, list)]),
        "mcp": len([k for k, v in mcp.items() if isinstance(v, dict)]),
    }


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    c = count(Path(sys.argv[1]))
    if "--json" in sys.argv[2:]:
        print(json.dumps(c))
    else:
        print(" ".join(f"{k}={v}" for k, v in c.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
