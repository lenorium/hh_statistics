from api.models import ApiVacancy
from db.db import DbInstance
from models import Skill, VacancySkill, DbVacancy


def add_all(vacancies: list[ApiVacancy]):
    session_maker = DbInstance().session_maker

    with session_maker.begin() as session:
        for vacancy in vacancies:
            skills = []
            for s in vacancy.skills:
                result = session.query(Skill).filter(Skill.name == s).first()
                skills.append(VacancySkill(result.id))

            db_vacancy = DbVacancy(vacancy.id, vacancy.name, vacancy.published_at, skills)
            session.add(db_vacancy)