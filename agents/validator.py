from config import settings
from agents.base_agent import BaseAgent


class ValidatorAgent(BaseAgent):

    def __init__(
        self,
        event_bus=None,
        memory_manager=None,
        temperature=0.0,
        num_predict=150,
    ):
        super().__init__(
            name="Validator Agent",
            role_prompt="""
You are the Validator Agent.

Input contains:

Original Request
Answer

Task:

Determine whether the Answer satisfies the Original Request.

Rules:

- Validate ONLY the supplied answer.
- Do NOT answer the user's request.
- Do NOT improve the answer.
- Do NOT invent new questions.
- Do NOT create examples.
- Do NOT generate conversations.
- Keep the response under 60 words.

Output ONLY in one of these formats.

If valid:

Status: VALID

Reason:
<one short sentence>

If invalid:

Status: INVALID

Reason:
<one short sentence>

Suggested Fix:
<one short sentence>
""",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
            temperature=temperature,
            num_predict=num_predict,
        )