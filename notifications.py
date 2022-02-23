"""
С помощью этого кода можно создавать уведомления в телеграм боте.
"""


import datetime
import buttons as bt


def distributor(update, context):
    buts = context.user_data['notify_buttons']
    actual_but = context.user_data['button']
    message = ''
    if actual_but == buts[0]:
        message = choose_type(update, context)
    elif actual_but == buts[1]:
        message = makeFirst(update, context)
    elif actual_but == buts[2]:
        message = notify(update, context)
    elif actual_but == buts[3]:
        message = Back(update, context)
    return message


def choose_type(update, context):
    but = context.user_data['notify_buttons']
    bot = context.user_data['bot']

    if update.message.text == but[0]:
        message = "Выбери период"
        context.user_data['Back'] = update.message.text
    else:
        message = "Укажи дату и время первого запуска"
        context.user_data['period'] = update.message.text
        context.user_data['Back'] = update.message.text

    return message


#### [DRAFT]


def getText(self, context):
    job = context.job
    context.bot.send_message(int(job.context['chat_id']), job.context['text'])

def makeFirst(self, update, context):
    if "Дата:" in update.message.text:
        text = update.message.text
        text = text.split(" ")
        dat = text[1].split(":")
        tim = text[2].split(":")
        hour = int(tim[0])
        if context.user_data['period'] != Main.phrases[2]:
            hour = int(tim[0]) - 3
        first = datetime.datetime(year = int(dat[0]), month = int(dat[1]), day = int(dat[2]), hour = hour, minute = int(tim[1]), second = int(tim[2][:2])) # -3 потому что бот сам прибавляет таймзону
        self.bot.sendMessage(self.getChatId(update), "Напиши напоминалку", reply_markup = self.keyboard(bt.keyboardBack(), input_field_placeholder = "Уведомление:"), reply_to_message_id = update.message.message_id)
        context.user_data['data'] = first
        context.user_data['Back'] = update.message.text


def notify(self, update, context):
    if 'Уведомление:' in update.message.text:
        first = context.user_data['data']
        text = update.message.text
        context.user_data['text'] = text
        context.user_data['chat_id'] = self.getChatId(update)
        context.user_data['Back'] = update.message.text
        self.bot.sendMessage(self.getChatId(update), "Готово", reply_markup = context.user_data["keyboard"], reply_to_message_id = update.message.message_id)
        if context.user_data['period'] == Main.phrases[1]:
            self.queue.run_repeating(self.getText, datetime.timedelta(days = 365), first = first, name = 'notifyYear', context = context.user_data)
        elif context.user_data['period'] == Main.phrases[2]:
            self.queue.run_monthly(self.getText, first.time(), first.day, context = context.user_data, name = 'notifyMonth', day_is_strict = False)
        elif context.user_data['period'] == Main.phrases[3]:
            self.queue.run_daily(self.getText, first.time(), days = str(first.weekday()), context = context.user_data, name = 'notifyWeek')
        elif context.user_data['period'] == Main.phrases[4]:
            self.queue.run_daily(self.getText, first.time(), context = context.user_data, name = 'notifyDaily')
        else:
            pass
    else:
        pass


def Back(self, update, context):
    if context.user_data != {}:
        if context.user_data['Back'] == Main.phrases[0]:
            self.hello(update, context)
        elif context.user_data['Back'] in Main.phrases:
            self.bot.sendMessage(self.getChatId(update), "Выбери период", reply_markup = self.keyboard(bt.keyboardPeriod(), bt.keyboardBack()), reply_to_message_id = update.message.message_id)
            context.user_data['Back'] = Main.phrases[0]
        elif 'Дата' in context.user_data['Back']:
            self.bot.sendMessage(self.getChatId(update), "Укажи дату и время первого запуска", reply_markup = self.keyboard(bt.keyboardBack(), input_field_placeholder = 'Дата: гггг:мм:дд чч:мм:сс'), reply_to_message_id = update.message.message_id)
            context.user_data['Back'] = "Ежегодно"
        else:
            self.hello(update, context)

