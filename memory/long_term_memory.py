from __future__ import annotations

import sqlite3
from pathlib import Path

from memory.memory_models import MemoryRecord


class LongTermMemory:
    """
    Persistent memory stored in SQLite.

    Responsible only for database operations.
    """

    def __init__(
        self,
        database_path: str = "memory/long_term.db",
    ):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _initialize(self) -> None:
        connection = self._connect()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    summary TEXT,
                    metadata TEXT,
                    created_at TEXT NOT NULL
                );
                """
            )

            connection.commit()

        finally:
            connection.close()

    def add(
        self,
        memory: MemoryRecord,
    ) -> None:
        connection = self._connect()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO memories (
                    id,
                    content,
                    summary,
                    metadata,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    memory.id,
                    memory.content,
                    memory.summary,
                    str(memory.metadata),
                    memory.created_at,
                ),
            )

            connection.commit()

        finally:
            connection.close()

    def get(
        self,
        memory_id: str,
    ) -> MemoryRecord | None:
        connection = self._connect()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    content,
                    summary,
                    metadata,
                    created_at
                FROM memories
                WHERE id = ?;
                """,
                (memory_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return MemoryRecord(
                id=row[0],
                content=row[1],
                summary=row[2] or "",
                metadata={},
                created_at=row[4],
            )

        finally:
            connection.close()

    def all(self) -> list[MemoryRecord]:
        connection = self._connect()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    content,
                    summary,
                    metadata,
                    created_at
                FROM memories
                ORDER BY created_at DESC;
                """
            )

            rows = cursor.fetchall()

            return [
                MemoryRecord(
                    id=row[0],
                    content=row[1],
                    summary=row[2] or "",
                    metadata={},
                    created_at=row[4],
                )
                for row in rows
            ]

        finally:
            connection.close()

    def delete(
        self,
        memory_id: str,
    ) -> None:
        connection = self._connect()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM memories
                WHERE id = ?;
                """,
                (memory_id,),
            )

            connection.commit()

        finally:
            connection.close()

    def count(self) -> int:
        connection = self._connect()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM memories;
                """
            )

            return cursor.fetchone()[0]

        finally:
            connection.close()