"""Input validation for settings updates.

Each setting key has its own validation rule.  Invalid values are
rejected before they reach the database.
"""

import config

_RULES = {
    "notification_frequency": lambda v: v in config.VALID_FREQUENCIES,
    "dark_mode": lambda v: isinstance(v, bool),
    "theme": lambda v: v in config.VALID_THEMES,
    "bio": lambda v: isinstance(v, str) and len(v) <= 200,
    "email_digest": lambda v: isinstance(v, bool),
    "timezone": lambda v: v in config.VALID_TIMEZONES,
}


def validate_settings(updates: dict) -> tuple[dict, list[str]]:
    """Validate *updates* and split into (valid, errors).

    Returns a tuple of the validated dict (only keys that passed) and
    a list of human-readable error strings for those that failed.
    """
    valid: dict = {}
    errors: list[str] = []

    for key, value in updates.items():
        rule = _RULES.get(key)
        if rule is None:
            errors.append(f"Unknown setting: {key}")
            continue
        if not rule(value):
            errors.append(f"Invalid value for {key}: {value!r}")
            continue
        valid[key] = value

    return valid, errors
