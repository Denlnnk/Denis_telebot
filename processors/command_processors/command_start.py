from telebot import types

from processors.abstcract_process.abstract_process import AbstractProcess
from processors.command_processors.command_buttons import ButtonsCommand


class StartCommand(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message: types.Message):
        self.bot.send_message(
            message.chat.id,
            f'Hello, {message.from_user.first_name} {message.from_user.last_name}'
            f'\n<b>Your id</b>: {message.from_user.id}'
            f'\n<b>Your username</b>: {message.from_user.username}'
            f'\n<b>Your language_code</b>: "{message.from_user.language_code}"',
            parse_mode='html'
        )
        buttons = ButtonsCommand()
        buttons.process_message(message)
