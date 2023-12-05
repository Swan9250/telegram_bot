import random
import copy
from . import enums
from . import errors
from . import default_objects as do


class TableModel:
    TRIES: int = 2
    DEFAULT_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    choice: int
    place: int
    current_table: list = []
    columns = do.default_columns
    raws = do.default_raws
    squares = do.default_squares

    def set_level(self, choice: int):
        match choice:
            case enums.Level.EASY | enums.Level.MEDIUM | enums.Level.HARD:
                self.choice = choice
            case _:
                raise errors.InputError(choice)

    def set_place(self, place: int):
        match place:
            case enums.Place.BASE | enums.Place.GENERATE:
                self.place = place
            case _:
                raise errors.InputError(place)

    def generate(self):
        tries = 0
        while len(self.current_table) < 9 or tries < self.TRIES:
            line = self.generate_line(len(self.current_table))
            self.current_table.append(line)
            print("result_table:", self.current_table)
            tries += 1

        # while None in self.current_table:
        #     self.retry_generate()
        return copy.deepcopy(self.current_table)

    def generate_line(self, raw_index):
        line = []
        try:
            for column_index in range(9):
                num = self.get_number(raw_index, column_index)
                line.append(num)
            return line
        except TypeError as e:
            print(e)

    def retry_generate(self):
        self.current_table = []
        self.reset_defaults()
        self.generate()

    def get_number(self, raw_index, column_index):
        if raw_index == 9:
            print("RAW_INDEX = 9")
            return
        square_index = Square.get_square_index(raw_index, column_index)
        accept_raw = self.raws.get(raw_index)
        accept_column = self.columns.get(column_index)
        accept_square = self.squares.get(square_index)
        try:
            accept_numbers = list(set(accept_raw) & set(accept_column) & set(accept_square))
            num = random.choice(accept_numbers)
            raw_pop = accept_raw.pop(accept_raw.index(num))
            column_pop = accept_column.pop(accept_column.index(num))
            square_pop = accept_square.pop(accept_square.index(num))
            return num
        except IndexError as e:
            print("INDEX_ERROR!")
            if 'raw_pop' in locals():
                accept_raw.append(raw_pop)
            if 'column_pop' in locals():
                accept_column.append(column_pop)
            if 'square_pop' in locals():
                accept_square.append(square_pop)
            self.raws.update({raw_index: accept_raw})
            self.columns.update({column_index: accept_column})
            self.squares.update({square_index: accept_square})

    def reset_defaults(self):
        for i in range(9):
            self.raws.update({i: self.DEFAULT_NUMBERS.copy()})
            self.columns.update({i: self.DEFAULT_NUMBERS.copy()})
            self.squares.update({i: self.DEFAULT_NUMBERS.copy()})


class Square:

    @staticmethod
    def get_square_index(raw_index, column_index):
        if raw_index < 3 and column_index < 3:
            return 0
        elif raw_index < 3 and column_index < 6:
            return 1
        elif raw_index < 3 and column_index < 9:
            return 2
        elif raw_index < 6 and column_index < 3:
            return 3
        elif raw_index < 6 and column_index < 6:
            return 4
        elif raw_index < 6 and column_index < 9:
            return 5
        elif raw_index < 9 and column_index < 3:
            return 6
        elif raw_index < 9 and column_index < 6:
            return 7
        elif raw_index < 9 and column_index < 9:
            return 8
