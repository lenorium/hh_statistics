from db.db import DbInstance


def session_maker():
    return DbInstance().session_maker


def create(entity):
    try:
        with session_maker().begin() as session:
            session.add(entity)
    except Exception as e:
        print(e)
    return entity


def create_all(entities: list):
    try:
        with session_maker().begin() as session:
            session.add_all(entities)
    except Exception as e:
        print(e)


# def get_or_create(cls, *filter_exp):
#     with session_maker().begin() as session:
#         instance = session.query(cls).filter(*filter_exp).first()
#         if not instance:
#             instance = cls(filter_exp)
#         return instance

# def


def get_all(cls, *filter_exp) -> list:
    with session_maker()() as session:
        return session.query(cls).filter(*filter_exp).all()


def get_first(cls, *filter_exp):
    with session_maker()() as session:
        return session.query(cls).filter(*filter_exp).first()


def update(cls, entity):
    try:
        with session_maker()() as session:
            session.expunge(entity)
    except Exception as e:
        print(e)