import typing  # noqa
import logging
from flask.logging import default_handler

__all__ = (
    'logger',
)
FLASK_APP = __name__.split('.', 1)[0]
logger = logging.getLogger(FLASK_APP)
logger.addHandler(default_handler)
