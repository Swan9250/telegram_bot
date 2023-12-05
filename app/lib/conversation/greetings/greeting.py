#!/usr/bin/python3.11

import telegram
from app.handlers.greeting_conversation_enum import GreetingConversation
from app.handlers.commandHandlers import action_base
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters, CommandHandler
from app.lib.conversation.auth.form import Form


class Greeting:

    def __init__(self, base_action: action_base.ActionBase):
        self.base_action = base_action
        self.application = self.base_action.application
        self.base_connection = self.base_action.base_connection

    async def need_form_pass(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        """
        Пытаемся понять, что кликнул пользователь
        """
        match update.message.text:
            case "Да":
                message = "Назови своё имя!"
                await self.application.bot.sendMessage(update.message.chat.id, message)
                return GreetingConversation.GET_NAME
            case _:
                """
                Если не хочет проходить опрос
                """

                message = "Ой, ну и ладно!"
                await self.application.bot.sendMessage(update.message.chat.id, message)
                return

    async def get_name(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        """
        Если хочет проходить опрос
        """

        Form.FORM_DICT["Имя"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови Фамилию!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_SURNAME

    async def get_surname(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Фамилия"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови Отчество!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_LAST_NAME

    async def get_last_name(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Отчество"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови дату рождения!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_BIRTH_DATE

    async def get_birth_date(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Дата рождения"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови город рождения!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_BIRTH_CITY

    async def get_birth_city(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Город рождения"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови цвет своих глаз!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_EYES_COLOR

    async def get_eyes_color(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Цвет глаз"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови цвет волос!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_HAIR_COLOR

    async def get_hair_color(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Цвет волос"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови любимый цветок!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_FAVORITE_FLOWER

    async def get_favorite_flower(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Любимый цветок"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови любимое животное!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_FAVORITE_PET

    async def get_favorite_pet(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Любимое животное"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови любимую книгу!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_FAVORITE_BOOK

    async def get_favorite_book(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Любимая книга"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови любимый фильм!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_FAVORITE_FILM

    async def get_favorite_film(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Любимый фильм"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови любимую песню!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_FAVORITE_SONG

    async def get_favorite_song(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Любимая песня"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови свои хобби(через запятую)!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_HOBBIES

    async def get_hobbies(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        hobbies = update.message.text
        if ',' in update.message.text:
            hobbies = update.message.text.split(',')
        Form.FORM_DICT["Хобби"] = hobbies
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови любимое время года!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_FAVORITE_SEASON

    async def get_favorite_season(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Любимое время года"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови твоё самое хорошее качество!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_BEST_QUALITY

    async def get_best_quality(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Твоё самое хорошее качество"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови твоё самое плохое качество!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_WORST_QUALITY

    async def get_worst_quality(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Твоё самое плохое качество"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови свою работу!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_WORK

    async def get_work(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Твоя работа"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь назови любимое блюдо!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_FAVORITE_MEAL

    async def get_favorite_meal(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Любимое блюдо"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. А теперь напиши, сколько зарабатываешь!"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return GreetingConversation.GET_SALARY

    async def get_salary(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        Form.FORM_DICT["Сколько зарабатываешь"] = update.message.text
        self.base_connection.add_to_user_context(self.base_action.get_chat_id(update), Form.FORM_DICT)
        message = "Записал. Теперь я знаю о тебе больше! Для дальнейшего общения ещё раз введи /hello"
        await self.application.bot.sendMessage(self.base_action.get_chat_id(update), message)
        return ConversationHandler.END

    @staticmethod
    async def cancel(update: telegram.Update, context: telegram.ext.CallbackContext):
        """
        Галя, у нас отмена!
        """
        return ConversationHandler.END

    def make_states(self) -> dict:

        states = {
            GreetingConversation.NEED_FORM_PASS: [
                MessageHandler(filters.Text(["Да", "Нет"]), self.need_form_pass)
            ],
            GreetingConversation.GET_NAME:            self.make_step(self.get_name),
            GreetingConversation.GET_SURNAME:         self.make_step(self.get_surname),
            GreetingConversation.GET_LAST_NAME:       self.make_step(self.get_last_name),
            GreetingConversation.GET_BIRTH_DATE:      self.make_step(self.get_birth_date),
            GreetingConversation.GET_BIRTH_CITY:      self.make_step(self.get_birth_city),
            GreetingConversation.GET_EYES_COLOR:      self.make_step(self.get_eyes_color),
            GreetingConversation.GET_HAIR_COLOR:      self.make_step(self.get_hair_color),
            GreetingConversation.GET_FAVORITE_FLOWER: self.make_step(self.get_favorite_flower),
            GreetingConversation.GET_FAVORITE_PET:    self.make_step(self.get_favorite_pet),
            GreetingConversation.GET_FAVORITE_BOOK:   self.make_step(self.get_favorite_book),
            GreetingConversation.GET_FAVORITE_FILM:   self.make_step(self.get_favorite_film),
            GreetingConversation.GET_FAVORITE_SONG:   self.make_step(self.get_favorite_song),
            GreetingConversation.GET_HOBBIES:         self.make_step(self.get_hobbies),
            GreetingConversation.GET_FAVORITE_SEASON: self.make_step(self.get_favorite_season),
            GreetingConversation.GET_BEST_QUALITY:    self.make_step(self.get_best_quality),
            GreetingConversation.GET_WORST_QUALITY:   self.make_step(self.get_worst_quality),
            GreetingConversation.GET_WORK:            self.make_step(self.get_work),
            GreetingConversation.GET_FAVORITE_MEAL:   self.make_step(self.get_favorite_meal),
            GreetingConversation.GET_SALARY:          self.make_step(self.get_salary),
        }
        return states

    @staticmethod
    def make_step(method):
        return [MessageHandler(filters.Regex('^[^/].+'), method)]
