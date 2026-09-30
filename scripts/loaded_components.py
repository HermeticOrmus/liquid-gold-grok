#!/usr/bin/env python3
"""Count what Grok actually loaded for one plugin, from `grok inspect --json`.

Usage: python3 scripts/loaded_components.py <inspect.json> <plugin name> <plugin dir>

`grok inspect` lists every skill, agent, hook file and MCP server Grok
discovered, each with the plugin it came from. Commands are listed with the
skills; they are told apart by their path. Hook events are counted from the
plugin's hook file (count_components.py) when Grok loaded a hook file for the
plugin, and are 0 when it did not.

Prints one line in the same shape as count_components.py:
skills=N agents=N commands=N hooks=N mcp=N
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from count_components import count  # noqa: E402


def mine(item: dict, name: str) -> bool:
    src = item.get("source") or {}
    return src.get("type") == "plugin" and src.get("plugin_name") == name


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__.strip())
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    name, plugin_dir = sys.argv[2], Path(sys.argv[3])
    skills = commands = 0
    for s in data.get("skills", []):
        if mine(s, name):
            if "/commands/" in (s.get("source") or {}).get("path", ""):
                commands += 1
            else:
                skills += 1
    agents = sum(1 for a in data.get("agents", []) if mine(a, name))
    mcp = sum(1 for m in data.get("mcpServers", []) if mine(m, name))
    hooks = count(plugin_dir)["hooks"] if any(mine(h, name) for h in data.get("hooks", [])) else 0
    print(f"skills={skills} agents={agents} commands={commands} hooks={hooks} mcp={mcp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
