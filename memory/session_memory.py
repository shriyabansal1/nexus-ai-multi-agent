from __future__ import annotations
from collections import deque
class SessionMemory:
    """
    Stores the short-term conversation history for the current session.
    """
    def __init__(self, max_messages: int = 8):
        self._history = deque(maxlen=max_messages)
    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        self._history.append(
            {
                "role": role,
                "content": content,
            }
        )
    def add_interaction(
        self,
        user_input: str,
        assistant_response: str,
    ) -> None:
        self.add_message(
            "user",
            user_input,
        )
        self.add_message(
            "assistant",
            assistant_response,
        )
    def get_messages(self) -> list[dict]:
        return list(self._history)
    def get_context(self) -> str:
        if not self._history:
            return ""
        return "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in self._history
        )
    def clear(self) -> None:
        self._history.clear()
    def __len__(self) -> int:
        return len(self._history)