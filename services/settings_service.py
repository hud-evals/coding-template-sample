"""Settings read / write service.

Merges per-user custom settings with application defaults so callers
always receive a complete settings dict.
"""

import database
import config


def get_effective_settings(user_id: str) -> dict | None:
    """Return the fully-merged settings for *user_id*.

    Custom values override defaults.  Keys that the user has never
    touched fall back to ``config.DEFAULT_SETTINGS``.  A ``None``
    return means the user does not exist.
    """
    custom = database.get_user_settings(user_id)
    if custom is None:
        return None

    effective = {**config.DEFAULT_SETTINGS}
    for key, value in custom.items():
        if value is not None:
            effective[key] = value

    return effective


def update_settings(user_id: str, updates: dict) -> dict | None:
    """Apply *updates* to the user's settings and return the new state.

    Only keys present in ``config.DEFAULT_SETTINGS`` are accepted.
    Returns ``None`` when the user does not exist.
    """
    if database.get_user(user_id) is None:
        return None

    valid = {k: v for k, v in updates.items() if k in config.DEFAULT_SETTINGS}
    database.update_user_settings(user_id, valid)
    return get_effective_settings(user_id)


def get_single_setting(user_id: str, key: str):
    """Return a single setting value, or ``None`` if user/key missing."""
    settings = get_effective_settings(user_id)
    if settings is None:
        return None
    return settings.get(key)
