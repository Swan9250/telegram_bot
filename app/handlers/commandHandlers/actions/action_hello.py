#!/usr/bin/python3.11

import random
import telegram
from app.handlers.commandHandlers import action_base
from app.lib.conversation.auth.model_enum import Model
from app.base.keyboards.base_keyboard import BaseKeyboard
from app.lib.conversation.auth.form import Form
from telegram.ext import CallbackContext
# from base.keyboards import base_keyboard
from app.lib.conversation.auth import auth
from app.handlers.base_conversation_handler import BaseConversationHandler
from app.handlers.greeting_conversation_enum import GreetingConversation
from app.lib.conversation.greetings.forMen.greetings import greeting_list


class ActionHello(action_base.ActionBase):

    def __init__(self, base_action: action_base.ActionBase):
        super().__init__()
        self.application = base_action.get_application()
        self.base_connection = base_action.get_base_connection()
        # self.keyboard = [
        #     base_keyboard.get_buttons_as_keyboard()
        # ]

    async def run(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        """
        Православное приветствие.
        """

        context.bot_data["base_connection"] = self.base_connection
        model = auth.Auth(update, context).get_behavior_model()
        match model:
            case Model.NEWBIE:
                buttons = BaseKeyboard().get_buttons_as_keyboard(BaseKeyboard().get_yes_no_buttons())
                greeting = f'Здравствуй, @{update.effective_user.username}! Хочешь пройти мини-опрос перед началом?'
                # await update.message.reply_text(greeting)
                await self.application.bot.sendMessage(self.get_chat_id(update),
                                                       greeting,
                                                       reply_markup=buttons)
                return GreetingConversation.NEED_FORM_PASS
            case Model.EXPERIENCED:
                buttons = BaseKeyboard().get_buttons_as_keyboard(BaseKeyboard().get_form_edit_button())
                greeting = f'Здравствуй, @{update.effective_user.username}! Что хочешь сделать?'
                await self.application.bot.sendMessage(self.get_chat_id(update), greeting, reply_markup=buttons)
            case Model.OWNER:
                buttons = BaseKeyboard().get_buttons_as_keyboard(BaseKeyboard().get_form_edit_button())
                greeting_number = random.randrange(1, len(greeting_list) - 1)
                greeting = greeting_list[greeting_number]
                await self.application.bot.sendMessage(self.get_chat_id(update), greeting, reply_markup=buttons)
            case _:
                print("Cannot choose behavior model")

        return

        # await self.application.bot.sendMessage(self.get_chat_id(update), greeting)

        # if update.message.chat.username == "Swan9250":
        #     # context.user_data["keyboards"] = self.keyboard_format(
        #     #     bt.keyboardNotify(),
        #     #     bt.keyboardKicker(),
        #     #     self.keyboard.get_sudoku_buttons().get("Title")
        #     # )
        #     # await self.application.bot.sendMessage(self.get_chat_id(update), hello,
        #     #                                        reply_markup=context.user_data["keyboards"],
        #     #                                        reply_to_message_id=update.message.message_id)
        #     await self.application.bot.sendMessage(self.get_chat_id(update), model.greeting)
        # elif update.message.chat.title == 'Доминирование':
        #     context.user_data["keyboards"] = self.keyboard_format(bt.keyboardKicker(), bt.keyboardNotify())
        #     await self.application.bot.sendMessage(self.get_chat_id(update), hello,
        #                                            reply_markup=context.user_data["keyboards"],
        #                                            reply_to_message_id=update.message.message_id)
        # elif update.message.chat.title == 'Че кого':
        #     context.user_data["keyboards"] = self.keyboard_format(bt.keyboardNotify())
        #     await self.application.bot.sendMessage(self.get_chat_id(update), hello,
        #                                            reply_markup=context.user_data["keyboards"],
        #                                            reply_to_message_id=update.message.message_id)
        # else:
        #     #            print(update.message)
        #     await self.application.bot.sendMessage(self.get_chat_id(update), hello,
        #                                            reply_to_message_id=update.message.message_id)
