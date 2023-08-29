import logging
import os
import sys
from pathlib import Path
from typing import Dict, Optional

from colorama import Back, Fore, Style

from src.config import LOG_DIR, LOG_LEVEL_CONSOLE, LOG_LEVEL_FILE


class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""

    def __init__(
        self, *args, colors: Optional[Dict[str, str]] = None, **kwargs
    ) -> None:
        """Initialize the formatter with specified format strings."""

        super().__init__(*args, **kwargs)

        self.colors = colors if colors else {}

    def format(self, record) -> str:
        """Format the specified record as text."""

        record.color = self.colors.get(record.levelname, "")
        record.reset = Style.RESET_ALL

        return super().format(record)


def create_file_if_not_exists(path):
    dir = os.path.dirname(path)
    Path(dir).mkdir(parents=True, exist_ok=True)
    Path(path).touch(exist_ok=True)


def get_logger(name, prefix: str = ""):
    formatter = ColoredFormatter(
        f"{{color}} {{asctime}} | {{levelname:8}} | {{funcName}}:{{lineno}} | {prefix}{{message}} {{reset}}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        colors={
            "DEBUG": Fore.CYAN,
            "INFO": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
        },
    )

    # stream = codecs.StreamWriter(sys.stdout)
    # stream.encode = lambda msg, errors="strict": (msg.encode(locale.getpreferredencoding(False), errors).decode(), msg)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(getattr(logging, LOG_LEVEL_CONSOLE))

    # dirname = os.path.dirname(__file__)
    # logs_path = os.path.join(dirname, '../bot_logs/bot.log')
    # logs_path = os.path.normpath(logs_path)
    logs_path = f"./{LOG_DIR}/log.txt"

    create_file_if_not_exists(logs_path)
    file_handler = logging.FileHandler(logs_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, LOG_LEVEL_FILE))

    logger = logging.getLogger(name)

    logger.handlers[:] = []
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    return logger
