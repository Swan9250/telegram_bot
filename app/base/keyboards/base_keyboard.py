#!/usr/bin/python3.11

import json
import telegram as tg

from app.path import Path


class BaseKeyboard:
    MAIN_BUTTONS_CONF = Path().get_app_path() + 'base/keyboards/buttons/main.json'
    YES_NO_BUTTONS_CONF = Path().get_app_path() + 'base/keyboards/buttons/yes_no.json'
    FORM_EDIT_BUTTON = Path().get_app_path() + 'base/keyboards/buttons/form.json'

    def __init__(self):
        with open(self.MAIN_BUTTONS_CONF, 'r') as main:
            self.main_buttons = json.loads(main.read())
        with open(self.YES_NO_BUTTONS_CONF, 'r') as yes_no:
            self.yes_no_buttons = json.loads(yes_no.read())
        with open(self.FORM_EDIT_BUTTON, 'r') as form:
            self.form_edit_button = json.loads(form.read())

    def get_main_buttons(self):
        return self.main_buttons

    def get_yes_no_buttons(self):
        return self.yes_no_buttons

    def get_form_edit_button(self):
        return self.form_edit_button

    def get_buttons_as_keyboard(self, buttons: dict):
        list_buttons = self.get_buttons_as_list(buttons)
        keyboard_buttons = []
        for button in list_buttons:
            keyboard_buttons.append(tg.KeyboardButton(button))
        return tg.ReplyKeyboardMarkup([keyboard_buttons], one_time_keyboard=True, resize_keyboard=True,
                                      selective=True)
        # return keyboard_buttons

    @staticmethod
    def get_buttons_as_list(buttons: dict):
        return list(buttons.values())
