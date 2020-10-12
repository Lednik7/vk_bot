import random, vk_api, vk
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
from threading import Thread
import threading
import datetime
import time

token = '4adbcb234ad29a3f780711d2803a7b3532a791dfedd0ba369a27a854b97127179e7b236ce961ffe5d2' + '440'
vk_session = vk_api.VkApi(token=token)

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

longpoll = VkBotLongPoll(vk_session, 199420763)
vk = vk_session.get_api()

def mention():
    members = vk.messages.getConversationMembers(
            peer_id=2000000001,
        )

    members_ids = [member['member_id'] for member in members['items'] if member['member_id'] > 0]
    members_names = [member['first_name'] for member in members["profiles"]]

    message = ''
    for name, member_id in zip(members_names, members_ids):
        message += f'[id{member_id}|{name}, ]'

    return message

tasks = [
         ["Меташкола", "2020.10.18", "19.30", "физика"],
         ["Меташкола", "2020.10.27", "19.30", "математика"],
         ["Меташкола", "2020.10.13", "19.30", "Программирование"]
]

tasks.sort(key=lambda x: x[1] + x[2])

def to_date(x):
    return [int(i) for i in x.split(".")]

def get_seconds(task):
    offset = datetime.timezone(datetime.timedelta(hours=3))
    date = datetime.datetime(*to_date(task[1]), *to_date(task[2])) - (datetime.datetime.now(offset)).replace(tzinfo=None) - datetime.timedelta(minutes=30)
    seconds = round(date.total_seconds())
    return seconds

def send_message(total_seconds, task, t):
    time.sleep(total_seconds)
    if t == 0:
        vk.messages.send(
            key = ('d978ad9160e7ff4b18057daf93f41acd1c94e4c2'),
            server = ('https://lp.vk.com/wh199420763'),
            ts = ('23'),
            random_id = get_random_id(),
            message =f'{mention()}сегодня олимпиада {task[0]} по предмету: {task[3]}',
            chat_id = 2,
            )
    else:
        vk.messages.send(
            key = ('d978ad9160e7ff4b18057daf93f41acd1c94e4c2'),
            server = ('https://lp.vk.com/wh199420763'),
            ts = ('23'),
            random_id = get_random_id(),
            message =f'{mention()}Олимпиада по предмету: {task[3]} - началась!',
            chat_id = 2,
            )
    
class myThread(threading.Thread):
    def __init__(self, total_seconds, task, n):
       threading.Thread.__init__(self)
       self.n = n
       self.task = task
       self.total_seconds = total_seconds

    def run(self):
       send_message(self.total_seconds, self.task, self.n)

for task in tasks:
    total_seconds = get_seconds(task)
    if total_seconds >= 0:
        thread1 = myThread(total_seconds, task, 0)
        thread2 = myThread(total_seconds + 1800, task, 1)
        thread1.start()
        thread2.start()