import json

from main import commands_processing, buttons_processing


def lambda_handler(event, context):
    message = event['message']
    text = message['text']
    if text in ['/start', '/help']:
        commands_processing(message)
    else:
        buttons_processing(message)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
