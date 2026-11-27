# no-verify-secret-kit

Companion kit for the iotxing essay on pre-commit hooks, `git commit --no-verify`,
and a required CI scan that actually re-runs the hook script.

This is lab material. The secret strings in the fixtures are fake and
were generated for this lab. They are not credentials for any real system.

## Layout

- `billing/webhook.py` — HMAC-SHA256 webhook verifier
- `tests/test_webhook.py` — three unit tests that use a `whsec_test_` secret
- `scripts/secret_scan.py` — portable scan used by the hook and by CI
- `scripts/install-hooks.sh` — installs `pre-commit` and `commit-msg`
- `scripts/no_hook_bypass_guard.py` — example PreToolUse-style command guard
- `scripts/agent_retry.sh` — fixture that retries a rejected commit with `--no-verify`
- `examples/` — the bad fixture, a good fixture, and a weakened scanner

## What this kit does not claim

It does not run a live coding model. The agent retry is a shell fixture.
It does not include a Windows run.
# Lab note: fixture secrets must use the whsec_test_ prefix.
