import config
from api import api_methods


def send_message(message):
    api_url = f'https://api.telegram.org/bot{config.TELEGRAM_API_TOKEN}/sendMessage'

    api_methods.post(api_url, json={'chat_id': int(config.TELEGRAM_CHAT_ID), 'text': message}, code=200)
