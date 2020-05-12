import typing
import os
import json
import flask
from flask_caching import Cache

from .log import logger

__all__ = (
    'register_extensions',
    'cache',
)

cache = Cache()  # pylint: disable=invalid-name


def register_extensions(app):
    # type: (flask.Flask) -> None
    extensions = [
        cache,
    ]
    for extension in extensions:
        extension.init_app(app)
