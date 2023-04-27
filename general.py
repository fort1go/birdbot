import telebot
from telebot import types
import asyncio

bot = telebot.TeleBot('5839359620:AAH0qocuLgZNKcLqBb4TyjUc8LP59kSf7IU')
data_users = {'Egor': ['bird_name', 'bird_starve', 'bird_fatigue', 'bird_mood', 'money']}


def change_stats(message, name='asjgbuebgabeugabueg', starve=-20, fatigue=-20, mood=-5, text=''):
    if name != 'asjgbuebgabeugabueg': data_users[message.from_user.id][0] = name
    data_users[message.from_user.id][1] += starve
    data_users[message.from_user.id][2] += fatigue
    data_users[message.from_user.id][3] += mood
    if text != '': bot.send_message(message.from_user.id, text)

 #async def reduction_stats(message):
 #   while True:
 #       await asyncio.sleep(600)
 #       change_stats(message)

#main menu>
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in data_users:
        bot.send_message(message.from_user.id, 'У тебя уже есть птичка :)\n'
                                               'Чтобы узнать список команд: /help')
    else:
        bot.send_message(message.from_user.id, 'Если ты тут впервые, выбери имя своей птичке: /set_name\n'
                                               'Чтобы узнать список команд: /help')
        data_users[message.from_user.id] = ['', 0, 0, 0, 0]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, 'Перейти в свой профиль: /my_bird\n'
                                           'Покормить птичку: /feed\n'
                                           'Поиграть с птичкой: /play\n'
                                           'Уложить птичку спать: /sleep\n'
                                           'Зайти в магазин: /shop\n'
                                           'Выбросить птичку: /remove')


@bot.message_handler(commands=['my_bird'])
def my_bird(message):
    if message.from_user.id in data_users:
        bot.send_message(message.from_user.id, 'Это твой профиль\n'
                                               f'🐦 {data_users[message.from_user.id][0]}\n'
                                               f'🍞 {data_users[message.from_user.id][1]}%\n'
                                               f'💤 {data_users[message.from_user.id][2]}%\n'
                                               f'🎮 {data_users[message.from_user.id][3]}%')
    else:
        pass
#main menu<

# stats>
@bot.message_handler(commands=['feed'])
def feed(message):
    if message.from_user.id in data_users:
        change_stats(message, starve=50, text='Было вкусно')
    else:
        pass


@bot.message_handler(commands=['sleep'])
def sleep(message):
    if message.from_user.id in data_users:
        change_stats(message, fatigue=70, text='Птичка выспалась и готова к полёту')
    else:
        pass


@bot.message_handler(commands=['play'])
def play(message):
    if message.from_user.id in data_users:
        change_stats(message, mood=20, text='Было весело')
    else:
        pass
# stats<

#other>
@bot.message_handler(commands=['remove'])
def remove(message):
    if message.from_user.id in data_users:
        change_stats(message, name='', starve=-data_users[message.from_user.id][1],
                     fatigue=-data_users[message.from_user.id][2], mood=-data_users[message.from_user.id][3], text='Выкинуть птичку - позор')
    else:
        pass


@bot.message_handler(content_types=['text'])
def set_name(message):
    if message.from_user.id in data_users and '/set_name' in message.text:
        data_users[message.from_user.id][0] = message.text[10:]
        bot.send_message(message.from_user.id, f'Имя успешно сменено на {data_users[message.from_user.id][0]}')
    else:
        pass
#other<

bot.polling(none_stop=True, interval=0)
