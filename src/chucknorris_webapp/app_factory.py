import typing
import sys
import logging
from http import HTTPStatus

import flask
from flask.logging import create_logger

from .config import WebappConfig
from .extensions import register_extensions
from .views import FaviconView, RandomQuoteView
from .quotes import get_categories

__all__ = (
    'create_app',
)

FLASK_APP = __name__.split('.', 1)[0]


def create_app():
    # type: () -> flask.Flask
    config = WebappConfig()
    app = flask.Flask(FLASK_APP)
    app.config.from_object(config)
    logger = create_logger(app)
    register_extensions(app)

    logger.info('Runtime: app=%s; flask=%s; debug=%s', FLASK_APP, flask.__version__, app.debug)
    logger.info('Runtime: python=%s;', sys.version)

    @app.context_processor
    def _inject_vars():
        return {
            'categories': get_categories(),
        }

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(err):
        return flask.render_template('404.html'), HTTPStatus.NOT_FOUND

    # Dummy endpoint for favicon.ico
    # avoid 404 Not Found error
    app.add_url_rule('/favicon.ico', view_func=FaviconView.as_view('favicon'))

    app.add_url_rule('/', defaults={'category': None}, view_func=RandomQuoteView.as_view('front'))
    quote_view = RandomQuoteView.as_view('quote')
    app.add_url_rule('/category/<category>', view_func=quote_view)
    app.add_url_rule('/category/random', defaults={'category': None}, view_func=quote_view)

    return app
