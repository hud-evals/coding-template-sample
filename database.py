"""In-memory data store with pre-seeded users.

This module acts as the persistence layer.  In production this would
be backed by PostgreSQL; here we keep everything in dicts for
simplicity and deterministic tests.
"""

import copy

from utils.types import CompactDict

_users = {
    "user-alice": {
        "id": "user-alice",
        "name": "Alice Chen",
        "email": "alice@example.com",
        "tier": "premium",
        "settings": {
            "notification_frequency": 0,   # NEVER — valid explicit choice
            "dark_mode": False,            # Explicitly disabled
            "theme": "ocean",
            "timezone": "America/New_York",
        },
    },
    "user-bob": {
        "id": "user-bob",
        "name": "Bob Martinez",
        "email": "bob@example.com",
        "tier": "free",
        "settings": {},
    },
    "user-charlie": {
        "id": "user-charlie",
        "name": "Charlie Kim",
        "email": "charlie@example.com",
        "tier": "premium",
        "settings": {
            "theme": "midnight",
            "bio": "",                     # Intentionally cleared by user
            "email_digest": True,
        },
    },
}

_sessions: dict[str, str] = {
    "tsk_alice_session": "user-alice",
    "tsk_bob_session": "user-bob",
    "tsk_charlie_session": "user-charlie",
}


def get_user(user_id: str) -> dict | None:
    user = _users.get(user_id)
    return copy.deepcopy(user) if user else None


def get_user_settings(user_id: str) -> CompactDict | None:
    """Return the user's custom settings as a CompactDict, or None."""
    user = _users.get(user_id)
    if user is None:
        return None
    return CompactDict(copy.deepcopy(user["settings"]))


def update_user_settings(user_id: str, updates: dict) -> bool:
    user = _users.get(user_id)
    if user is None:
        return False
    user["settings"].update(updates)
    return True


def get_all_users() -> list[dict]:
    return [copy.deepcopy(u) for u in _users.values()]


def resolve_session(token: str) -> str | None:
    return _sessions.get(token)
