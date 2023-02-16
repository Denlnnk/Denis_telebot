from datetime import datetime

from dotenv import load_dotenv

from bot.settings.bot import Bot
from settings import config
from telebot import types

from bot.processors.voice_processors.voice_process import VoiceProcess

from bot.processors.command_processors.command_start import StartCommand
from bot.processors.command_processors.command_help import HelpCommand
from bot.processors.command_processors.command_buttons import ButtonsCommand

from bot.processors.callback_processors.callback_admin import AdminPoint
from bot.processors.callback_processors.callback_back import BackPoint
from bot.processors.callback_processors.callback_user import UserPoint

from bot.processors.button_processors.user_buttons.button_convert_currencies import ButtonConvertCurrencies
from bot.processors.button_processors.user_buttons.button_unfollowers import ButtonUnfollowers
from bot.processors.button_processors.user_buttons.button_motivation import ButtonMotivation

from bot.processors.button_processors.admin_buttons.admin_add_motivation import AddMotivation

from database.database import UserDatabase, UserQueryDatabase
# TODO Разобраться со всеми импортами, чтоб работало через терминал, посмотреть логику всего бота, залогировать все
load_dotenv()
bot = Bot().get_instance_of_bot()
user_database = UserDatabase()
user_query_database = UserQueryDatabase()


@bot.message_handler(commands=['start', 'help', 'buttons'])
def commands_processing(message: types.Message) -> None:
    if not user_database.check_if_user_exist(user_id=message.from_user.id):
        try:
            username = message.from_user.username
        except ValueError:
            username = "Default"

        user_database.save_user_to_db(
            user_id=message.from_user.id,
            username=username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            active=True,
            register_at=datetime.now()
        )
    commands = {
        config.START_COMMAND: StartCommand(),
        config.HELP_COMMAND: HelpCommand(),
        config.BUTTONS_COMMAND: ButtonsCommand()
    }
    command_name = message.text
    command_process = commands[command_name]
    command_process.process_message(message)


@bot.callback_query_handler(
    func=lambda call: call.data in config.LIST_OF_USER_BUTTONS or call.data in config.LIST_OF_ADMIN_BUTTONS
)
def buttons_call_back(call: types.CallbackQuery) -> None:
    if call.data in config.LIST_OF_USER_BUTTONS:
        buttons_processing(call.message, button_name=call.data)
    elif call.data in config.LIST_OF_ADMIN_BUTTONS:
        admin_processing(call.message, button_name=call.data)


@bot.callback_query_handler(func=lambda call: call.data in config.LIST_OF_POINTS)
def points_call_back(call: types.CallbackQuery) -> None:
    points = {
        config.ADMIN_POINT: AdminPoint(),
        config.USER_POINT: UserPoint(),
        config.BACK_POINT: BackPoint()
    }
    point_process = points[call.data]
    point_process.process_call(call)


@bot.message_handler(func=lambda message: message.from_user.id in config.ADMIN_IDS)
def admin_processing(message: types.Message, button_name: str = None):
    buttons = {
        config.ADMIN_ADD_MOTIVATION_BUTTON: AddMotivation(),
    }
    button_process = buttons[button_name]
    button_process.process_message(message)


@bot.message_handler(content_types=['text'])
def text_processing(message: types.Message):
    bot.send_message(message.chat.id, 'Sorry, now i work only with buttons')


@bot.message_handler(content_types=['voice'])
def voice_processing(message: types.Message):
    audio_process = VoiceProcess()
    audio_process.process_message(message)


def buttons_processing(message: types.Message, button_name: str = None):
    buttons = {
        config.MOTIVATION_BUTTON: ButtonMotivation(),
        config.UNFOLLOWERS_BUTTON: ButtonUnfollowers(),
        config.CONVERT_CURRENCIES_BUTTON: ButtonConvertCurrencies()
    }
    button_process = buttons[button_name]
    button_process.process_message(message)
