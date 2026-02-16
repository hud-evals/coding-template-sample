"""Message formatting utilities."""


def format_subject(event_type, data):
    """Return a short subject line for an event.

    Parameters
    ----------
    event_type : str
    data : dict

    Returns
    -------
    str
    """
    task_id = data.get("task_id", "unknown")
    return f"[{event_type}] {task_id}"


def format_body(event_type, data, recipient):
    """Return a plain-text body for a notification.

    Parameters
    ----------
    event_type : str
    data : dict
    recipient : str

    Returns
    -------
    str
    """
    task_id = data.get("task_id", "unknown")
    project = data.get("project", "unknown")
    return (
        f"Hi {recipient},\n\n"
        f"Event {event_type} for {task_id} in project {project}."
    )


def truncate(text, max_length=140):
    """Truncate *text* to *max_length* characters.

    Parameters
    ----------
    text : str
    max_length : int

    Returns
    -------
    str
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 1] + "\u2026"


def channel_label(channel):
    """Return a display-friendly label for a delivery channel.

    Parameters
    ----------
    channel : str

    Returns
    -------
    str
    """
    labels = {
        "email": "Email",
        "sms": "SMS",
        "slack": "Slack",
        "push": "Push Notification",
        "pagerduty": "PagerDuty",
    }
    return labels.get(channel, channel.title())
