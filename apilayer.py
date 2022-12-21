import json
import requests
import config


class ApiLayer:

    def __init__(self):
        self.headers = {
            'apikey': config.API_LAYER_TOKEN,
            'user-agent': config.USER_AGENT
        }

    def get_allowed_currencies(self):
        response = requests.get('https://api.apilayer.com/fixer/symbols', headers=self.headers)
        data = response.json()
        allowed_values = data['symbols']

        with open('static/allowed_currencies/allowed_currencies.json', 'w') as file:
            json.dump(allowed_values, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    api = ApiLayer()
    api.get_allowed_currencies()
