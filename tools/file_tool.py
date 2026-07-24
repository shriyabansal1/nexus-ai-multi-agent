from __future__ import annotations

import csv
from pathlib import Path

from pypdf import PdfReader


class FileTool:

    def read_text(self, path: str) -> str:

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write_text(self, path: str, content: str) -> str:

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Saved {path}"

    def read_pdf(self, path: str) -> str:

        reader = PdfReader(path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    def read_csv(self, path: str):

        with open(
            path,
            newline="",
            encoding="utf-8",
        ) as f:

            return list(csv.reader(f))

    def write_csv(self, path: str, rows):

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8",
        ) as f:

            csv.writer(f).writerows(rows)

        return f"Saved {path}"

    def list_files(self, directory):

        directory = Path(directory)

        if not directory.exists():
            return []

        return sorted(
            [
                str(x)
                for x in directory.iterdir()
                if x.is_file()
            ]
        )