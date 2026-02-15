"""
In-memory data store with pre-seeded user accounts.

In production this would be backed by PostgreSQL; for the evaluation
harness we keep everything in dictionaries so the container stays
lightweight and deterministic.
"""

from __future__ import annotations

import copy
from typing import Any

# ── Pre-seeded user data ────────────────────────────────────────────
_users: dict[str, dict[str, Any]] = {
    "user-alice": {
        "id": "user-alice",
        "name": "Alice Chen",
        "email": "alice@example.com",
        "tier": "premium",
        "settings": {
            "notification_frequency": 0,    # Alice opted OUT of notifications
            "dark_mode": False,             # Alice explicitly disabled dark mode
            "theme": "ocean",
            "timezone": "America/New_York",
        },
    },
    "user-bob": {
        "id": "user-bob",
        "name": "Bob Martinez",
        "email": "bob@example.com",
        "tier": "free",
        "settings": {},                     # Bob uses all defaults
    },
    "user-charlie": {
        "id": "user-charlie",
        "name": "Charlie Kim",
        "email": "charlie@example.com",
        "tier": "premium",
        "settings": {
            "theme": "midnight",
            "bio": "",                      # Charlie intentionally cleared their bio
            "email_digest": True,
        },
    },
}


# ── Public helpers ──────────────────────────────────────────────────

def get_user(user_id: str) -> dict[str, Any] | None:
    """Return a deep copy of the user record, or None if not found."""
    record = _users.get(user_id)
    if record is None:
        return None
    return copy.deepcopy(record)


def save_user(user_id: str, data: dict[str, Any]) -> None:
    """Persist the full user record."""
    _users[user_id] = copy.deepcopy(data)


def list_users() -> list[dict[str, Any]]:
    """Return shallow summaries of every user (no settings included)."""
    return [
        {"id": u["id"], "name": u["name"], "email": u["email"], "tier": u["tier"]}
        for u in _users.values()
    ]


def get_user_settings(user_id: str) -> dict[str, Any] | None:
    """Return the raw stored settings dict for a user, or None."""
    record = _users.get(user_id)
    if record is None:
        return None
    return copy.deepcopy(record.get("settings", {}))


def save_user_settings(user_id: str, settings: dict[str, Any]) -> bool:
    """Write the settings dict back to the user record.

    Returns False if the user does not exist.
    """
    record = _users.get(user_id)
    if record is None:
        return False
    record["settings"] = copy.deepcopy(settings)
    return True
