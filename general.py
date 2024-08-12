import telebot
from telebot import types
import time
import random

bot = telebot.TeleBot('TOKEN')
data_users = {
    'Egor': ['bird_name', 'bird_starve', 'bird_fatigue', 'bird_mood', 'money', 'first-aid-kit', 'gladiator-kit',
             'on_work', 'on_arena']}


def change_stats(message, name='asjgbuebgabeugabueg', starve=-20, fatigue=-20, mood=-5, money=0, text=''):
    if name != 'asjgbuebgabeugabueg':
        data_users[message.from_user.id][0] = name
    data_users[message.from_user.id][1] += starve
    data_users[message.from_user.id][2] += fatigue
    data_users[message.from_user.id][3] += mood
    data_users[message.from_user.id][4] += money
    if text != '':
        bot.send_message(message.from_user.id, text)


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
        data_users[message.from_user.id] = ['Ваша птичка', 100, 100, 100, 0, 0, 0, False, False]


@bot.message_handler(commands=['menu'])
def menu(message):
    with open('C:\\Users\\Windows\\PycharmProjects\\MineProjects3.10\\pictures\\main.jpg', 'rb') as img:
        bot.send_photo(message.from_user.id, img)
    img.close()
    name_of_bird = ("Ваша птичка" if data_users[message.from_user.id][0] == '' else data_users[message.from_user.id][0])
    keyboard = types.InlineKeyboardMarkup()

    button_bird = types.InlineKeyboardButton(text=name_of_bird, callback_data="button_bird")
    button_arena = types.InlineKeyboardButton(text="Арена", callback_data="button_arena")
    button_shop = types.InlineKeyboardButton(text="Магазин", callback_data="button_shop")
    button_work = types.InlineKeyboardButton(text="Работа", callback_data="button_work")
    button_name = types.InlineKeyboardButton(text="Сменить имя", callback_data="button_name")
    keyboard.add(button_bird)
    keyboard.row(button_arena, button_shop)
    keyboard.row(button_work, button_name)
    bot.send_message(message.from_user.id, 'Меню', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "button_bird":
            my_bird(call)
        elif call.data == "button_arena":
            arena(call)
        elif call.data == "button_shop":
            shop(call)
        elif call.data == "button_work":
            work(call)
        elif call.data == "button_name":
            bot.send_message(call.from_user.id, "Пока не готово")
        elif call.data == "button_feed":
            feed(call)
        elif call.data == "button_play":
            play(call)
        elif call.data == "button_sleep":
            sleep(call)
        elif call.data == "button_status":
            switch_status(call)
        elif call.data == "button_search":
            find_opponent(call)
        elif call.data == "button_rating":
            bot.send_message(call.from_user.id, "Пока не готово")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, 'Перейти в свой профиль: /my_bird\n'
                                           'Покормить птичку: /feed\n'
                                           'Поиграть с птичкой: /play\n'
                                           'Уложить птичку спать: /sleep\n'
                                           'Зайти в магазин: /shop\n'
                                           'Выбросить птичку: /remove\n'
                                           'Сразиться на арене: /find_opponent\n'
                                           'Отправить птичку на работу: /work')


@bot.message_handler(commands=['my_bird'])
def my_bird(message):
    with open('C:\\Users\\Windows\\PycharmProjects\\MineProjects3.10\\pictures\\bird.png', 'rb') as img:
        bot.send_photo(message.from_user.id, img)
    img.close()
    keyboard = types.InlineKeyboardMarkup()

    button_feed = types.InlineKeyboardButton(text="Есть", callback_data="button_feed")
    button_sleep = types.InlineKeyboardButton(text="Спать", callback_data="button_sleep")
    button_play = types.InlineKeyboardButton(text="Играть", callback_data="button_play")
    keyboard.add(button_feed)
    keyboard.add(button_sleep)
    keyboard.add(button_play)
    bot.send_message(message.from_user.id, f'Это твой профиль\n'
                                           f'🐦 {data_users[message.from_user.id][0]}\n'
                                           f'🍞 {data_users[message.from_user.id][1]}%\n'
                                           f'💤 {data_users[message.from_user.id][2]}%\n'
                                           f'🎮 {data_users[message.from_user.id][3]}%\n'
                                           f'🟡 {data_users[message.from_user.id][4]}\n'
                                           f'💊 {data_users[message.from_user.id][5]}\n'
                                           f'🗡️🛡️ {data_users[message.from_user.id][6]}', reply_markup=keyboard)


# main menu<

# arena
def arena(message):
    keyboard = types.InlineKeyboardMarkup()
    button_status = types.InlineKeyboardButton(text="Сменить статус", callback_data="button_status")
    button_search = types.InlineKeyboardButton(text="Искать противника", callback_data="button_search")
    button_rating = types.InlineKeyboardButton(text="Рейтинг", callback_data="button_rating")
    keyboard.row(button_status, button_rating)
    keyboard.add(button_search)
    bot.send_message(message.from_user.id, f'Это арена, здесь вы можете сразиться с другими птицами за место в рейтинге и золотые горы', reply_markup=keyboard)


@bot.message_handler(commands=['switch_status'])
def switch_status(message):
    data_users[message.from_user.id][8] = not data_users[message.from_user.id][8]
    bot.send_message(message.from_user.id, (
        "Вы выставили птичку на арену" if data_users[message.from_user.id][8] else "Вы вернули птичку с арены"))


@bot.message_handler(commands=['find_opponent'])
def find_opponent(message):
    for i in data_users:
        if data_users[i][8] and i != message.from_user.id and i != "Egor":
            bot.send_message(message.from_user.id, "Противник найден, бой начался")
            data_users[message.from_user.id][8] = True
            data_users[i][8] = True
            fight(message.from_user.id, i)
            data_users[message.from_user.id][8] = False
            data_users[i][8] = False
            break
    bot.send_message(message.from_user.id, "Противников не найдено")


def fight(first_id, second_id):
    log_of_fight = ''
    rounds = 0
    firstp = random.choice([first_id, second_id])
    secondp = first_id if firstp != first_id else second_id
    first_health, second_health = 100, 100
    who_attack = True
    while first_health > 0 and second_health > 0:
        rounds += 1
        log_of_fight += '\n\n РАУНД ' + str(rounds) + '\n'
        if who_attack:
            stagelog = stage(firstp)
            log_of_fight += stagelog[1]
            second_health = int(protection(secondp, stagelog[0], second_health))
            who_attack = False
            log_of_fight += f'\n У {data_users[secondp][0]} осталось {second_health} hp'
        else:
            stagelog = stage(secondp)
            log_of_fight += stagelog[1]
            first_health = int(protection(firstp, stagelog[0], first_health))
            who_attack = True
            log_of_fight += f'\n У {data_users[firstp][0]} осталось {first_health} hp'
    log_of_fight += '\n\n КОНЕЦ БИТВЫ'
    winner = (first_id if first_health > 0 else second_id)
    loser = (second_id if second_health > 0 else first_id)
    with open('C:\\Users\\Windows\\PycharmProjects\\MineProjects3.10\\pictures\\win.png', 'rb') as img:
        bot.send_photo(winner, img)
    img.close()
    bot.send_message(winner,
                     log_of_fight + f"\n\n Поздравляю с победой. Вы получаете {data_users[loser][4] / 20 + 10}sep")
    with open('C:\\Users\\Windows\\PycharmProjects\\MineProjects3.10\\pictures\\lose.png', 'rb') as img:
        bot.send_photo(loser, img)
    img.close()
    bot.send_message(loser,
                     log_of_fight + f"Сожалею, вы проиграли. В результате битвы были утеряны {data_users[loser][4] / 20}sep")
    data_users[winner][4] += data_users[loser][4] / 20 + 10
    data_users[loser][4] -= data_users[loser][4] / 20


def protection(player, damage, playerhp):
    if data_users[player][6] >= 1:
        if ((10 <= damage <= 14) or (20 < damage < 28)) and random.randint(0, 100) >= 50:
            data_users[player][6] -= 1
            return playerhp - damage / 2
    return playerhp - damage


def stage(player):
    damage = random.randint(0, 14)
    a = random.randint(0, 100)
    if a >= 85:
        damage *= 2
        log = f'\n {data_users[player][0]} НАНОСИТ КРИТ УРОН {damage}'
    elif a < 15:
        log = f'\n {data_users[player][0]} не попал'
        damage = 0
    else:
        log = f'\n {data_users[player][0]} наносит урон {damage}'
    return [damage, log]


# stats>
@bot.message_handler(commands=['feed'])
def feed(message):
    if message.from_user.id in data_users:
        if not is_busy(message.from_user.id):
            with open('C:\\Users\\Windows\\PycharmProjects\\MineProjects3.10\\pictures\\eat.png', 'rb') as img:
                bot.send_photo(message.from_user.id, img)
            img.close()
            change_stats(message, starve=50, text='Было вкусно')


@bot.message_handler(commands=['sleep'])
def sleep(message):
    if message.from_user.id in data_users:
        if not is_busy(message.from_user.id):
            with open('C:\\Users\\Windows\\PycharmProjects\\MineProjects3.10\\pictures\\sleep.png', 'rb') as img:
                bot.send_photo(message.from_user.id, img)
            img.close()
            change_stats(message, fatigue=70, text='Птичка выспалась и готова к полёту')


@bot.message_handler(commands=['play'])
def play(message):
    if message.from_user.id in data_users:
        if not is_busy(message.from_user.id):
            with open('C:\\Users\\Windows\\PycharmProjects\\MineProjects3.10\\pictures\\play.png', 'rb') as img:
                bot.send_photo(message.from_user.id, img)
            img.close()
            change_stats(message, mood=20, text='Было весело')


@bot.message_handler(commands=['work'])
def work(message):
    if message.from_user.id in data_users:
        if not is_busy(message.from_user.id):
            with open('C:\\Users\\Windows\\PycharmProjects\\MineProjects3.10\\pictures\\work.png', 'rb') as img:
                bot.send_photo(message.from_user.id, img)
            img.close()
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
                     fatigue=-data_users[message.from_user.id][2], mood=-data_users[message.from_user.id][3],
                     money=-data_users[message.from_user.id][4],
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
def oprint(self):
    print(data_users, sep='\n')

@bot.message_handler(commands=['test_bot'])
def test_bot(self):
    data_users[1192563050] = ['test_bot', 100, 100, 100, 0, 0, 125, False, True]
# other<


# shop>
@bot.message_handler(commands=['buy_first_aid_kit'])
def buy_first_aid_kit(message):
    if message.from_user.id in data_users:
        buy(message.from_user.id, 20, 5, 1, f'Теперь у тебя {data_users[message.from_user.id][5]} аптечек(а)')


@bot.message_handler(commands=['buy_gladiator_kit'])
def buy_gladiator_kit(message):
    if message.from_user.id in data_users:
        buy(message.from_user.id, 40, 6, 1,
            f'Теперь у тебя {data_users[message.from_user.id][6]} набора(ов) гладиатора')


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


# shop<


bot.polling(none_stop=True, interval=0)
