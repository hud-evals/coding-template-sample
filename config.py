"""Application configuration."""

APP_CONFIG = {
    "host": "0.0.0.0",
    "port": 8090,
    "debug": False,
    "api_version": "v2",
    "max_payload_bytes": 65536,
    "request_timeout_ms": 30000,
}

PLAN_TIERS = {
    "free": {"max_channels": 1, "rate_limit": 10},
    "starter": {"max_channels": 3, "rate_limit": 100},
    "business": {"max_channels": 5, "rate_limit": 1000},
    "enterprise": {"max_channels": None, "rate_limit": None},
}

CHANNEL_DEFAULTS = {
    "high": ["email", "sms", "push"],
    "normal": ["email", "push"],
    "low": ["email"],
}

CHANNEL_REGISTRY = {
    "email": {"provider": "ses", "enabled": True, "priority_weight": 1},
    "sms": {"provider": "twilio", "enabled": True, "priority_weight": 3},
    "slack": {"provider": "slack_api", "enabled": True, "priority_weight": 2},
    "push": {"provider": "fcm", "enabled": True, "priority_weight": 2},
    "pagerduty": {"provider": "pagerduty_api", "enabled": False, "priority_weight": 5},
}

DELIVERY_CONFIG = {
    "max_retries": 3,
    "retry_delay_seconds": 5,
    "timeout_seconds": 10,
    "batch_size": 50,
    "dead_letter_ttl_hours": 72,
}

DEDUP_CONFIG = {
    "window_seconds": 300,
    "hash_fields": ["event_type", "assignee", "data.task_id"],
}

SUPPORTED_EVENT_TYPES = [
    "task.assigned",
    "task.completed",
    "task.urgent",
    "comment.added",
    "review.requested",
]
