# orchestrator/execution_state.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class ExecutionState:
    """
    Stores the shared state of a single NEXUS execution.

    Every agent can access this object through the
    ExecutionContext. It serves as the single source
    of truth during orchestration.
    """

    goal: str

    created_at: datetime = field(default_factory=datetime.utcnow)

    started_at: datetime | None = None
    finished_at: datetime | None = None

    current_agent: str | None = None

    completed_tasks: set[UUID] = field(default_factory=set)
    failed_tasks: set[UUID] = field(default_factory=set)
    cancelled_tasks: set[UUID] = field(default_factory=set)

    shared_data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    retry_count: int = 0
    replan_count: int = 0

    success: bool = False
    error: str | None = None

    def start(self) -> None:
        """Marks the beginning of execution."""
        self.started_at = datetime.utcnow()

    def finish(self, success: bool = True) -> None:
        """Marks the end of execution."""
        self.finished_at = datetime.utcnow()
        self.success = success

    def set_current_agent(self, agent_name: str) -> None:
        """Updates the currently active agent."""
        self.current_agent = agent_name

    def mark_completed(self, task_id: UUID) -> None:
        """Marks a task as completed."""
        self.completed_tasks.add(task_id)

    def mark_failed(self, task_id: UUID) -> None:
        """Marks a task as failed."""
        self.failed_tasks.add(task_id)

    def mark_cancelled(self, task_id: UUID) -> None:
        """Marks a task as cancelled."""
        self.cancelled_tasks.add(task_id)

    def increment_retry(self) -> None:
        """Increments the retry counter."""
        self.retry_count += 1

    def increment_replan(self) -> None:
        """Increments the replan counter."""
        self.replan_count += 1

    def put(self, key: str, value: Any) -> None:
        """Stores shared data for downstream agents."""
        self.shared_data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves shared data."""
        return self.shared_data.get(key, default)

    @property
    def total_completed(self) -> int:
        return len(self.completed_tasks)

    @property
    def total_failed(self) -> int:
        return len(self.failed_tasks)

    @property
    def total_cancelled(self) -> int:
        return len(self.cancelled_tasks)

    @property
    def duration(self) -> float | None:
        """
        Returns the total execution time in seconds.
        """
        if self.started_at is None:
            return None

        end_time = self.finished_at or datetime.utcnow()
        return (end_time - self.started_at).total_seconds()