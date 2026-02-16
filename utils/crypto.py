"""Token and hashing helpers.

Lightweight wrappers around hashlib for session tokens and
settings fingerprints.
"""

import hashlib
import time

import config


def generate_token(user_id: str) -> str:
    """Create a new session token for *user_id*."""
    raw = f"{user_id}:{time.time()}".encode()
    digest = hashlib.sha256(raw).hexdigest()[:24]
    return f"{config.TOKEN_PREFIX}{digest}"


def settings_fingerprint(settings: dict) -> str:
    """Return a short hash representing the settings state.

    Used for ETag headers and cache invalidation checks.
    """
    ordered = sorted(settings.items())
    raw = str(ordered).encode()
    return hashlib.md5(raw).hexdigest()[:12]


def verify_token_format(token: str) -> bool:
    """Return ``True`` if *token* looks like a valid session token."""
    if not token.startswith(config.TOKEN_PREFIX):
        return False
    remainder = token[len(config.TOKEN_PREFIX):]
    if len(remainder) < 8:
        return False
    return all(c in "0123456789abcdef" for c in remainder)
