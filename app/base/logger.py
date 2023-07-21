#!/usr/bin/python3.11

import logging
from logging.handlers import RotatingFileHandler


class Logger:
    LOG_PATH = '/root/projects/telegram_bot/app/base/logs/'

    def __init__(self, name, level):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handler = RotatingFileHandler(f"{self.LOG_PATH}{name}.log", maxBytes=2000, backupCount=10)
        self.formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def get_logger(self):
        return self.logger
