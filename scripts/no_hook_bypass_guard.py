#!/usr/bin/env python3
"""Command-string guard in the shape of a Claude Code PreToolUse hook.

Exit 2 means blocked. This is not process-level enforcement of Git itself;
it only sees the command text (or the edited path) that a tool hook receives.
A live coding model was not used to evaluate this script.
"""
from __future__ import annotations

import json
import os
import re
import sys

NARROW = [
    re.compile(r"--no-verify"),
]

WIDE = [
    re.compile(r"--no-verify"),
    re.compile(r"\bcommit\b[^|;&]*\s-[a-zA-Z]*n"),
    re.compile(r"\bpush\b[^|;&]*\s-[a-zA-Z]*n\b"),
    re.compile(r"\bHUSKY=0\b"),
    re.compile(r"core\.hooksPath"),
    re.compile(r"--hooksPath"),
    re.compile(r"(\.husky|\.git/hooks)/"),
]


def is_hit(tool: str, inp: dict, patterns: list[re.Pattern]) -> bool:
    if tool in ("Edit", "Write"):
        path = str(inp.get("file_path", "") or inp.get("path", ""))
        return bool(re.search(r"(^|/)(\.husky|\.git/hooks|\.githooks)(/|$)", path))
    cmd = str(inp.get("command", ""))
    return any(p.search(cmd) for p in patterns)


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        print("guard: invalid json on stdin", file=sys.stderr)
        return 2
    mode = os.environ.get("GUARD_MODE", "wide")
    patterns = WIDE if mode != "narrow" else NARROW
    tool = d.get("tool_name", "") or d.get("tool", "")
    inp = d.get("tool_input", {}) or {}
    if is_hit(tool, inp, patterns):
        print(
            "Blocked: this skips or changes the git hooks. "
            "Do not try another way around them. Fix what the hook reported "
            "and commit again, or stop and report the hook's error.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
