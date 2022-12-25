from abstcract_process.abstract_process import AbstractProcess


class AddMotivation(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        msg = self.bot.send_message(message.chat.id, 'Enter motivation that you want to add: ')
        self.bot.register_next_step_handler(msg, self.add_motivation)

    def add_motivation(self, message):
        with open('./static/motivation/motivation_examples', 'a') as file:
            file.write('\n' + '"' + message.text + '"')

        self.bot.send_message(message.chat.id, 'Motivation added successfully')
