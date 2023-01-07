from bot.api_layer import ApiLayer


def test_get_allowed_currencies():
    apilayer = ApiLayer()
    data = apilayer.get_allowed_currencies()

    assert type(data) == dict
    assert len(data) == 170
