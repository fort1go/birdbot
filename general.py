import telebot
from telebot import types
import time


bot = telebot.TeleBot('6942944111:AAEy94IuRQ4CEPfdQ1_EEj0h0t9K9ZsIMcY')
data_users = {
    'Egor': ['bird_name', 'bird_starve', 'bird_fatigue', 'bird_mood', 'money', 'first-aid-kit', 'gladiator-kit',
             'on_work', 'on_fight', 'id_of_menu_message']}


def change_stats(message, name='asjgbuebgabeugabueg', starve=-20, fatigue=-20, mood=-5, money=0, text=''):
    if name != 'asjgbuebgabeugabueg': data_users[message.from_user.id][0] = name
    data_users[message.from_user.id][1] += starve
    data_users[message.from_user.id][2] += fatigue
    data_users[message.from_user.id][3] += mood
    data_users[message.from_user.id][4] += money
    if text != '': bot.send_message(message.from_user.id, text)

def is_busy(messageiuserd):
    if data_users[messageiuserd][7] is True:
        bot.send_message(messageiuserd,
                         f'Не получится, птичка на работе')
        return True
    elif data_users[messageiuserd][7] is True:
        bot.send_message(messageiuserd,
                         f'Не получится, птичка на арене')
        return True
    else:
        return False

def buy(messageiuserd, cost, idofitem, amount, successfullytext):
    failtext = f'Недостаточно септимов ({data_users[messageiuserd][4]})'
    if data_users[messageiuserd][4] >= cost:
        data_users[messageiuserd][4] -= cost
        data_users[messageiuserd][idofitem] += amount
        bot.send_message(messageiuserd, successfullytext)
    else:
        bot.send_message(messageiuserd, failtext)

# main menu>
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in data_users and data_users[message.from_user.id][0]:
        bot.send_message(message.from_user.id, 'У тебя уже есть птичка :)\n'
                                               'Чтобы узнать список команд: /help')
    else:
        bot.send_message(message.from_user.id, 'Если ты тут впервые, выбери имя своей птичке: /set_name {имя}\n'
                                               'Чтобы узнать список команд: /help')
        data_users[message.from_user.id] = ['Введите имя', 100, 100, 100, 0, 0, 0, False, False, '']


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, 'Перейти в свой профиль: /my_bird\n'
                                           'Покормить птичку: /feed\n'
                                           'Поиграть с птичкой: /play\n'
                                           'Уложить птичку спать: /sleep\n'
                                           'Зайти в магазин: /shop\n'
                                           'Выбросить птичку: /remove\n'
                                           'Отправить птичку на работу: /work')


@bot.message_handler(commands=['my_bird'])
def my_bird(message):
    try:
        bot.edit_message_text(f'Это твой профиль\n🐦 {data_users[message.from_user.id][0]}\n🍞 {data_users[message.from_user.id][1]}%\n💤 {data_users[message.from_user.id][2]}%\n🎮 {data_users[message.from_user.id][3]}%\n🟡 {data_users[message.from_user.id][4]}\n💊 {data_users[message.from_user.id][5]}\n🗡️🛡️ {data_users[message.from_user.id][6]}', message.from_user.id, data_users[message.from_user.id][9])
    except telebot.apihelper.ApiTelegramException:
        pass

# main menu<

# stats>
@bot.message_handler(commands=['feed'])
def feed(message):
    if message.from_user.id in data_users:
        if not is_busy(message.from_user.id):
            change_stats(message, starve=50, text='Было вкусно')

@bot.message_handler(commands=['sleep'])
def sleep(message):
    if message.from_user.id in data_users:
        if not is_busy(message.from_user.id):
            change_stats(message, fatigue=70, text='Птичка выспалась и готова к полёту')

@bot.message_handler(commands=['play'])
def play(message):
    if message.from_user.id in data_users:
        if not is_busy(message.from_user.id):
            change_stats(message, mood=20, text='Было весело')

@bot.message_handler(commands=['work'])
def work(message):
    if message.from_user.id in data_users:
        if not is_busy(message.from_user.id):
            bot.send_message(message.from_user.id,
                             f'{data_users[message.from_user.id][0]} ушёл на работу. Он занят вернётся через 10 сек.')
            data_users[message.from_user.id][7] = True
            time.sleep(10)
            change_stats(message, starve=0, fatigue=0, mood=0, money=10, text='')
            data_users[message.from_user.id][7] = False
    else:
        pass
# stats<

# other>
@bot.message_handler(commands=['remove'])
def remove(message):
    if message.from_user.id in data_users and data_users[message.from_user.id][0] != '':
        bot.send_message(message.from_user.id, 'Уверены ли вы? /cremove')
    else:
        pass

@bot.message_handler(commands=['cremove'])
def cremove(message):
    if message.from_user.id in data_users:
        change_stats(message, name='', starve=-data_users[message.from_user.id][1],
                     fatigue=-data_users[message.from_user.id][2], mood=-data_users[message.from_user.id][3], money=-data_users[message.from_user.id][4],
                     text='Выкинуть птичку - позор')
    else:
        pass

@bot.message_handler(commands=['shop'])
def shop(message):
    if message.from_user.id in data_users:
        bot.send_message(message.from_user.id, '1) Аптечка - 20sep /buy_first_aid_kit\n'
                                               '2) Набор гладиатора - 40sep /buy_gladiator_kit\n'
                                               '3) Набор еды(+500) - 15sep /buy_food_set\n'
                                               '4) Бочка чая(+500) - 15sep /buy_barrel_of_tea\n'
                                               '5) Набор игрушек(+500) - 15sep /buy_set_of_toys')
    else:
        pass

@bot.message_handler(commands=['oprint'])
def oprint(message):
    print(data_users, sep='\n')
# other<


# shop>
@bot.message_handler(commands=['buy_first_aid_kit'])
def buy_first_aid_kit(message):
    if message.from_user.id in data_users:
        buy(message.from_user.id, 20, 5, 1, f'Теперь у тебя {data_users[message.from_user.id][5]} аптечек(а)')

@bot.message_handler(commands=['buy_gladiator_kit'])
def buy_gladiator_kit(message):
    if message.from_user.id in data_users:
        buy(message.from_user.id, 40, 6, 1, f'Теперь у тебя {data_users[message.from_user.id][6]} набора(ов) гладиатора')

@bot.message_handler(commands=['buy_food_set'])
def buy_food_set(message):
    if message.from_user.id in data_users:
        buy(message.from_user.id, 15, 1, 500, f'🍞 +500')

@bot.message_handler(commands=['buy_barrel_of_tea'])
def buy_barrel_of_tea(message):
    if message.from_user.id in data_users:
        buy(message.from_user.id, 15, 2, 500, f'💤 +500')

@bot.message_handler(commands=['buy_set_of_toys'])
def buy_set_of_toys(message):
    if message.from_user.id in data_users:
        buy(message.from_user.id, 15, 3, 500, f'🎮 +500')

@bot.message_handler(content_types=['text'])
def set_name(message):
    if message.from_user.id in data_users and '/set_name' in message.text:
        data_users[message.from_user.id][0] = message.text[10:]
        bot.send_message(message.from_user.id, f'Имя успешно сменено на {data_users[message.from_user.id][0]}')
        data_users[message.from_user.id][9] = bot.send_message(message.from_user.id, 'Это твой профиль\n'
                                                                                     f'🐦 {data_users[message.from_user.id][0]}\n'
                                                                                     f'🍞 {data_users[message.from_user.id][1]}%\n'
                                                                                     f'💤 {data_users[message.from_user.id][2]}%\n'
                                                                                     f'🎮 {data_users[message.from_user.id][3]}%\n'
                                                                                     f'🟡 {data_users[message.from_user.id][4]}\n'
                                                                                     f'💊 {data_users[message.from_user.id][5]}\n'
                                                                                     f'🗡️🛡️ {data_users[message.from_user.id][6]}').message_id
        bot.pin_chat_message(message.from_user.id, data_users[message.from_user.id][9], True)
    else:
        pass
# shop<



bot.polling(none_stop=True, interval=0)
