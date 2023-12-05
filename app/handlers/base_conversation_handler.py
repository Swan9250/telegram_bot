from telegram.ext import ConversationHandler


class BaseConversationHandler:

    def __init__(self):
        pass

    @staticmethod
    def make_conversation_handler(entrypoints: list, states: dict, fallbacks: list):
        return ConversationHandler(entrypoints, states, fallbacks)
