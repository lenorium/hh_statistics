import time
from datetime import datetime, timedelta

from dotenv import load_dotenv

from api import vacancies_api
from db import skill_repo, vacancies_repo, repository
from models import DbVacancy

if __name__ == '__main__':
    load_dotenv()

    time.sleep(1)

    date_to = datetime.now()
    date_from = date_to - timedelta(days=1)
    vacancies = vacancies_api.get_vacancies(text='data engineer',
                                            date_from=date_from.isoformat(),
                                            date_to=date_to.isoformat(),
                                            per_page=100)

    vacancies = filter(lambda v: not repository.get_first(DbVacancy, DbVacancy.external_id == v.id), vacancies)
    vacancies = [vacancies_api.get_vacancy_full(vacancy.id) for vacancy in vacancies]

    for v in vacancies:
        # выбираем только те навыки, которые написаны на англ, чтоб не попадали всякие типа "Ответственность"
        v.skills = set([s.lower() for s in v.skills if s.isascii()])

    all_skills = set(item for vacancy in vacancies for item in vacancy.skills)
    skill_repo.add_all(all_skills)

    vacancies_repo.add_all(vacancies)

    print('Done!')
