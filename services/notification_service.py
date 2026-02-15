"""Notification dispatch service.

Listens for domain events and creates user-facing notifications.
Handlers are registered by event type at startup.
"""

from models import Notification
import config
import database

_instance = None


class NotificationService:
    """Fanout notifications based on incoming domain events."""

    def __init__(self):
        self._handlers: dict[str, callable] = {}
        self._register_handlers()

    def _register_handlers(self):
        for action, handler in [
            ("created", self._handle_task_created),
            ("assigned", self._handle_task_assigned),
            ("completed", self._handle_task_completed),
        ]:
            self._handlers[f"task.{action}"] = handler

        # Legacy format kept for backwards compat (pre-refactor callers
        # still emit "task_created" with underscore delimiter).
        self._handlers["task_created"] = self._handle_task_created

    def handle_event(self, event: dict) -> None:
        """Route an event to its registered handler, if any."""
        handler = self._handlers.get(event.get("type"))
        if handler:
            handler(event)

    def _handle_task_created(self, event: dict) -> None:
        task = event["data"]["task"]
        notif = Notification(
            event_type=event["type"],
            recipient_id="system",
            message=f"Task '{task['title']}' was created.",
            created_at=config.get_timestamp(),
        )
        database.save_notification(notif.to_dict())

    def _handle_task_assigned(self, event: dict) -> None:
        task = event["data"]["task"]
        assignee = event["data"]["assignee_id"]
        notif = Notification(
            event_type=event["type"],
            recipient_id=assignee,
            message=f"You have been assigned task '{task['title']}'.",
            created_at=config.get_timestamp(),
        )
        database.save_notification(notif.to_dict())

    def _handle_task_completed(self, event: dict) -> None:
        task = event["data"]["task"]
        recipient = task.get("assignee_id") or "system"
        notif = Notification(
            event_type=event["type"],
            recipient_id=recipient,
            message=f"Task '{task['title']}' has been completed.",
            created_at=config.get_timestamp(),
        )
        database.save_notification(notif.to_dict())


def get_instance() -> NotificationService:
    global _instance
    if _instance is None:
        _instance = NotificationService()
    return _instance
