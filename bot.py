import datetime
import json
import telegram as tg
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters#JobQueue
from telegram.ext import CallbackQueryHandler


phrases = ['Задать уведомление',
          'Ежегодно', 'Ежемесячно', 'Еженедельно', 'Ежедневно']

class main:
    def __init__(self, buttons):
        self.bot_token = "1252528974:AAHXokVMmpKs80OHuTZdbArBFeBCs2PZKtU"
        self.swans_chat_id = 177870052
        self.schet = "E 19:22 В"
        self.pred = "E 19:22 В"
        self.phrases = phrases
        self.updater = Updater(self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        self.queue = self.updater.job_queue
        self.queue.start()
        self.cronTasks(tg.Update)
        self.commandsHandler()
        self.updater.start_polling()
        self.updater.idle()


    def keyboardBack(self):
        back = tg.KeyboardButton("Назад")
        return [back]


    def keyboardPeriod(self):
        year = tg.KeyboardButton(self.phrases[1])
        month = tg.KeyboardButton(self.phrases[2])
        week = tg.KeyboardButton(self.phrases[3])
        day = tg.KeyboardButton(self.phrases[4])
        return [year, month, week, day]


    def keyboardNotify(self):
        notify = tg.KeyboardButton('Задать уведомление')
        return [notify]



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
            if context.user_data['period'] != self.phrases[2]:
                hour = int(tim[0]) - 3
            first = datetime.datetime(year = int(dat[0]), month = int(dat[1]), day = int(dat[2]), hour = hour, minute = int(tim[1]), second = int(tim[2][:2])) # -3 потому что бот сам прибавляет таймзону
            self.bot.sendMessage(self.getChatId(update), "Напиши напоминалку", reply_markup = self.keyboard(self.keyboardBack(), input_field_placeholder = "Уведомление:"))
            context.user_data['data'] = first
            context.user_data['Back'] = update.message.text

    def notifications(self, update, context: CallbackContext):
        if update.message.text == self.phrases[0]:
            self.bot.sendMessage(self.getChatId(update), "Выбери период", reply_markup = self.keyboard(self.keyboardPeriod(), self.keyboardBack()))
            context.user_data['Back'] = update.message.text
        else:
            self.bot.sendMessage(self.getChatId(update), "Укажи дату и время первого запуска", reply_markup = self.keyboard(self.keyboardBack(), input_field_placeholder = 'Дата: гггг:мм:дд чч:мм:сс'))
            context.user_data['period'] = update.message.text
            context.user_data['Back'] = update.message.text

    def notify(self, update, context):
        if 'Уведомление:' in update.message.text:
            first = context.user_data['data']
            text = update.message.text
            context.user_data['text'] = text
            context.user_data['chat_id'] = self.getChatId(update)
            context.user_data['Back'] = update.message.text
            self.bot.sendMessage(self.getChatId(update), "Готово", reply_markup = context.user_data["keyboard"])
            if context.user_data['period'] == self.phrases[1]:
                self.queue.run_repeating(self.getText, datetime.timedelta(days = 365), first = first, name = 'notifyYear', context = context.user_data)
            elif context.user_data['period'] == self.phrases[2]:
                self.queue.run_monthly(self.getText, first.time(), first.day, context = context.user_data, name = 'notifyMonth', day_is_strict = False)
            elif context.user_data['period'] == self.phrases[3]:
                self.queue.run_daily(self.getText, first.time(), days = str(first.weekday()), context = context.user_data, name = 'notifyWeek')
            elif context.user_data['period'] == self.phrases[4]:
                self.queue.run_daily(self.getText, first.time(), context = context.user_data, name = 'notifyDaily')
            else:
                pass
        else:
            pass
        
    
    def keyboardNot(self, update):
        year = tg.KeyboardButton(self.phrases[1])
        month = tg.KeyboardButton(self.phrases[2])
        week = tg.KeyboardButton(self.phrases[3])
        day = tg.KeyboardButton(self.phrases[4])
        return [[year, month], [week, day]]
        

    def Back(self, update, context):
        if context.user_data != {}:
            if context.user_data['Back'] == self.phrases[0]:
                self.hello(update, context)
                context.user_data["keyboard"] = self.keyboard(self.keyboardMain(), self.keyboardNotify())
            elif context.user_data['Back'] in self.phrases:
                self.bot.sendMessage(self.getChatId(update), "Выбери период", reply_markup = self.keyboard(self.keyboardPeriod(), self.keyboardBack()))
                context.user_data['Back'] = self.phrases[0]
            elif 'Дата' in context.user_data['Back']:
                self.bot.sendMessage(self.getChatId(update), "Укажи дату и время первого запуска", reply_markup = self.keyboard(self.keyboardBack(), input_field_placeholder = 'Дата: гггг:мм:дд чч:мм:сс'))
                context.user_data['Back'] = "Ежегодно"
            else:
                self.hello(update, context)


#### Блок захардкоженных напоминаний


    def medicine(self, context: CallbackContext):
        """
        Сообщение, используемое в захардкоженных заданиях
        """
        message = "Выпей таблетки"
        context.bot.send_message(self.swans_chat_id, message)

    def cronTasks(self, update, *args):
        """
        Ставим задания в очередь выполнения
        """
        self.queue.run_daily(self.medicine, days = (0, 1, 2, 3, 4, 5, 6),
                                    time=datetime.time(hour = 10, minute=30, second=00), context=update)
        self.queue.run_daily(self.medicine, days = (0, 1, 2, 3, 4, 5, 6),
                                    time=datetime.time(hour = 15, minute=30, second=00), context=update)

#### Конец блока захардкоженных напоминаний


#### Игровой блок


    def keyboardKicker(self):
        Vwin = tg.KeyboardButton('/VovaWin')
        Ewin = tg.KeyboardButton('/EgorWin')
        Otkat = tg.KeyboardButton('/Otkat')
        return [Vwin, Ewin, Otkat]



    def Vwin(self, update:tg.Update, context:CallbackContext):
        e = int(self.schet[2:self.schet.find(":")])
        v = int(self.schet[self.schet.find(":") + 1:self.schet.rfind("В") - 1])
        Vwin = f'E {e}:{v + 1} В'
        self.bot.sendMessage(self.getChatId(update), Vwin)
        self.pred = self.schet
        self.schet = Vwin

    def Ewin(self, update:tg.Update, context:CallbackContext):
        e = int(self.schet[2:self.schet.find(":")])
        v = int(self.schet[self.schet.find(":") + 1:self.schet.rfind("В") - 1])
        Ewin = f'E {e + 1}:{v} В'
        self.bot.sendMessage(self.getChatId(update), Ewin) 
        self.pred = self.schet
        self.schet = Ewin

    def Otkat(self, update:tg.Update, context:CallbackContext):
        self.schet = self.pred
        self.bot.sendMessage(self.getChatId(update), self.schet)

#### Конец игрового блока

#### Главные функции


    def keyboard(*args, input_field_placeholder = None):
        board = []
        for i in args[1:]:
            board.append(i)
        return tg.ReplyKeyboardMarkup(board, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = input_field_placeholder)


    def keyboardMain(self):
        hello = tg.KeyboardButton('/hello')
        help = tg.KeyboardButton('/help')
        start = tg.KeyboardButton('/start')
        return [hello, help, start]

    
    def commandsHandler(self):
        """
        Здесь представлены все обработчики команд, сообщений.
        """
        self.dispatcher.add_handler(CommandHandler("hello", self.hello))   #
        self.dispatcher.add_handler(CommandHandler("help", self.help))     #
        self.dispatcher.add_handler(CommandHandler("start", self.start))   #
        self.dispatcher.add_handler(CommandHandler("EgorWin", self.Ewin))  # Переписать этот блок через MessageHandler
        self.dispatcher.add_handler(CommandHandler("VovaWin", self.Vwin))  #
        self.dispatcher.add_handler(CommandHandler("Otkat", self.Otkat))   #
        self.dispatcher.add_handler(MessageHandler(Filters.text(self.phrases), self.notifications))
        self.dispatcher.add_handler(MessageHandler(Filters.regex('^.*:.*:.* .*:.*:.*$'), self.makeFirst))
        self.dispatcher.add_handler(MessageHandler(Filters.regex('^Уведомление:'), self.notify))
        self.dispatcher.add_handler(MessageHandler(Filters.regex('^Назад$'), self.Back))                   # Я пока хз, как делать CallbackQueryHandler, наверное, для этого нужен CallbackQuery

    
    def getChatId(self, update:tg.Update):
        """
        Получение id чата.
        """
        return update.message.chat.id


    def help(self, update:tg.Update, context:CallbackContext):
        """
        Помощь по командам. Надо доделать.
        """
        help = f'Для начала скажи /hello'
        self.bot.sendMessage(self.getChatId(update), help)


    def hello(self, update:tg.Update, context:CallbackContext):
        """
        Православное приветствие.
        """
        hello = f'Hello @{update.effective_user.username}'
        if update.message.chat.id == self.swans_chat_id:
            context.user_data["keyboard"] = self.keyboard(self.keyboardMain(), self.keyboardNotify())
            self.bot.sendMessage(self.getChatId(update), hello, reply_markup = context.user_data["keyboard"])
        elif update.message.chat.title == 'Доминирование':
            context.user_data["keyboard"] = self.keyboard(self.keyboardMain(), self.keyboardKicker(), self.keyboardNotify())
            self.bot.sendMessage(self.getChatId(update), hello, reply_markup = context.user_data["keyboard"])
        else:
            context.user_data["keyboard"] = self.keyboard(self.keyboardMain())
            self.bot.sendMessage(self, getChatId(update), hello, reply_markup = contex.user_data["keyboard"])


    def start(self, update:tg.Update, context:CallbackContext):
        """
        Обрабатываем стандартный запуск бота.
        """
        start = f'Ты обратился к боту, но сделал это без уважения, введи /hello'
        photo = 'https://i.ytimg.com/vi/q8ADpnunCGo/hqdefault.jpg'
        self.bot.sendMessage(self.getChatId(update), start)
        self.bot.sendPhoto(self.getChatId(update), photo)



if __name__ == '__main__':
    main(phrases)
