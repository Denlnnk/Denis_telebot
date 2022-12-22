import pytest
from bot import Bot


@pytest.fixture()
def bot():
    return Bot().get_instance_of_bot()


def test_is_same_instances(bot):
    bot1 = bot
    bot2 = bot
    assert bot1 == bot2
    assert bot1 is bot2
