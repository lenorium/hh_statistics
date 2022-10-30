import os
from datetime import datetime

from dotenv import load_dotenv, dotenv_values

load_dotenv()
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
LOG_LEVEL = os.getenv('LOG_LEVEL').upper()
POSTGRES_LOG = LOG_LEVEL == 'DEBUG'

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

__search = dotenv_values('.env.search')
SEARCH_TEXT = __search['text']
SEARCH_FIELD = __search['search_field']
SEARCH_AREA = int(__search['area'])
SEARCH_PER_PAGE = int(__search['per_page'])
SEARCH_ORDER_BY = __search['order_by']
SEARCH_DATE_TO = datetime.strptime(__search['date_to'], 'DD.MM.YYYY H:mm:ss') \
    if 'date_to' in __search and __search['date_to'] else datetime.now()
SEARCH_TIME_DELTA = int(__search['time_delta'])
SEARCH_URL = __search['url']
