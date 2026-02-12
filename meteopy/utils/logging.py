from __future__ import annotations

import logging
from pathlib import Path


def get_logger(
    name: str,
    log_level: int | str = logging.INFO,
    log_file: Path = Path(__file__).resolve().parent.parent/"logs"/"meteopy.log"
) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    log_file.parent.mkdir(parents=True, exist_ok=True)

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )


        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)  # Set level for stream
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(logging.ERROR)  # Set level for file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
