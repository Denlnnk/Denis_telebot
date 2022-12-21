import telebot
import config
from telebot import types
from unfollowers_test import Unfollowers_test
from convert_currencies_test import ConvertCurrenciesTest
from motivation_test import Motivation_test

bot = telebot.TeleBot(config.TOKEN)
buttons = {
    config.MOTIVATION_BUTTON: Motivation_test(),
    config.UNFOLLOWERS_BUTTON: Unfollowers_test(),
    config.CONVERT_CURRENCIES_BUTTON: ConvertCurrenciesTest(),
}


@bot.message_handler(commands=['start', 'help'])
def commands_processing(message):
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        motivation_button = types.KeyboardButton(config.MOTIVATION_BUTTON)
        dont_follow_back_button = types.KeyboardButton(config.UNFOLLOWERS_BUTTON)
        convert_currencies_button = types.KeyboardButton(config.CONVERT_CURRENCIES_BUTTON)

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
    button = message.text
    command = buttons[button]
    command.process_message(message)


if __name__ == '__main__':
    bot.polling()
