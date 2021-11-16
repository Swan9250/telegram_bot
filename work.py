"""
Реализация статистики тикетов, находящихся на линии больше 20 минут, и уведомления ведущего.
"""

import buttons as bt
import datetime
import os, sys
import auth
from Line import Line
#p = os.path.abspath('../beget/')
#sys.path.insert(1, p)
#from api.base import auth
#from api.internal import Line


def work(update, context): # Не забыть передать в context self.queue
    if update.message.text == bt.buttons['Критикал'][0]: # "Критикал" : ['Получать уведомления', 'Не получать уведомления']
        return run(context)
    else:
        return relax(context)


def relax(context):
    queue = context['queue']
#    print(queue.jobs())
    list_jobs_by_name = queue.get_jobs_by_name('Work')
    try:
        for job in list_jobs_by_name:
            job.schedule_removal()
#            print(job.enabled)
        return "Уведомления отключены"
    except:
        return "Что-то пошло не так, обратитесь к разработчику"


def neus(context):
    print(context.job.context)
    queue = context.job.context['queue']
    bot = context.job.context['bot']
    print('popal', queue.get_jobs_by_name('Work')[0].enabled)
    line = Line('first')
    count = 0
    workers_on_line = []
    tickets_over_20 = []
    for i in line.get():
        dattim = i['in_queue_from']
        if i['assignee_name'] != '':
            workers_on_line.append(i['assignee_name'])
        tim = dattim[dattim.find('T') + 1:dattim.find('+')]
        cut = tim.split(':')
        hour = int(cut[0])
        minute = int(cut[1])
        if (datetime.datetime.now() - datetime.timedelta(hours = hour, minutes = minute)).minute > 20:
            tickets_over_20.append([i['subject'], str((datetime.datetime.now() - datetime.timedelta(hours = hour, minutes = minute)).minute) + ' мин', i['assignee_name']])
            count += 1
    if count > 0:
        pizdit = f"Пора пиздить ребят: на линии {count} тикетов больше 20 минут"
        beauty_tickets = '\n'.join(str(i) for i in tickets_over_20)
        tickets_count = f"Тикеты больше 20 мин:\n {beauty_tickets}"
        people_on_line = ''
        if len(workers_on_line) != 0:
            beauty_people = '\n'.join(workers_on_line)
            people_on_line = f"Сотрудники на линии:\n{beauty_people}"
        else:
            people_on_line = "ALARM!!! Никого нет на линии!"
#        self.bot.sendMessage(Main.neustroev_chat_id, pizdit + '\n\n' + tickets_count + '\n\n' + people_on_line)
        bot.sendMessage(177870052, pizdit + '\n\n' + tickets_count + '\n\n' + people_on_line)
#        return pizdit + '\n\n' + tickets_count + '\n\n' + people_on_line


def run(context):
    queue = context['queue']
    print('Очередь', queue)
    try:
        auth.Auth()
        if len(queue.get_jobs_by_name('Work')) == 0:
            queue.run_repeating(neus, 60, last=datetime.time(hour = 17, minute = 0, second = 00), context=context, name='Work')
        else:
            return "Задание уже запущено.\n"
#        queue.get_jobs_by_name('Work')[0].enabled = True
        return "Уведомления включены.\n"
    except:
        return "Что-то пошло не так, обратитесь к разработчику."
