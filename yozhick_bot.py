import datetime
import json
import mysql.connector
import telegram as tg
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters#JobQueue
from telegram.ext import CallbackQueryHandler
import os, sys
p = os.path.abspath('../beget/')
sys.path.insert(1, p)
from api.base import auth
from api.internal import Line
import kicker, buttons as bt, work as wrk

__author__ = 'Vladimir Stanotin'
__version__ = 0.35


phrases = ['Задать уведомление',
          'Ежегодно', 'Ежемесячно', 'Еженедельно', 'Ежедневно']


class Main:
    """
    All code of bot ideas
    """

    swans_chat_id = 177870052
    neustroev_chat_id = 749074706
    phrases = phrases


    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        print(self.updater.bot)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        self.queue = self.updater.job_queue
        self.queue.start()
        self.cronTasks(tg.Update)
        self.commandsHandler()
        self.updater.start_polling()
        self.updater.idle()


#    def work(self, update, context):
#        but = bt.buttons['Критикал']
#        if update.message.text == but[0] or update.message.text == but[2]:
#            self.neustroev(update, context)
#        else:
#            self.relax(context)
#            self.bot.sendMessage(self.getChatId(update), 'Принято')


    def work(self, update, context):
        context.user_data['queue'] = self.queue
        context.user_data['bot'] = self.bot
        response = wrk.work(update, context.user_data)
        self.bot.sendMessage(Main.swans_chat_id, response)


#    def relax(self, context):
#        print(self.queue.jobs())
#        list_jobs_by_name = self.queue.get_jobs_by_name('Work')
#        for job in list_jobs_by_name:
#            print(job.enabled)
#            job.schedule_removal()
#            print(job.enabled)


    
#    def neus(self, context: CallbackContext):
#        print('popal', self.queue.get_jobs_by_name('Work')[0].enabled)
#        enter = auth.Auth()
#        line = Line('first')
#        count = 0
#        workers_on_line = []
#        tickets_over_20 = []
#        for i in line.get():
#            dattim = i['in_queue_from']
#            if i['assignee_name'] != '':
#                workers_on_line.append(i['assignee_name'])
#            tim = dattim[dattim.find('T') + 1:dattim.find('+')]
#            cut = tim.split(':')
#            hour = int(cut[0])
#            minute = int(cut[1])
#            if (datetime.datetime.now() - datetime.timedelta(hours = hour, minutes = minute)).minute > 20:
#                tickets_over_20.append([i['subject'], str((datetime.datetime.now() - datetime.timedelta(hours = hour, minutes = minute)).minute) + ' мин', i['assignee_name']])
#                count += 1
#        if count > 0:
#            pizdit = f"Пора пиздить ребят: на линии {count} тикетов больше 20 минут"
#            beauty_tickets = '\n'.join(str(i) for i in tickets_over_20)
#            tickets_count = f"Тикеты больше 20 мин:\n {beauty_tickets}"
#            people_on_line = ''
#            self.bot.sendMessage(self.neustroev_chat_id, f"Пора пиздить ребят: на линии {count} тикетов больше 20 минут")
#            self.bot.sendMessage(self.neustroev_chat_id, f"тикеты больше 20 мин: {tickets_over_20}")
#            if len(workers_on_line) != 0: 
#                beauty_people = '\n'.join(workers_on_line)
#                people_on_line = f"Сотрудники на линии:\n{beauty_people}"
#                self.bot.sendMessage(self.neustroev_chat_id, f"Сотрудники на линии: {workers_on_line}")
#            else:
#                people_on_line = "ALARM!!! Никого нет на линии!"
#                self.bot.sendMessage(self.neustroev_chat_id, "ALARM!!! Никого нет на линии!")
#            self.bot.sendMessage(Main.neustroev_chat_id, pizdit + '\n\n' + tickets_count + '\n\n' + people_on_line)
#            self.bot.sendMessage(Main.swans_chat_id, pizdit + '\n\n' + tickets_count + '\n\n' + people_on_line)


#    def neustroev(self,update, context: CallbackContext):
#        enter = auth.Auth()
#        if enter is not None:
#            context.user_data['enter'] = enter
#            self.queue.run_repeating(self.neus, 60, last=datetime.time(hour = 17, minute = 0, second = 00), context=context, name='Work')
#            self.queue.get_jobs_by_name('Work')[0].enabled = True
#            self.bot.sendMessage(self.getChatId(update), 'Принято')
#        else:
#            self.bot.sendMessage(self.getChatId(update), 'Что-то пошло не так, нажми ещё раз')

#        print(self.queue.get_jobs_by_name('Work'))
#        context.user_data['enter'] = auth.Auth()  # Может быть None, засунуть в try/except
#        self.queue.run_repeating(self.neus, 60, last=datetime.time(hour = 17, minute = 0, second = 00), context=context, name='Work')
#        self.queue.get_jobs_by_name('Work')[0].enabled = True # Джоба тоже может быть None
#        print(self.queue.get_jobs_by_name('Work')[0].enabled)


#### Блок нотификаций


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

    def notifications(self, update, context: CallbackContext):
        if update.message.text == Main.phrases[0]:
            self.bot.sendMessage(self.getChatId(update), "Выбери период", reply_markup = self.keyboard(bt.keyboardPeriod(), bt.keyboardBack()), reply_to_message_id = update.message.message_id)
            context.user_data['Back'] = update.message.text
        else:
            self.bot.sendMessage(self.getChatId(update), "Укажи дату и время первого запуска", reply_markup = self.keyboard(bt.keyboardBack(), input_field_placeholder = 'Дата: гггг:мм:дд чч:мм:сс'), reply_to_message_id = update.message.message_id)
            context.user_data['period'] = update.message.text
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

#### Конец блока нотификаций


#### Игровой блок


    def kicker(self, update, context):
        context.user_data['kicker_db'] =  self.base_connect()
        context.user_data['kicker_buttons'] = bt.buttons['Кикер']
        response = kicker.kicker(update, context)
        self.bot.sendMessage(self.getChatId(update), response)

#### Конец игрового блока


#### Блок захардкоженных напоминаний


    def poll(self, context: CallbackContext):
        context.bot.send_poll(Main.swans_chat_id, question="Обед", options=['13:00', '13:30', '14:00', '14:30', '15:00', 'позже 15'], is_anonymous=False, allows_multiple_answers=True)


    def medicine(self, context: CallbackContext):
        """
        Сообщение, используемое в захардкоженных заданиях
        """
        message = "Выпей таблетки"
        context.bot.send_message(Main.swans_chat_id, message)

    def cronTasks(self, update, *args):
        """
        Ставим задания в очередь выполнения
        """
#        self.queue.run_daily(self.medicine, days = (0, 1, 2, 3, 4, 5, 6),
#                                    time=datetime.time(hour = 10, minute=30, second=00), context=update)
#        self.queue.run_daily(self.medicine, days = (0, 1, 2, 3, 4, 5, 6),
#                                    time=datetime.time(hour = 15, minute=30, second=00), context=update)
        self.queue.run_daily(self.poll, days = (0, 1, 2, 3, 4), time=datetime.time(hour = 9, minute=0, second=00), context=update)
#        self.queue.run_daily(self.neustroev, days = (0, 1, 2, 3, 4), time=datetime.time(hour = 8, minute=0, second=00), context=update)
            

#### Конец блока захардкоженных напоминаний


#### Главные функции


    def keyboard(*args, input_field_placeholder = None):
        board = []
        for i in args[1:]:
            if len(i) <= 3:
                board.append(i)
            else:
                column = []
                for j in i:
                    column.append(j)
                    if len(column) >= 3:
                        board.append(column)
                        column = []
                if len(column) > 0:
                    board.append(column)
        return tg.ReplyKeyboardMarkup(board, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = input_field_placeholder, selective = True)


    def commandsHandler(self):
        """
        Здесь представлены все обработчики команд, сообщений.
        """
        self.dispatcher.add_handler(CommandHandler("hello", self.hello))   
        self.dispatcher.add_handler(CommandHandler("help", self.help))      
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("stop", self.stop))
        self.dispatcher.add_handler(MessageHandler(Filters.regex('^/.*'), self.default))
        self.dispatcher.add_handler(MessageHandler(Filters.text(bt.buttons['Кикер']), self.kicker))
        self.dispatcher.add_handler(MessageHandler(Filters.text(bt.buttons['Критикал']), self.work))
        self.dispatcher.add_handler(MessageHandler(Filters.text(Main.phrases), self.notifications))
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


    def hello(self, update, context):
        """
        Православное приветствие.
        """
        hello = f'Hello @{update.effective_user.username}'
#        print(self.dispatcher) == update
        print(update)
        if update.message.chat.id == Main.swans_chat_id:
            context.user_data["keyboard"] = self.keyboard(bt.keyboardMain(), bt.keyboardNotify(), bt.keyboardKicker(), bt.keyboardWork())
            self.bot.sendMessage(self.getChatId(update), hello, reply_markup = context.user_data["keyboard"], reply_to_message_id = update.message.message_id)
        elif update.message.chat.id == Main.neustroev_chat_id:
            context.user_data["keyboard"] = self.keyboard(bt.keyboardWork())
            self.bot.sendMessage(self.getChatId(update), hello, reply_markup = context.user_data["keyboard"], reply_to_message_id = update.message.message_id)
        elif update.message.chat.title == 'Доминирование':
            context.user_data["keyboard"] = self.keyboard(bt.keyboardMain(), bt.keyboardKicker(), bt.keyboardNotify())
            self.bot.sendMessage(self.getChatId(update), hello, reply_markup = context.user_data["keyboard"], reply_to_message_id = update.message.message_id)
        elif update.message.chat.title == 'Че кого':
            context.user_data["keyboard"] = self.keyboard(bt.keyboardMain(), bt.keyboardNotify())
            self.bot.sendMessage(self.getChatId(update), hello, reply_markup = context.user_data["keyboard"], reply_to_message_id = update.message.message_id)
        elif update.message.chat.title == 'Идеология мертва':
            self.bot.sendMessage(self.getChatId(update), hello, reply_to_message_id = update.message.message_id)
#            print(self.getChatId(update))
        else:
#            print(update.message)
            context.user_data["keyboard"] = self.keyboard(bt.keyboardMain())
            self.bot.sendMessage(self.getChatId(update), hello, reply_markup = context.user_data["keyboard"], reply_to_message_id = update.message.message_id)


    def start(self, update:tg.Update, context:CallbackContext):
        """
        Обрабатываем стандартный запуск бота.
        """
        start = f'Ты обратился к боту, но сделал это без уважения, введи /hello'
        photo = 'https://i.ytimg.com/vi/q8ADpnunCGo/hqdefault.jpg'
        self.bot.sendMessage(self.getChatId(update), start)
        self.bot.sendPhoto(self.getChatId(update), photo)


    def default(self, update, context):
        """
        Обработка неверных команд
        """
        dich = f'Ты несёшь какую-то дичь! Введи /hello'
        self.bot.sendMessage(self.getChatId(update), dich, reply_to_message_id = update.message.message_id)


    def stop(self, update, context):
        pass


    def base_connect(self):
        try:
            con = mysql.connector.connect(
                    host='localhost',
                    user='bot',
                    password='telegram_bot',
                    database='telegram_bot',
                    auth_plugin='mysql_native_password',
                    )
            return con
        except:
            print("Error")


if __name__ == '__main__':
    with open('yozhick_token', 'r') as t:
        token = str(t.read())
        print(token[:-1])
    Main(token[:-1])
