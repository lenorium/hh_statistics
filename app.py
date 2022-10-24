from db import DbInstance
from models import Vacancy

if __name__ == '__main__':
    print('Start')
    session = DbInstance().session_maker
    entity = Vacancy('ghjfgj')
    try:
        with session.begin() as session:
            session.add(entity)
    except Exception as e:
        print(e)

    print('Done!')