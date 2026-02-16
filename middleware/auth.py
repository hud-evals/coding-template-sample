"""Webhook signature verification and API key validation."""

import hashlib
import hmac
import time


_API_KEYS = {
    "wh_live_k1a2b3c4d5e6f7": {"owner": "service-a", "plan": "business"},
    "wh_live_x9y8z7w6v5u4t3": {"owner": "service-b", "plan": "enterprise"},
    "wh_test_0000000000000": {"owner": "test-harness", "plan": "enterprise"},
}

_SIGNING_SECRET = "whsec_default_dev_secret"


def verify_signature(payload_bytes, signature, timestamp=None):
    """Validate an HMAC-SHA256 webhook signature.

    Parameters
    ----------
    payload_bytes : bytes
    signature : str
    timestamp : str or None

    Returns
    -------
    bool
    """
    if not signature:
        return False

    ts = timestamp or str(int(time.time()))
    signed_payload = f"{ts}.{payload_bytes.decode('utf-8', errors='replace')}"
    expected = hmac.new(
        _SIGNING_SECRET.encode(),
        signed_payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected}", signature)


def validate_api_key(key):
    """Look up an API key and return owner metadata.

    Parameters
    ----------
    key : str

    Returns
    -------
    dict or None
    """
    return _API_KEYS.get(key)


def get_plan_for_key(key):
    """Return the plan tier associated with *key*.

    Parameters
    ----------
    key : str

    Returns
    -------
    str
    """
    meta = _API_KEYS.get(key)
    if meta is None:
        return "free"
    return meta.get("plan", "free")
