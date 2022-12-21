import config
from dotenv import load_dotenv
from telebot import types
from bot import Bot
from button_processors.button_unfollowers import ButtonUnfollowers
from button_processors.button_convert_currencies import ButtonConvertCurrencies
from button_processors.button_motivation import ButtonMotivation

load_dotenv()
bot = Bot().get_instance_of_bot()


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
    buttons = {
        config.MOTIVATION_BUTTON: ButtonMotivation(),
        config.UNFOLLOWERS_BUTTON: ButtonUnfollowers(),
        config.CONVERT_CURRENCIES_BUTTON: ButtonConvertCurrencies(),
    }
    button_name = message.text
    button_process = buttons[button_name]
    button_process.process_message(message)


if __name__ == '__main__':
    bot.polling()
