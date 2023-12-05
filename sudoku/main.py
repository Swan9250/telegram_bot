import os
from . import controllers, views
from . import errors
#import views

author: str = "Vladimir Stanotin"
version: str = "0.1.0"


class Sudoku:

    def __init__(self):
        self.table = controllers.TableController()

    def run(self):
        """Запускаем бесконечный цикл с меню."""
        while True:
            result = self.set_start_parameters()
            if result == 1:
                continue
            self.table.create()
            self.process()

    def set_start_parameters(self):
        views.MainMenu.show_levels()
        level = input(views.MainMenu.choose_level())
        result = self.table.get_start_parameters(level)
        if result == 1:
            return 1
        views.MainMenu.show_birth()
        place = input(views.MainMenu.choose_birth())
        return self.table.get_start_parameters(level, place)

    def process(self):
        pass

    @staticmethod
    def info():
        return views.MainMenu.show_info(author, version)


if __name__ == "__main__":
    game = Sudoku()
    game.run()
