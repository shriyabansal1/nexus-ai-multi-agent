from agents.base_agent import BaseAgent
from config import settings


class OptimizerAgent(BaseAgent):

    def __init__(self, event_bus=None, memory_manager=None,temperature=0.1,
num_predict=250,):
        super().__init__(
            name="optimizer",
            role_prompt="""
You are an expert AI optimizer.
Return at most 3 issues. Maximum 100 words.
Responsibilities:
- Improve outputs produced by previous agents.
- Apply improvements suggested by the critic.
- Increase clarity, accuracy and completeness.
- Remove redundancy.
- Improve logical flow.
- Preserve the original meaning.
- Produce the highest quality version.

Rules:
- Do not invent facts.
- Do not perform additional research.
- Do not ignore valid criticism.
- Keep all technically correct information.
- Return only the optimized result.
""",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
            temperature=temperature,
            num_predict=num_predict,
        )