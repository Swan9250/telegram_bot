#!/usr/bin/python3.11

import database  # Класс для подключения к базе
import argparse  # Модуль для работы с аргументами консоли
import json
from app.path import Path


class Migration01:  # Тренирую в питоне технологии yii2

    def __init__(self):
        self.params = None
        with open(Path().get_db_path(), 'r') as mysql_config:
            self.params = json.loads(mysql_config.read())
        db = database.Mysql(self.params)  # Создаëм объект Mysql
        self.connect = db.connection  # Подключаемся к базе
        self.cursor = db.cursor  # Инициализируем объект для операций с базой
        self.args = self.parse_args()  # Получаем аргументы из консоли

    def up(self):  # Видоизменяем базу
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS person_info(
            chat_id INT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            type VARCHAR(30),
            username VARCHAR(255),
            date DATETIME,
            title VARCHAR(255))
            """
        )  # Создание таблицы person_info

    def down(self):  # Возвращаем, как было до up
        self.cursor.execute(
            """
                DROP TABLE IF EXISTS person_info
            """
        )  # Удаление person_info

    @staticmethod
    def parse_args():
        parser_obj = argparse.ArgumentParser()  # Создаëм объект парсера
        group = parser_obj.add_mutually_exclusive_group(required=True)  # Группа взаимоисключаемых аргументов
        group.add_argument('up',
                           nargs='?')  # Добавляем аргумент up в группу. Второй параметр показывает, что количество аргументов для up не определено (а то бы ожидался хотя бы один)
        group.add_argument('down', nargs='?')  # Добавляем аргумент down в группу
        return parser_obj.parse_args()  # Парсим аргументы, согласно заданным выше правилам


connection = Migration01()  # Создаëм объект миграции
try:
    if connection.args.up:
        connection.up()
        print("Up query execution succeeded")
    elif connection.args.down:  # elif здесь потому, что мало ли что я там ввëл, и как argparse на это отреагировал
        connection.down()
        print("Down query execution succeeded")
except Exception as e:  # Вообще так не рекомендуется писать
    print(f"Query error execution: {e}\n")
    rollback = input("Need rollback?")  # Это, когда down ещë был не написан. Надо переделать.
    if rollback in ('Y', 'y'):
        print('Rollback')
        connection.down()
