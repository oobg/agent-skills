#!/usr/bin/env python3
"""Collect a mechanical inventory from a frontend implementation (read-only).

Scans files, routes, events, state, API calls, style tokens, side effects,
stub markers and destructive-looking functions, and prints them with
file:line evidence. The output is an *inventory*, not a judgment: every item
must be re-checked against the source or runtime before it becomes a finding.

Contract:
- read-only: the target is never modified; repeated runs have no side effects.
- deterministic: the same input and the same COLLECTOR_VERSION yield the same
  inventory (everything except the `run` object). Diff two inventories with
  `run` removed.
- run metadata (`run`: target path, git commit, generated_at) is kept apart.
- 0 items means "not detected by the current patterns", never "absent".

Usage:
  python3 collect_inventory.py <path> [--json OUT.json] [--md OUT.md]

The target is never modified. Outputs are written only where --json/--md say.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

COLLECTOR_VERSION = "1.1.0"

SCAN_EXT = {".html", ".htm", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".css", ".scss"}
SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".turbo", ".cache", "coverage"}
BUILD_DIRS = {"dist", "build", ".next", "out", ".output", ".svelte-kit"}
MINIFIED_LINE = 2000

PATTERNS = {
    "routes": [
        re.compile(r"""<Route[^>]*\spath=["'{]([^"'}]+)"""),
        re.compile(r"""\bpath\s*:\s*["'`]([^"'`]+)["'`]"""),
        re.compile(r"""\b(?:app|router)\.(?:get|post|put|patch|delete|all)\(\s*["'`]([^"'`]+)["'`]"""),
        re.compile(r"""["'`](#/[^"'`\s]*)["'`]"""),
        re.compile(r"""\bdata-(?:route|view|page|screen)=["']([^"']+)["']"""),
    ],
    "events": [
        re.compile(r"""\.addEventListener\(\s*["'`](\w+)["'`]"""),
        re.compile(r"""\son([a-z]+)=["'{]"""),
        re.compile(r"""\son([A-Z]\w+)=\{"""),
        re.compile(r"""\.on\(\s*["'`](\w+)["'`]"""),
    ],
    "delegation_attrs": [
        re.compile(r"""\bdata-((?:action|act|cmd|command|op|do|handler|click)[\w-]*)=["']([^"']+)["']"""),
        re.compile(r"""\.dataset\.(\w+)"""),
    ],
    "state": [
        re.compile(r"""\b(useState|useReducer|useContext|createStore|configureStore|defineStore|writable|readable|reactive|ref|signal|createSignal|atom|observable|makeAutoObservable)\("""),
        re.compile(r"""^\s*(?:const|let|var)\s+([A-Z][A-Z0-9_]{1,})\s*=\s*[\[{]"""),
        re.compile(r"""^\s*(?:const|let|var)\s+(state|store|db|DB|data|model|appState)\s*="""),
    ],
    "api": [
        re.compile(r"""\b(fetch)\("""),
        re.compile(r"""\b(axios)\.\w+\("""),
        re.compile(r"""\bnew\s+(XMLHttpRequest|WebSocket|EventSource)\("""),
        re.compile(r"""\b(useQuery|useMutation|useSWR|createQuery|trpc)\b"""),
        re.compile(r"""\$\.(ajax|get|post)\("""),
    ],
    "side_effects": [
        re.compile(r"""\b(localStorage|sessionStorage|indexedDB)\b"""),
        re.compile(r"""\b(document\.cookie)"""),
        re.compile(r"""\b(history\.(?:pushState|replaceState|push|replace|back))"""),
        re.compile(r"""\b(location\.(?:href|assign|replace|hash))"""),
        re.compile(r"""\b(window\.open|window\.print)\("""),
        re.compile(r"""\b(URL\.createObjectURL|URL\.revokeObjectURL)\("""),
        re.compile(r"""\s(download)=["']"""),
        re.compile(r"""\b(toast|notify|showToast|alert|confirm|prompt)\("""),
        re.compile(r"""\bnew\s+(Notification)\("""),
        re.compile(r"""\b(setTimeout|setInterval|requestAnimationFrame)\("""),
    ],
    "stub_markers": [
        re.compile(r"""\b(TODO|FIXME|HACK|XXX)\b"""),
        re.compile(r"""\b(stub|mock|placeholder|dummy|fake)\b""", re.I),
        re.compile(r"""(실제로는|임시|가짜|더미|목업|자리 표시자|플레이스홀더)"""),
    ],
    "destructive_defs": [
        re.compile(r"""\bfunction\s+(\w*(?:delete|remove|close|cancel|reset|clear|unlink|detach|drop|purge|wipe|archive|terminate|revoke)\w*)\s*\(""", re.I),
        re.compile(r"""\b(?:const|let|var)\s+(\w*(?:delete|remove|close|cancel|reset|clear|unlink|detach|drop|purge|wipe|archive|terminate|revoke)\w*)\s*=\s*(?:async\s*)?(?:\(|function)""", re.I),
    ],
    "functions": [
        re.compile(r"""\bfunction\s+(\w+)\s*\("""),
        re.compile(r"""\b(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|\w+)\s*=>"""),
    ],
    "css_tokens": [
        re.compile(r"""(--[\w-]+)\s*:\s*([^;}]+)"""),
    ],
    "status_enums": [
        re.compile(r"""\b(status|state|stage|phase|step|type|kind)\s*[:=]\s*["'`]([\w-]+)["'`]"""),
    ],
}

COMMENT_LINE = re.compile(r"""(//|/\*|<!--|\*|#)""")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit(path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(path if path.is_dir() else path.parent), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() or None


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    root_parts = set(root.resolve().parts)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in SKIP_DIRS and (d not in BUILD_DIRS or d in root_parts)
        )
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if p.suffix.lower() in SCAN_EXT:
                yield p


def guess_kind(root: Path, files: list[Path], minified: int) -> str:
    if root.is_file() and root.suffix.lower() in {".html", ".htm"}:
        return "single-html"
    if root.is_dir() and (root / "package.json").exists():
        return "framework-project" if minified == 0 else "framework-project (bundle mixed)"
    if files and minified >= max(1, len(files) // 2):
        return "bundle"
    if not files:
        return "no-scannable-source"
    return "source-files"


def collect(root: Path) -> dict:
    inv: dict = {k: [] for k in PATTERNS}
    inv["files"] = []
    inv["files_skipped"] = []
    tokens_seen: dict[str, dict] = {}
    minified = 0
    for path in iter_files(root):
        rel = str(path.relative_to(root.parent if root.is_file() else root))
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            inv["files_skipped"].append({"file": rel, "reason": f"read error: {exc}"})
            continue
        lines = text.split("\n")
        is_min = any(len(l) > MINIFIED_LINE for l in lines) and len(lines) < 200
        if is_min:
            minified += 1
        inv["files"].append({"file": rel, "lines": len(lines), "bytes": len(text.encode("utf-8")), "minified": is_min})
        for ln, line in enumerate(lines, 1):
            snippet = line.strip()[:160]
            for key, pats in PATTERNS.items():
                for pat in pats:
                    for m in pat.finditer(line):
                        if key == "stub_markers" and not COMMENT_LINE.search(line):
                            continue
                        if key == "css_tokens":
                            name, value = m.group(1), m.group(2).strip()
                            t = tokens_seen.setdefault(name, {"token": name, "first_value": value, "defs": 0, "evidence": f"{rel}:{ln}"})
                            t["defs"] += 1
                            continue
                        groups = [g for g in m.groups() if g]
                        inv[key].append({"match": " ".join(groups)[:120], "evidence": f"{rel}:{ln}", "line": snippet if not is_min else "(minified)"})
    inv["css_tokens"] = sorted(tokens_seen.values(), key=lambda t: t["token"])
    # `meta` is a function of the input only: same target + same collector version → same inventory.
    inv["meta"] = {
        "target": root.name,
        "kind_guess": guess_kind(root, [Path(f["file"]) for f in inv["files"]], minified),
        "sha256": sha256(root) if root.is_file() else None,
        "files_scanned": len(inv["files"]),
        "files_skipped": len(inv["files_skipped"]),
        "minified_files": minified,
        "skip_rules": sorted(SKIP_DIRS | BUILD_DIRS),
        "collector_version": COLLECTOR_VERSION,
        "note": "inventory only — every item must be re-checked against source or runtime before it becomes a finding",
        "zero_means": "0 items = not detected by this collector's current patterns, not absence of the capability",
    }
    # `run` is execution metadata. It is excluded when diffing two inventories.
    inv["run"] = {
        "target_path": str(root),
        "base_commit": git_commit(root),
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    return inv


def summarize(inv: dict) -> str:
    m, r = inv["meta"], inv["run"]
    out = [f"# Inventory — {r['target_path']}", ""]
    out.append(f"- kind_guess: {m['kind_guess']} · collector: {m['collector_version']}")
    out.append(f"- sha256: {m['sha256'] or 'n/a'}")
    out.append(f"- files_scanned: {m['files_scanned']} · skipped: {m['files_skipped']} · minified: {m['minified_files']}")
    out.append(f"- skip_rules: {', '.join(m['skip_rules'])}")
    out.append(f"- run: base_commit {r['base_commit'] or 'n/a'} · generated_at {r['generated_at']} (run metadata, excluded from diff)")
    out.append(f"- note: {m['zero_means']}")
    out.append("")
    out.append("## Files")
    for f in inv["files"][:200]:
        out.append(f"- {f['file']} ({f['lines']} lines{', minified' if f['minified'] else ''})")
    if len(inv["files"]) > 200:
        out.append(f"- … {len(inv['files']) - 200} more")
    for key, title in [
        ("routes", "Routes"), ("events", "Events"), ("delegation_attrs", "Delegation attributes"),
        ("state", "State"), ("api", "API / network"), ("side_effects", "Side effects"),
        ("stub_markers", "Stub markers"), ("destructive_defs", "Destructive-looking functions"),
        ("status_enums", "Status-like literals"),
    ]:
        items = inv[key]
        out.append("")
        out.append(f"## {title} ({len(items)})")
        counts = Counter(i["match"] for i in items)
        for match, n in counts.most_common(60):
            first = next(i["evidence"] for i in items if i["match"] == match)
            out.append(f"- {match} ×{n} — first at {first}")
    out.append("")
    out.append(f"## Functions ({len(inv['functions'])})")
    by_file = defaultdict(int)
    for f in inv["functions"]:
        by_file[f["evidence"].split(":")[0]] += 1
    for file, n in sorted(by_file.items(), key=lambda kv: -kv[1])[:40]:
        out.append(f"- {file}: {n}")
    out.append("")
    out.append(f"## CSS tokens ({len(inv['css_tokens'])})")
    for t in inv["css_tokens"][:150]:
        dup = f" (defined ×{t['defs']})" if t["defs"] > 1 else ""
        out.append(f"- {t['token']}: {t['first_value']}{dup} — {t['evidence']}")
    out.append("")
    out.append("_inventory only — re-check every item against source or runtime before it becomes a finding._")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="file or directory; URLs are not fetched (use the runtime path instead)")
    ap.add_argument("--json", type=Path, help="write full inventory JSON here")
    ap.add_argument("--md", type=Path, help="write markdown summary here (default: stdout)")
    args = ap.parse_args(argv)
    if args.target.startswith(("http://", "https://")):
        print("deployed service: this script does not fetch URLs. Record the URL and analysis time, then use the runtime path (browser DOM/network capture). Source-level items stay UNKNOWN without source maps.", file=sys.stderr)
        return 2
    root = Path(args.target).expanduser().resolve()
    if not root.exists():
        print(f"not found: {root}", file=sys.stderr)
        return 2
    inv = collect(root)
    if args.json:
        args.json.write_text(json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")
    md = summarize(inv)
    if args.md:
        args.md.write_text(md, encoding="utf-8")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
