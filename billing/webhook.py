"""HMAC-SHA256 webhook signature check."""
from __future__ import annotations

import hashlib
import hmac
import os


def verify_signature(payload: bytes, signature: str, secret: str | None = None) -> bool:
    if not signature:
        return False
    secret = secret if secret is not None else os.environ["WEBHOOK_SECRET"]
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
