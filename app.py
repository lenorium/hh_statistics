from datetime import timedelta
from time import sleep

from utils import telegram_bot
import config
from api import vacancies_api
from db import db_utils as db
from utils.logger import logger


def collect_data():
    date_from, date_to = get_search_period()
    page = 0

    while True:
        logger.info(f'1. Get vacancies list: page {page} per_page {config.SEARCH_PER_PAGE}\n')
        vacancies = vacancies_api.get_vacancies(text=config.SEARCH_TEXT,
                                                search_field=config.SEARCH_FIELD,
                                                date_from=date_from.isoformat(),
                                                date_to=date_to.isoformat(),
                                                area=config.SEARCH_AREA,  # Россия
                                                per_page=config.SEARCH_PER_PAGE,
                                                page=page,
                                                order_by=config.SEARCH_ORDER_BY)
        if not vacancies:
            break

        page += 1

        logger.info('2. Remove vacancies that already exist in the database\n')
        # убираем вакансии, которые уже есть в бд
        vacancies = filter(lambda v: not db.find_vacancy_by_ext_id(v.id), vacancies)

        logger.info('3. Get full description of each vacancy\n')
        vacancies = [vacancies_api.get_vacancy_full(vacancy.id) for vacancy in vacancies]

        for v in vacancies:
            # выбираем только те навыки, которые написаны на англ, чтоб не попадали всякие типа "Ответственность"
            v.skills = set([s.lower() for s in v.skills if s.isascii()])

        all_skills = set(item for vacancy in vacancies for item in vacancy.skills)

        logger.info('4. Save new skills in database\n')
        db.create_skills(all_skills)

        logger.info('5. Save vacancies in database\n')
        db.create_vacancies(vacancies)


def rate_skills():
    date_from, date_to = get_search_period()
    skills = db.get_skills_sort_by_rate(date_from, date_to)
    return {s[0]: s[1] for s in skills}


def get_search_period() -> tuple:
    time_delta = config.SEARCH_TIME_DELTA
    date_to = config.SEARCH_DATE_TO
    date_from = date_to - timedelta(days=time_delta)

    return date_from, date_to


if __name__ == '__main__':
    sleep(1)    # временно
    collect_data()
    skills = rate_skills()

    msg = '\n'.join(f'{key}: {value}' for key, value in skills.items())

    telegram_bot.send_message(msg)
