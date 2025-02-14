from __future__ import annotations

from pathlib import Path


class Dirs:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent

        self.src_dir = self.project_root / "src"
        self.data_dir = self.project_root / "data"
        self.logs_dir = self.project_root / "logs"
        self.config_dir = self.project_root / "config"

    def create_dirs(self):
        for directory in [self.src_dir, self.data_dir, self.logs_dir, self.config_dir]:
            directory.mkdir(parents=True, exist_ok=True)

