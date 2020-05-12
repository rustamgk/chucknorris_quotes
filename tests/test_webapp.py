import typing  # pylint: disable=unused-import
import os
from http import HTTPStatus
import unittest
from unittest import mock

import requests_mock
import flask  # pylint: disable=unused-import
from flask import url_for
import flask.wrappers  # pylint: disable=unused-import
import flask.testing  # pylint: disable=unused-import

import chucknorris_webapp as webapp

__all__ = (
    'WebappTestCase',
)


class WebappTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(WebappTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        # type: () -> None
        environment = {
            'CACHE_TYPE': 'null',
        }
        self.mock_env = mock.patch.dict(os.environ, environment)
        self.mock_env.start()

        # Prepare Flask webapp and client
        self.app = webapp.create_app()  # type: flask.Flask
        self.app_context = self.app.test_request_context()  # type: flask.ctx.RequestContext
        self.app_context.push()
        self.client = self.app.test_client()  # type: flask.testing.FlaskClient

    def tearDown(self):
        # type: () -> None
        try:
            pass
        finally:
            self.mock_env.stop()

    def test_favicon_return_no_content(self):
        assert url_for('favicon') == '/favicon.ico'
        rv = self.client.get(url_for('favicon'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NO_CONTENT
        assert rv.data == b'', 'Expected empty response'

    def test_favicon_post_not_allowed(self):
        rv = self.client.post(url_for('favicon'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_urls(self):
        assert url_for('front') == '/'
        assert url_for('quote') == '/category/random'
        assert url_for('quote', category='food') == '/category/food'

    def _test_random_api(self):
        rv = self.client.get('/')  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert rv.content_type == 'application/json'
        assert 'random' in rv.json

    @requests_mock.Mocker()
    def test_random_quote(self, m):
        m.register_uri(
            'GET', 'https://api.chucknorris.io/jokes/categories',
            json=['food', 'foobar', 'qwerty']
        )
        m.register_uri(
            'GET', 'https://api.chucknorris.io/jokes/random',
            json={
                "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
                "id": "4ccl_U5ISBm86IJJYeoPIg",
                "url": "",
                "value": "Sotheby's once auctioned off 1/4 lb of Chuck Norris toenail clippings for $400,000."
            }
        )

        rv = self.client.get('/')  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert 'text/html' in rv.content_type
        assert b'foobar' in rv.data
        assert b'lb of Chuck Norris toenail clippings for $400,000.' in rv.data

    @requests_mock.Mocker()
    def test_random_quote_not_found(self, m):
        m.register_uri(
            'GET', 'https://api.chucknorris.io/jokes/categories',
            json=['food', 'foobar', 'qwerty']
        )
        m.register_uri(
            'GET', 'https://api.chucknorris.io/jokes/random',
            json={

            }, status_code=HTTPStatus.NOT_FOUND
        )

        rv = self.client.get('/')  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND
        assert 'text/html' in rv.content_type
        assert b'foobar' in rv.data
        assert b'Page not found' in rv.data


if __name__ == '__main__':
    unittest.main()
