"""In-memory data store for events and notifications."""

_events: list[dict] = []
_notifications: list[dict] = []


def save_event(event_dict):
    """Persist an event dict.

    Parameters
    ----------
    event_dict : dict
    """
    _events.append(event_dict)


def get_events():
    """Return all stored events.

    Returns
    -------
    list[dict]
    """
    return list(_events)


def save_notification(payload):
    """Persist a notification payload.

    Parameters
    ----------
    payload : dict
    """
    _notifications.append(payload)


def get_notifications():
    """Return all stored notifications.

    Returns
    -------
    list[dict]
    """
    return list(_notifications)


def get_notifications_for_recipient(recipient):
    """Return notifications for *recipient*.

    Parameters
    ----------
    recipient : str

    Returns
    -------
    list[dict]
    """
    return [n for n in _notifications if n.get("recipient") == recipient]
