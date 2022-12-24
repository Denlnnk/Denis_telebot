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
        allowed_currencies = data['symbols']

        return allowed_currencies

    @staticmethod
    def save_to_file(allowed_currencies):
        with open('/home/denis/PycharmProjects/Denis_telebot/static/allowed_currencies/allowed_currencies.json', 'w') as file:
            json.dump(allowed_currencies, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    api = ApiLayer()
    data = api.get_allowed_currencies()
