"""
A class to interact with Marketplace's api, using OAuth.

For full spec please read Marketplace API documentation
https://github.com/mozilla/zamboni/blob/master/docs/topics/api.rst
"""

import json
import logging
import mimetypes

from base64 import b64encode

import oauth2 as oauth

from urlparse import urlunparse

from .connection import Connection

log = logging.getLogger('marketplace.%s' % __name__)

MARKETPLACE_PORT = 443
MARKETPLACE_DOMAIN = 'marketplace.mozilla.org'
MARKETPLACE_PROTOCOL = 'https'

URLS = {'validate': '/apps/validation/',
        'validation_result': '/apps/validation/%s/',
        'create': '/apps/app/',
        'app': '/apps/app/%s/',
        'create_screenshot': '/apps/preview/?app=%s',
        'screenshot': '/apps/preview/%s/',
        'categories': '/apps/category/'}


class Client:
    """A base class to authenticate and work with Marketplace OAuth.
    """
    signature_method = oauth.SignatureMethod_HMAC_SHA1()

    def __init__(self, domain=MARKETPLACE_DOMAIN,
                 protocol=MARKETPLACE_PROTOCOL,
                 port=MARKETPLACE_PORT,
                 prefix='',
                 consumer_key=None, consumer_secret=None):
        self.domain = domain
        self.protocol = protocol
        self.port = port
        self.prefix = prefix
        self.conn = None
        if consumer_secret and consumer_key:
            self.conn = self.get_connection(consumer_key, consumer_secret)

    @staticmethod
    def get_connection(consumer_key, consumer_secret):
        """Provide Connection object used for communication with the API
        """
        return Connection(consumer_key, consumer_secret)

    def url(self, key):
        """Creates a full URL to the API using urls dict
        """
        return urlunparse((self.protocol, '%s:%s' % (self.domain, self.port),
                           '%s/api%s' % (self.prefix, URLS[key]),
                           '', '', ''))

    def validate_manifest(self, manifest_url):
        """Order manifest validation

        :returns: dict with an ``id`` to check the result
        """
        # there is a bug request to make this synchronous on Marketplace side
        # this will return the same as :method:`get_manifest_validation_result`
        return self.conn.fetch('POST',
                               self.url('validate'), {'manifest': manifest_url})

    def get_manifest_validation_result(self, manifest_id):
        """Check if the manifest is processed and if it's valid

        :param: manifest_id (string) id received in :method:`validate_manifest`
        :returns: (HttpResponse)
            * status_code - 200 if manifest in validation
            * content - (dict) with some important fields alongs the other:
                * processed (Boolean) has manifest been processed?
                * valid (Boolean) is manifest valid?
                * validation - empty string if valid else error dict
        """
        return self.conn.fetch('GET',
                               self.url('validation_result') % manifest_id)

    def is_manifest_valid(self, manifest_id):
        """Check validation shortcut

        :param: manifest_id (string) id received in :method:`validate_manifest`
        :returns:
            * True if manifest was valid
            * None if manifest wasn't checked yet
            * validation dict if not valid
        """
        response = self.get_manifest_validation_result(manifest_id)
        if response.status_code != 200:
            raise Exception(response.status_code)
        content = json.loads(response.content)
        if not content['processed']:
            return None
        if content['valid']:
            return True
        return content['validation']

    def create(self, manifest_id):
        """Issue create process

        :returns: HttpResponse:
            * status_code - 201 if successful
            * content - dict with some important fields:
                * id (string) application id in marketplace
                * resource_uri (string) url in marketplace
                * slug (string) unique name in marketplace
        """
        return self.conn.fetch('POST', self.url('create'),
                               {'manifest': '%s' % manifest_id})

    def update(self, app_id, data):
        """Update app identified by app_id with data

        :params:
            * app_id (int) id in the marketplace received with :method:`create`
            * data (dict) some keys are required:
                * *name*: the title of the app. Maximum length 127
                  characters.
                * *summary*: the summary of the app. Maximum length
                  255 characters.
                * *categories*: a list of the categories, at least
                  two of the category ids provided from the category api
                  (see below).
                * *support_email*: the email address for support.
                * *device_types*: a list of the device types at least
                  one of: 'desktop', 'phone', 'tablet'.
                * *payment_type*: only choice at this time is 'free'.
        :returns: HttResponse:
            * status_code (int) 202 if successful
            * content (dict) or empty if successful
        """
        assert ('name' in data
                and data['name']
                and 'summary' in data
                and 'categories' in data
                and data['categories']
                and 'support_email' in data
                and data['support_email']
                and 'device_types' in data
                and data['device_types']
                and 'payment_type' in data
                and data['payment_type']
                and 'privacy_policy' in data
                and data['privacy_policy'])
        return self.conn.fetch('PUT', self.url('app') % app_id, data)

    def status(self, app_id):
        """View details of an app identified by its id

        :returns: HttResponse:
            * status_code (int) 200 if successful
            * content (JSON String) with all available app information
        """
        return self.conn.fetch('GET', self.url('app') % app_id)

    def delete(self, app_id):
        """Delete an app from Marketplace
        """
        # XXX: This isn't yet implemented on API
        # return self.conn.fetch('DELETE', self.url('app') % app_id)
        raise NotImplementedError()

    def create_screenshot(self, app_id, filename, position=1):
        """Add a screenshot to the web app identified by by ``app_id``.
        Screenshots are ordered by ``position``.

        :returns: HttpResponse:
            * status_code (int) 201 is successful
            * content (dict) containing screenshot data
        """
        # prepare file for upload
        with open(filename, 'rb') as s_file:
            s_content = s_file.read()
        s_encoded = b64encode(s_content)
        url = self.url('create_screenshot') % app_id

        mtype, encoding = mimetypes.guess_type(filename)
        if mtype is None:
            mtype = 'image/jpeg'

        data = {'position': position,
                'file': {'type': mtype,
                         'data': s_encoded}}
        return self.conn.fetch('POST', url, data)

    def get_screenshot(self, screenshot_id):
        """Get information about screenshot or video

        :returns HttpResponse:
            * status_code (int) 200 is successful
            * content (JSON string)
        """
        return self.conn.fetch('GET', self.url('screenshot') % screenshot_id)

    def del_screenshot(self, screenshot_id):
        """Deletes screenshot

        :returns: HttpResponse:
            * status_code (int) 204 if successful
        """
        return self.conn.fetch('DELETE',
                               self.url('screenshot') % screenshot_id)

    def get_categories(self):
        """Get all categories from Marketplae
        """
        return self.conn.fetch('GET', self.url('categories'))
