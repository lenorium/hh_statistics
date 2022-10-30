import config
from api import api_methods as api
from api.models import ApiVacancy, VacancySearchResult


def get_vacancies(**params) -> list:
    response = api.get(config.SEARCH_URL + '/vacancies', 200, **params)
    result = VacancySearchResult(response)
    vacancies = []
    for item in result.items:
        vacancies.append(ApiVacancy(item))
    return vacancies


def get_vacancy_full(id: int) -> ApiVacancy:
    response = api.get(config.SEARCH_URL + '/vacancies/' + id)
    return ApiVacancy(response)
