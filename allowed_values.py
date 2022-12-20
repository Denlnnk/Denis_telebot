import json
import requests
import config


def get_allowed_values():
    headers = {
        'apikey': config.API_LAYER_TOKEN
    }
    response = requests.get('https://api.apilayer.com/fixer/symbols', headers=headers)
    data = response.json()
    allowed_values = data['symbols']

    with open('static/allowed_values/allowed_values.json', 'w') as file:
        json.dump(allowed_values, file, ensure_ascii=False, indent=4)
