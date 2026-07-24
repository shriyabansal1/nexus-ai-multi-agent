from config import settings
from agents.base_agent import BaseAgent


class ReflectionAgent(BaseAgent):

    def __init__(self, event_bus=None,memory_manager=None,temperature=0.0,
num_predict=120,):
        super().__init__(
            name="Reflection Agent",
            role_prompt="""
You are an expert Reflection Agent.
Return at most 3 issues. Maximum 100 words.
Responsibilities:
- Carefully review the provided answer.
- Improve clarity.
- Remove repetition.
- Fix grammatical mistakes.
- Improve structure.
- Keep technical accuracy.
- Make the explanation easier to understand.

Constraints:
- Do NOT invent new facts.
- Do NOT perform additional research.
- Do NOT change the meaning.
- Return only the improved answer.
""",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
            temperature=temperature,
            num_predict=num_predict,
        )