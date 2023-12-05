#!/usr/bin/python3.11

import telegram
from app.handlers.commandHandlers import action_base
from telegram.ext import CallbackContext


class ActionStart(action_base.ActionBase):

    def __init__(self, base_action: action_base.ActionBase):
        self.application = base_action.get_application()

    async def run(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        """
        Обрабатываем стандартный запуск бота.
        """
        start = f'Ты обратился к боту, но сделал это без уважения, введи /hello'
        photo = 'https://i.ytimg.com/vi/q8ADpnunCGo/hqdefault.jpg'
        await self.application.bot.sendMessage(self.get_chat_id(update), start)
        await self.application.bot.sendPhoto(self.get_chat_id(update), photo)
