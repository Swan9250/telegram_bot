#!/usr/bin/python3.11

import mysql.connector  # Для подключения к мускулю
import json  # Для работы с json
import datetime  # Для работы со временем
import telegram  # Для работы с телеграмом
import sys  # Для работы с системой
from app.path import Path  # Модуль, в котором пути


class Mysql:

    def __init__(self, params):
        self.params = params  # Читаем данные
        self.connection = self.__connect()  # Создаëм подключение
        self.cursor = self.connection.cursor()  # Создаëм оператор sql

    def __connect(self):
        try:  # Пытаемся подключиться с имеющимися данными
            connection = mysql.connector.connect(
                host=self.params['host'],
                user=self.params['user'],
                password=self.params['password'],
                database=self.params['database'],
                auth_plugin='mysql_native_password',
            )
            return connection
        except Exception as e:  # Желательно указывать конкретные Exception
            print(f"Database connection error: {e}")

    def add_person_to_base(self, chat_info: telegram.Chat):
        ids_list = []
        date = datetime.datetime.now()  # Запоминаем текущее время
        if self.connection.is_closed():  # Проверяем, вдруг соединение закрыто - переоткрываем.
            self.__connect()
            print('reconnected')

        self.cursor.execute("""SELECT chat_id from person_info""")  # Получаем все айдишники
        remembered_ids = self.cursor.fetchall()  # Извлекаем ответ из курсора
        for chat_id in remembered_ids:  # Получаем прям именно айдишник
            ids_list.append(chat_id[0])

        if chat_info.id not in ids_list:  # Проверка на наличие нашего айди в списке, если нет - добавляем
            try:
                self.cursor.execute(
                    """
                    INSERT INTO person_info(
                    chat_id,
                    first_name,
                    last_name,
                    type,
                    username,
                    date,
                    title)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        chat_info.id,
                        chat_info.first_name,
                        chat_info.last_name,
                        chat_info.type,
                        chat_info.username,
                        date,
                        chat_info.title
                    )
                )
                self.connection.commit()
            except Exception as e:
                print(f"Insert error: {e}")
        else:  # Если такой айди уже есть
            print('User already exists')

    def find_one(self, condition: dict, select='*', table="person_info"):  # Попытка сделать, как в квериках у yii2
        where = f"{list(condition.keys())[0]}='{list(condition.values())[0]}'"  # Так себе костыль для поиска первого значения
        print(where)
        request = f"""SELECT {select} FROM {table} WHERE {where}"""  # Собираем запрос
        try:
            self.cursor.execute(request)
            return self.cursor.fetchone()  # Получаем первый подходящий ответ
        except Exception as e:
            print("Значение не найдено: ", e)

    def add_to_user_context(self, user_id: int, data: dict):
        where = f"chat_id={user_id}"
        request = f"""SELECT user_context FROM person_info WHERE {where}"""
        self.cursor.execute(request)
        context = self.cursor.fetchone()  # return tuple
        if context[0] is not None:
            extra = json.loads(context[0].replace("'", '"'))
            print(extra)
            extra.update(data)
            print(extra, "extra2")
        else:
            extra = data
        update = f"""UPDATE person_info SET user_context="{extra}" WHERE {where}"""
        self.cursor.execute(update)
        self.connection.commit()

    def close(self):  # Закрываем соединение
        self.connection.close()
