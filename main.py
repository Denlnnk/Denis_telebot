import random
import telebot
import telebot_token
from translate import Translator
from static.motivation import motivation

bot = telebot.TeleBot(telebot_token.token)
motivation_for_user = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_motivation(message):
    for matches in motivation.possible_matches:
        if matches in message.text.lower():
            with open('static/motivation/motivation_examples', 'r') as file:
                motivation_text = random.choice(file.readlines()).strip()
                motivation_for_user.append(motivation_text)
                bot.send_message(message.chat.id, f'Here is: {motivation_text}')

    if message.text.lower() == 'translate' and len(motivation_for_user) > 0:
        translator = Translator(to_lang='Russian')
        translated_motivation = translator.translate(motivation_for_user[0])
        bot.send_message(message.chat.id, translated_motivation)
        motivation_for_user.pop(0)

    elif message.text.lower() == 'translate' and len(motivation_for_user) == 0:
        bot.send_message(message.chat.id, 'No motivation to translate')


bot.infinity_polling()
