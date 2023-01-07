from bot.settings import config
from bot.settings.bot import Bot
from dotenv import load_dotenv

from bot.processors.command_processors.command_start import StartCommand
from bot.processors.command_processors.command_help import HelpCommand
from bot.processors.command_processors.command_buttons import ButtonsCommand

from bot.processors.callback_processors.callback_admin import AdminPoint
from bot.processors.callback_processors.callback_back import BackPoint
from bot.processors.callback_processors.callback_user import UserPoint

from bot.processors.button_processors.user_buttons.button_unfollowers import ButtonUnfollowers
from bot.processors.button_processors.user_buttons.button_convert_currencies import ButtonConvertCurrencies
from bot.processors.button_processors.user_buttons.button_motivation import ButtonMotivation
from bot.processors.voice_processors.voice_process import AudioTest

from bot.processors.button_processors.admin_buttons.admin_add_motivation import AddMotivation

bot = Bot().get_instance_of_bot()
load_dotenv()


@bot.message_handler(commands=['start', 'help', 'buttons'])
def commands_processing(message):
    commands = {
        config.START_COMMAND: StartCommand(),
        config.HELP_COMMAND: HelpCommand(),
        config.BUTTONS_COMMAND: ButtonsCommand()
    }
    command_name = message['text']
    command_process = commands[command_name]
    command_process.process_message(message)


@bot.callback_query_handler(
    func=lambda call: call.data in config.LIST_OF_USER_BUTTONS or call.data in config.LIST_OF_ADMIN_BUTTONS
)
def buttons_call_back(call):
    if call.data in config.LIST_OF_USER_BUTTONS:
        buttons_processing(call.message, button_name=call.data)
    elif call.data in config.LIST_OF_ADMIN_BUTTONS:
        admin_processing(call.message, button_name=call.data)


@bot.callback_query_handler(func=lambda call: call.data in config.LIST_OF_POINTS)
def points_call_back(call):
    points = {
        config.ADMIN_POINT: AdminPoint(),
        config.USER_POINT: UserPoint(),
        config.BACK_POINT: BackPoint()
    }

    print(f'Received call {call}')
    point_process = points[call['data']]
    point_process.process_call(call)


@bot.message_handler(func=lambda message: message["from"]["id"] in config.ADMIN_IDS)
def admin_processing(message, button_name: str = None):
    buttons = {
        config.ADMIN_ADD_MOTIVATION_BUTTON: AddMotivation(),
    }
    button_process = buttons[button_name]
    button_process.process_message(message)


@bot.message_handler(content_types=['text'])
def text_processing(message):
    bot.send_message(message['chat']['id'], 'Sorry, now i work only with buttons')


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    audio_process = AudioTest()
    audio_process.process_message(message)


def buttons_processing(message, button_name: str = None):
    buttons = {
        config.MOTIVATION_BUTTON: ButtonMotivation(),
        config.UNFOLLOWERS_BUTTON: ButtonUnfollowers(),
        config.CONVERT_CURRENCIES_BUTTON: ButtonConvertCurrencies()
    }
    button_process = buttons[button_name]
    button_process.process_message(message)


if __name__ == '__main__':
    bot.polling()
