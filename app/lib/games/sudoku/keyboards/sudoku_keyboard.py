#!/usr/bin/python3.11

import json

from app import path
from app.base.keyboards import base_keyboard


class SudokuKeyboard(base_keyboard.BaseKeyboard):
    SUDOKU_BUTTONS_CONF = path.Path().get_app_path() + 'lib/games/sudoku/keyboards/buttons/sudoku.json'

    def __init__(self):
        base_keyboard.BaseKeyboard.__init__(self)
        with open(self.SUDOKU_BUTTONS_CONF, 'r') as sudoku:
            self.sudoku_buttons: dict = json.loads(sudoku.read())

    def get_sudoku_keyboard(self):
        return self.get_buttons_as_keyboard(self.sudoku_buttons)
