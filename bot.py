import telebot
import config


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Bot(metaclass=SingletonMeta):

    def __init__(self):
        self.bot = None

    def get_instance_of_bot(self):
        if not self.bot:
            self.bot = telebot.TeleBot(config.TOKEN)
        return self.bot
