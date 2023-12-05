#!/usr/bin/python3.11

class ActionBase:

    def __init__(self):
        self.application = None
        self.base_connection = None
        self.keyboard = None

    def set_application(self, application):
        self.application = application
        return self

    def get_application(self):
        return self.application

    def set_base_connection(self, base_connection):
        self.base_connection = base_connection
        return self

    def get_base_connection(self):
        return self.base_connection

    def set_keyboard(self, keyboard):
        self.keyboard = keyboard
        return self

    def get_keyboard(self):
        return self.keyboard

    @staticmethod
    def get_chat_id(update):
        return update.message.chat.id
