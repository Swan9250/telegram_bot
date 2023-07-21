#!/usr/bin/python3.11

import database
import argparse


class Migration01:

    def __init__(self):
        db = database.Mysql()
        self.connect = db.connection
        self.cursor = db.cursor
        self.args = self.parse_args()

    def up(self):
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
        )

    def down(self):
        self.cursor.execute(
            """
                DROP TABLE IF EXISTS person_info
            """
        )

    @staticmethod
    def parse_args():
        parser_obj = argparse.ArgumentParser()
        group = parser_obj.add_mutually_exclusive_group(required=True)
        group.add_argument('up', action='store_true')
        group.add_argument('down', action='store_true')
        return parser_obj.parse_args()


connection = Migration01()
try:
    if connection.args.up:
        connection.up()
        print("Up query execution succeeded")
    elif connection.args.down:
        connection.down()
        print("Down query execution succeeded")
except Exception as e:
    print(f"Query error execution: {e}\n")
    rollback = input("Need rollback?")
    if rollback in ('Y', 'y'):
        print('Rollback')
        connection.down()
