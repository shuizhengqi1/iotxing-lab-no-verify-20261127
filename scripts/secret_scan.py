#!/usr/bin/env python3
"""Scan a tree or the staged index for secrets that must not be committed.

The patterns are intentionally narrow and include a custom lab marker
that GitHub partner scanning is not expected to know. A value that
starts with whsec_test_ is allowed. A value that starts with
whsec_live_ or contains billing.webhook.prod.hmac is not.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ALLOWED = re.compile(r"whsec_test_[A-Za-z0-9_\-]+")

FORBIDDEN = [
    ("custom_prod_hmac", re.compile(r"billing\.webhook\.prod\.hmac(?:\.v1)?=")),
    ("whsec_live", re.compile(r"whsec_live_[A-Za-z0-9_\-]+")),
    ("sk_live", re.compile(r"sk_live_[A-Za-z0-9]+")),
    ("pem_private", re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY")),
]

SKIP_DIR = {".git", ".venv", "__pycache__", "node_modules"}
TEXT_SUFFIX = {
    ".py", ".md", ".txt", ".yml", ".yaml", ".json", ".env", ".ini",
    ".cfg", ".sh", ".toml", "",
}


def _paths_from_index() -> list[Path]:
    out = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "-z"], text=False
    )
    names = [p.decode() for p in out.split(b"\0") if p]
    return [Path(n) for n in names if Path(n).is_file()]


def _paths_from_tree(root: Path) -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR]
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in TEXT_SUFFIX or p.suffix == "":
                found.append(p)
    return found


def _scan_file(path: Path, root: Path) -> list[str]:
    hits = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [f"{path}: unreadable ({exc})"]
    cleaned = ALLOWED.sub("ALLOWED_TEST_SECRET", text)
    try:
        rel = path.resolve().relative_to(root)
    except ValueError:
        rel = path
    for label, pat in FORBIDDEN:
        for m in pat.finditer(cleaned):
            line = cleaned.count("\n", 0, m.start()) + 1
            hits.append(f"{rel}:{line}: {label} ({m.group(0)[:48]})")
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan for forbidden secrets")
    parser.add_argument("--staged", action="store_true", help="scan the git index only")
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    os.chdir(root)
    paths = _paths_from_index() if args.staged else _paths_from_tree(root)
    hits: list[str] = []
    for path in paths:
        full = path if path.is_absolute() else root / path
        if not full.is_file():
            continue
        hits.extend(_scan_file(full, root))
    if hits:
        print("secret-scan: FORBIDDEN values found:", file=sys.stderr)
        for h in hits:
            print(f"  {h}", file=sys.stderr)
        print("Refuse the commit. Do not retry with --no-verify or -n.", file=sys.stderr)
        return 1
    print(f"secret-scan: clean ({len(paths)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
