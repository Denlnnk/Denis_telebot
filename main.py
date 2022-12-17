import random
import instaloader
import telebot
import config
from telebot import types
from instagram import Instagram

bot = telebot.TeleBot(config.token)
motivation_for_user = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    get_help = types.KeyboardButton(config.help_button)
    motivation = types.KeyboardButton(config.motivation_button)
    dont_follow_back = types.KeyboardButton(config.unfollowers_button)

    markup.add(get_help, motivation, dont_follow_back)
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_motivation(message):
    if message.text == config.motivation_button or 'motivation' in message.text.lower():
        with open('static/motivation/motivation_examples', 'r') as file:
            motivation_text = random.choice(file.readlines()).strip()
            motivation_for_user.insert(0, motivation_text)
            bot.send_message(message.chat.id, f'<b>Here is</b>: \n{motivation_text}', parse_mode='html')

    elif message.text == config.help_button:
        help_message = '<b>Here you can</b>: ' \
                       '\n1) Get motivation ' \
                       '\n2) See who didn\'t follow you back at Instagram'
        bot.send_message(message.chat.id, help_message, parse_mode='html')

    elif message.text == config.unfollowers_button:
        bot.send_message(message.chat.id, '<b>[Info]</b>Make sure account privacy is OFF', parse_mode='html')
        msg = bot.send_message(message.chat.id, 'Write Instagram Username: ')
        bot.register_next_step_handler(msg, get_unfollowers)
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


bot.polling()
