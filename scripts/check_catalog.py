#!/usr/bin/env python3
"""Check that the marketplace file, the entry cards and the catalog agree.

Usage: python3 scripts/check_catalog.py

Checks:
  1. Every JSON file in the repository parses, and every YAML file under
     .github/ parses (when PyYAML is installed).
  2. .grok-plugin/marketplace.json lists remote entries only, each pinned to a
     full 40-character SHA.
  3. Every card in entries/ is linked from CATALOG.md, and every link in
     CATALOG.md points at a card that exists.
  4. Every marketplace entry has a card whose level is gold or assayed and whose
     pinned SHA matches the marketplace file; no watch card is in the marketplace.
  5. Every relative link in a card (seals, rubric) points at a file that exists.
  6. Every ledger row has seven cells and a grade, and the card's level obeys
     RUBRIC.md: a gold card has no open fracture or break, an assayed card has
     no open break. A row is closed when its State starts with sealed,
     hallmarked or withdrawn.
Exits 1 and prints each problem when any check fails.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHA = re.compile(r"^[0-9a-f]{40}$")
problems = []


def fail(msg: str) -> None:
    problems.append(msg)


def check_parse() -> None:
    for p in sorted(ROOT.rglob("*.json")):
        if ".git" in p.parts:
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            fail(f"{p.relative_to(ROOT)}: invalid JSON: {e}")
    try:
        import yaml  # type: ignore
    except ImportError:
        print("note: PyYAML not installed; YAML files not parsed")
        return
    for p in sorted((ROOT / ".github").rglob("*.y*ml")):
        try:
            yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            fail(f"{p.relative_to(ROOT)}: invalid YAML: {e}")


def card_field(text: str, field: str) -> str:
    m = re.search(rf"^\| {re.escape(field)} \| (.+?) \|$", text, re.M)
    return m.group(1) if m else ""


def check_ledger(rel: str, text: str, level: str) -> None:
    section = text.split("## Ledger", 1)
    if len(section) < 2:
        fail(f"{rel}: no Ledger section")
        return
    body = section[1].split("\n## ", 1)[0]
    for line in body.splitlines():
        if not re.match(r"^\| K-\d+ ", line):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) != 7:
            fail(f"{rel}: ledger row {cells[0]} has {len(cells)} cells, expected 7 (escape a | inside a cell as \\|)")
            continue
        crack_id, grade, state = cells[0], cells[3].lower().split()[0] if cells[3] else "", cells[6].lower()
        if grade not in ("hairline", "fracture", "break"):
            fail(f"{rel}: {crack_id} grade must be hairline, fracture or break")
            continue
        closed = state.startswith(("sealed", "hallmarked", "withdrawn"))
        if closed:
            continue
        if level == "gold" and grade in ("fracture", "break"):
            fail(f"{rel}: gold, but {crack_id} is an open {grade}")
        if level == "assayed" and grade == "break":
            fail(f"{rel}: assayed, but {crack_id} is an open break")


def main() -> int:
    check_parse()
    mk_path = ROOT / ".grok-plugin" / "marketplace.json"
    mk = json.loads(mk_path.read_text(encoding="utf-8"))
    if mk.get("name") != "liquid-gold-grok":
        fail("marketplace name must be liquid-gold-grok")
    listed = {}
    for p in mk.get("plugins", []):
        name, src = p.get("name"), p.get("source", {})
        if not name or not isinstance(src, dict):
            fail(f"marketplace entry without a name or a source object: {p}")
            continue
        if name in listed:
            fail(f"{name}: listed twice in the marketplace")
        listed[name] = src
        if src.get("source") != "url" or not str(src.get("url", "")).startswith("https://github.com/"):
            fail(f"{name}: source must be {{source: url, url: https://github.com/...}}")
        if not SHA.match(str(src.get("sha", ""))):
            fail(f"{name}: sha must be a full 40-character commit SHA")
        if "path" in src and (not src["path"] or src["path"].startswith(("./", "/"))):
            fail(f"{name}: path must be a relative subfolder like plugins/<name>, or absent for a repo-root plugin")
        if "subdir" in src:
            fail(f"{name}: use path, not subdir (Grok ignores subdir)")

    catalog = (ROOT / "CATALOG.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\]\((entries/[^)#]+\.md)\)", catalog))
    cards = {f"entries/{p.name}" for p in (ROOT / "entries").glob("*.md")}
    for c in sorted(cards - linked):
        fail(f"{c}: not linked from CATALOG.md")
    for c in sorted(linked - cards):
        fail(f"CATALOG.md links {c}, which does not exist")

    for rel in sorted(cards):
        path = ROOT / rel
        name = path.stem
        text = path.read_text(encoding="utf-8")
        level = re.sub(r"[*\s]", "", card_field(text, "Level"))
        pinned = re.search(r"`([0-9a-f]{40})`", card_field(text, "Pinned SHA"))
        if level not in ("gold", "assayed", "watch"):
            fail(f"{rel}: Level must be gold, assayed or watch (found '{level}')")
        if not pinned:
            fail(f"{rel}: Pinned SHA row must hold a full 40-character SHA in backticks")
        check_ledger(rel, text, level)
        if name in listed:
            if level == "watch":
                fail(f"{rel}: a watch entry must not be in the marketplace")
            if pinned and pinned.group(1) != listed[name].get("sha"):
                fail(f"{rel}: pinned SHA differs from the marketplace file")
        elif level in ("gold", "assayed"):
            fail(f"{rel}: level {level} but not in .grok-plugin/marketplace.json")
        for target in re.findall(r"\]\((\.\./[^)#\s]+)\)", text):
            if not (path.parent / target).resolve().exists():
                fail(f"{rel}: link to {target}, which does not exist")
    for name in listed:
        if f"entries/{name}.md" not in cards:
            fail(f"{name}: in the marketplace without a card at entries/{name}.md")

    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} problem(s)")
        return 1
    print(f"ok: {len(listed)} marketplace entries, {len(cards)} cards, all linked from CATALOG.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
