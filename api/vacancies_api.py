from api import api_methods as api
from api import urls
from api.models import ApiVacancy
from models import VacancySearchResult


def get_vacancies(**params) -> list:
    response = api.get(urls.VACANCIES, 200, **params)
    result = VacancySearchResult(response)
    vacancies = []
    for item in result.items:
        vacancies.append(ApiVacancy(item))
    return vacancies


def get_vacancy_full(id: int) -> ApiVacancy:
    response = api.get(urls.VACANCY_FULL(id))
    return ApiVacancy(response)