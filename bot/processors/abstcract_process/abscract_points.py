from abc import ABC, abstractmethod

from bot.settings.bot import Bot


class AbstractPoints(ABC):

    def __init__(self):
        self.bot = Bot().get_instance_of_bot()

    @abstractmethod
    def process_call(self, callback):
        pass
