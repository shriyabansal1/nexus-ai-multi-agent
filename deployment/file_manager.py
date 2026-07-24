from pathlib import Path
import shutil
from fastapi import UploadFile


class FileManager:
    """
    Handles uploaded files and remembers
    the latest uploaded files.
    """

    BASE_DIR = Path("data")

    PDF_DIR = BASE_DIR / "raw"
    CSV_DIR = BASE_DIR / "csv"
    DB_DIR = BASE_DIR / "db"

    LAST_PDF = None
    LAST_CSV = None
    LAST_DB = None

    @classmethod
    def create_directories(cls):
        cls.PDF_DIR.mkdir(parents=True, exist_ok=True)
        cls.CSV_DIR.mkdir(parents=True, exist_ok=True)
        cls.DB_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    async def save_pdf(cls, file: UploadFile):

        cls.create_directories()

        filename = Path(file.filename).name
        destination = cls.PDF_DIR / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        cls.LAST_PDF = destination

        return {
            "success": True,
            "filename": filename,
            "path": str(destination),
            "type": "pdf",
        }

    @classmethod
    async def save_csv(cls, file: UploadFile):

        cls.create_directories()

        filename = Path(file.filename).name
        destination = cls.CSV_DIR / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        cls.LAST_CSV = destination

        return {
            "success": True,
            "filename": filename,
            "path": str(destination),
            "type": "csv",
        }

    @classmethod
    async def save_database(cls, file: UploadFile):

        cls.create_directories()

        filename = Path(file.filename).name
        destination = cls.DB_DIR / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        cls.LAST_DB = destination

        return {
            "success": True,
            "filename": filename,
            "path": str(destination),
            "type": "database",
        }