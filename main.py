import random
import telebot
import telebot_token
from translate import Translator
from static.motivation import motivation

bot = telebot.TeleBot(telebot_token.token)
motivation_list = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_motivation(message):
    if message.text.lower() in motivation.possible_matches:
        with open('static/motivation/motivation_examples', 'r') as file:
            motivation_text = random.choice(file.readlines()).strip()
            motivation_list.append(motivation_text)
            bot.send_message(message.chat.id, f'Here is: {motivation_text}')

    if message.text.lower() == 'translate':
        translator = Translator(to_lang='Russian')
        bot.send_message(message.chat.id, translator.translate(motivation_list[0]))
        motivation_list.pop(0)


bot.infinity_polling()
