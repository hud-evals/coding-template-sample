"""Request and notification lifecycle logging."""

import time
from collections import deque


_log_buffer = deque(maxlen=500)


def _timestamp():
    """Return the current time as a float.

    Returns
    -------
    float
    """
    return time.time()


def log_request(method, path, status_code, duration_ms=None):
    """Record an HTTP request.

    Parameters
    ----------
    method : str
    path : str
    status_code : int
    duration_ms : float or None
    """
    _log_buffer.append({
        "kind": "request",
        "method": method,
        "path": path,
        "status": status_code,
        "duration_ms": duration_ms,
        "ts": _timestamp(),
    })


def log_notification(notification_id, recipient, channels, outcome):
    """Record a notification delivery attempt.

    Parameters
    ----------
    notification_id : str
    recipient : str
    channels : list[str]
    outcome : str
    """
    _log_buffer.append({
        "kind": "notification",
        "notification_id": notification_id,
        "recipient": recipient,
        "channels": list(channels),
        "outcome": outcome,
        "ts": _timestamp(),
    })


def log_event(event_id, event_type, assignee):
    """Record an ingested event.

    Parameters
    ----------
    event_id : str
    event_type : str
    assignee : str
    """
    _log_buffer.append({
        "kind": "event",
        "event_id": event_id,
        "event_type": event_type,
        "assignee": assignee,
        "ts": _timestamp(),
    })


def get_recent_logs(limit=50):
    """Return the most recent log entries.

    Parameters
    ----------
    limit : int

    Returns
    -------
    list[dict]
    """
    entries = list(_log_buffer)
    return entries[-limit:]


def clear():
    """Flush the log buffer."""
    _log_buffer.clear()
