"""
Domain models for the settings API.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class User:
    id: str
    name: str
    email: str
    tier: str = "free"
    settings: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "tier": self.tier,
            "settings": dict(self.settings),
        }
