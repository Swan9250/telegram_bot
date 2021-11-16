import telegram as tg


buttons = {"Уведомления" :
              ['Задать уведомление',
              'Ежегодно', 'Ежемесячно', 'Еженедельно', 'Ежедневно', 'Одноразово'],
          "Кикер" :
              ['Вова выиграл', 'Егор выиграл', 'Откат'],
          "Критикал" :
              ['Получать уведомления', 'Не получать уведомления'],
          "Назад" :
              ['Назад']
          }


def keyboardKicker():
    """
    Делаем кнопки выбора победившего, возврата.
    """
    but = buttons['Кикер']
    Vwin = tg.KeyboardButton(but[0])
    Ewin = tg.KeyboardButton(but[1])
    Otkat = tg.KeyboardButton(but[2])
    return [Vwin, Ewin, Otkat]


def keyboardWork():
    """
    Делаем кнопки начала и конца работы.
    """
    but = buttons['Критикал']
    start_work = tg.KeyboardButton(but[0])
    end_work = tg.KeyboardButton(but[1])
    return [start_work, end_work]


def keyboardBack():
    """
    Делаем кнопку "Назад" на клавиатуре.
    """
    but = buttons['Назад']
    back = tg.KeyboardButton(but[0])
    return [back]


def keyboardPeriod():
    """
    Делаем кнопки периодов нотификаций.
    """
    but = buttons['Уведомления']
    year = tg.KeyboardButton(but[1])
    month = tg.KeyboardButton(but[2])
    week = tg.KeyboardButton(but[3])
    day = tg.KeyboardButton(but[4])
    once = tg.KeyboardButton(but[5])
    return [year, month, week, day, once]


def keyboardNotify():
    """
    Делаем кнопку "Задать уведомление".
    """
    but = buttons['Уведомления']
    notify = tg.KeyboardButton(but[0])
    return [notify]
