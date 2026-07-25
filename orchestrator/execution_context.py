from __future__ import annotations

from typing import Any

from orchestrator.execution_logger import ExecutionLogger
from orchestrator.execution_state import ExecutionState
from orchestrator.execution_trace import ExecutionTrace


class ExecutionContext:
    """
    Shared execution context for a single NEXUS run.

    Every component (Planner, Orchestrator, Agents, Tools)
    receives the same ExecutionContext instance.

    It acts as the communication layer between all modules.
    """

    def __init__(self, goal: str) -> None:
        self.state = ExecutionState(goal)
        self.trace = ExecutionTrace()
        self.logger = ExecutionLogger()

    @property
    def goal(self) -> str:
        """
        Returns the original user goal.
        """
        return self.state.goal

    def start_execution(self) -> None:
        """
        Starts execution tracking.
        """
        self.state.start()
        self.logger.execution_started(self.goal)

    def finish_execution(self, success: bool = True) -> None:
        """
        Finishes execution tracking.
        """
        self.state.finish(success)
        duration = self.state.duration or 0.0

        if success:
            self.logger.execution_completed(duration)
        else:
            self.logger.execution_failed(
                self.state.error or "Unknown execution failure."
            )

    def set_current_agent(self, agent: str) -> None:
        """
        Updates the currently active agent.
        """
        self.state.set_current_agent(agent)

    def start_agent(self, agent: str, task: str, input_data: Any = None):
        """
        Starts tracing an agent execution.
        """
        self.set_current_agent(agent)

        self.logger.agent_started(agent, task)

        return self.trace.start(
            agent=agent,
            task=task,
            input_data=input_data,
        )

    def finish_agent(self, trace_entry, output_data: Any = None) -> None:
        """
        Marks an agent execution as successful.
        """
        trace_entry.finish(output_data)

        self.logger.agent_completed(
            trace_entry.agent,
            trace_entry.duration or 0.0,
        )

    def fail_agent(self, trace_entry, error: str) -> None:
        """
        Marks an agent execution as failed.
        """
        trace_entry.fail(error)

        self.state.error = error

        self.logger.agent_failed(
            trace_entry.agent,
            error,
        )

    def put(self, key: str, value: Any) -> None:
        """
        Stores shared data that downstream agents can use.
        """
        self.state.put(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves shared data.
        """
        return self.state.get(key, default)

    def increment_retry(self) -> None:
        """
        Increments retry counter.
        """
        self.state.increment_retry()

    def increment_replan(self) -> None:
        """
        Increments replan counter.
        """
        self.state.increment_replan()

    def summary(self) -> dict[str, Any]:
        """
        Returns an overall execution summary.
        """
        return {
            "goal": self.goal,
            "success": self.state.success,
            "duration": self.state.duration,
            "retry_count": self.state.retry_count,
            "replan_count": self.state.replan_count,
            "completed_tasks": self.state.total_completed,
            "failed_tasks": self.state.total_failed,
            "trace": self.trace.summary(),
        }