import telebot
from telebot import types
import time
import pandas as pd
import numpy as np
import random
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
token = config["yatzee"]["token"]

bot = telebot.TeleBot(token)
status = 'none'
game = None


def generate_markup(btn_list):
    markup = types.ReplyKeyboardMarkup(row_width=8, resize_keyboard=True)
    btn_dict = {'1': types.KeyboardButton('1'), '2': types.KeyboardButton('2'), '3': types.KeyboardButton('3'),
                '4': types.KeyboardButton('4'), '5': types.KeyboardButton('5'), '6': types.KeyboardButton('6')
                , 'пара': types.KeyboardButton('пара'), '2 пары': types.KeyboardButton('2 пары'),
                'тройка': types.KeyboardButton('тройка'), 'м. стр': types.KeyboardButton('м. стр'),
                'б. стр': types.KeyboardButton('б. стр'), 'чёт': types.KeyboardButton('чёт')
                , 'нечёт': types.KeyboardButton('нечёт'), 'фул хаус': types.KeyboardButton('фул хаус'),
                'каре': types.KeyboardButton('каре'), 'мусор': types.KeyboardButton('мусор'),
                'ятцы': types.KeyboardButton('ятцы')}

    markup.add(btn_dict['1'] if '1' in btn_list else ' ', btn_dict['2'] if '2' in btn_list else ' ',
               btn_dict['3'] if '3' in btn_list else ' ', btn_dict['4'] if '4' in btn_list else ' ', 
               btn_dict['5'] if '5' in btn_list else ' ', btn_dict['6'] if '6' in btn_list else ' ', 
               btn_dict['пара'] if 'пара' in btn_list else ' ', btn_dict['2 пары'] if '2 пары' in btn_list else ' ', 
               btn_dict['тройка'] if 'тройка' in btn_list else ' ', btn_dict['м. стр'] if 'м. стр' in btn_list else ' ', 
               btn_dict['б. стр'] if 'б. стр' in btn_list else ' ', btn_dict['чёт'] if 'чёт' in btn_list else ' ', 
               btn_dict['нечёт'] if 'нечёт' in btn_list else ' ', btn_dict['фул хаус'] if 'фул хаус' in btn_list else ' ', 
               btn_dict['каре'] if 'каре' in btn_list else ' ', btn_dict['мусор'] if 'мусор' in btn_list else ' ', 
               btn_dict['ятцы'] if 'ятцы' in btn_list else ' ')

    return markup


class Sheet:
    def __init__(self, gamers_names):
        self.table = pd.DataFrame(index=['1', '2', '3', '4', '5', '6', ' ', 'пара', '2 пары', 'тройка', 'м. стр',
                                         'б. стр', 'чёт', 'нечёт', 'фул хаус', 'каре', 'мусор', 'ятцы', 'Сумма:'],
                                  columns=gamers_names)
        self.gamers_names = gamers_names
        self.move = None
        self.current_combination = None
        self.id_massage_move = None
        self.id_massage_table = None
        self.id_massage_start = None
        self.id_massage_information = None
        self.game_log = []

    def insert_in_table(self, number):
        if np.isnan(self.table[self.move][self.current_combination]):
            self.table[self.move][self.current_combination] = int(number)
        else:
            raise Exception
        print(self.table)
        self.game_log.append([self.move, self.current_combination, number])

    def re_move(self):
        if len(self.game_log) > 0:
            self.table[self.game_log[-1][0]][self.game_log[-1][1]] = np.nan
            self.current_combination = None
            self.move = self.game_log[-1][0]
            self.game_log.pop()

    def next_move(self):
        if self.move is None:
            self.move = self.gamers_names[0]
        else:
            if self.gamers_names.index(self.move) == len(self.gamers_names)-1:
                self.move = self.gamers_names[0]
            else:
                self.move = self.gamers_names[self.gamers_names.index(self.move)+1]

        self.current_combination = None

    def sheet_in_text(self):
        dict_available_btn_for_user = {}

        for name in self.table.columns:
            sum_school = self.table[name][:6].sum()
            self.table[name][' '] = sum_school if sum_school < 63 else sum_school + 50
        for name in self.table.columns:
            self.table[name]['Сумма:'] = self.table[name][6:-1].sum()

        final_list_to_list = self.table.iterrows()
        final_list = [self.table.columns.tolist()]
        final_list[0].insert(0, '')

        for index, row in final_list_to_list:
            final_list.append([index] + row.tolist())

        # записываем в словарь все доступные ходы для каждого игрока
        for i in range(len(final_list[0])-1):
            dict_available_btn_for_user[self.table.columns[i]] = []
            for row in final_list[1:]:
                if np.isnan(row[i+1]):
                    dict_available_btn_for_user[self.table.columns[i]].append(row[0])

        # поиск самого длинного имени
        max_len_name = 0
        for name in final_list[0]:
            if len(name) > max_len_name:
                max_len_name = len(name)

        final_text = ''
        for row in final_list:
            for col in row:
                final_text += f'|{col:_^{max_len_name+6}}'
            final_text += '|\n'

        final_text = final_text.replace('nan', '___')
        return final_text, dict_available_btn_for_user


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Для начала игры введите команду /start_game')


@bot.message_handler(commands=['re_move'])
def re_move(message):
    global status
    if len(game.game_log) > 0:
        game.re_move()
        text, combination_for_markup = game.sheet_in_text()

        bot.edit_message_text(text, game.id_massage_table.chat.id, game.id_massage_table.message_id)

        bot.delete_message(game.id_massage_move.chat.id, game.id_massage_move.message_id)
        game.id_massage_move = bot.send_message(message.chat.id, f'Ход игрока: {game.move}',
                                                reply_markup=generate_markup(combination_for_markup[game.move]))

        if game.id_massage_information is not None:
            bot.delete_message(game.id_massage_information.chat.id, game.id_massage_information.message_id)
            game.id_massage_information = None
        status = 'game'
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['start_game'])
def start_message(message):
    global status
    start_text = ['Привет!', 'Добро пожаловать в игру Ятцы', 'Введите через запятую имена игроков: ']
    main_text = bot.send_message(message.chat.id, "👌")
    for text in start_text:
        text_for_edit = ''
        for letter in text:
            time.sleep(0.03)
            text_for_edit += letter
            if letter == ' ':
                continue
            bot.edit_message_text(text_for_edit, main_text.chat.id, main_text.message_id)
        time.sleep(1.3)
    status = 'start_game'


def error_massage(message):
    to_delet = bot.send_message(message.chat.id, 'Неверное число')
    time.sleep(2)
    bot.delete_message(to_delet.chat.id, to_delet.message_id)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=["text"])
def game(message):
    global status, game
    combination = ['1', '2', '3', '4', '5', '6', 'пара', '2 пары', 'тройка', 'м. стр',
                   'б. стр', 'чёт', 'нечёт', 'фул хаус', 'каре', 'мусор', 'ятцы']

    print(message.chat.username, message.text)

    # старт игры
    if ',' in message.text and status == 'start_game':
        gamers = message.text.replace(' ', '').split(',')
        random.shuffle(gamers)
        game = Sheet(gamers)

        text, combination_for_markup = game.sheet_in_text()

        game.next_move()
        game.id_massage_start = bot.send_message(message.chat.id, 'Старт',
                                                 reply_markup=generate_markup(combination_for_markup[game.move]))
        game.id_massage_table = bot.send_message(message.chat.id, text)
        game.id_massage_move = bot.send_message(message.chat.id, f'Ход игрока: {game.move}')
        status = 'game'

    # выбор комбинации
    elif message.text in combination and status == 'game':
        game.current_combination = message.text
        if game.id_massage_information is None:
            game.id_massage_information = bot.send_message(message.chat.id, f'Выбрана комбинация: {message.text}\n'
                                                                        f'Введите число: ')
        else:
            bot.edit_message_text(f'Выбрана комбинация: {message.text}\nВведите число: ',
                                  game.id_massage_information.chat.id, game.id_massage_information.message_id)
        bot.delete_message(message.chat.id, message.message_id)
        status = 'game_input_number'

    # ввод значения
    elif message.text.isnumeric() and status == 'game_input_number':
        try:
            game.insert_in_table(message.text)
            text, combination_for_markup = game.sheet_in_text()
            bot.edit_message_text(text, game.id_massage_table.chat.id, game.id_massage_table.message_id)
        except Exception as exc:
            print(exc)
            error_massage(message)
            if len(game.game_log) > 0:
                game.game_log.pop()
            status = 'game'
            bot.delete_message(game.id_massage_information.chat.id, game.id_massage_information.message_id)
            game.id_massage_information = None
            return

        game.next_move()
        try:
            bot.delete_message(game.id_massage_move.chat.id, game.id_massage_move.message_id)
            game.id_massage_move = bot.send_message(message.chat.id, f'Ход игрока: {game.move}',
                                                    reply_markup=generate_markup(combination_for_markup[game.move]))
        except Exception as exc:
            print(exc)

        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(game.id_massage_information.chat.id, game.id_massage_information.message_id)
        game.id_massage_information = None
        status = 'game'

    else:
        error_massage(message)


if __name__ == '__main__':
    bot.infinity_polling()


# bot.delete_message(main_text.chat.id, main_text.message_id)
# bot.edit_message_text('Пока', main_text.chat.id, main_text.message_id)
