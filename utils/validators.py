"""
Input validation for settings values.

Every public function returns a ``(bool, str)`` tuple: the first
element is ``True`` when the value is acceptable, and the second
carries a human-readable reason on failure.
"""

from __future__ import annotations

import config


def validate_notification_frequency(value: int) -> tuple[bool, str]:
    """Frequency must be one of the predefined cadence values."""
    if not isinstance(value, int):
        return False, "notification_frequency must be an integer"
    if value not in config.VALID_FREQUENCIES:
        return False, f"notification_frequency must be one of {config.VALID_FREQUENCIES}"
    return True, ""


def validate_theme(value: str) -> tuple[bool, str]:
    if not isinstance(value, str):
        return False, "theme must be a string"
    if value not in config.VALID_THEMES:
        return False, f"theme must be one of {config.VALID_THEMES}"
    return True, ""


def validate_timezone(value: str) -> tuple[bool, str]:
    if not isinstance(value, str):
        return False, "timezone must be a string"
    if value not in config.VALID_TIMEZONES:
        return False, f"timezone must be one of {config.VALID_TIMEZONES}"
    return True, ""


def validate_bio(value: str) -> tuple[bool, str]:
    if not isinstance(value, str):
        return False, "bio must be a string"
    if len(value) > config.MAX_BIO_LENGTH:
        return False, f"bio must not exceed {config.MAX_BIO_LENGTH} characters"
    return True, ""


# ── Dispatcher ──────────────────────────────────────────────────────

_VALIDATORS = {
    "notification_frequency": validate_notification_frequency,
    "theme": validate_theme,
    "timezone": validate_timezone,
    "bio": validate_bio,
}


def validate_settings(updates: dict) -> tuple[bool, list[str]]:
    """Validate every key in *updates* that has a registered validator.

    Returns ``(True, [])`` when everything passes, or
    ``(False, [error, ...])`` when one or more checks fail.
    """
    errors: list[str] = []
    for key, value in updates.items():
        validator = _VALIDATORS.get(key)
        if validator is not None:
            ok, reason = validator(value)
            if not ok:
                errors.append(reason)
    return (len(errors) == 0), errors
