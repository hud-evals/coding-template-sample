"""
Settings pipeline — read and write user preferences.

The *effective settings* for a user are computed by overlaying their stored
custom values on top of the application defaults defined in ``config.py``.
See Issue #22 for the original pipeline refactor discussion.
"""

from __future__ import annotations

from typing import Any

import config
import database


def get_effective_settings(user_id: str) -> dict[str, Any] | None:
    """Return the fully-resolved settings for *user_id*.

    Merges the application-wide defaults with whatever the user has
    explicitly customised.  Returns ``None`` when the user doesn't exist.
    """
    custom = database.get_user_settings(user_id)
    if custom is None:
        return None

    # Merge: defaults first, then overlay user's custom settings.
    # Filter out any null/empty entries from the user's stored settings
    # so that defaults apply for unset preferences (Issue #22).
    effective = {
        **config.DEFAULT_SETTINGS,
        **{k: v for k, v in custom.items() if v is not None},
    }
    return effective


def update_user_settings(user_id: str, updates: dict[str, Any]) -> bool:
    """Apply *updates* to the user's stored settings.

    Only keys present in ``updates`` are touched; every other setting
    is left unchanged.  A value of ``None`` removes that key (resets it
    to default on next read).

    Returns ``False`` when the user does not exist.
    """
    current = database.get_user_settings(user_id)
    if current is None:
        return False

    for key, value in updates.items():
        if value is not None:
            current[key] = value
        else:
            current.pop(key, None)

    return database.save_user_settings(user_id, current)


def reset_setting(user_id: str, key: str) -> bool:
    """Remove a single setting so the default applies on next read.

    Returns ``False`` when the user does not exist.
    """
    current = database.get_user_settings(user_id)
    if current is None:
        return False

    current.pop(key, None)
    return database.save_user_settings(user_id, current)
