import os
from settings import config
from dotenv import load_dotenv

load_dotenv()


def test_is_in_config_buttons():
    assert config.MOTIVATION_BUTTON
    assert config.UNFOLLOWERS_BUTTON
    assert config.CONVERT_CURRENCIES_BUTTON
    assert config.USER_AGENT


def test_is_in_env():
    assert 'TOKEN' in os.environ
    assert 'INSTA_USERNAME' in os.environ
    assert 'INSTA_PASSWORD' in os.environ
    assert 'API_LAYER_TOKEN' in os.environ
