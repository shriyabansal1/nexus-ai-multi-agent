from pathlib import Path
from agents.base_agent import BaseAgent
from config import settings
from deployment.file_manager import FileManager
from tools import FileTool


class FileAgent(BaseAgent):
    def __init__(self, event_bus=None, memory_manager=None):
        super().__init__(
            name="file",
            role_prompt="""
You are a File Agent.

You can:
- Read uploaded PDFs
- Read uploaded CSVs
- Read text files
- Write text files
- List files

Return only the requested result.
""",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
        )
        self.file_tool = FileTool()

    async def think(
        self,
        user_input: str,
        context: str | None = None,
        execution_context=None,
    ) -> str:
        request = user_input.lower().strip()
        try:
            if "uploaded pdf" in request:
                if FileManager.LAST_PDF is None:
                    return "No uploaded PDF found."
                return self.file_tool.read_pdf(
                    str(FileManager.LAST_PDF)
                )
            if "uploaded csv" in request:
                if FileManager.LAST_CSV is None:
                    return "No uploaded CSV found."
                rows = self.file_tool.read_csv(
                    str(FileManager.LAST_CSV)
                )
                return "\n".join(
                    str(r)
                    for r in rows
                )
            if "list" in request:
                files = []
                for folder in [
                    "data/raw",
                    "data/csv",
                    "data/db",
                ]:
                    files.extend(
                        self.file_tool.list_files(folder)
                    )
                return "\n".join(files)
            if request.startswith("read"):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    return "Filename missing."
                filename = parts[1]
                path = Path(filename)
                if path.suffix.lower() == ".pdf":
                    return self.file_tool.read_pdf(filename)
                elif path.suffix.lower() == ".csv":
                    rows = self.file_tool.read_csv(filename)
                    return "\n".join(
                        str(r)
                        for r in rows
                    )
                else:
                    return self.file_tool.read_text(filename)
            if request.startswith("write"):
                parts = user_input.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: write file.txt content"
                return self.file_tool.write_text(
                    parts[1],
                    parts[2],
                )
            return "Unsupported file operation."
        except Exception as e:
            return str(e)