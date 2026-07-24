from agents.base_agent import BaseAgent
from config import settings
from llm.ollama_client import OllamaClient
from tools import CodeExecutor


class CodeAgent(BaseAgent):

    def __init__(self, event_bus=None,  memory_manager=None,):
        super().__init__(
            name="code",
            role_prompt="""
You are an expert Python developer.

Your responsibilities:
- Generate correct Python code.
- Return ONLY executable Python code.
- Do not use markdown.
- Do not use triple backticks.
- Do not explain the code.
""",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
        )

        self.executor = CodeExecutor()

    async def think(self, user_input: str, context: str | None = None, execution_context=None) -> str:

        messages = self.build_messages(
            user_input,
            context,
        )

        code = await OllamaClient.chat(
            model=self.model,
            messages=messages,
        )

        code = code.strip()

        if code.startswith("```"):
            code = code.replace("```python", "")
            code = code.replace("```", "")
            code = code.strip()

        result = self.executor.execute(code)

        self._update_history(
            user_input,
            result,
        )

        return result