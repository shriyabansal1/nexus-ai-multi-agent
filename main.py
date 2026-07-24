import asyncio

from config import settings

from memory import MemoryManager

from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.answer_agent import AnswerAgent
from agents.reflection_agent import ReflectionAgent
from agents.validator import ValidatorAgent
from agents.code_agent import CodeAgent
from agents.db_agent import DBAgent
from agents.file_agent import FileAgent

from agents.analyst_agent import AnalystAgent
from agents.critic_agent import CriticAgent
from agents.optimizer_agent import OptimizerAgent
from agents.reporter_agent import ReporterAgent

from orchestrator.planner import Planner
from orchestrator.registry import AgentRegistry
from orchestrator.orchestrator import Orchestrator


async def main():

    memory_manager = MemoryManager()

    registry = AgentRegistry()

    registry.register("research", ResearchAgent(memory_manager=memory_manager))
    registry.register("answer", AnswerAgent(memory_manager=memory_manager))

    registry.register("analyst", AnalystAgent())
    registry.register("summarizer", SummarizerAgent())
    registry.register("critic", CriticAgent())
    registry.register("optimizer", OptimizerAgent())
    registry.register("reflection", ReflectionAgent())
    registry.register("validator", ValidatorAgent())
    registry.register("reporter", ReporterAgent())

    # Tool agents also don't need conversational memory
    registry.register("code", CodeAgent())
    registry.register("db", DBAgent())
    registry.register("file", FileAgent())

    planner = Planner()

    orchestrator = Orchestrator(
        planner=planner,
        registry=registry,
    )

    goal = input("Goal: ")

    tasks, execution = await orchestrator.run(goal)

    print("\nExecution Results\n")

    for task in tasks:
        print("=" * 50)
        print(task.description)
        print(task.status.value)
        print(task.result)
        print()

    print("=" * 50)
    print("Execution Summary")
    print(execution)

if __name__ == "__main__":
    asyncio.run(main())