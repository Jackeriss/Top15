"""
log handler
"""
import os
import logging

from config import ROOT_PATH

class Logger(object):
    def __init__(self, log_name, log_file=None, log_format=None, log_level=None):
        self._log_name = log_name
        self._log_file = log_file
        self._log_format = log_format
        self._log_level = log_level
        if not self._log_file:
            self._log_file = os.path.join(ROOT_PATH,
                                          'logs',
                                          self._log_name + '.log')
        if not self._log_format:
            self._log_format = '[%(asctime)s] $%(levelname)s (%(filename)s:%(lineno)d) %(message)s'
        if not self._log_level:
            self._log_level = logging.INFO
        self._logger = logging.getLogger(self._log_name)
        handler = logging.FileHandler(self._log_file)
        formatter = logging.Formatter(self._log_format)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(self._log_level)

    def log(self, msg):
        if self._logger is not None:
            self._logger.log(self._log_level, msg)

    def get_logger(self):
        return self._logger


class LogFilter(logging.Filter):
    """
    Filters (lets through) all messages with level < LEVEL
    """
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level
