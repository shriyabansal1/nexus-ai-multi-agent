from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteTool:

    def __init__(self, database_path: str):

        self.database_path = Path(database_path)

    def _connect(self):

        return sqlite3.connect(self.database_path)

    def execute(self, query: str):

        connection = self._connect()

        try:

            cursor = connection.cursor()

            cursor.execute(query)

            if cursor.description:

                rows = cursor.fetchall()

                if not rows:
                    return "No records found."

                columns = [
                    desc[0]
                    for desc in cursor.description
                ]

                output = []

                output.append(
                    " | ".join(columns)
                )

                output.append("-" * 60)

                for row in rows:
                    output.append(
                        " | ".join(
                            map(str, row)
                        )
                    )

                return "\n".join(output)

            connection.commit()

            return "Query executed."

        except Exception as e:

            return f"SQLite Error: {e}"

        finally:

            connection.close()

    def table_names(self):

        return self.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
            """
        )

    def schema(self, table):

        return self.execute(
            f"PRAGMA table_info({table});"
        )