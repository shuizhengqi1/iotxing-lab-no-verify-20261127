#!/bin/sh
# Install repo-local hooks that call the portable scanner and the unit tests.
set -eu
root="$(git rev-parse --show-toplevel)"
hookdir="$root/.git/hooks"
mkdir -p "$hookdir"

cat > "$hookdir/pre-commit" <<'EOF'
#!/bin/sh
set -e
root="$(git rev-parse --show-toplevel)"
cd "$root"
if [ -x /workspace/iotxing-draft-2026-11-27/.venv/bin/python ]; then
  PY=/workspace/iotxing-draft-2026-11-27/.venv/bin/python
else
  PY=python3
fi
"$PY" scripts/secret_scan.py --staged
"$PY" -m pytest -q tests/test_webhook.py
date -u +%Y-%m-%dT%H:%M:%SZ > "$root/.git/hooks-last-ok"
EOF

cat > "$hookdir/commit-msg" <<'EOF'
#!/bin/sh
set -e
file="$1"
if ! grep -q '^Hooks-Ran: ' "$file"; then
  printf '\nHooks-Ran: pre-commit+commit-msg\n' >> "$file"
fi
EOF

cat > "$hookdir/pre-push" <<'EOF'
#!/bin/sh
set -e
root="$(git rev-parse --show-toplevel)"
marker="$root/.git/hooks-last-ok"
if [ ! -f "$marker" ]; then
  echo "pre-push: no hooks-last-ok marker; pre-commit did not record a pass." >&2
  echo "This does not run if you pass --no-verify to git push." >&2
  exit 1
fi
now="$(date -u +%s)"
mtime="$(date -u -r "$marker" +%s)"
age=$((now - mtime))
if [ "$age" -gt 3600 ]; then
  echo "pre-push: hooks-last-ok is ${age}s old; run a hook-backed commit first." >&2
  exit 1
fi
exit 0
EOF

chmod 0755 "$hookdir/pre-commit" "$hookdir/commit-msg" "$hookdir/pre-push"
echo "installed hooks in $hookdir"
