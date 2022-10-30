from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import config
from models import Base


class DbInstance:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            database = {
                'drivername': 'postgresql+psycopg2',
                'host': config.POSTGRES_HOST,
                'port': config.POSTGRES_PORT,
                'username': config.POSTGRES_USER,
                'password': config.POSTGRES_PASSWORD,
                'database': config.POSTGRES_DB
            }

            cls._instance = super(DbInstance, cls).__new__(cls)
            cls._instance.engine = create_engine(URL(**database), echo=config.POSTGRES_LOG)
            cls._instance.session_maker = sessionmaker(bind=cls._instance.engine)
            Base.metadata.create_all(cls._instance.engine)
        return cls._instance
