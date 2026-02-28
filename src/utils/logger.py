from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self, log_dir: str = "logs", log_file: str = "game.log"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.log_dir / log_file

    def _write(self, level: str, message: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] [{level}] {message}\n"
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line)

    def info(self, message: str):
        self._write("INFO", message)

    def warn(self, message: str):
        self._write("WARN", message)

    def error(self, message: str):
        self._write("ERROR", message)