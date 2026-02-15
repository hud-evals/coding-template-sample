"""
Simple tier-based permission checks.

Premium users may configure every available setting.  Free-tier users
are restricted to a smaller subset.
"""

from __future__ import annotations

from typing import Any

import database

# Settings that free-tier users are allowed to change.
FREE_TIER_ALLOWED = {"theme", "timezone", "bio"}


def can_modify_setting(user_id: str, key: str) -> tuple[bool, str]:
    """Check whether the user is permitted to change *key*.

    Returns ``(True, "")`` on success, or ``(False, reason)`` on denial.
    """
    record = database.get_user(user_id)
    if record is None:
        return False, "user not found"

    tier = record.get("tier", "free")

    if tier == "premium":
        return True, ""

    if key in FREE_TIER_ALLOWED:
        return True, ""

    return False, f"free-tier users cannot modify '{key}'"


def filter_allowed_updates(user_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    """Strip any keys the user isn't allowed to change."""
    return {
        k: v for k, v in updates.items()
        if can_modify_setting(user_id, k)[0]
    }
