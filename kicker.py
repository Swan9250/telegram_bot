"""
Реализация игрового блока для подсчёта счёта игры в кикер между двумя соперниками
"""


def kicker(update, context):
    but = context.user_data['kicker_buttons']

    search_last = """SELECT schet FROM kicker ORDER BY id DESC LIMIT 1"""
    result = f'Е 0:0 В'
    con = context.user_data['kicker_db']
    cursor = con.cursor()
    cursor.execute(search_last)
    btw_result = cursor.fetchone()
    if btw_result is not None:
        result = btw_result[0]
    else:
        result = None

    if update.message.text == but[0]:
        return Vwin(update, context, result, con)
    elif update.message.text == but[1]:
        return Ewin(update, context, result, con)
    elif update.message.text == but[2]:
        return Otkat(update, context, result, con, search_last)
    else:
        pass


def Vwin(update, context, result, con):

    cursor = con.cursor()
    Vwin = result
    if result is not None:
        e = int(result[2:result.find(":")])
        v = int(result[result.find(":") + 1:result.rfind("В") - 1])
        Vwin = f'E {e}:{v + 1} В'

    cursor.execute("""INSERT INTO kicker(message_from_id, message_from_username, message_from_first_name, schet) VALUES(%s, %s, %s, %s)""",
            (update.message.from_user.id, update.message.from_user.username, update.message.from_user.first_name, Vwin))
    con.commit()
    return Vwin


def Ewin(update, context, result, con):
    cursor = con.cursor()
    Ewin = result
    if result is not None:
        e = int(result[2:result.find(":")])
        v = int(result[result.find(":") + 1:result.rfind("В") - 1])
        Ewin = f'E {e + 1}:{v} В'

    cursor.execute("""INSERT INTO kicker(message_from_id, message_from_username, message_from_first_name, schet) VALUES(%s, %s, %s, %s)""",
            (update.message.from_user.id, update.message.from_user.username, update.message.from_user.first_name, Ewin))
    con.commit()
    return Ewin

def Otkat(update, context, result, con, search_last):
    cursor = con.cursor()
    cursor.execute("""DELETE FROM kicker ORDER BY id DESC LIMIT 1""")
    con.commit()
    cursor.execute(search_last)
    btw_result = cursor.fetchone()
    if btw_result is not None:
        result = btw_result[0]
    else:
        result = f'Е 0:0 В'
    return result
