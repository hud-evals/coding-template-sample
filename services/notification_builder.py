"""Notification payload construction."""

import hashlib
import time

from services.channel_resolver import resolve_channels, resolve_priority
import copy
from config import CHANNEL_REGISTRY
from utils.formatters import format_subject, format_body, truncate


_notification_counter = 0


def _generate_notification_id(event_type, recipient):
    """Produce a deterministic short id from event type and recipient.

    Parameters
    ----------
    event_type : str
    recipient : str

    Returns
    -------
    str
    """
    global _notification_counter
    _notification_counter += 1
    seed = f"{event_type}:{recipient}:{_notification_counter}"
    digest = hashlib.sha256(seed.encode()).hexdigest()[:12]
    return f"ntf-{digest}"


def _sort_channels_by_weight(channels):
    """Order *channels* by their configured priority weight (ascending).

    Parameters
    ----------
    channels : list[str]

    Returns
    -------
    list[str]
    """
    def _weight(ch):
        entry = CHANNEL_REGISTRY.get(ch)
        if entry is None:
            return 99
        return entry.get("priority_weight", 50)

    return sorted(channels, key=_weight)


def _build_metadata(event_type, recipient, event_data, priority):
    """Assemble metadata dict for the notification payload.

    Parameters
    ----------
    event_type : str
    recipient : str
    event_data : dict
    priority : str

    Returns
    -------
    dict
    """
    subject = format_subject(event_type, event_data)
    body = format_body(event_type, event_data, recipient)
    return {
        "subject": truncate(subject, 120),
        "body": body,
        "priority": priority,
        "task_id": event_data.get("task_id"),
        "project": event_data.get("project"),
    }


def _merge_extra_channels(channels, extra_channels):
    """Add *extra_channels* into *channels*, skipping duplicates.

    Parameters
    ----------
    channels : list[str]
    extra_channels : list[str] or None

    Returns
    -------
    list[str]
    """
    if not extra_channels:
        return channels
    new_channels = [ch for ch in extra_channels if ch not in channels]
    channels += new_channels
    return channels


def build_notification(event_type, recipient, event_data, extra_channels=None):
    """Assemble a notification payload for delivery.

    Parameters
    ----------
    event_type : str
    recipient : str
    event_data : dict
    extra_channels : list[str] or None

    Returns
    -------
    dict or None
    """
    channels = list(resolve_channels(event_type))
    priority = resolve_priority(event_type)

    if channels is None:
        return None

    channels = _merge_extra_channels(channels, extra_channels)
    channels = _sort_channels_by_weight(channels)

    notification_id = _generate_notification_id(event_type, recipient)
    metadata = _build_metadata(event_type, recipient, event_data, priority)

    return {
        "notification_id": notification_id,
        "type": event_type,
        "priority": priority,
        "recipient": recipient,
        "channels": channels,
        "metadata": metadata,
        "event_data": event_data,
        "created_at": time.time(),
    }
