from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from deployment.schemas import (
    ExecuteRequest,
    ExecuteResponse,
    UploadResponse,
    HealthResponse,
)
from deployment.services import service
from deployment.file_manager import FileManager

app = FastAPI(
    title="NEXUS AI",
    version="1.0.0",
    description="Multi-Agent AI System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/execute")
async def execute(request: ExecuteRequest):
    import traceback
    try:
        execution_id, answer, execution = await service.execute(request.goal)
        return {
            "execution_id": execution_id,
            "success": True,
            "answer": answer,
            "execution": execution,
        }
    except Exception:
        traceback.print_exc()
        raise

@app.post("/upload/pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )
    result = await FileManager.save_pdf(file)
    return UploadResponse(
        success=True,
        filename=result["filename"],
        file_type="pdf",
        message="PDF uploaded successfully.",
    )

@app.post("/upload/csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed.",
        )
    result = await FileManager.save_csv(file)
    return UploadResponse(
        success=True,
        filename=result["filename"],
        file_type="csv",
        message="CSV uploaded successfully.",
    )

@app.post("/upload/db", response_model=UploadResponse)
async def upload_database(file: UploadFile = File(...)):
    if not (
        file.filename.endswith(".db")
        or file.filename.endswith(".sqlite")
        or file.filename.endswith(".sqlite3")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only SQLite databases are supported.",
        )
    result = await FileManager.save_database(file)
    return UploadResponse(
        success=True,
        filename=result["filename"],
        file_type="database",
        message="Database uploaded successfully.",
    )

@app.get("/history")
def history():
    return service.get_history()

@app.get("/execution/{execution_id}")
def execution(execution_id: str):
    execution = service.get_execution(execution_id)
    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found.",
        )
    return execution

@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        planner_model="Qwen3",
        default_model="Phi-3",
    )