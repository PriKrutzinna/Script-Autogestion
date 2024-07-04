"""Logger"""
from os.path import (isdir, join as path_join)
import logging
from datetime import datetime, UTC


class Logger():
    """This Logger persists the logs in a specific file for each execution of the process."""

    def __init__(self, logs_dir: str):
        if isdir(logs_dir):
            self.start_time = datetime.now(UTC)
            self.file_logger = logging
            logs_path = path_join(
                logs_dir,
                f'process_{self.start_time.strftime("%Y%m%d_%H.%M.%S")}.log',
            )
            self.file_logger.basicConfig(
                filename=logs_path,
                filemode="w",
                format="%(name)s - %(levelname)s - %(message)s",
                encoding="utf-8",
            )
        else:
            raise ValueError(
                "El parámetro logs_dir debe ser la ruta a un directorio/carpeta.")

    def __enter__(self):
        return self

    def log(self, level, message):
        self.file_logger.log(level, message)

    def debug(self, message):
        self.log(logging.DEBUG, message=message)

    def info(self, message):
        self.log(logging.INFO, message=message)

    def warning(self, message):
        self.log(logging.WARNING, message=message)

    def error(self, message):
        self.log(logging.ERROR, message=message)

    def critical(self, message):
        self.log(logging.CRITICAL, message=message)

