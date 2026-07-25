from __future__ import annotations

from memory.long_term_memory import LongTermMemory
from memory.memory_models import MemoryRecord
from memory.session_memory import SessionMemory
from memory.summarizer import MemorySummarizer
from memory.vector_store import VectorStore


class MemoryManager:
    """
    Coordinates all memory systems.

    Responsibilities:
    - Maintain session memory
    - Store long-term memories
    - Store vector embeddings
    - Retrieve similar memories
    """

    def __init__(self, session_memory: SessionMemory | None = None, long_term_memory: LongTermMemory | None = None, vector_store: VectorStore | None = None, summarizer: MemorySummarizer | None = None):
        self.session_memory = session_memory if session_memory is not None else SessionMemory()
        self.long_term_memory = long_term_memory if long_term_memory is not None else LongTermMemory()
        self.vector_store = vector_store if vector_store is not None else VectorStore()
        self.summarizer = summarizer if summarizer is not None else MemorySummarizer()

    def add_to_session(self, role: str, content: str) -> None:
        self.session_memory.add_message(role, content)

    def session_context(self) -> str:
        return self.session_memory.get_context()

    async def remember(self, user_input: str, assistant_response: str) -> MemoryRecord:
        """
        Save an interaction into all memory systems.
        """

        print("\n" + "=" * 70)
        print("REMEMBER() CALLED")
        print("=" * 70)

        # Store conversation in short-term memory
        self.session_memory.add_interaction(user_input, assistant_response)

        conversation = f"User: {user_input}\nAssistant: {assistant_response}"

        print(f"User Input: {user_input}")

        # Extract long-term memory
        summary = await self.summarizer.summarize(conversation)

        print(f"Summary: {summary}")

        memory = MemoryRecord(
            content=conversation,
            summary=summary,
        )

        if self._is_empty_memory(summary):
            print("❌ Memory rejected because summary is empty.")
            return memory

        existing = self.vector_store.search(
            query=summary,
            k=1,
        )

        print("Existing:", existing)

        if existing and existing[0]["score"] >= 0.75:
            print(
                f"Duplicate memory detected (score={existing[0]['score']:.3f})"
            )
            return memory

        print("Saving to LongTermMemory...")
        self.long_term_memory.add(memory)
        print("✓ LongTermMemory saved")

        print("Saving to VectorStore...")
        self.vector_store.add(memory)
        print("✓ VectorStore saved")

        print("=" * 70)

        return memory

    def search(self, query: str, k: int = 5) -> list[dict]:
        """
        Search semantic memory.
        """
        return self.vector_store.search(query=query, k=k)
    
    def _is_empty_memory(self, summary: str) -> bool:

        if not summary:
            return True

        summary = summary.strip().lower()

        return (
            summary.startswith("no long-term memory")
            or "cannot extract" in summary
            or "no long-term memory provided" in summary
        )
    def build_context(self, query: str, k: int = 2) -> str:
        """
        Build memory context for prompt injection.
        """

        memories = self.search(query=query, k=k)

        if not memories:
            return self.session_context()

        recalled = []

        for memory in memories:
            recalled.append(memory["summary"] or memory["content"])

        parts = []
        parts.append(
            "=== Relevant Long-Term Memory ===\n"
            + "\n\n".join(recalled)
        )
        return "\n\n".join(parts)