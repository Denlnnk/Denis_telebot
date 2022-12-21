import json
import requests
import config
from button_process import ButtonProcess


class ButtonConvertCurrencies(ButtonProcess):

    def __init__(self):
        super().__init__()
        self.headers = {
            'apikey': config.API_LAYER_TOKEN,
            'user-agent': config.USER_AGENT
        }

    def process_message(self, message):
        msg = self.bot.send_message(
            message.chat.id,
            '<b>Please enter currencies, following this example</b>: USD to UAH',
            parse_mode='html'
        )
        self.bot.register_next_step_handler(msg, self.convert_money)

    def convert_money(self, message):

        try:
            first = message.text.split('to')[0].strip().upper()
            second = message.text.split('to')[1].strip().upper()
        except IndexError:
            return self.bot.send_message(message.chat.id, 'Please follow example and try again')

        with open('static/allowed_currencies/allowed_currencies.json', 'r') as file:
            allowed_values = json.load(file)

        try:
            if first not in allowed_values.keys() or second not in allowed_values.keys():
                raise ValueError('Please make sure you enter right currencies')
        except ValueError as ex:
            self.bot.send_message(message.chat.id, f'{ex}')
            return self.bot.send_message(
                message.chat.id,
                f'<b>Available currencies</b>: {", ".join(allowed_values.keys())}',
                parse_mode='html'
            )

        msg = self.bot.send_message(message.chat.id, f'How many {first} do you have?')
        self.bot.register_next_step_handler(msg, self.convert_request, value={'first': first, 'second': second})

    def convert_request(self, message, **kwargs):
        first, second = kwargs['value']['first'], kwargs['value']['second']

        if not message.text.isdigit():
            self.bot.send_message(message.chat.id, f'Please enter amount by numbers')
            msg = self.bot.send_message(message.chat.id, f'How many {first} do you have?')
            return self.bot.register_next_step_handler(
                msg, self.convert_request,
                value={'first': first, 'second': second}
            )

        try:
            response = requests.get(f'https://api.apilayer.com/fixer/latest?base={first}&symbols={second}',
                                    headers=self.headers)
            if response.status_code != 200:
                raise ConnectionError('Sorry some problem with connection')
        except ConnectionError as ex:
            return self.bot.send_message(message.chat.id, f'{ex}')

        data = response.json()
        value_course = round(data['rates'][second], 2)
        converted_money = round(float(message.text) * value_course, 2)
        self.bot.send_message(
            message.chat.id,
            f'<b>Course {first} is</b>: {value_course}'
            f'\n<b>Here is {message.text} {first}</b>: {converted_money} {second}',
            parse_mode='html')
