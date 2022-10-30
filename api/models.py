class ApiVacancy:
    id = None
    name = None
    published_at = None
    skills = []

    def __init__(self, attrs: dict):
        super().__init__()
        for key in attrs:
            if key in type(self).__dict__:
                setattr(self, key, attrs[key])
            if key == 'key_skills':
                self.skills = [item['name'] for item in attrs[key]]


class VacancySearchResult:
    def __init__(self, attrs: dict):
        self.items = attrs['items'] if 'items' in attrs else []
