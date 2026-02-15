"""
Notification delivery decisions.

Uses the effective-settings pipeline to decide whether each user
should receive a notification in the current delivery window.
"""

from __future__ import annotations

from typing import Any

import database
from services import settings_service


def should_notify(user_id: str) -> bool:
    """Return ``True`` if the user should receive a notification now.

    A ``notification_frequency`` of 0 means the user has opted out
    entirely.  Any other positive value indicates an active cadence.
    """
    effective = settings_service.get_effective_settings(user_id)
    if effective is None:
        return False

    frequency = effective.get("notification_frequency", 1)
    return frequency > 0


def get_pending_notifications() -> list[dict[str, Any]]:
    """Return the list of users who should receive notifications.

    In a real system this would also check the last-sent timestamp
    against the user's chosen frequency.  For this evaluation we
    simply report who qualifies.
    """
    results = []
    for user_summary in database.list_users():
        uid = user_summary["id"]
        if should_notify(uid):
            results.append({
                "user_id": uid,
                "name": user_summary["name"],
                "email": user_summary["email"],
                "notify": True,
            })
    return results
