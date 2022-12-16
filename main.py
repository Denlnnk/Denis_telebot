import random
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
    motivation = types.KeyboardButton('Motivation')
    dont_follow_back = types.KeyboardButton('Don\'t follow back(instagram)')

    markup.add(get_help, motivation, dont_follow_back)
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_motivation(message):
    if message.text == 'Motivation':
        with open('static/motivation/motivation_examples', 'r') as file:
            motivation_text = random.choice(file.readlines()).strip()
            motivation_for_user.insert(0, motivation_text)
            bot.send_message(message.chat.id, f'Here is: {motivation_text}')

    elif message.text == 'Help':
        help_message = '<b>Here you can</b>: \n1) Get motivation'
        bot.send_message(message.chat.id, help_message, parse_mode='html')



bot.infinity_polling()
