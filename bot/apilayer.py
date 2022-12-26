import json
import os
import requests
import config


class ApiLayer:

    def __init__(self):
        self.headers = {
            'apikey': os.getenv('API_LAYER_TOKEN'),
            'user-agent': config.USER_AGENT
        }

    def get_allowed_currencies(self):
        response = requests.get('https://api.apilayer.com/fixer/symbols', headers=self.headers)
        data = response.json()

        return data['symbols']

    @staticmethod
    def save_to_file(data):
        with open(
                '/home/denis/PycharmProjects/Denis_telebot/static/allowed_currencies/allowed_currencies.json',
                'w'
        ) as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    api = ApiLayer()
    allowed_currencies = api.get_allowed_currencies()
    api.save_to_file(allowed_currencies)
