from typing import Any, List, Optional
from pydantic import BaseModel, Field

class ExecuteRequest(BaseModel):
    goal: str = Field(..., min_length=1)

class ExecuteResponse(BaseModel):
    execution_id: str
    success: bool
    message: str
    answer: Optional[str] = None
    execution: Optional[dict[str, Any]] = None

class AgentStatus(BaseModel):
    name: str
    status: str
    runtime: Optional[float] = None

class ExecutionResponse(BaseModel):
    execution_id: str
    goal: str
    completed: bool
    agents: List[AgentStatus]
    final_answer: Optional[str] = None
    validation: Optional[str] = None
    report: Optional[str] = None

class UploadResponse(BaseModel):
    success: bool
    filename: str
    file_type: str
    message: str

class HealthResponse(BaseModel):
    status: str
    planner_model: str
    default_model: str

class MemoryItem(BaseModel):
    score: float
    memory: str

class MemoryResponse(BaseModel):
    memories: List[MemoryItem]

class AgentsResponse(BaseModel):
    agents: List[str]