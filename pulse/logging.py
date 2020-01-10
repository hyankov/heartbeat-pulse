# System imports
import logging
from logging import Logger

# Local imports
from .config import Config


def get_module_logger(mod_name) -> Logger:
    logger = logging.getLogger(mod_name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(Config.load('logging', 'format'))
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(Config.load('logging', 'level'))
        logger.propagate = False

    return logger
