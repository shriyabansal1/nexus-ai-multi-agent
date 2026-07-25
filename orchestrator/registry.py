"""
Registry for all available agents.
The Orchestrator uses this registry to find the correct
agent for a given task.
"""
from agents.base_agent import BaseAgent
class AgentRegistry:
    """
    Stores and provides access to all available agents.
    """
    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, name: str, agent: BaseAgent) -> None:
        """
        Register an agent using a unique name.
        """
        self._agents[name] = agent

    def get(self, name: str) -> BaseAgent:
        """
        Retrieve a registered agent.
        """
        if name not in self._agents:
            raise ValueError(f"Agent '{name}' is not registered.")
        return self._agents[name]

    def exists(self, name: str) -> bool:
        """
        Check whether an agent is registered.
        """
        return name in self._agents

    def list_agents(self) -> list[str]:
        """
        Return the names of all registered agents.
        """
        return list(self._agents.keys())