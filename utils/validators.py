"""Input validation for incoming webhook events."""

from config import SUPPORTED_EVENT_TYPES


def validate_event(raw):
    """Validate the top-level structure of a raw webhook event.

    Parameters
    ----------
    raw : dict

    Returns
    -------
    list[str]
    """
    errors = []

    if not isinstance(raw, dict):
        return ["Payload must be a JSON object"]

    event_type = raw.get("event_type")
    if not event_type:
        errors.append("Missing required field: event_type")
    elif event_type not in SUPPORTED_EVENT_TYPES:
        errors.append(
            f"Unsupported event_type '{event_type}'. "
            f"Must be one of: {', '.join(SUPPORTED_EVENT_TYPES)}"
        )

    assignee = raw.get("assignee")
    if not assignee or not isinstance(assignee, str):
        errors.append("Missing or invalid field: assignee (must be a non-empty string)")

    data = raw.get("data")
    if data is not None and not isinstance(data, dict):
        errors.append("Field 'data' must be a JSON object if provided")

    prefs = raw.get("assignee_preferences")
    if prefs is not None and not isinstance(prefs, dict):
        errors.append("Field 'assignee_preferences' must be a JSON object if provided")

    return errors


def validate_event_type(event_type):
    """Return ``True`` if *event_type* is recognised.

    Parameters
    ----------
    event_type : str

    Returns
    -------
    bool
    """
    return event_type in SUPPORTED_EVENT_TYPES
