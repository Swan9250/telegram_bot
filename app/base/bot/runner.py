#!/usr/bin/python3.11

from app.handlers import base_handler
from app.base.db.mysql import database
from telegram.ext import ApplicationBuilder


class Runner:

    def __init__(self, token, db_params):
        self.token = token
        self.db_params = db_params
        self.application = None
        self.base_connection = None

    def run(self):
        self.application = ApplicationBuilder().token(self.token).build()               # собираем приложение
        self.application.builder().get_updates_http_version('1.1').http_version('1.1')  # указываем, что будем
                                                                                        # работать с http/1.1
        self.application.builder().concurrent_updates(False)
        self.base_connection = database.Mysql(self.db_params)                           # подключаемся к базе данных
        self.application.add_handlers(
            base_handler.BaseHandler(self.application, self.base_connection).get_handlers()
        )                                                                               # добавляем обработчики команд
        self.application.run_polling()                                                  # начинаем слушать запросы


