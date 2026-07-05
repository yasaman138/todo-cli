from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from __future__ import annotations


class Priority(str, Enum):
    """Task priority levels, ordered low to high."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class Task:
    """a single todo item"""

    id: int
    description: str
    done: bool = False
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None

    def mark_done(self) -> None:
        self.done = True
        self.completed_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "done": self.done,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        created_at = data.get("created_at")
        completed_at = data.get("completed_at")
        return cls(
            id=data["id"],
            description=data["description"],
            done=data.get("done", False),
            priority=Priority(data.get("priority", Priority.MEDIUM.value)),
            created_at=(
                datetime.fromisoformat(created_at) if created_at else datetime.now(timezone.utc)
            ),
            completed_at=datetime.fromisoformat(completed_at) if completed_at else None,
        )
