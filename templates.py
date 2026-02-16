"""Notification routing configuration."""

_ROUTING = {
    "task.assigned": {
        "priority": "normal",
        "channels": ["email"],
        "actions": [],
        "cooldown_minutes": 0,
    },
    "task.completed": {
        "priority": "low",
        "channels": ["email"],
        "actions": [],
        "cooldown_minutes": 5,
    },
    "task.urgent": {
        "priority": "high",
        "channels": ["email", "sms"],
        "actions": ["page_oncall"],
        "cooldown_minutes": 0,
    },
    "comment.added": {
        "priority": "low",
        "channels": ["email"],
        "actions": [],
        "cooldown_minutes": 15,
    },
    "review.requested": {
        "priority": "normal",
        "channels": ["email"],
        "actions": [],
        "cooldown_minutes": 0,
    },
}

SUPPORTED_EVENTS = list(_ROUTING.keys())


def get_routing(event_type):
    """Return routing config dict for *event_type*, or ``None``."""
    return _ROUTING.get(event_type)


def get_channels(event_type):
    """Return the base delivery channel list for *event_type*."""
    route = get_routing(event_type)
    if route is None:
        return ["email"]
    return route["channels"]


def get_priority(event_type):
    """Return the priority string for *event_type*."""
    route = get_routing(event_type)
    if route is None:
        return "normal"
    return route["priority"]


def get_actions(event_type):
    """Return the action list for *event_type*."""
    route = get_routing(event_type)
    if route is None:
        return []
    return route["actions"]


def get_cooldown(event_type):
    """Return cooldown in minutes for *event_type*."""
    route = get_routing(event_type)
    if route is None:
        return 0
    return route.get("cooldown_minutes", 0)
