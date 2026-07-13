"""
EDGE_ENGINE
Core Logger
"""

from datetime import datetime


class Logger:

    def info(self, message: str) -> None:
        self._write("INFO", message)

    def warning(self, message: str) -> None:
        self._write("WARNING", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def debug(self, message: str) -> None:
        self._write("DEBUG", message)

    def _write(self, level: str, message: str) -> None:

        timestamp = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{timestamp}] [{level}] {message}"
        )