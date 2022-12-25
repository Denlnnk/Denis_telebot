from telebot import types

import config
from abstcract_process.abstract_process import AbstractProcess


class StartCommand(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        motivation_button = types.KeyboardButton(config.MOTIVATION_BUTTON)
        dont_follow_back_button = types.KeyboardButton(config.UNFOLLOWERS_BUTTON)
        convert_currencies_button = types.KeyboardButton(config.CONVERT_CURRENCIES_BUTTON)

        if message.from_user.id in config.ADMIN_IDS:
            admin_add_motivation = types.KeyboardButton(config.ADMIN_ADD_MOTIVATION_BUTTON)
            markup.add(motivation_button, convert_currencies_button, dont_follow_back_button, admin_add_motivation)
        else:
            markup.add(motivation_button, convert_currencies_button, dont_follow_back_button)

        self.bot.send_message(
            message.chat.id,
            f'Hello, {message.from_user.first_name} {message.from_user.last_name}'
            f'\n<b>Your id</b>: {message.from_user.id}'
            f'\n<b>Your username</b>: {message.from_user.username}'
            f'\n<b>Your language_code</b>: "{message.from_user.language_code}"',
            reply_markup=markup,
            parse_mode='html'
        )
