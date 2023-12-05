class InputError(Exception):

    def __init__(self, *args):
        if args:
            super().__init__(*args)

    def __str__(self):
        return f"Ты что-то не то ввёл: {self.args[0]}"


class IsNotInt(ValueError):

    def __init__(self, *args):
        if args:
            super.__init__(*args)

    def __str__(self):
        arg = self.args if self.args else "эту белиберду"
        return f"Цифру введи, а не {arg}"
