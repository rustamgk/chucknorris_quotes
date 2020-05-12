import typing
from http import HTTPStatus

import requests

from .extensions import cache

__all__ = (
    'get_random',
    'get_categories',
)


def get_random(category=None):
    # type: (typing.Optional[str]) -> typing.Optional[typing.Dict]
    params = {}
    if category is not None:
        params['category'] = category
    try:
        resp = requests.get('https://api.chucknorris.io/jokes/random', params=params)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as exc:
        if exc.response.status_code == HTTPStatus.NOT_FOUND:
            return None
        raise exc


@cache.cached(timeout=60)
def get_categories():
    # type: () -> typing.List[str]
    resp = requests.get('https://api.chucknorris.io/jokes/categories')
    resp.raise_for_status()
    return resp.json()
