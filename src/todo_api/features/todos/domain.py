"""Todo domain model. Defines the Todo entity and related value objects with framework-agnostic business logic."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Todo:
    """A todo item."""

    title: str
    completed: bool = False
    id: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
