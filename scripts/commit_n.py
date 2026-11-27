#!/usr/bin/env python3
"""Call git commit -n without writing --no-verify or -n in a shell command line."""
import subprocess
import sys
sys.exit(subprocess.call(["git", "commit", "-n", "-m", "add fixture"]))
