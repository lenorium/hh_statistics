import requests

from api import urls
from logger import logger


def __send_request(action, code):
    response = action()

    log_msg = __log_msg(response)
    logger.debug(log_msg)

    __raise_error(response, code, log_msg)

    return response.json()


def get(path: str, code: int = 200, **kwargs) -> dict:
    return __send_request(lambda: requests.get(urls.BASE + path, params=kwargs), code)


def post(path: str, json, code: int = 200):
    __send_request(lambda: requests.post(path, json=json), code)


def __log_msg(response):
    return f'Request: {response.request.method} {response.request.url}\n' \
           f'Response: {response.status_code} {response.text}'


def __raise_error(response, code: int, msg):
    if response.status_code != code:
        msg = f'Unexpected response code\n{msg}'
        logger.error(msg)
        raise Exception(msg)
