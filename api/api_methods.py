import requests
from api import urls
from logger import logger


def get(path: str, code: int = 200, **kwargs) -> dict:
    response = requests.get(urls.BASE + path, params=kwargs)

    log_msg_info = f'Request: {response.request.method} {response.request.url}\n'
    log_msg_full = log_msg_info + f'Response: {response.status_code} {response.text}'
    logger.info(log_msg_info)
    logger.debug(log_msg_full)

    if response.status_code != code:
        msg = f'Unexpected response code\n{log_msg_full}'
        logger.error(msg)
        raise Exception(msg)

    return response.json()
