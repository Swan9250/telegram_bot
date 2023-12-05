#!/usr/bin/python3.11

import logging
from logging.handlers import RotatingFileHandler


class Logger:
    LOG_PATH = '/root/projects/telegram_bot/app/base/logs/' # При запуске из другого файла к относительному пути добавляется путь до того файла. Поэтому, используем абсолютный.

    def __init__(self, name, level):
        self.logger = logging.getLogger(name) # Имя файла
        self.logger.setLevel(level) # Устанавливаем уровень отображения ошибок
        self.handler = RotatingFileHandler(f"{self.LOG_PATH}{name}.log", maxBytes=2000, backupCount=10) # Обрабатывает файл с логами по указанному пути, с указанным размером и максимальным количеством файлов.
        self.formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s") # Формат записи в лог. Время, имя файла, уровень ошибки, сообщение.
        self.handler.setFormatter(self.formatter) # Применяем форматтер к обработчику
        self.logger.addHandler(self.handler) # Добавляем обработчик к главному логгеру

    def get_logger(self):
        return self.logger # Чтоб один и тот же использовать
