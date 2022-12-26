from bot.abstcract_process.abstract_process import AbstractProcess
from bot.command_processors.command_buttons import ButtonsCommand


class StartCommand(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        self.bot.send_message(
            message["chat"]["id"],
            f'Hello, {message["from"]["first_name"]} {message["from"]["last_name"]}'
            f'\n<b>Your id</b>: {message["from"]["id"]}'
            f'\n<b>Your username</b>: {message["from"]["username"]}'
            f'\n<b>Your language_code</b>: "{message["from"]["language_code"]}"',
            parse_mode='html'
        )
        buttons = ButtonsCommand()
        buttons.process_message(message)
