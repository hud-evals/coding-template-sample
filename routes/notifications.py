"""Notification endpoints."""

from services import notification_service


def handle_notifications(method, path_parts, body, send_json, send_error):
    """GET /notifications/<user_id> — notification preference summary."""
    if method != "GET":
        return send_error(405, "Method not allowed")
    if len(path_parts) < 2:
        return send_error(400, "Missing user id")

    user_id = path_parts[1]
    summary = notification_service.get_notification_summary(user_id)
    if summary is None:
        return send_error(404, "User not found")
    return send_json(200, summary)
