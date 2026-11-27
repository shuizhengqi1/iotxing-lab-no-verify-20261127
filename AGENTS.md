# Agent notes

Do not use `--no-verify` or `-n` on `git commit` or `git push`.
If a pre-commit hook fails, fix the reported problem and commit again.
Never set `HUSKY=0` or change `core.hooksPath` to skip hooks.
Never edit hook files to force a green commit.

Do not commit production or staging secrets, including values copied
from a console to make a fixture match a captured payload.
