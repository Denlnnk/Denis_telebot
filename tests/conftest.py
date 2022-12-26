import pytest

from bot.bot import Bot


@pytest.fixture()
def bot():
    bot = Bot().get_instance_of_bot()
    return bot
