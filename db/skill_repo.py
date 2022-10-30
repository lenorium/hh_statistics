from db.db import DbInstance
from models import Skill


def session_maker():
    return DbInstance().session_maker


def add_all(skill_names):
    skills = [Skill(name) for name in skill_names]
    with session_maker().begin() as session:
        # session.add_all(skills)
        for skill in skills:
            result = session.query(Skill).filter(Skill.name == skill.name).first()
            if not result:
                session.add(skill)

# def attach_skills():
