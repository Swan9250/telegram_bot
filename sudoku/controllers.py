from . import models
from . import errors
import sys
from . import enums


class TableController:
    SET_PARAMS_NOT_SUCCESS: int = 1

    def __init__(self):
        self.table = models.TableModel()

    def get_start_parameters(self, level, place=None):
        try:
            level = int(level)
            if level == enums.Level.EXIT:
                sys.exit(0)
            self.table.set_level(level)
            if place is not None:
                place = int(place)
                if place == enums.Place.RETURN:
                    return self.SET_PARAMS_NOT_SUCCESS
                self.table.set_place(place)
        except ValueError:
            print(errors.IsNotInt())
            return self.SET_PARAMS_NOT_SUCCESS
        except errors.InputError as e:
            print(e)
            return self.SET_PARAMS_NOT_SUCCESS

    def create(self):
        """В зависимости от уровня генерируем таблицу и показываем её."""
        match self.table.place:
            case enums.Place.BASE:
                print("Когда-нибудь будет")
            case enums.Place.GENERATE:
                print(self.table.generate())


#        self.refactor_by_level(self.generate_table(), level)

# def make_easy_table(self, level):
#     """Генерация таблицы для лёгкой игры. Убираем 3 значения из каждой строки."""
#     easy_table = self.refactor_by_level(self.generate_table(), level)
#     return easy_table
#
# def make_medium_table(self, level):
#     """Генерация таблицы для средней по сложности игры. Убираем 4 значения из каждой строки."""
#     medium_table = self.refactor_by_level(self.generate_table(), level)
#     return medium_table
#
# def make_hard_table(self, level):
#     "Генерация таблицы для сложной игры. Убираем 5 значений из каждой строки."
#     hard_table = self.refactor_by_level(self.generate_table(), level)
#     return hard_table
#
# def refactor_by_level(self, table, level):
#     if level == 1:
#         for line in table:
#             tries = 0
#             while tries < 4:
#                 hide_num = random.choice(line)
#                 num_index = line.index(hide_num)
#                 line.pop(num_index)
#                 line.insert(num_index, " ")
#                 tries += 1
#     elif level == 2:
#         pass
#     elif level == 3:
#         pass
#     return table
#
# def check(self, table, iter):
#     if iter >= 3:
#         print("Fail")
#         return
#     suc_col = self.check_columns(table)
#     # self.check_square()
#     if suc_col != True:
#         iter += 1
#         self.make_easy_table(iter, suc_col)
#
# def check_columns(self, table):
#     column = []
#     for i in range(10):
#         for line in table:
#             column.append(line[i])
#         err = [x for j, x in enumerate(column) if j != column.index(x)]
#         print(i, err, column)
#         if len(err) != 0:
#             return i
#         else:
#             return True


class CreateTable:

    def create_table(level):
        """В зависимости от уровня генерируем таблицу и показываем её."""
        if level == 1:
            table = self.make_easy_table(level)
        elif level == 2:
            table = self.make_medium_table(level)
        elif level == 3:
            table = self.make_hard_table(level)
        views.Table.show(table)
        views.Table.show(self.current_table)
