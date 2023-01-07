from abc import ABC, abstractmethod

from telebot import types

from bot.settings.bot import Bot


class AbstractPoints(ABC):

    def __init__(self):
        self.bot = Bot().get_instance_of_bot()

    @abstractmethod
    def process_call(self, callback: types.CallbackQuery):
        pass
