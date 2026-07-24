"""
Task model for the NEXUS AI orchestration system.

A Task represents a single unit of work produced by the Planner.
It contains only data. It does not know how to execute itself.

Execution is the responsibility of the Orchestrator.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class TaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Task:
    id: UUID = field(default_factory=uuid4)
    description: str = ""
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    depends_on: list[UUID] = field(default_factory=list)