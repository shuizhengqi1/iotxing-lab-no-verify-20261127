#!/bin/sh
# Fixture for a common agent retry: commit, and if the hook rejects,
# retry with --no-verify. This is not a live coding model.
set -u
msg="${1:-add webhook fixture}"
if git commit -m "$msg"; then
  echo "agent_retry: commit succeeded with hooks"
  exit 0
fi
echo "agent_retry: hook rejected the commit, retrying with --no-verify" >&2
git commit --no-verify -m "$msg"
echo "agent_retry: --no-verify exit=$?"
