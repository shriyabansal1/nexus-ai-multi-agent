from config import settings
from agents.base_agent import BaseAgent


class AnswerAgent(BaseAgent):

    def __init__(
        self,
        event_bus=None,
        memory_manager=None,
        temperature=0.2,
        num_predict=500,
    ):
        super().__init__(
            name="Answer Agent",
            role_prompt="""
You are the final response agent.

You NEVER perform research.

You NEVER invent facts.

You NEVER pretend to access files.

You ONLY use the supplied context.

Rules:

1. If the context contains PDF text,
   return the PDF text or summarize it depending on the user's request.

2. If the context contains CSV data,
   present the CSV clearly.

3. If the context contains database results,
   present them clearly.

4. Never say:
   - "I would read..."
   - "I would access..."
   - "I have access..."

5. The context already contains the tool output.
   Treat it as the source of truth.

6. If the user asks to read a file,
   simply return the file contents.

7. If the user asks to summarize,
   summarize ONLY the supplied context.

8. Never use outside knowledge.

9. Never use memory unless no tool output exists.

Your job is formatting only.
""",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
            temperature=temperature,
            num_predict=num_predict,
        )

    async def think(
        self,
        user_input: str,
        context: str | None = None,
        execution_context=None,
    ):

        if context:

            text = context.strip()

            # -----------------------------
            # Database
            # -----------------------------
            if (
                text.startswith("(")
                or "INTEGER" in text
                or "TEXT" in text
                or "REAL" in text
                or "BLOB" in text
                or "|" in text
            ):
                return text

            if text.startswith("Execution Output:"):
                return text
            lower = user_input.lower()

            if "read" in lower and (
                "pdf" in lower
                or "file" in lower
                or "csv" in lower
            ):
                return text

        return await super().think(
            user_input,
            context,
            execution_context=execution_context,
        )