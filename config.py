import os

from dotenv import load_dotenv

load_dotenv()
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_USER')
POSTGRES_USER = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PASSWORD = os.getenv('POSTGRES_DB')
LOG_LEVEL = os.getenv('LOG_LEVEL').upper()
POSTGRES_LOG = bool(LOG_LEVEL) == 'DEBUG'
