import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from models import Base


class DbInstance:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            database = {
                'drivername': 'postgresql+psycopg2',
                'host': os.getenv('POSTGRES_HOST'),
                'port': os.getenv('POSTGRES_PORT'),
                'username': os.getenv('POSTGRES_USER'),
                'password': os.getenv('POSTGRES_PASSWORD'),
                'database': os.getenv('POSTGRES_DB')
            }

            cls._instance = super(DbInstance, cls).__new__(cls)
            cls._instance.engine = create_engine(URL(**database), echo=bool(os.getenv('POSTGRES_LOG')))
            cls._instance.session_maker = sessionmaker(bind=cls._instance.engine)
            Base.metadata.create_all(cls._instance.engine)
        return cls._instance