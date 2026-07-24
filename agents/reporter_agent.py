from agents.base_agent import BaseAgent
from config import settings


class ReporterAgent(BaseAgent):

    def __init__(self, event_bus=None, memory_manager=None,temperature=0.1,
num_predict=200,):
        super().__init__(
            name="reporter",
            role_prompt="""
You are an expert AI reporting agent.

Responsibilities:
- Produce a structured execution report.
- Summarize the work completed by all agents.
- Highlight key findings and conclusions.
- List important recommendations.
- Present information clearly and professionally.

Rules:
- Do not invent facts.
- Do not perform additional research.
- Do not modify previous outputs.
- Do not criticize previous agents.
- Organize the report with clear headings.
- Keep the report concise and easy to read.
""",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
            temperature=temperature,
            num_predict=num_predict,
        )