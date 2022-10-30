import time
from datetime import datetime, timedelta

from logger import logger
from api import vacancies_api
from db import skill_repo, vacancies_repo, repository
from models import DbVacancy


def collect_data():
    date_to = datetime.now()
    date_from = date_to - timedelta(days=1)
    per_page = 10
    page = 0

    while True:
        logger.info(f'1. Get vacancies list: page {page} per_page {per_page}\n')
        vacancies = vacancies_api.get_vacancies(text='data engineer or etl or dwh',
                                                search_field='name',
                                                date_from=date_from.isoformat(),
                                                date_to=date_to.isoformat(),
                                                per_page=per_page,
                                                page=page,
                                                # page="page",
                                                order_by='publication_time')
        if not vacancies:
            break

        page += 1

        logger.info('2. Remove vacancies that already exist in the database\n')

        # убираем вакансии, которые уже есть в бд
        vacancies = filter(lambda v: not repository.get_first(DbVacancy, DbVacancy.external_id == v.id), vacancies)

        logger.info('3. Get full description of each vacancy\n')
        vacancies = [vacancies_api.get_vacancy_full(vacancy.id) for vacancy in vacancies]

        for v in vacancies:
            # выбираем только те навыки, которые написаны на англ, чтоб не попадали всякие типа "Ответственность"
            v.skills = set([s.lower() for s in v.skills if s.isascii()])

        all_skills = set(item for vacancy in vacancies for item in vacancy.skills)

        logger.info('4. Save new skills in database\n')
        skill_repo.add_all(all_skills)

        logger.info('5. Save vacancies in database\n')
        vacancies_repo.add_all(vacancies)


if __name__ == '__main__':
    time.sleep(1)
    collect_data()

    print('Done!')
