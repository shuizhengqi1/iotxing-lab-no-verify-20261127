#!/usr/bin/env python3
"""CI gate: re-run the secret scan on the tree. Pytest is a separate job.

A missing Hooks-Ran trailer is reported, not treated as a pass.
A present trailer is not a pass either: it can be written by hand.
The merge decision must follow the scan, which re-reads the files.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    scan = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "secret_scan.py"), "--root", str(ROOT)],
    )
    try:
        body = subprocess.check_output(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%B"], text=True
        )
    except subprocess.CalledProcessError:
        body = ""
    if "Hooks-Ran: pre-commit+commit-msg" in body:
        print("gate: commit message has Hooks-Ran trailer (forgeable, not a pass)")
    else:
        print("gate: commit message has no Hooks-Ran trailer (possible --no-verify)")
    if scan.returncode != 0:
        print("gate: secret-scan FAILED", file=sys.stderr)
        return 1
    print("gate: secret-scan PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
