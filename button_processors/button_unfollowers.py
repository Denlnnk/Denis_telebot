import instaloader
import time
from insta_info import Instagram
from button_process import ButtonProcess


class ButtonUnfollowers(ButtonProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        self.bot.send_message(message.chat.id, '<b>[ INFO ]</b>\nMake sure account privacy is OFF', parse_mode='html')
        time.sleep(1)
        msg = self.bot.send_message(message.chat.id, 'Write Instagram Username: ')
        self.bot.register_next_step_handler(msg, self.get_unfollowers)

    def get_unfollowers(self, message):
        self.bot.send_message(message.chat.id, 'Working...')
        try:
            difference_length, difference = Instagram(message.text).get_unfollowers()
            dont_follow_back = ', '.join(difference)
            self.bot.send_message(message.chat.id, f'<b>Amount</b>: {difference_length}'
                                                   f'\n<b>They are</b>: '
                                                   f'\n{dont_follow_back}', parse_mode='html')

        except instaloader.exceptions.ProfileNotExistsException as ex:
            self.bot.send_message(message.chat.id, f'{ex}')
        except instaloader.exceptions.QueryReturnedBadRequestException:
            self.bot.send_message(message.chat.id, 'Oops... Some trouble here')
        except ValueError as ex:
            self.bot.send_message(message.chat.id, f'{ex}')
