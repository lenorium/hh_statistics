import requests
from api import urls
from logger import logger


def get(path: str, code: int = 200, **kwargs) -> dict:
    response = requests.get(urls.BASE + path, params=kwargs)

    log_msg = f'Request: {response.request.method} {response.request.url}\n' \
                   f'Response: {response.status_code} {response.text}'
    logger.debug(log_msg)

    if response.status_code != code:
        msg = f'Unexpected response code\n{log_msg}'
        logger.error(msg)
        raise Exception(msg)

    return response.json()
