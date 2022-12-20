import json
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
        convert_currencies_button = types.KeyboardButton(config.convert_currencies_button)

        markup.add(motivation_button, convert_currencies_button, dont_follow_back_button)
        bot.send_message(
            message.chat.id,
            f'Hello, {message.from_user.first_name} {message.from_user.last_name}'
            f'\n<b>Your id</b>: {message.from_user.id}'
            f'\n<b>Your username</b>: {message.from_user.username}'
            f'\n<b>Your language_code</b>: "{message.from_user.language_code}"',
            reply_markup=markup,
            parse_mode='html'
        )

    elif message.text == '/help':

        help_message = '<b>Here you can</b>: ' \
                       '\n1) Get motivation ' \
                       '\n2) See who didn\'t follow you back at Instagram' \
                       '\n3) Convert currencies'
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

    elif message.text == config.convert_currencies_button:
        msg = bot.send_message(
            message.chat.id,
            '<b>Please enter currencies, following this example</b>: USD to UAH',
            parse_mode='html'
        )
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
    except instaloader.exceptions.QueryReturnedBadRequestException:
        bot.send_message(message.chat.id, 'Oops... Some trouble here')
    except ValueError as ex:
        bot.send_message(message.chat.id, f'{ex}')


def convert_money(message):
    try:
        first = message.text.split('to')[0].strip().upper()
        second = message.text.split('to')[1].strip().upper()
    except IndexError:
        return bot.send_message(message.chat.id, 'Please follow example and try again')

    with open('static/allowed_values/allowed_currencies.json', 'r') as file:
        allowed_values = json.load(file)

    try:
        if first not in allowed_values.keys() or second not in allowed_values.keys():
            raise ValueError('Please make sure you enter right currencies')
    except ValueError as ex:
        bot.send_message(message.chat.id, f'{ex}')
        return bot.send_message(
            message.chat.id,
            f'<b>Available currencies</b>: {", ".join(tuple(allowed_values.keys()))}',
            parse_mode='html'
        )

    msg = bot.send_message(message.chat.id, f'How many {first} do you have?')
    bot.register_next_step_handler(msg, convert_request, value={'first': first, 'second': second})


def convert_request(message, **kwargs):
    first, second = kwargs['value']['first'], kwargs['value']['second']

    if not message.text.isdigit():
        bot.send_message(message.chat.id, f'Please enter amount by numbers')
        msg = bot.send_message(message.chat.id, f'How many {first} do you have?')
        return bot.register_next_step_handler(msg, convert_request, value={'first': first, 'second': second})

    headers = {
        'apikey': config.API_LAYER_TOKEN
    }
    try:
        response = requests.get(f'https://api.apilayer.com/fixer/latest?base={first}&symbols={second}', headers=headers)
        if response.status_code != 200:
            raise ConnectionError('Sorry some problem with connection')
    except ConnectionError as ex:
        return bot.send_message(message.chat.id, f'{ex}')

    data = response.json()
    value_course = round(data['rates'][second], 2)
    converted_money = round(float(message.text) * value_course, 2)
    bot.send_message(
        message.chat.id,
        f'<b>Course {first} is</b>: {value_course}'
        f'\n<b>Here is {message.text} {first}</b>: {converted_money} {second}',
        parse_mode='html')


if __name__ == '__main__':
    bot.polling()
