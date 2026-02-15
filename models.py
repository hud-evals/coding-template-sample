"""Domain models for the task management API.

Uses plain dataclasses — no ORM, no external dependencies.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    title: str
    description: str = ""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    status: str = TaskStatus.OPEN.value
    assignee_id: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "assignee_id": self.assignee_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class Notification:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    event_type: str = ""
    recipient_id: str = ""
    message: str = ""
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "recipient_id": self.recipient_id,
            "message": self.message,
            "created_at": self.created_at,
        }
