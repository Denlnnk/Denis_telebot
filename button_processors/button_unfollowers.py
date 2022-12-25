import instaloader
import time
from fpdf import FPDF
from insta_info import Instagram
from abstcract_process.abstract_process import AbstractProcess


class ButtonUnfollowers(AbstractProcess):

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
            unfollowers_amount, unfollowers = Instagram(message.text).get_unfollowers()

            target = message.text
            file_path = f'./static/unfollowers_folder/{target}_unfollowers.pdf'

            self.save_to_pdf(unfollowers, message.text)
            self.bot.send_message(message.chat.id, f'<b>Amount</b>: {unfollowers_amount}', parse_mode='html')
            self.bot.send_document(message.chat.id, open(file_path, 'rb'))

        except instaloader.exceptions.ProfileNotExistsException as ex:
            self.bot.send_message(message.chat.id, f'{ex}')
        except instaloader.exceptions.QueryReturnedBadRequestException:
            self.bot.send_message(message.chat.id, 'Oops... Some trouble here')
        except ValueError as ex:
            self.bot.send_message(message.chat.id, f'{ex}')

    @staticmethod
    def save_to_pdf(difference: set, target: str):
        pdf = FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for unfollowers in difference:
            pdf.write(5, unfollowers)
            pdf.ln()

        pdf.output(f'./static/unfollowers_folder/{target}_unfollowers.pdf')
