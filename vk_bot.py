import random, vk_api, vk
from vk_api.utils import get_random_id
from threading import Thread
import threading
import datetime
import time

chat_id = 2

token = '4adbcb234ad29a3f780711d2803a7b3532a791dfedd0ba369a27a854b97127179e7b236ce961ffe5d2' + '440'
vk_session = vk_api.VkApi(token=token)

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

longpoll = VkBotLongPoll(vk_session, 199420763)
vk = vk_session.get_api()

def mention(): #получем строку с пользователями беседы
    members = vk.messages.getConversationMembers(
            peer_id=int(f"200000000{chat_id}"),
        )

    members_ids = [member['member_id'] for member in members['items'] if member['member_id'] > 0]
    members_names = [member['first_name'] for member in members["profiles"]][::-1]

    message = ''
    for name, member_id in zip(members_names, members_ids):
        message += f'[id{member_id}|{name}, ]'

    return message

tasks = [
         ["Меташкола", "2020.10.18", "19.30", "физика"],
         ["Меташкола", "2020.10.27", "19.30", "математика"],
         ["Меташкола", "2020.10.13", "19.30", "Программирование"]
]

tasks_to_run = []

tasks.sort(key=lambda x: x[1] + x[2])

def to_date(x):
    return [int(i) for i in x.split(".")]

def get_seconds(task): #получаем кол-во секунд до даты
    offset = datetime.timezone(datetime.timedelta(hours=3))
    date = datetime.datetime(*to_date(task[1]), *to_date(task[2])) - (datetime.datetime.now(offset)).replace(tzinfo=None) - datetime.timedelta(minutes=30)
    seconds = round(date.total_seconds())
    return seconds

def vk_send(s): #отправляем сообщение через vk
    vk.messages.send(
        key = ('d978ad9160e7ff4b18057daf93f41acd1c94e4c2'),
        server = ('https://lp.vk.com/wh199420763'),
        ts = ('23'),
        random_id = get_random_id(),
        message = s,
        chat_id = chat_id,
        )

def send_message(total_seconds, task, t): #отправка шаблона сообщения
    time.sleep(total_seconds)
    if t == 0:
        s = f'{mention()}сегодня олимпиада {task[0]} по предмету: {task[3]}'
    else:
        s = f'{mention()}Олимпиада по предмету: {task[3]} - началась!'

    vk_send(s)

def add(s):
    return s.strip().split()[3:]
    
class myThread(threading.Thread): #отправляем уведомление в поток
    def __init__(self, total_seconds, task, n):
       threading.Thread.__init__(self)
       self.n = n
       self.task = task
       self.total_seconds = total_seconds

    def run(self):
       send_message(self.total_seconds, self.task, self.n)

def run_programm(tasks): #запускает программу
    for task in tasks:
        if task not in tasks_to_run:
            total_seconds = get_seconds(task)
            if total_seconds >= 0:
                tasks_to_run.append(task)
                thread1 = myThread(total_seconds, task, 0)
                thread2 = myThread(total_seconds + 1800, task, 1)
                thread1.start()
                thread2.start()

            elif (total_seconds + 1800) >= 0:
                tasks_to_run.append(task)
                thread1 = myThread(total_seconds + 1800, task, 1)
                thread1.start()

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        s = str(event.object.text).lower().strip()
        if "настройка" in s:
            chat_id = event.chat_id
            run_programm(tasks)
            print(event.chat_id)
            if event.from_chat:
                vk_send('Настройка выполнена')
                
        elif "добавить" in s:
            print(event.chat_id)
            try:
                tasks.append(add(s))
                tasks.sort(key=lambda x: x[1] + x[2])
                run_programm(tasks)
                if event.from_chat:
                    vk_send('Олимпиада добавлена')
            except:
                if event.from_chat:
                    vk_send('Формат данных неправильный')
                
        elif "данные" in s:
            print(tasks)
            print(tasks_to_run)
