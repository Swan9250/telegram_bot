class MainMenu:
    @staticmethod
    def show_levels():
        print("""
            1 - Легко\n
            2 - Средне\n
            3 - Сложно\n
            0 - Выход\n
        """)

    @staticmethod
    def choose_level() -> str:
        return "Выбери уровень: "

    @staticmethod
    def show_birth():
        print("""
        1 - Сгенерировать новый уровень\n
        2 - Взять готовый из базы\n
        0 - Вернуться к выбору уровня\n
        """)

    @staticmethod
    def choose_birth() -> str:
        return "Выбери, откуда взять игру: "

    @staticmethod
    def show_info(author: str, version: str):
        return f"""Автор: {author}
Версия игры: {version}
"""


class Table:

    def show(lines):
        print("╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗")
        for line in lines:
            print("║", " │ ".join(str(i) for i in line[:3]), "║", " │ ".join(str(i) for i in line[3:6]), "║",
                  " │ ".join(str(i) for i in line[6:]), "║")
            if (lines.index(line) + 1) % 3 == 0 and (lines.index(line) + 1) != 9:
                print("╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣")
            elif (lines.index(line) + 1) != 9:
                print("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢")
        print("╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝")
