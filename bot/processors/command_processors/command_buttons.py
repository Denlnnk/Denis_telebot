from bot.settings import config
from telebot import types
from bot.processors.abstcract_process.abstract_process import AbstractProcess


class ButtonsCommand(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        if message.from_user.id in config.ADMIN_IDS:
            self.bot.send_message(
                chat_id=message.chat.id,
                text='Choose from the following:',
                reply_markup=self.admin_first_points()
            )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text='Choose from the following:',
                reply_markup=self.user_buttons(message)
            )

    def admin_first_points(self):
        buttons_list = [
            types.InlineKeyboardButton(config.ADMIN_POINT, callback_data=config.ADMIN_POINT),
            types.InlineKeyboardButton(config.USER_POINT, callback_data=config.USER_POINT)
        ]
        reply_markup = types.InlineKeyboardMarkup(self._build_menu(buttons_list, n_cols=2))

        return reply_markup

    def admin_second_points(self):
        buttons_list = [
            types.InlineKeyboardButton(config.ADMIN_ADD_MOTIVATION_BUTTON,
                                       callback_data=config.ADMIN_ADD_MOTIVATION_BUTTON),
            types.InlineKeyboardButton('<-- ' + config.BACK_POINT, callback_data=config.BACK_POINT)
        ]
        reply_markup = types.InlineKeyboardMarkup(self._build_menu(buttons_list, n_cols=1))

        return reply_markup

    def user_buttons(self, message):
        buttons_list = []
        for buttons in config.LIST_OF_USER_BUTTONS:
            buttons_list.append(types.InlineKeyboardButton(buttons, callback_data=buttons))

        if message.from_user.id in config.ADMIN_IDS:
            buttons_list.append(types.InlineKeyboardButton('<-- ' + config.BACK_POINT, callback_data=config.BACK_POINT))

        reply_markup = types.InlineKeyboardMarkup(self._build_menu(buttons_list, n_cols=2))

        return reply_markup

    @staticmethod
    def _build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu
