import random
import default_objects as do

all_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
lines = []


def reset_defaults():
    default_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        do.default_raws.update({i: default_nums.copy()})
        do.default_columns.update({i: default_nums.copy()})
        do.default_squares.update({i: default_nums.copy()})

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


def generate_line_from_defaults(raw, raw_index, column_index, columns, raws, squares):
    if raw_index == 9:
        print("RAW_INDEX = 9")
        return
    try:
        square_index = get_square_index(raw_index, column_index)
        print("raw_index: ", raw_index, "column_index: ", column_index, "square_index: ", square_index)
        accept_raw = raws.get(raw_index)
        accept_column = columns.get(column_index)
        accept_square = squares.get(square_index)
        print("accept_raw: ", accept_raw, "accept_column: ", accept_column, "accept_square: ", accept_square)
        accept_numbers = list(set(accept_raw) & set(accept_column) & set(accept_square))
        print("accept_numbers:", accept_numbers)
        num = random.choice(accept_numbers)
        print(accept_column, accept_raw)
        raw_pop = accept_raw.pop(accept_raw.index(num))
        print(accept_column, accept_raw)
        column_pop = accept_column.pop(accept_column.index(num))
        square_pop = accept_square.pop(accept_square.index(num))
        print("result_num:", num)
        return num, columns, raws, squares
    except IndexError as e:
        print("INDEX_ERROR!")
        if 'raw_pop' in locals():
            accept_raw.append(raw_pop)
        if 'column_pop' in locals():
            accept_column(column_pop)
        if 'square_pop' in locals():
            accept_square(square_pop)
        do.default_raws.update({raw_index: accept_raw})
        do.default_columns.update({column_index: accept_column})
        do.default_squares.update({square_index: accept_square})



def generate_table(raw, raw_index):
    line = []
    print("do.default_columns", do.default_columns)
    columns = do.default_columns
    raws = do.default_raws
    squares = do.default_squares
    try:
        for column_index in range(9):
            num, columns, raws, squares = generate_line_from_defaults(raw, raw_index, column_index, columns, raws, squares)
            line.append(num)
            print("new_line:", line)
        return line
    except TypeError:
        random.shuffle(raw)
        print("TYPE_ERROR:", raw)


def gen_tab():
    tries = 0
    while len(lines) < 9 or tries < 2:
        if len(lines) == 0:
            random.shuffle(all_nums)
        print("all_nums", all_nums)
        line = generate_table(all_nums, len(lines))
        lines.append(line)
        print("result_table:", lines)
        tries += 1

gen_tab()

while None in lines:
    lines = []
    reset_defaults()
    gen_tab()
