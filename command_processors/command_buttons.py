import config
from telebot import types
from abstcract_process.abstract_process import AbstractProcess


class ButtonsCommand(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        buttons_list = []
        for buttons in config.LIST_OF_BUTTONS:
            buttons_list.append(types.InlineKeyboardButton(buttons, callback_data=buttons))

        if message.from_user.id in config.ADMIN_IDS:
            buttons_list.append(types.InlineKeyboardButton(
                config.ADMIN_ADD_MOTIVATION_BUTTON,
                callback_data=config.ADMIN_ADD_MOTIVATION_BUTTON)
            )

        reply_markup = types.InlineKeyboardMarkup(self.build_menu(buttons_list, n_cols=2))

        self.bot.send_message(
            chat_id=message.chat.id,
            text='Choose from the following:',
            reply_markup=reply_markup
        )

    @staticmethod
    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu
