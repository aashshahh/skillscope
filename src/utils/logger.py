import sys
from loguru import logger
from src.utils.config import load_settings


def setup_logger():
    settings = load_settings()
    log_cfg = settings.get("logging", {})
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_cfg.get("level", "INFO"),
        format=log_cfg.get("format", "{time} | {level} | {message}"),
        colorize=True,
    )
    return logger