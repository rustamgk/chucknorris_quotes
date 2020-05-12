import typing

import random
from http import HTTPStatus

import requests
from flask.views import MethodView, View
from flask import Response, make_response, jsonify, request, url_for, render_template, abort

from .log import logger
from .quotes import get_random, get_categories

__all__ = (
    'FaviconView',
    'RandomQuoteView',
)


class FaviconView(View):
    def dispatch_request(self):
        # type: () -> Response
        return make_response('', HTTPStatus.NO_CONTENT)


class RandomQuoteView(MethodView):
    def get(self, category=None):
        # type: (typing.Optional[str]) -> Response
        quote = get_random(category)
        if quote is None:
            abort(HTTPStatus.NOT_FOUND)
        return render_template('quote.html', category=category, quote=quote)
