"""
tests.testClient
----------------
"""
import json
import logging
import unittest
import urllib

import requests
import oauth2 as oauth

from mock import Mock

from marketplace.connection import Connection

log = logging.getLogger('test.%s' % __name__)

# Preparing to mock the requests
OLD_POST = requests.post
OLD_PUT = requests.put
OLD_GET = requests.get
OLD_DELETE = requests.delete


class Response(requests.Response):
    def __init__(self, status_code, content=None):
        super(Response, self).__init__()
        self.status_code = status_code
        self._content = content

class TestClient(unittest.TestCase):

    def setUp(self):
        self.conn = Connection(consumer_key='key', consumer_secret='secret')

    def tearDown(self):
        requests.post = OLD_POST
        requests.put = OLD_PUT
        requests.get = OLD_GET
        requests.delete = OLD_DELETE

    def test_raising_on_httperror(self):
        resp = {"reason": "Error with OAuth headers"}
        requests.post = Mock(return_value=Response(401, json.dumps(resp)))
        self.assertRaises(requests.exceptions.HTTPError, self.conn.fetch,
                'POST', 'http://example.com/', {})

        resp = "<html><title>404</title><body><p>Error 404</p></body></html>"
        requests.post = Mock(return_value=Response(404, resp))
        self.assertRaises(requests.exceptions.HTTPError, self.conn.fetch,
                'POST', 'http://example.com/', {})

    def test_raising_on_unexpected(self):
        resp = {"reason": "Error with OAuth headers"}
        requests.post = Mock(return_value=Response(204, json.dumps(resp)))
        self.assertRaises(requests.exceptions.HTTPError, self.conn.fetch,
                'POST', 'http://example.com/', {}, 201)

    def test_error_reason_json(self):
        resp = {"reason": "message"}
        self.assertEquals(
                Connection._get_error_reason(Response(204,
                    json.dumps(resp))), resp['reason'])

    def test_error_reason_text(self):
        resp = "<html><title>404</title><body><p>Error 404</p></body></html>"
        self.assertEquals(
                Connection._get_error_reason(Response(204, resp)),
                resp)

    def test_set_consumer(self):
        assert isinstance(self.conn.consumer, oauth.Consumer)

    def test_prepare_request(self):
        prepared = self.conn.prepare_request('GET', 'http://example.com')
        assert 'headers' in prepared
        assert 'data' in prepared
        assert not prepared['data']

        data = {"some": "data"}
        prepared = self.conn.prepare_request('POST', 'http://ex.com', data)
        self.assertEquals(prepared['data'], json.dumps(data))

        prepared = self.conn.prepare_request('GET', 'http://ex.com', data)
        self.assertEquals(prepared['data'], urllib.urlencode(data))

    def test_get(self):
        requests.get = Mock(return_value=Response(200, '{}'))
        self.conn.fetch('GET', 'http://ex.com')
        assert requests.get.called

    def test_post(self):
        requests.post = Mock(return_value=Response(201, '{}'))
        self.conn.fetch('POST', 'http://ex.com')
        assert requests.post.called

    def test_put(self):
        requests.put = Mock(return_value=Response(202, '{}'))
        self.conn.fetch('PUT', 'http://ex.com')
        assert requests.put.called

    def test_delete(self):
        requests.delete = Mock(return_value=Response(204, '{}'))
        self.conn.fetch('DELETE', 'http://ex.com')
        assert requests.delete.called
