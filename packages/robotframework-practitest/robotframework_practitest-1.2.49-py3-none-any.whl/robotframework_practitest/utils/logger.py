import io
import logging
import logging.handlers
import os
import os.path
import sys

_log_name = __name__.split('.')[0]

LOGGER = logging.getLogger(_log_name)

LOGGER_FORMAT = '[%(asctime)s][%(levelname)-8s : %(threadName)-15s][%(funcName)-20s ' \
                '-> %(filename)-20s::%(lineno)-03d] - %(message)s'


def set_logging(log_level='INFO', *handlers):
    log_level = logging.getLevelName('DEBUG' if log_level == 'TRACE' else log_level)
    global LOGGER
    LOGGER.setLevel(log_level)
    for h in handlers:
        LOGGER.addHandler(h)


def create_system_out_handler(stream: io = None) -> logging.Handler:
    handler = logging.StreamHandler(stream or sys.stdout)
    handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    return handler


def create_file_handler(path) -> logging.Handler:
    p, f = os.path.split(path)

    if not os.path.exists(p):
        os.mkdir(p)

    if os.path.isdir(path):
        path += '.log'

    if os.path.exists(path):
        os.remove(path)

    handler = logging.FileHandler(os.path.normpath(path))
    handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    return handler


def add_handler(handler: logging.Handler):
    global LOGGER
    LOGGER.addHandler(handler)


def set_level(level='INFO'):
    level = logging.getLevelName('DEBUG' if level == 'TRACE' else level)
    global LOGGER
    LOGGER.setLevel(level)


logger = LOGGER


__all__ = [
    'logger',
    'create_file_handler',
    'create_system_out_handler',
    'add_handler',
    'set_level',
]


