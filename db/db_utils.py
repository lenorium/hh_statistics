from datetime import datetime

from sqlalchemy import func, desc

from api.models import ApiVacancy
from db.db_connect import session_maker
from db.models import Skill, VacancySkill, DbVacancy


def create_skills(skill_names):
    skills = [Skill(name) for name in skill_names]
    with session_maker().begin() as session:
        for skill in skills:
            result = session.query(Skill).filter(Skill.name == skill.name).first()
            if not result:
                session.add(skill)


def get_skills_sort_by_rate(date_from: datetime, date_to: datetime) -> list:
    with session_maker()() as session:
        rate = session.query(Skill.name,
                             func.count(VacancySkill.skill_id)) \
            .join(Skill, Skill.id == VacancySkill.skill_id) \
            .join(DbVacancy, DbVacancy.id == VacancySkill.vacancy_id) \
            .filter(DbVacancy.published_at.between(date_from, date_to)) \
            .having(func.count(VacancySkill.skill_id) > 1) \
            .group_by(Skill.name) \
            .order_by(desc(func.count(VacancySkill.skill_id))) \
            .all()

    return rate


def find_vacancy_by_ext_id(ext_id):
    with session_maker()() as session:
        return session.query(DbVacancy).filter(DbVacancy.external_id == ext_id).first()


def create_vacancies(vacancies: list[ApiVacancy]):
    with session_maker().begin() as session:
        for vacancy in vacancies:
            skills = []
            for s in vacancy.skills:
                result = session.query(Skill).filter(Skill.name == s).first()
                skills.append(VacancySkill(result.id))

            db_vacancy = DbVacancy(vacancy.id, vacancy.name, vacancy.published_at, skills)
            session.add(db_vacancy)
