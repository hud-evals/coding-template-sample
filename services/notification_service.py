"""Notification decision logic.

Determines whether a user should receive notifications based on
their effective settings.
"""

from services import settings_service


def should_notify(user_id: str) -> bool:
    """Return ``True`` if *user_id* should receive notifications.

    A ``notification_frequency`` of ``0`` means the user has opted out
    entirely.  Any positive value means notifications are enabled
    (the actual cadence is handled by the scheduler).
    """
    settings = settings_service.get_effective_settings(user_id)
    if settings is None:
        return False

    freq = settings.get("notification_frequency", 1)
    return freq > 0


def get_notification_summary(user_id: str) -> dict | None:
    """Build a summary of a user's notification preferences."""
    settings = settings_service.get_effective_settings(user_id)
    if settings is None:
        return None

    freq = settings.get("notification_frequency", 1)
    digest = settings.get("email_digest", True)

    freq_label = {0: "never", 1: "daily", 7: "weekly", 30: "monthly"}.get(
        freq, f"every {freq} days"
    )

    return {
        "user_id": user_id,
        "notifications_enabled": freq > 0,
        "frequency_label": freq_label,
        "email_digest": digest,
    }
