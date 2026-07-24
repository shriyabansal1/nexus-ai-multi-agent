# orchestrator/execution_trace.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class TraceEntry:
    """
    Represents a single agent execution.
    """

    agent: str
    task: str

    started_at: datetime = field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None

    status: str = "RUNNING"

    input_data: Any = None
    output_data: Any = None

    error: str | None = None

    def finish(self, output_data: Any = None, status: str = "SUCCESS") -> None:
        """
        Marks this execution as completed.
        """
        self.finished_at = datetime.utcnow()
        self.status = status
        self.output_data = output_data

    def fail(self, error: str) -> None:
        """
        Marks this execution as failed.
        """
        self.finished_at = datetime.utcnow()
        self.status = "FAILED"
        self.error = error

    @property
    def duration(self) -> float | None:
        """
        Returns execution duration in seconds.
        """
        if self.finished_at is None:
            return None

        return (self.finished_at - self.started_at).total_seconds()


class ExecutionTrace:
    """
    Stores the complete execution history of one NEXUS run.
    """

    def __init__(self) -> None:
        self.entries: list[TraceEntry] = []

    def start(self, agent: str, task: str, input_data: Any = None) -> TraceEntry:
        """
        Starts a new trace entry.
        """
        entry = TraceEntry(
            agent=agent,
            task=task,
            input_data=input_data,
        )

        self.entries.append(entry)
        return entry

    def latest(self) -> TraceEntry | None:
        """
        Returns the most recent trace entry.
        """
        if not self.entries:
            return None

        return self.entries[-1]

    def successful(self) -> list[TraceEntry]:
        """
        Returns all successful executions.
        """
        return [
            entry
            for entry in self.entries
            if entry.status == "SUCCESS"
        ]

    def failed(self) -> list[TraceEntry]:
        """
        Returns all failed executions.
        """
        return [
            entry
            for entry in self.entries
            if entry.status == "FAILED"
        ]

    def total_agents(self) -> int:
        """
        Returns the number of executed agents.
        """
        return len(self.entries)

    def total_failures(self) -> int:
        """
        Returns the number of failed executions.
        """
        return len(self.failed())

    def total_successes(self) -> int:
        """
        Returns the number of successful executions.
        """
        return len(self.successful())

    def clear(self) -> None:
        """
        Clears the execution history.
        """
        self.entries.clear()

    def summary(self) -> dict[str, Any]:
        """
        Returns a summary of the execution.
        """
        return {
            "total_agents": self.total_agents(),
            "successful": self.total_successes(),
            "failed": self.total_failures(),
            "entries": [
                {
                    "agent": entry.agent,
                    "task": entry.task,
                    "status": entry.status,
                    "started_at": (
                        entry.started_at.isoformat()
                        if entry.started_at
                        else None
                    ),
                    "finished_at": (
                        entry.finished_at.isoformat()
                        if entry.finished_at
                        else None
                    ),
                    "duration": entry.duration,
                    "input_data": entry.input_data,
                    "output_data": entry.output_data,
                    "error": entry.error,
                }
                for entry in self.entries
            ],
        }