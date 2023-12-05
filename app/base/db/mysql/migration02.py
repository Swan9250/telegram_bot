import database  # Класс для подключения к базе
import argparse  # Модуль для работы с аргументами консоли
from app.path import Path
import json


class Migration02:  # Тренирую в питоне технологии yii2

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
            ALTER TABLE person_info
            ADD user_context TEXT
            """
        )  # Добавляем столбец user_context к person_info

    def down(self):  # Возвращаем, как было до up
        self.cursor.execute(
            """
                ALTER TABLE person_info
                DROP COLUMN IF EXISTS user_context
            """
        )  # Удаление столбца user_context

    @staticmethod
    def parse_args():
        parser_obj = argparse.ArgumentParser()  # Создаëм объект парсера
        group = parser_obj.add_mutually_exclusive_group(required=True)  # Группа взаимоисключаемых аргументов
        group.add_argument('up',
                           nargs='?')  # Добавляем аргумент up в группу. Второй параметр показывает, что количество аргументов для up не определено (а то бы ожидался хотя бы один)
        group.add_argument('down', nargs='?')  # Добавляем аргумент down в группу
        return parser_obj.parse_args()  # Парсим аргументы, согласно заданным выше правилам


connection = Migration02()  # Создаëм объект миграции
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
