"""Tier-based permission checks.

Certain settings or features are restricted to premium users.
"""

_PREMIUM_SETTINGS = {"theme", "bio"}


def can_modify(user_tier: str, setting_key: str) -> bool:
    """Return ``True`` if a user on *user_tier* may change *setting_key*.

    Free-tier users cannot change premium-only settings (theme, bio).
    Premium users can change everything.
    """
    if user_tier == "premium":
        return True
    if setting_key in _PREMIUM_SETTINGS:
        return False
    return True


def get_restricted_keys(user_tier: str) -> list[str]:
    """Return settings keys that *user_tier* is NOT allowed to modify."""
    if user_tier == "premium":
        return []
    return sorted(_PREMIUM_SETTINGS)
