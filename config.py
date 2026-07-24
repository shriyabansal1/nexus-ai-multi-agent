import os
from dataclasses import dataclass

@dataclass
class LLMConfig:
    base_url: str = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )
    default_model: str = os.getenv(
        "NEXUS_MODEL",
        "phi3:mini"
    )
    planner_model: str = os.getenv(
        "NEXUS_PLANNER_MODEL",
        "qwen3:1.7b"
    )
    timeout: int = 1000
    retries: int = 2
    temperature: float = 0.2

@dataclass
class AgentConfig:
    memory_window: int = 10
    max_react_iterations: int = 5
    max_validation_retries: int = 2
    enable_reflection: bool = True
    max_parallel_workers: int = 4

@dataclass
class MemoryConfig:
    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_dimension: int = 384
    faiss_index_path: str = "memory/store/faiss.index"
    metadata_path: str = "memory/store/meta.jsonl"
    sqlite_path: str = "company.db"

@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

@dataclass
class ToolConfig:
    python_timeout: int = 10
    sandbox_directory: str = "tools/sandbox"
    allow_shell: bool = False

@dataclass
class LoggingConfig:
    level: str = "INFO"
    log_directory: str = "logs"
    save_conversations: bool = True
    enable_tracing: bool = True

@dataclass
class Settings:
    llm: LLMConfig
    agent: AgentConfig
    memory: MemoryConfig
    server: ServerConfig
    tools: ToolConfig
    logging: LoggingConfig
settings = Settings(
    llm=LLMConfig(),
    agent=AgentConfig(),
    memory=MemoryConfig(),
    server=ServerConfig(),
    tools=ToolConfig(),
    logging=LoggingConfig(),
)