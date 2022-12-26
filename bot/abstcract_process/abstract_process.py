from abc import ABC, abstractmethod
from bot.bot import Bot


class AbstractProcess(ABC):

    def __init__(self):
        self.bot = Bot().get_instance_of_bot()

    @abstractmethod
    def process_message(self, message):
        pass
