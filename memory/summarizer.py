from __future__ import annotations

from config import settings
from llm.ollama_client import OllamaClient


class MemorySummarizer:
    """
    Summarizes conversations before storing them in long-term memory.
    """

    def __init__(
        self,
        model: str | None = None,
    ):
        self.model = model or settings.llm.planner_model

    async def summarize(
        self,
        conversation: str,
    ) -> str:
        """
        Extract only important long-term facts.

        Returns a concise summary suitable for semantic search.
        """

        if not conversation.strip():
            return ""

        messages = [
    {
        "role": "system",
        "content": """
You are a memory extraction system.

Your job is to extract ONLY explicit long-term facts from the conversation.

Rules:
Extract ONLY facts explicitly stated by the user.

Never infer.
Never classify.
Never explain.
Never add labels such as:
- implicit
- likely
- presumably
- given origin

Keep only:
- User facts
- User preferences
- User goals
- Long-term decisions
- Constraints

If there is no long-term fact, return exactly:
No long-term memory.

Maximum 30 words.
- Never invent information.
- Never infer information.
- Never rewrite into paragraphs.
- Never explain.
- Never embellish.
- Never include temporary discussion.
- Never include assistant reasoning.
- If there are no long-term facts, return:
No long-term memory.

Keep only:
- User preferences
- User facts
- User goals
- Permanent decisions
- Important project facts
- Constraints

Return short bullet points.

Examples:

Favorite color: Blue

Preferred language: Python

Project: AI Multi-Agent System

Goal: Learn Generative AI

Maximum 30 words.
"""
            },
            {
                "role": "user",
                "content": conversation,
            },
        ]

        summary = await OllamaClient.chat(
            model=self.model,
            messages=messages,
        )

        return summary.strip()