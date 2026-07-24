from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class MemoryRecord:
    """
    Represents a single memory entry.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    content: str = ""
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )