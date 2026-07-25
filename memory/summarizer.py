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

Your job is to extract ONLY permanent long-term user information.

Rules:
- Extract ONLY facts explicitly stated by the user.
- Never infer information.
- Never rewrite or summarize.
- Never explain.
- Never invent facts.
- Never include assistant responses.
- Preserve the meaning of the original statement.
- Keep relationships between entities.

If there is no permanent user fact, return exactly:

No long-term memory.

Store memories in key-value style.

Examples:

Input:
My name is Shriya

Output:
Name: Shriya

Input:
I am from Delhi

Output:
Location: Delhi

Input:
I study at IGDTUW

Output:
College: IGDTUW

Input:
I prefer Python over Java

Output:
Preferred language: Python

Input:
My favourite colour is Blue

Output:
Favourite colour: Blue

Input:
My goal is to become an AI Engineer

Output:
Goal: Become an AI Engineer

Input:
Explain Transformers

Output:
No long-term memory.

Return only the extracted memory.

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