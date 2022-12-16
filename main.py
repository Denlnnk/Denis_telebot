import random

import instaloader
import telebot
import konfig
from telebot import types
from insta_unfollow import get_unfollowers

bot = telebot.TeleBot(konfig.token)
motivation_for_user = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    get_help = types.KeyboardButton('Help')
    motivation = types.KeyboardButton('Give motivation')
    dont_follow_back = types.KeyboardButton('Who didn\'t follow back')

    markup.add(get_help, motivation, dont_follow_back)
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_motivation(message):
    if message.text == 'Give motivation':
        with open('static/motivation/motivation_examples', 'r') as file:
            motivation_text = random.choice(file.readlines()).strip()
            motivation_for_user.insert(0, motivation_text)
            bot.send_message(message.chat.id, f'Here is: <b>{motivation_text}</b>', parse_mode='html')

    elif message.text == 'Help':
        help_message = '<b>Here you can</b>: \n1) Get motivation'
        bot.send_message(message.chat.id, help_message, parse_mode='html')

    elif message.text == 'Who didn\'t follow back':
        bot.send_message(message.chat.id, 'Make sure <b>account privacy</b> is <b>off</b>', parse_mode='html')
        msg = bot.send_message(message.chat.id, 'Write Instagram Username: ')
        bot.register_next_step_handler(msg, unfollowers)


def unfollowers(message):
    bot.send_message(message.chat.id, 'Working...')
    try:
        dont_follow_back = ', '.join(get_unfollowers(message.text))
        bot.send_message(message.chat.id, f'<b>They are</b>: {dont_follow_back}', parse_mode='html')
    except instaloader.exceptions.ProfileNotExistsException as ex:
        bot.send_message(message.chat.id, f'{ex}')


bot.infinity_polling()
