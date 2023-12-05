import telegram
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters

from app.handlers.commandHandlers import action_base
from app.handlers.commandHandlers import start_handler, hello_handler
from app.handlers.greeting_conversation_enum import GreetingConversation
from app.lib.conversation.greetings.greeting import Greeting


class BaseHandler:

    def __init__(self, application, base_connection):
        self.base_action = action_base.ActionBase()
        self.base_action.set_application(application).set_base_connection(base_connection)
        self.greeting = Greeting(self.base_action)
        self.command_handlers = []
        self.message_handlers = []
        self.conversation_handlers = []
        self.__set_command_handlers()
        self.__set_message_handlers()
        self.__set_conversation_handlers()
        self.handlers = self.command_handlers + self.message_handlers + self.conversation_handlers

    def __set_command_handlers(self):
        actions = [
            start_handler.StartHandler(self.base_action.application).actions(),
        ]
        for action in actions:
            for key, value in action.items():
                self.command_handlers.append(CommandHandler(key, value))

    def __set_message_handlers(self):
        pass

    def __set_conversation_handlers(self):
        entrypoints = [
            CommandHandler("hello", hello_handler.HelloHandler(self.base_action).actions()['hello'])
        ]
        states = self.greeting.make_states()
        fallbacks = [CommandHandler("cancel", self.greeting.cancel)]
        self.conversation_handlers.append(
            ConversationHandler(entrypoints, states, fallbacks, per_user=False)
        )

    def add_handler(self, handler):
        self.handlers.append(handler)

    @staticmethod
    def get_chat_id(update):
        return update.message.chat.id

    def get_handlers(self):
        return self.handlers
