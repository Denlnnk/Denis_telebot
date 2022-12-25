from abstcract_process.abscract_points import AbstractPoints
from command_processors.command_buttons import ButtonsCommand


class BackPoint(AbstractPoints):

    def __init__(self):
        super().__init__()

    def process_call(self, callback):
        self.bot.edit_message_reply_markup(
            chat_id=callback["message"]["chat"]["id"],
            message_id=callback["message"]["id"],
            reply_markup=ButtonsCommand().admin_first_points()
        )
