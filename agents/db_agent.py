from agents.base_agent import BaseAgent
from config import settings
from deployment.file_manager import FileManager
from tools import SQLiteTool


class DBAgent(BaseAgent):

    def __init__(
        self,
        event_bus=None,
        memory_manager=None,
    ):

        super().__init__(
            name="DB Agent",
            role_prompt="SQLite Database Agent",
            model=settings.llm.default_model,
            event_bus=event_bus,
            memory_manager=memory_manager,
        )

    async def think(
        self,
        user_input: str,
        context: str | None = None,
        execution_context=None,
    ) -> str:

        if FileManager.LAST_DB is None:
            return "No uploaded database found."

        db = SQLiteTool(str(FileManager.LAST_DB))

        request = user_input.lower().strip()

        try:

            # ===================================================
            # SHOW TABLES
            # ===================================================

            if any(
                phrase in request
                for phrase in [
                    "show tables",
                    "list tables",
                    "database tables",
                    "show database",
                    "uploaded database",
                    "show uploaded database",
                    "what tables",
                    "tables in database",
                    "tables",
                ]
            ):
                return db.table_names()

            # ===================================================
            # SCHEMA / COLUMNS
            # ===================================================

            if any(
                phrase in request
                for phrase in [
                    "schema",
                    "columns",
                    "column",
                    "structure",
                    "describe",
                    "fields",
                ]
            ):

                tables = db.table_names()

                if isinstance(tables, str):
                    table_names = [
                        t.strip()
                        for t in tables.replace(",", "\n").split("\n")
                        if t.strip()
                    ]
                else:
                    table_names = tables

                for table in table_names:
                    clean_table = table.lower().strip()
                    if clean_table in request:
                        return db.schema(clean_table)

                    # Singular/plural match
                    if clean_table.endswith("s"):
                        singular = clean_table[:-1]
                        if singular in request:
                            return db.schema(clean_table)

                return (
                    "Please specify a table name.\n\n"
                    "Example:\n"
                    "Schema employees\n"
                    "Show columns of employees"
                )

            # ===================================================
            # RAW SQL
            # ===================================================

            if request.startswith(
                (
                    "select",
                    "pragma",
                    "insert",
                    "update",
                    "delete",
                    "create",
                    "drop",
                    "alter",
                )
            ):
                return db.execute(user_input)

            # ===================================================
            # HELP
            # ===================================================

            return (
                "I can help with SQLite databases.\n\n"
                "Examples:\n"
                "• Show tables\n"
                "• List tables\n"
                "• Show database\n"
                "• Schema employees\n"
                "• Show columns of employees\n"
                "• Describe employees\n"
                "• SELECT * FROM employees;\n"
                "• SELECT COUNT(*) FROM employees;"
            )

        except Exception as e:
            return f"Database Error:\n{e}"