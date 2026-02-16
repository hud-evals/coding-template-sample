"""Event ingestion service."""

import time

from database import save_event, get_events
from utils.validators import validate_event
from services import webhook_handler


_event_counter = 100


def ingest_event(raw):
    """Validate, store, and process a raw webhook event.

    Parameters
    ----------
    raw : dict

    Returns
    -------
    tuple[int, dict]
    """
    global _event_counter

    errors = validate_event(raw)
    if errors:
        return 400, {"error": "Validation failed", "details": errors}

    _event_counter += 1
    event = {
        "event_id": f"evt-{_event_counter:04d}",
        "event_type": raw["event_type"],
        "assignee": raw["assignee"],
        "data": raw.get("data", {}),
        "assignee_preferences": raw.get("assignee_preferences", {}),
        "received_at": time.time(),
    }

    save_event(event)

    result = webhook_handler.process_event(event)

    return 201, {
        "event_id": event["event_id"],
        "notification": result,
    }


def list_events():
    """Return all stored events.

    Returns
    -------
    list[dict]
    """
    return get_events()
