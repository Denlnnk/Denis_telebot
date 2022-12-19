import random
import time
import instaloader
import requests
import telebot
import config
from telebot import types
from instagram import Instagram

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def commands_processing(message):
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        motivation_button = types.KeyboardButton(config.motivation_button)
        dont_follow_back_button = types.KeyboardButton(config.unfollowers_button)
        convert_money_button = types.KeyboardButton(config.convert_money_button)

        markup.add(motivation_button, dont_follow_back_button, convert_money_button)
        bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}', reply_markup=markup)

    elif message.text == '/help':
        help_message = '<b>Here you can</b>: ' \
                       '\n1) Get motivation ' \
                       '\n2) See who didn\'t follow you back at Instagram'
        bot.send_message(message.chat.id, help_message, parse_mode='html')


@bot.message_handler(content_types=['text'])
def buttons_processing(message):
    if message.text == config.motivation_button or 'motivation' in message.text.lower():
        with open('static/motivation/motivation_examples', 'r') as file:
            motivation_text = random.choice(file.readlines()).strip()
            bot.send_message(message.chat.id, f'<b>Here is</b>: \n{motivation_text}', parse_mode='html')

    elif message.text == config.unfollowers_button:
        bot.send_message(message.chat.id, '<b>[ INFO ]</b>\nMake sure account privacy is OFF', parse_mode='html')
        time.sleep(1)
        msg = bot.send_message(message.chat.id, 'Write Instagram Username: ')
        bot.register_next_step_handler(msg, get_unfollowers)

    elif message.text == config.convert_money_button:
        msg = bot.send_message(message.chat.id, 'Enter from what to what do u want to convert:')
        bot.register_next_step_handler(msg, convert_money)

    else:
        bot.send_message(message.chat.id, 'Ooops... I\'m so stupid for that :(')


def get_unfollowers(message):
    bot.send_message(message.chat.id, 'Working...')
    try:
        difference_length, difference = Instagram(message.text).get_unfollowers()
        dont_follow_back = ', '.join(difference)
        bot.send_message(message.chat.id, f'<b>Amount</b>: {difference_length}'
                                          f'\n<b>They are</b>: '
                                          f'\n{dont_follow_back}', parse_mode='html')

    except instaloader.exceptions.ProfileNotExistsException as ex:
        bot.send_message(message.chat.id, f'{ex}')
    except ValueError as ex:
        bot.send_message(message.chat.id, f'{ex}')


def convert_money(message):
    first, second = message.text.split(',')
    msg = bot.send_message(message.chat.id, f'How many {first} do u have?')
    bot.register_next_step_handler(msg, convert_request, value={'first': first, 'second': second})


def convert_request(message):
    pass


if __name__ == '__main__':
    bot.polling()
