"""Webhook HTTP route dispatcher."""

from services.event_service import ingest_event, list_events
from database import get_notifications, get_notifications_for_recipient


def handle_webhook_routes(path, method, body):
    """Route an HTTP request to the appropriate handler.

    Parameters
    ----------
    path : str
    method : str
    body : dict or None

    Returns
    -------
    tuple[int, dict]
    """
    if method == "POST" and path == "/webhooks/events":
        return ingest_event(body)

    if method == "GET":
        if path == "/health":
            return 200, {"status": "ok"}

        if path == "/events":
            return 200, {"events": list_events()}

        if path == "/notifications":
            return 200, {"notifications": get_notifications()}

        if path.startswith("/notifications/"):
            recipient = path.split("/notifications/", 1)[1]
            if not recipient:
                return 400, {"error": "Recipient required in path"}
            found = get_notifications_for_recipient(recipient)
            return 200, {"recipient": recipient, "notifications": found}

    return 404, {"error": f"No route for {method} {path}"}
