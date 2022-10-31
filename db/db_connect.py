from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import config
from db.models import Base


class DbConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DbConnection, cls).__new__(cls)

            # если запускаем на heroku, то используется перем. DATABASE_URL
            if config.DATABASE_URL:
                connect_url = config.DATABASE_URL
                if connect_url.startswith("postgres://"):
                    connect_url = connect_url.replace("postgres://", "postgresql://", 1)
            else:
                database = {
                    'drivername': 'postgresql+psycopg2',
                    'host': config.POSTGRES_HOST,
                    'port': config.POSTGRES_PORT,
                    'username': config.POSTGRES_USER,
                    'password': config.POSTGRES_PASSWORD,
                    'database': config.POSTGRES_DB
                }
                connect_url = URL(**database)

            cls._instance.engine = create_engine(connect_url,
                                                 connect_args={'sslmode': 'require'},  # для heroku
                                                 echo=config.POSTGRES_LOG)
            cls._instance.session_maker = sessionmaker(bind=cls._instance.engine)
            Base.metadata.create_all(cls._instance.engine)
        return cls._instance


def session_maker():
    return DbConnection().session_maker
