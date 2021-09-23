import telegram as tg


buttons = {"Уведомления" :
              ['Задать уведомление',
              'Ежегодно', 'Ежемесячно', 'Еженедельно', 'Ежедневно', 'Одноразово'],
          "Кикер" :
              ['Вова выиграл', 'Егор выиграл', 'Откат'],
          "Главные" :
              ['/hello', '/help', '/start', '/stop'],
          "Критикал" :
              ['Получать уведомления', 'Не получать уведомления']
          }


def keyboardKicker():
    but = buttons['Кикер']
    Vwin = tg.KeyboardButton(but[0])
    Ewin = tg.KeyboardButton(but[1])
    Otkat = tg.KeyboardButton(but[2])
    return [Vwin, Ewin, Otkat]


def keyboardWork():
    """
    Делаем кнопки периодов нотификаций
    """
    but = buttons['Критикал']
    start_work = tg.KeyboardButton(but[0])
    end_work = tg.KeyboardButton(but[1])
    return [start_work, end_work]


def keyboardBack():
    """
    Делаем кнопку "Назад" на клавиатуре
    """
    back = tg.KeyboardButton("Назад")
    return [back]


def keyboardPeriod():
    """
    Делаем кнопки периодов нотификаций
    """
    but = buttons['Уведомления']
    year = tg.KeyboardButton(but[1])
    month = tg.KeyboardButton(but[2])
    week = tg.KeyboardButton(but[3])
    day = tg.KeyboardButton(but[4])
    return [year, month, week, day]


def keyboardNotify():
    """
    Делаем кнопку "Задать уведомление"
    """
    notify = tg.KeyboardButton('Задать уведомление')
    return [notify]


def keyboardMain():
    hello = tg.KeyboardButton('/hello')
    help = tg.KeyboardButton('/help')
    start = tg.KeyboardButton('/start')
    stop = tg.KeyboardButton('/stop')
    return [hello, help, start, stop] # Подумать, нахера мне вообще эти кнопки
