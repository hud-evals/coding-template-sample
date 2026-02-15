"""
User CRUD operations.

Profile changes that include settings are forwarded to the settings
service so the write path stays consistent.
"""

from __future__ import annotations

from typing import Any

import database
from services import settings_service


def get_user_profile(user_id: str) -> dict[str, Any] | None:
    """Return the public profile for a user (settings excluded)."""
    record = database.get_user(user_id)
    if record is None:
        return None
    return {
        "id": record["id"],
        "name": record["name"],
        "email": record["email"],
        "tier": record["tier"],
    }


def list_all_users() -> list[dict[str, Any]]:
    """Return a summary list of every registered user."""
    return database.list_users()


def update_profile(user_id: str, changes: dict[str, Any]) -> bool:
    """Update a user's profile and/or settings.

    Keys ``name``, ``email``, and ``tier`` are written directly to the
    user record.  If a ``settings`` sub-dict is present it is delegated
    to the settings service.

    Returns ``False`` when the user does not exist.
    """
    record = database.get_user(user_id)
    if record is None:
        return False

    for field in ("name", "email", "tier"):
        if field in changes:
            record[field] = changes[field]

    database.save_user(user_id, record)

    if "settings" in changes and isinstance(changes["settings"], dict):
        settings_service.update_user_settings(user_id, changes["settings"])

    return True
