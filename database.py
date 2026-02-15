"""In-memory data store.

Simple dict-based storage. Suitable for development and testing.
"""

from typing import Optional


_tasks: dict[str, dict] = {}
_notifications: list[dict] = []


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

def save_task(task: dict) -> dict:
    _tasks[task["id"]] = task
    return task


def get_task(task_id: str) -> Optional[dict]:
    return _tasks.get(task_id)  # TODO: should this raise?


def list_tasks() -> list[dict]:
    return list(_tasks.values())


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------

def save_notification(notification: dict) -> dict:
    _notifications.append(notification)
    return notification


def list_notifications() -> list[dict]:
    return list(_notifications)
