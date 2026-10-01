#!/usr/bin/env python3
"""Mine public sources for Grok Build plugins this library has not assayed yet.

Usage: python3 scripts/mine.py [--out pantry/YYYY-MM-DD-candidate-mine.md] [--top N]

Sources, all public:
  1. xai-org/plugin-marketplace: every plugin in xAI's official catalog.
  2. GitHub code search: repositories that ship `.grok-plugin/plugin.json` or
     `.grok-plugin/marketplace.json`.
  3. DominikTobureto/awesome-grok-build: every GitHub repository its README links.

Each candidate repository is read once through the GitHub API (stars, last
push, license, archived), and repositories that already have a card in
entries/ or a line in .grok-plugin/marketplace.json are left out. The result
is a dated pantry file: a ranked table and a log of what was searched and what
failed. Nothing is installed and nothing is assayed; the table is where the
next assays come from.

Needs a GitHub token in GH_TOKEN or GITHUB_TOKEN (code search requires one).
Without a token, or when code search refuses the token, the run continues with
the other sources and the log says so.

Ranking: entries in xAI's catalog first (Grok users already see them, so their
cracks matter most), then the rest by stars. Stars describe the vessel; they
never admit it.
"""
import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"
REPO = re.compile(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
log: list[str] = []


def request(url: str, body: dict | None = None) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "liquid-gold-grok-mine"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def raw(owner_repo: str, path: str) -> str:
    meta = request(f"{API}/repos/{owner_repo}/contents/{path}")
    return base64.b64decode(meta["content"]).decode("utf-8", "replace")


def norm(owner: str, repo: str) -> str:
    return f"{owner}/{repo.removesuffix('.git')}".lower()


def already_carded() -> set[str]:
    seen = set()
    for card in (ROOT / "entries").glob("*.md"):
        m = re.search(r"^\| Source \| \[[^\]]+\]\((https://github\.com/[^)]+)\)", card.read_text(encoding="utf-8"), re.M)
        if m and (r := REPO.search(m.group(1))):
            seen.add(norm(*r.groups()))
    market = json.loads((ROOT / ".grok-plugin/marketplace.json").read_text(encoding="utf-8"))
    for p in market["plugins"]:
        if (r := REPO.search(p["source"].get("url", ""))):
            seen.add(norm(*r.groups()))
    return seen


def from_xai(cands: dict) -> None:
    try:
        market = json.loads(raw("xai-org/plugin-marketplace", ".grok-plugin/marketplace.json"))
    except (urllib.error.URLError, KeyError, ValueError) as e:
        log.append(f"xai-org/plugin-marketplace: not read ({e})")
        return
    n = 0
    for p in market.get("plugins", []):
        src = p.get("source", {})
        url = src.get("url", "") if isinstance(src, dict) else ""
        if (r := REPO.search(url)):
            key = norm(*r.groups())
            c = cands.setdefault(key, {"sources": set(), "paths": set(), "names": set()})
            c["sources"].add("xai")
            c["names"].add(p.get("name", ""))
            if src.get("path"):
                c["paths"].add(src["path"])
            n += 1
    log.append(f"xai-org/plugin-marketplace: {len(market.get('plugins', []))} plugins, {n} on GitHub")


def from_code_search(cands: dict) -> None:
    if not TOKEN:
        log.append("code search: skipped, no token")
        return
    for fname in ("plugin.json", "marketplace.json"):
        q = f"path:.grok-plugin filename:{fname}"
        total, got = 0, 0
        for page in range(1, 11):
            url = f"{API}/search/code?q={urllib.parse.quote(q)}&per_page=100&page={page}"
            try:
                res = request(url)
            except urllib.error.HTTPError as e:
                log.append(f"code search `{q}` page {page}: HTTP {e.code}, stopped")
                break
            total = res.get("total_count", 0)
            for item in res.get("items", []):
                key = norm(*item["repository"]["full_name"].split("/"))
                c = cands.setdefault(key, {"sources": set(), "paths": set(), "names": set()})
                c["sources"].add("search")
                c["paths"].add(str(Path(item["path"]).parent.parent))
                got += 1
            if len(res.get("items", [])) < 100:
                break
            time.sleep(7)  # code search allows 10 requests a minute
        log.append(f"code search `{q}`: {total} files reported, {got} read")


def from_awesome(cands: dict) -> None:
    try:
        text = raw("DominikTobureto/awesome-grok-build", "README.md")
    except (urllib.error.URLError, KeyError) as e:
        log.append(f"DominikTobureto/awesome-grok-build: not read ({e})")
        return
    keys = {norm(*m.groups()) for m in REPO.finditer(text)} - {"dominiktobureto/awesome-grok-build"}
    for key in keys:
        cands.setdefault(key, {"sources": set(), "paths": set(), "names": set()})["sources"].add("awesome")
    log.append(f"DominikTobureto/awesome-grok-build: {len(keys)} repositories linked")


def enrich(cands: dict) -> None:
    keys = sorted(cands)
    for i in range(0, len(keys), 50):
        chunk = keys[i:i + 50]
        parts = []
        for j, key in enumerate(chunk):
            owner, name = key.split("/", 1)
            parts.append(f'r{j}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) '
                         '{ nameWithOwner stargazerCount pushedAt isArchived isFork '
                         'licenseInfo { spdxId } description }')
        try:
            res = request(f"{API}/graphql", {"query": "{" + " ".join(parts) + "}"})
        except urllib.error.HTTPError as e:
            log.append(f"graphql batch {i // 50 + 1}: HTTP {e.code}")
            continue
        for j, key in enumerate(chunk):
            repo = (res.get("data") or {}).get(f"r{j}")
            if repo:
                cands[key]["repo"] = repo
    missing = [k for k in keys if "repo" not in cands[k]]
    if missing:
        log.append(f"not readable through the API (moved, private or deleted): {len(missing)}")


def cell(s: str) -> str:
    return (s or "").replace("|", "/").replace("\n", " ").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    today = dt.date.today().isoformat()
    ap.add_argument("--out", default=f"pantry/{today}-candidate-mine.md")
    ap.add_argument("--top", type=int, default=40)
    args = ap.parse_args()

    cands: dict = {}
    from_xai(cands)
    from_code_search(cands)
    from_awesome(cands)
    seen = already_carded()
    for key in list(cands):
        if key in seen or (key.startswith("hermeticormus/") and "xai" not in cands[key]["sources"]):
            del cands[key]  # our own packs are assayed from their own ledgers
    enrich(cands)

    rows = []
    for key, c in cands.items():
        r = c.get("repo")
        if not r or r["isArchived"] or r["isFork"]:
            continue
        rows.append((0 if "xai" in c["sources"] else 1, -r["stargazerCount"], key, c, r))
    rows.sort()
    archived = sum(1 for c in cands.values() if c.get("repo", {}).get("isArchived"))

    out = [f"# Candidate mine: liquid-gold-grok", "",
           f"Read on {today} by `scripts/mine.py`. Every row is a public GitHub repository that ships a Grok Build plugin "
           "or is listed by a source below, with no card in `entries/` yet. Stars, last push and license are as the "
           "GitHub API returned them on that day. A row is a lead for an assay, not a recommendation.", "",
           "## Candidates", "",
           "| # | Repository | Sources | Stars | Last push | License | Plugin paths | Description |",
           "|---|------------|---------|-------|-----------|---------|--------------|-------------|"]
    for n, (_, _, key, c, r) in enumerate(rows[:args.top], 1):
        lic = (r.get("licenseInfo") or {}).get("spdxId") or "none found"
        paths = ", ".join(sorted(p for p in c["paths"] if p))[:60]
        out.append(f"| {n} | [{r['nameWithOwner']}](https://github.com/{r['nameWithOwner']}) | "
                   f"{', '.join(sorted(c['sources']))} | {r['stargazerCount']} | {r['pushedAt'][:10]} | {lic} | "
                   f"{cell(paths)} | {cell(r.get('description') or '')[:120]} |")
    out += ["", f"{len(rows)} candidates in all; the table shows the top {min(args.top, len(rows))}. "
            f"Left out: {len(seen)} repositories already carded, {archived} archived, forks.", "",
            "Sources: `xai` is xAI's official catalog, `search` is GitHub code search for `.grok-plugin` manifests, "
            "`awesome` is DominikTobureto/awesome-grok-build.", "",
            "## Search log", ""] + [f"- {line}" for line in log]
    path = ROOT / args.out
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"mine: {len(rows)} candidates, wrote {path.relative_to(ROOT)}")
    for line in log:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
