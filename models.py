from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class VacancySkill(Base):
    __tablename__ = 'vacancy_skill'

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), primary_key=True, onupdate='CASCADE')
    skill_id = Column(Integer, ForeignKey('skills.id'), primary_key=True, onupdate='CASCADE')

    def __init__(self, skill_id):
        super().__init__()
        self.skill_id = skill_id

    def __repr__(self):
        return f'VacancySkill <{id(self)}>  vacancy_id: {self.vacancy_id}  skill_id: {self.skill_id}'


class DbVacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    external_id = Column(Integer, nullable=False, unique=True)
    skills = relationship('VacancySkill')

    temp_skills = []

    def __init__(self, external_id, name, published_at, skills: list):
        super().__init__()
        self.external_id = external_id
        self.name = name
        self.published_at = published_at
        self.skills = skills

    # def __init__(self, attrs: dict):
    #     super().__init__()
    #     for key in attrs:
    #         if key in type(self).__dict__:
    #             setattr(self, key, attrs[key])
    #         if
    #         if key == 'key_skills':
    #             self.temp_skills = [item['name'] for item in attrs[key]]


class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, )
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f'Skill <{id(self)}> {self.name} {self.id}'


class VacancySearchResult:
    def __init__(self, attrs: dict):
        self.items = attrs['items'] if 'items' in attrs else []
