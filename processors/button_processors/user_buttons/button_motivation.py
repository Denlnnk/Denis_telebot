import random

from telebot import types

from processors.abstcract_process.abstract_process import AbstractProcess


class ButtonMotivation(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message: types.Message):
        with open('static/motivation/motivation_examples', 'r') as file:
            motivation_text = random.choice(file.readlines()).strip()
            self.bot.send_message(message.chat.id, f'<b>Here is</b>: \n{motivation_text}', parse_mode='html')
