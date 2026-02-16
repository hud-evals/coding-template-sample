"""Domain models for the settings API."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class User:
    id: str
    name: str
    email: str
    tier: str = "free"
    settings: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEntry:
    user_id: str
    action: str
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    timestamp: float = 0.0
