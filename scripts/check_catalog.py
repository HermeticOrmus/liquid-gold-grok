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
  7. The level counts (gold, assayed, watch), the entry total, and the crack
     and sealed totals written in CATALOG.md and README.md match the cards in
     entries/. Each CATALOG.md cell "N found, M sealed" matches that card's
     ledger. A crack is one ledger row. The row counts as sealed when its
     State starts with sealed or hallmarked. A withdrawn row stays in the
     found total and is not sealed.
Exits 1 and prints each problem when any check fails.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHA = re.compile(r"^[0-9a-f]{40}$")
LEVEL_COUNT = re.compile(r"\b(gold|assayed|watch)\b(?:\*\*)? \((\d+)\)")
ENTRY_TOTAL = re.compile(r"\b(\d+) entries\b")
CRACK_TOTAL = re.compile(r"\b(\d+) cracks\b")
SEALED_TOTAL = re.compile(r"\b(\d+) of them (?:are )?sealed\b")
CRACK_CELL = re.compile(
    r"^\| \[[^\]]+\]\(entries/([^)]+)\.md\).*\|\s*(\d+) found,\s*(\d+) sealed\s*\|",
    re.M,
)
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


def ledger_found_and_sealed(text: str) -> tuple[int, int]:
    """Count cracks on one card.

    Every well-formed ledger row was found, including a withdrawn row: the
    rubric keeps that row and never reuses its ID. A row is sealed when its
    State starts with sealed or hallmarked. Withdrawn closes a row for the
    level check and is not a seal, so it counts as found only.
    """
    section = text.split("## Ledger", 1)
    if len(section) < 2:
        return 0, 0
    body = section[1].split("\n## ", 1)[0]
    found = sealed = 0
    for line in body.splitlines():
        if not re.match(r"^\| K-\d+ ", line):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) != 7:
            continue
        found += 1
        if cells[6].lower().startswith(("sealed", "hallmarked")):
            sealed += 1
    return found, sealed


def require_count(rel: str, text: str, pattern: re.Pattern[str], held: int, label: str) -> None:
    written = sorted({int(n) for n in pattern.findall(text)})
    if not written:
        fail(f"{rel}: {label} is not written; the cards hold {held}")
        return
    for n in written:
        if n != held:
            fail(f"{rel}: {label} is written as {n}; the cards hold {held}")


def check_counts() -> None:
    by_entry: dict[str, tuple[int, int]] = {}
    levels = {"gold": 0, "assayed": 0, "watch": 0}
    for path in sorted((ROOT / "entries").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        level = re.sub(r"[*\s]", "", card_field(text, "Level"))
        if level in levels:
            levels[level] += 1
        by_entry[path.stem] = ledger_found_and_sealed(text)
    cracks = sum(found for found, _ in by_entry.values())
    sealed_total = sum(sealed for _, sealed in by_entry.values())

    for rel in ("CATALOG.md", "README.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        seen: dict[str, set[int]] = {name: set() for name in levels}
        for level, n in LEVEL_COUNT.findall(text):
            seen[level].add(int(n))
        for level, held in levels.items():
            if not seen[level]:
                fail(f"{rel}: {level} count is not written; the cards hold {held}")
            for n in sorted(seen[level]):
                if n != held:
                    fail(f"{rel}: {level} count is written as {n}; the cards hold {held}")
        require_count(rel, text, ENTRY_TOTAL, len(by_entry), "entry total")
        require_count(rel, text, CRACK_TOTAL, cracks, "crack total")
        require_count(rel, text, SEALED_TOTAL, sealed_total, "sealed total")

    cells: dict[str, set[tuple[int, int]]] = {}
    for stem, found_s, sealed_s in CRACK_CELL.findall((ROOT / "CATALOG.md").read_text(encoding="utf-8")):
        cells.setdefault(stem, set()).add((int(found_s), int(sealed_s)))
    for stem, (found, sealed) in sorted(by_entry.items()):
        written = cells.get(stem)
        if not written:
            fail(
                f"CATALOG.md: {stem} has no crack cell; "
                f"the card holds {found} found, {sealed} sealed"
            )
            continue
        for written_found, written_sealed in sorted(written):
            if written_found != found:
                fail(f"CATALOG.md: {stem} found is written as {written_found}; the card holds {found}")
            if written_sealed != sealed:
                fail(f"CATALOG.md: {stem} sealed is written as {written_sealed}; the card holds {sealed}")
    for stem in sorted(set(cells) - set(by_entry)):
        for written_found, written_sealed in sorted(cells[stem]):
            fail(
                f"CATALOG.md: {stem} is written as {written_found} found, {written_sealed} sealed; "
                "entries/ has no such card"
            )


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

    check_counts()

    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} problem(s)")
        return 1
    print(f"ok: {len(listed)} marketplace entries, {len(cards)} cards, all linked from CATALOG.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
