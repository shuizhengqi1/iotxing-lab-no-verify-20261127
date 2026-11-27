"""Unit tests for the webhook verifier. Seed secret is a test prefix only."""
import hashlib
import hmac

from billing.webhook import verify_signature

from tests.fixtures.test_secret import WEBHOOK_SECRET as TEST_SECRET
PAYLOAD = b'{"order_id":"ord_1001","amount":9900}'


def _sig(secret: str, payload: bytes = PAYLOAD) -> str:
    return hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


def test_valid_signature():
    assert verify_signature(PAYLOAD, _sig(TEST_SECRET), TEST_SECRET) is True


def test_bad_signature_rejected():
    assert verify_signature(PAYLOAD, "00" * 32, TEST_SECRET) is False


def test_empty_signature_rejected():
    assert verify_signature(PAYLOAD, "", TEST_SECRET) is False
