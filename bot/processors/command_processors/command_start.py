from bot.processors.abstcract_process.abstract_process import AbstractProcess
from bot.processors.command_processors.command_buttons import ButtonsCommand


class StartCommand(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        self.bot.send_message(
            message.chat.id,
            f'Hello, {message.from_user.first_name} {message.from_user.last_name}\n'
            f'My name is SIGMA | BOT 🤖.\n'
            f'I\'m going to help you with your motivation and give you some helpful advantages\n'
            f'If you are ready. Let\'s start!',
            parse_mode='html'
        )
        buttons = ButtonsCommand()
        buttons.process_message(message)
