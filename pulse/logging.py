import logging
from logging import Logger


def get_module_logger(mod_name) -> Logger:
    logger = logging.getLogger(mod_name)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(thread)d] %(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    return logger
