"""
Routes tasks to the correct agent.
"""

from orchestrator.task import Task
from orchestrator.registry import AgentRegistry


class Router:

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def route(self, task: Task):

        if task.assigned_agent is None:
            raise ValueError(
                f"Task '{task.description}' has no assigned agent."
            )

        if not self.registry.exists(task.assigned_agent):
            available = ", ".join(self.registry.list_agents())

            raise ValueError(
                f"Unknown agent '{task.assigned_agent}'. "
                f"Available agents: {available}"
            )

        return self.registry.get(task.assigned_agent)