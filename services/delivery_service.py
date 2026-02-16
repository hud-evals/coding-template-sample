"""Notification delivery service."""

import time

from database import save_notification

_delivery_counter = 200


def deliver(notification_payload):
    """Store *notification_payload* and return a delivery receipt.

    Parameters
    ----------
    notification_payload : dict

    Returns
    -------
    dict
    """
    global _delivery_counter

    if notification_payload is None:
        return {"delivered": False, "reason": "empty payload"}

    _delivery_counter += 1
    delivery_id = f"dlv-{_delivery_counter:04d}"

    save_notification(notification_payload)

    return {
        "delivered": True,
        "delivery_id": delivery_id,
        "channels": notification_payload.get("channels", []),
        "recipient": notification_payload.get("recipient"),
        "delivered_at": time.time(),
    }
