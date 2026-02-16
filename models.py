"""Domain models for events and notifications."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Event:
    """Incoming webhook event."""

    event_id: str
    event_type: str
    assignee: str
    data: dict = field(default_factory=dict)
    assignee_preferences: dict = field(default_factory=dict)
    received_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "assignee": self.assignee,
            "data": self.data,
            "assignee_preferences": self.assignee_preferences,
            "received_at": self.received_at,
        }


@dataclass
class Notification:
    """Built notification ready for delivery."""

    notification_id: str
    recipient: str
    event_type: str
    channels: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    actions: list = field(default_factory=list)
    payload: dict = field(default_factory=dict)
    delivered: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "notification_id": self.notification_id,
            "recipient": self.recipient,
            "event_type": self.event_type,
            "channels": self.channels,
            "metadata": self.metadata,
            "actions": self.actions,
            "payload": self.payload,
            "delivered": self.delivered,
        }


@dataclass
class DeliveryReceipt:
    """Receipt returned after notification dispatch."""

    delivery_id: str
    notification_id: str
    channels: list = field(default_factory=list)
    delivered: bool = False
    delivered_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "delivery_id": self.delivery_id,
            "notification_id": self.notification_id,
            "channels": self.channels,
            "delivered": self.delivered,
            "delivered_at": self.delivered_at,
        }
