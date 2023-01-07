from art import text2art
from bot.processors.abstcract_process.abstract_process import AbstractProcess


class HelpCommand(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        art = text2art("Bot")
        help_message = '\n<b>Here you can</b>: ' \
                       '\n1) Get motivation ' \
                       '\n2) See who didn\'t follow you back at Instagram' \
                       '\n3) Convert currencies'

        self.bot.send_message(message["chat"]["id"], art)
        self.bot.send_message(message["chat"]["id"], help_message, parse_mode='html')
