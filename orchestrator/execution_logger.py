# orchestrator/execution_logger.py

from __future__ import annotations

import logging
from pathlib import Path


class ExecutionLogger:
    """
    Centralized logger used across the NEXUS framework.

    Logs are written to both:
    - Console
    - Log file
    """

    def __init__(
        self,
        name: str = "NEXUS",
        log_dir: str = "logs",
        log_file: str = "execution.log",
        level: int = logging.INFO,
    ) -> None:

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Avoid duplicate handlers
        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(
            self.log_dir / log_file,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        """Logs a debug message."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Logs an info message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Logs an error message."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Logs a critical message."""
        self.logger.critical(message)

    def exception(self, message: str) -> None:
        """
        Logs an exception with traceback.
        Should be called inside an except block.
        """
        self.logger.exception(message)

    def agent_started(self, agent: str, task: str) -> None:
        """
        Logs the start of an agent.
        """
        self.info(f"[START] {agent} -> {task}")

    def agent_completed(self, agent: str, duration: float) -> None:
        """
        Logs successful completion of an agent.
        """
        self.info(f"[SUCCESS] {agent} completed in {duration:.2f}s")

    def agent_failed(self, agent: str, error: str) -> None:
        """
        Logs an agent failure.
        """
        self.error(f"[FAILED] {agent}: {error}")

    def execution_started(self, goal: str) -> None:
        """
        Logs the beginning of a workflow.
        """
        self.info("=" * 70)
        self.info(f"Execution Started")
        self.info(f"Goal : {goal}")
        self.info("=" * 70)

    def execution_completed(self, duration: float) -> None:
        """
        Logs successful completion of the workflow.
        """
        self.info("=" * 70)
        self.info(f"Execution Completed ({duration:.2f}s)")
        self.info("=" * 70)

    def execution_failed(self, error: str) -> None:
        """
        Logs workflow failure.
        """
        self.error("=" * 70)
        self.error("Execution Failed")
        self.error(error)
        self.error("=" * 70)