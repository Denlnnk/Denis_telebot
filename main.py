import config
from bot import Bot
from dotenv import load_dotenv

from command_processors.command_start import StartCommand
from command_processors.command_help import HelpCommand
from command_processors.command_buttons import ButtonsCommand

from button_processors.button_unfollowers import ButtonUnfollowers
from button_processors.button_convert_currencies import ButtonConvertCurrencies
from button_processors.button_motivation import ButtonMotivation
from button_processors.button_audio_test import AudioTest

from admin_processors.admin_add_motivation import AddMotivation

bot = Bot().get_instance_of_bot()
load_dotenv()


@bot.message_handler(commands=['start', 'help', 'buttons'])
def commands_processing(message):
    commands = {
        config.START_COMMAND: StartCommand(),
        config.HELP_COMMAND: HelpCommand(),
        config.BUTTONS_COMMAND: ButtonsCommand()
    }
    command_name = message.text
    command_process = commands[command_name]
    command_process.process_message(message)


@bot.callback_query_handler(
    func=lambda call: call.data in config.LIST_OF_BUTTONS or call.data in config.LIST_OF_ADMIN_BUTTONS)
def call_back(call):
    if call.message:
        if call.data in config.LIST_OF_BUTTONS:
            buttons_processing(call.message, button_name=call.data)
        elif call.data in config.LIST_OF_ADMIN_BUTTONS:
            admin_processing(call.message, button_name=call.data)


@bot.message_handler(func=lambda message: message.from_user.id in config.ADMIN_IDS, content_types=['text'])
def admin_processing(message, button_name: str = None):
    buttons = {
        config.ADMIN_ADD_MOTIVATION_BUTTON: AddMotivation(),
        config.MOTIVATION_BUTTON: ButtonMotivation(),
        config.UNFOLLOWERS_BUTTON: ButtonUnfollowers(),
        config.CONVERT_CURRENCIES_BUTTON: ButtonConvertCurrencies()
    }
    if button_name:
        button_process = buttons[button_name]
        button_process.process_message(message)
    elif message.text not in buttons:
        bot.send_message(message.chat.id, 'Sorry, now i work only with buttons')
    else:
        button_name = message.text
        button_process = buttons[button_name]
        button_process.process_message(message)


@bot.message_handler(content_types=['text'])
def buttons_processing(message, button_name: str = None):
    buttons = {
        config.MOTIVATION_BUTTON: ButtonMotivation(),
        config.UNFOLLOWERS_BUTTON: ButtonUnfollowers(),
        config.CONVERT_CURRENCIES_BUTTON: ButtonConvertCurrencies()
    }
    if button_name:
        button_process = buttons[button_name]
        button_process.process_message(message)
    elif message.text not in buttons:
        bot.send_message(message.chat.id, 'Sorry, now i work only with buttons')
    else:
        button_name = message.text
        button_process = buttons[button_name]
        button_process.process_message(message)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    audio_process = AudioTest()
    audio_process.process_message(message)


if __name__ == '__main__':
    bot.delete_webhook()
    bot.polling()
