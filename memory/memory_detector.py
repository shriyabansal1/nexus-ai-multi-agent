class MemoryDetector:

    @staticmethod
    def is_memory_statement(text: str) -> bool:
        text = text.lower().strip()

        patterns = [
            "my name is",
            "i am",
            "i'm",
            "i prefer",
            "my favorite",
            "remember that",
            "i study at",
            "i work at",
        ]

        return any(text.startswith(p) for p in patterns)