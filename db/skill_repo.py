from datetime import datetime

from sqlalchemy import func, desc

from db.db import DbInstance
from models import Skill, VacancySkill, DbVacancy


def session_maker():
    return DbInstance().session_maker


def add_all(skill_names):
    skills = [Skill(name) for name in skill_names]
    with session_maker().begin() as session:
        for skill in skills:
            result = session.query(Skill).filter(Skill.name == skill.name).first()
            if not result:
                session.add(skill)


class Vacancy:
    pass


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
