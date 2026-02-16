"""Webhook event orchestrator."""

from services import notification_builder
from services import delivery_service
from services.dedup_service import is_duplicate
from services.rate_limiter import check_rate_limit, record_event
from services.preference_service import get_user_plan
from services.escalation_service import should_escalate, get_escalation_targets, record_escalation


def process_event(event):
    """Process a single event through the notification pipeline.

    Parameters
    ----------
    event : dict

    Returns
    -------
    dict
    """
    if is_duplicate(event):
        return {"delivered": False, "reason": "duplicate"}

    event_type = event["event_type"]
    recipient = event["assignee"]
    event_data = event.get("data", {})
    preferences = event.get("assignee_preferences", {})

    plan_tier = get_user_plan(recipient)
    allowed, rate_info = check_rate_limit(recipient, plan_tier)
    if not allowed:
        return {
            "delivered": False,
            "reason": "rate_limited",
            "rate_limit": rate_info,
        }

    extra_channels = _resolve_extra_channels(preferences)

    notification = notification_builder.build_notification(
        event_type,
        recipient,
        event_data,
        extra_channels,
    )

    if notification is None:
        return {"delivered": False, "reason": "unrecognised event type"}

    if should_escalate(event_type, event_data):
        targets = get_escalation_targets(event_type, event_data)
        record_escalation(event.get("event_id", ""), targets)

    record_event(recipient)
    return delivery_service.deliver(notification)


def _resolve_extra_channels(preferences):
    """Derive additional delivery channels from assignee preferences.

    Parameters
    ----------
    preferences : dict

    Returns
    -------
    list[str] or None
    """
    channels = []

    if preferences.get("slack_enabled"):
        channels.append("slack")

    if preferences.get("push_enabled"):
        channels.append("push")

    return channels if channels else None
