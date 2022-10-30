import requests
from api import urls


def get(path: str, code: int = 200, **kwargs) -> dict:
    response = requests.get(urls.BASE + path, params=kwargs)
    if response.status_code != code:
        raise Exception(f'Unexpected response code: {response.status_code}\n'
                        f'response: {response.text}')
    return response.json()
