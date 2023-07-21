#!/usr/bin/python3.11

import mysql.connector
import json
import datetime
import telegram
import sys
from app import path


class Mysql:

    def __init__(self):
        print(sys.path)
        with open(f'{path.Path().get_root_path()}db_conn', 'r') as credentials:
            self.params = json.loads(credentials.read())
            self.connection = self.__connect()
            self.cursor = self.connection.cursor()

    def __connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.params['host'],
                user=self.params['user'],
                password=self.params['password'],
                database=self.params['database'],
                auth_plugin='mysql_native_password',
            )
            self.connection = connection
            return connection
        except Exception as e:
            print(f"Database connection error: {e}")

    def add_person_to_base(self, chat_info: telegram.Chat):
        ids_list = []
        date = datetime.datetime.now()
        if self.connection.is_closed():
            self.__connect()

        self.cursor.execute("""SELECT chat_id from person_info""")
        remembered_ids = self.cursor.fetchall()
        for chat_id in remembered_ids:
            ids_list.append(chat_id[0])

        if chat_info.id not in ids_list:
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
        else:
            print('User already exists')

    def find_one(self, condition: dict, select='*'):
        where = f"{list(condition.keys())[0]}='{list(condition.values())[0]}'"
        print(where)
        request = f"""SELECT {select} FROM person_info WHERE {where}"""
        try:
            self.cursor.execute(request)
            return self.cursor.fetchone()
        except Exception as e:
            print("Значение не найдено: ", e)

    def close(self):
        self.connection.close()
