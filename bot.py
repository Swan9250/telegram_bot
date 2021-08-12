import datetime
import json
import telegram as tg
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler

#bot_token = "1252528974:AAHXokVMmpKs80OHuTZdbArBFeBCs2PZKtU"

#chat_id_with_Swan = '177870052'


class countGame():
    def __init__(self):
        self.bot_token = "1252528974:AAHXokVMmpKs80OHuTZdbArBFeBCs2PZKtU"
        self.schet = "E 17:22 В"
        self.pred = "E 17:22 В"
        self.updater = Updater(self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        self.queue = self.updater.job_queue
        self.queue.start()
        self.cronTasks(tg.Update)
        self.commandsHandler()
        self.updater.start_polling()
        self.updater.idle()

    def medicine(self, context: CallbackContext):
#        print('popal')
        message = "Выпей таблетки"
        context.bot.send_message(177870052, message)
#        print('Popal')

    def cronTasks(self, update, *args):
#        print('run')
#        self.queue.run_repeating(self.medicine, interval=10.0, first=0.0)
        self.queue.run_daily(self.medicine, days = (0, 1, 2, 3, 4, 5, 6),
                                    time=datetime.time(hour = 13, minute=30, second=00), context=update)
        self.queue.run_daily(self.medicine, days = (0, 1, 2, 3, 4, 5, 6),
                                    time=datetime.time(hour = 18, minute=30, second=00), context=update)
#        print(self.queue.jobs())
        

    def commandsHandler(self):
        self.dispatcher.add_handler(CommandHandler("hello", self.hello))
        self.dispatcher.add_handler(CommandHandler("help", self.help))
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("EgorWin", self.Ewin))
        self.dispatcher.add_handler(CommandHandler("VovaWin", self.Vwin))
        self.dispatcher.add_handler(CommandHandler("Otkat", self.Otkat))
#        self.dispatcher.add_handler(CallbackQueryHandler(self.cronTasks, pass_job_queue = True))

 #       self.dispatcher.add_handler(CommandHandler("Timer", self.cronTasks))

    def update(self)->list:
        return self.bot.getUpdates()

    def getChatId(self, update:tg.Update):
        return update.message.chat.id

    def keyboardDom(self, update):
        hello = tg.KeyboardButton('/hello')
        help = tg.KeyboardButton('/help')
        Vwin = tg.KeyboardButton('/VovaWin')
        Ewin = tg.KeyboardButton('/EgorWin')
        start = tg.KeyboardButton('/start')
        Otkat = tg.KeyboardButton('/Otkat')
#        timer = tg.KeyboardButton('/Timer')
        if update.message.chat.title == 'Доминирование':
            return tg.ReplyKeyboardMarkup([[hello], [help], [Vwin], [Ewin], [start], [Otkat]])
        elif update.message.chat.id == 177870052:
            return tg.ReplyKeyboardMarkup([[hello], [help], [start]])
        else:
            print('Лошара')


    def hello(self, update:tg.Update, context:CallbackContext):
        hello = f'Hello {update.effective_user.first_name}'
        self.bot.sendMessage(self.getChatId(update), hello, reply_markup=self.keyboardDom(update))

    def help(self, update:tg.Update, context:CallbackContext):
        help = f'Say /hello to start'
        self.bot.sendMessage(self.getChatId(update), help)

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


    def start(self, update:tg.Update, context:CallbackContext):
        start = f'Ты обратился к боту, но сделал это без уважения, введи /hello'
        photo = 'https://i.ytimg.com/vi/q8ADpnunCGo/hqdefault.jpg'
        self.bot.sendMessage(self.getChatId(update), start)
        self.bot.sendPhoto(self.getChatId(update), photo)


    def get_chat_id(self):
        self.chat_id = self.updater.message_id



if __name__ == '__main__':
    countGame()
