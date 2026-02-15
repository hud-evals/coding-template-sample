"""Tests for the notification system.

Verifies that task assignment triggers the correct notification and that
existing notification types (task creation) continue to work.
"""

import sys
import os
import json
import threading
import time
import urllib.request
import urllib.error

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

import database
from services import task_service, notification_service


class TestNotificationDirect:
    """Test notification dispatch without HTTP (direct service calls)."""

    def setup_method(self):
        """Reset state between tests."""
        database._tasks.clear()
        database._notifications.clear()
        notification_service._instance = None

    def test_create_task_sends_notification(self):
        """Task creation should produce a notification."""
        task = task_service.create_task("Write docs")
        notifs = database.list_notifications()
        assert len(notifs) >= 1, f"Expected at least 1 notification, got {len(notifs)}"
        assert any("Write docs" in n["message"] for n in notifs)

    def test_assign_task_sends_notification(self):
        """Assigning a task must produce an assignment notification."""
        task = task_service.create_task("Review PR")
        task_id = task["id"]

        # Clear notifications from creation
        database._notifications.clear()

        task_service.assign_task(task_id, "user-456")

        notifs = database.list_notifications()
        assert len(notifs) >= 1, (
            f"Expected an assignment notification, got {len(notifs)} notifications. "
            "The notification service should handle task assignment events."
        )
        assignment_notif = notifs[0]
        assert assignment_notif["recipient_id"] == "user-456", (
            f"Notification should be sent to assignee 'user-456', "
            f"got '{assignment_notif['recipient_id']}'"
        )
        assert "Review PR" in assignment_notif["message"]

    def test_assign_task_notification_has_correct_event_type(self):
        """The assignment notification event_type should indicate task assignment."""
        task = task_service.create_task("Deploy fix")
        database._notifications.clear()

        task_service.assign_task(task["id"], "user-789")

        notifs = database.list_notifications()
        assert len(notifs) >= 1, "No assignment notification was created"
        # Accept either delimiter style — both are valid fixes
        assert notifs[0]["event_type"] in ("task.assigned", "task_assigned"), (
            f"Expected event_type 'task.assigned' or 'task_assigned', "
            f"got '{notifs[0]['event_type']}'"
        )

    def test_complete_task_sends_notification(self):
        """Completing a task should produce a completion notification."""
        task = task_service.create_task("Ship feature")
        task_service.assign_task(task["id"], "user-999")
        database._notifications.clear()

        task_service.complete_task(task["id"])

        notifs = database.list_notifications()
        assert len(notifs) >= 1, (
            "Expected a completion notification, got none. "
            "The notification service should handle task completion events."
        )
        assert "Ship feature" in notifs[0]["message"]
