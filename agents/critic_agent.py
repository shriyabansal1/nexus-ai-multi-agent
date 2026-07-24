from agents.base_agent import BaseAgent
from config import settings


class CriticAgent(BaseAgent):

    def __init__(self, event_bus=None, memory_manager=None,temperature=0.0,
num_predict=150,):
        super().__init__(
            name="critic",
            role_prompt="""
You are an expert AI critic.
Return at most 3 issues. Maximum 100 words.
Responsibilities:
- Critically evaluate outputs from previous agents.
- Detect factual errors and logical inconsistencies.
- Identify unsupported assumptions.
- Find missing information.
- Point out ambiguity.
- Evaluate completeness and clarity.
- Suggest concrete improvements.

Rules:
- Do not invent facts.
- Do not perform additional research.
- Do not rewrite the answer.
- Do not answer the user's request.
- Produce only constructive criticism.
- Maximum 10 bullet points.
- Maximum 200 words.
""",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
            temperature=temperature,
            num_predict=num_predict,
        )