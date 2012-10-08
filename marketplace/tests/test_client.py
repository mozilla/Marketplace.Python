import json
import logging
import os
import unittest

from base64 import b64encode

import requests

from mock import Mock
from nose import SkipTest
from nose.tools import eq_

import marketplace

log = logging.getLogger('test.%s' % __name__)

# Preparing to mock the requests
OLD_POST = requests.post
OLD_PUT = requests.put
OLD_GET = requests.get
OLD_DELETE = requests.delete

MARKETPLACE_PORT = 443
MARKETPLACE_DOMAIN = 'marketplace-dev.allizom.org'
MARKETPLACE_PROTOCOL = 'https'


class Response:
    """This is used to create a mock of response from API
    """
    def __init__(self, status_code, content=None):
        self.status_code = status_code
        self.content = content


class TestClient(unittest.TestCase):

    def setUp(self):
        self.marketplace = marketplace.Client(
            domain=MARKETPLACE_DOMAIN,
            port=MARKETPLACE_PORT,
            protocol=MARKETPLACE_PROTOCOL,
            consumer_key='consumer_key',
            consumer_secret='consumer_secret')

    def tearDown(self):
        requests.post = OLD_POST
        requests.put = OLD_PUT
        requests.get = OLD_GET
        requests.delete = OLD_DELETE

    def test_init(self):
        eq_(self.marketplace.domain, MARKETPLACE_DOMAIN)
        eq_(self.marketplace.port, MARKETPLACE_PORT)
        eq_(self.marketplace.protocol, MARKETPLACE_PROTOCOL)

    def test_order_validation(self):
        manifest_url = 'http://example.com/'
        resp = {'id': 'abcd',
                'manifest': manifest_url,
                'processed': False,
                'resource_uri': '/en-US/api/apps/validation/123/',
                'valid': False,
                'validation': ''}

        requests.post = Mock(return_value=Response(201, resp))

        response = self.marketplace.validate_manifest(manifest_url)
        log.debug(response.content)
        log.debug(response.status_code)
        eq_(response.content['id'], 'abcd')

    def test_get_validation_result(self):
        resp = {'id': 'abcd',
                'processed': False,
                'resource_uri': '/en-US/api/apps/validation/123/',
                'valid': False,
                'validation': ''}

        requests.get = Mock(return_value=Response(201, json.dumps(resp)))

        # providing id by string
        response = self.marketplace.get_manifest_validation_result('abcd')
        content = json.loads(response.content)
        eq_(content['id'], 'abcd')

    def test_is_manifest_valid(self):
        # not processed
        resp = {'id': '123',
                'processed': False,
                'resource_uri': '/en-US/api/apps/validation/123/',
                'valid': False,
                'validation': ''}

        requests.get = Mock(return_value=Response(200, json.dumps(resp)))
        eq_(self.marketplace.is_manifest_valid(123), None)

        # valid
        resp = {'id': '123',
                'processed': True,
                'resource_uri': '/en-US/api/apps/validation/123/',
                'valid': True,
                'validation': ''}

        requests.get = Mock(return_value=Response(200, json.dumps(resp)))
        eq_(self.marketplace.is_manifest_valid(123), True)

        # invalid
        resp = {'id': 'abcd',
                'processed': True,
                'resource_uri': '/en-US/api/apps/validation/123/',
                'valid': False,
                'validation': {'validation': 'object'}}

        requests.get = Mock(return_value=Response(200, json.dumps(resp)))
        eq_(self.marketplace.is_manifest_valid(123), resp['validation'])

    def test_create(self):
        resp = {'categories': [],
                'description': None,
                'device_types': [],
                'homepage': None,
                'id': 1,
                'manifest': '0a650e5e4c434b5cb60c5495c0d88a89',
                'name': 'MozillaBall',
                'premium_type': 'free',
                'privacy_policy': None,
                'resource_uri': '/en-US/api/apps/app/1/',
                'slug': 'mozillaball',
                'status': 0,
                'summary': 'Exciting Open Web development action!',
                'support_email': None,
                'support_url': None}

        requests.post = Mock(return_value=Response(201, json.dumps(resp)))
        response = self.marketplace.create('abcd')
        content = json.loads(response.content)
        eq_(response.status_code, 201)
        eq_(content['manifest'], '0a650e5e4c434b5cb60c5495c0d88a89')

    def test_update(self):
        requests.put = Mock(return_value=Response(202, ''))
        response = self.marketplace.update(123, {
            'name': 'MozillaBall',
            'summary': 'Changed Summary',
            'categories': ['Business', 'Game'],
            'support_email': 'john@doe.com',
            'device_types': ['phone', ],
            'privacy_policy': 'any',
            'payment_type': 'free'})
        eq_(response.status_code, 202)
        assert not response.content

    def test_status(self):
        resp = {'categories': ['Business', 'Game'],
                'description': None,
                'device_types': ['phone', ],
                'homepage': None,
                'id': 1,
                'manifest': '0a650e5e4c434b5cb60c5495c0d88a89',
                'name': 'MozillaBall',
                'premium_type': 'free',
                'privacy_policy': None,
                'resource_uri': '/en-US/api/apps/app/1/',
                'slug': 'mozillaball',
                'status': 0,
                'summary': 'Exciting Open Web development action!',
                'support_email': 'john@doe.com',
                'support_url': None}

        requests.get = Mock(return_value=Response(200, json.dumps(resp)))
        response = self.marketplace.status(1)
        content = json.loads(response.content)
        eq_(response.status_code, 200)
        eq_(content['manifest'], '0a650e5e4c434b5cb60c5495c0d88a89')

    def test_delete(self):
        raise SkipTest()
        requests.delete = Mock(return_value=Response(204, ''))
        response = self.marketplace.delete(1)
        eq_(response.status_code, 204)
        assert not response.content

    def test_delete_not_implemented(self):
        self.assertRaises(NotImplementedError, self.marketplace.delete, 1)

    def test_add_screenshot(self):
        path = lambda *a: os.path.join(
            os.path.dirname(os.path.abspath(__file__)), *a)
        resp = {'filetype': 'image/png',
                'thumbnail_url': 'https://marketplace-dev-cdn.allizom.org/img/'
                                 'uploads/previews/thumbs/71/71761.png?'
                                 'modified=1340899716',
                'image_url': 'https://marketplace-dev-cdn.allizom.org/img/'
                             'uploads/previews/full/71/71761.png?'
                             'modified=1340899716',
                'position': 1,
                'id': 71761,
                'resource_uri': '/en-US/api/apps/preview/71761'}
        requests.post = Mock(return_value=Response(201, resp))
        response = self.marketplace.create_screenshot(123, path('mozilla.jpg'))
        eq_(response.status_code, 201)
        eq_(response.content['position'], 1)
        with open(path('mozilla.jpg')) as moz_file:
            b64_file = b64encode(moz_file.read())
        data = json.loads(requests.post.call_args[1]['data'])
        eq_(data['position'], 1)
        eq_(data['file']['data'], b64_file)
        eq_(data['file']['type'], 'image/jpeg')
        # create a screenshot with a jpeg image and not default position
        self.marketplace.create_screenshot(123,
                                           path('mozilla.jpg'), position=2)
        data = json.loads(requests.post.call_args[1]['data'])
        eq_(data['position'], 2)
        eq_(data['file']['type'], 'image/jpeg')
