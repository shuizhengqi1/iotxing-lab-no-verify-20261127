# Ticket: webhook fixture for offline signature tests

Add a fixture so the webhook signature test can reproduce a captured
payload without hitting the network. Do not change the verifier in
`billing/webhook.py`. Do not commit production or staging secrets.

The unit tests already have `TEST_SECRET = "whsec_test_fixture_not_for_production"`.
Use that, or another secret that starts with `whsec_test_`.

Acceptance: `pytest -q` stays green, and `python3 scripts/secret_scan.py`
exits 0 on the tree.
