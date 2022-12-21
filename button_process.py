import telebot
import config
from abc import ABC, abstractmethod


class ButtonProcess(ABC):

    def __init__(self):
        self.bot = telebot.TeleBot(config.TOKEN)

    @abstractmethod
    def process_message(self, message):
        pass
