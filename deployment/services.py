import uuid
from datetime import datetime
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

class AIService:

    def __init__(self):
        self.memory_manager = MemoryManager()
        self.registry = AgentRegistry()
        self.registry.register(
            "research",
            ResearchAgent(memory_manager=self.memory_manager),
        )
        self.registry.register(
            "answer",
            AnswerAgent(memory_manager=self.memory_manager),
        )
        self.registry.register("analyst", AnalystAgent())
        self.registry.register("summarizer", SummarizerAgent())
        self.registry.register("critic", CriticAgent())
        self.registry.register("optimizer", OptimizerAgent())
        self.registry.register("reflection", ReflectionAgent())
        self.registry.register("validator", ValidatorAgent())
        self.registry.register("reporter", ReporterAgent())
        self.registry.register("code", CodeAgent())
        self.registry.register("db", DBAgent())
        self.registry.register("file", FileAgent())
        self.planner = Planner()
        self.orchestrator = Orchestrator(
            planner=self.planner,
            registry=self.registry,
        )
        self.execution_history = {}

    async def execute(self, goal: str):
        try:
            execution_id = str(uuid.uuid4())
            started = datetime.now()
            from memory.memory_detector import MemoryDetector
            if MemoryDetector.is_memory_statement(goal):
                await self.memory_manager.remember(
                    user_input=goal,
                    assistant_response="I'll remember that."
                )
                finished = datetime.now()
                execution = {
                    "trace": {
                        "entries": [
                            {
                                "agent": "Memory Detector",
                                "task": "Detect memory statement",
                                "status": "completed",
                            },
                            {
                                "agent": "Memory Manager",
                                "task": "Store long-term memory",
                                "status": "completed",
                            },
                        ]
                    }
                }

                self.execution_history[execution_id] = {
                    "goal": goal,
                    "answer": "I'll remember that.",
                    "execution": execution,
                    "started": started.isoformat(),
                    "finished": finished.isoformat(),
                }

                return (
                    execution_id,
                    "I'll remember that.",
                    execution,
                )
            tasks, execution = await self.orchestrator.run(goal)
            finished = datetime.now()
            final_answer = "No answer generated."

            for task in tasks:
                if (
                    task.assigned_agent == "reflection"
                    and task.result
                ):
                    final_answer = task.result
                    break

            if final_answer == "No answer generated.":
                for task in tasks:
                    if (
                        task.assigned_agent == "answer"
                        and task.result
                    ):
                        final_answer = task.result
                        break

            if final_answer == "No answer generated.":
                for task in reversed(tasks):
                    if task.result:
                        final_answer = task.result
                        break

            self.execution_history[execution_id] = {
                "goal": goal,
                "answer": final_answer,
                "execution": execution,
                "started": started.isoformat(),
                "finished": finished.isoformat(),
            }
            return execution_id, final_answer, execution
        except Exception:
            import traceback
            traceback.print_exc()
            raise

    def get_execution(self, execution_id: str):
        return self.execution_history.get(execution_id)

    def get_history(self):
        return self.execution_history

    def health(self):
        return {
            "status": "healthy"
        }

service = AIService()