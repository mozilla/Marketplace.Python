""" Provide connection with Marketplace API
"""

import json
import logging
import time
import urllib

import oauth2 as oauth
import requests

log = logging.getLogger('marketplace.%s' % __name__)


class NotExpectedStatusCode(requests.exceptions.HTTPError):
    """ Raise if status code returned from API is not the expected one
    """
    pass


def _get_args(consumer):
    """Provide a dict with oauth data
    """
    return dict(
        oauth_consumer_key=consumer.key,
        oauth_nonce=oauth.generate_nonce(),
        oauth_signature_method='HMAC-SHA1',
        oauth_timestamp=int(time.time()),
        oauth_version='1.0')


class Connection:
    """ Keeps the consumer class and provides the way to connect to the
    Marketplace API
    """
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    consumer = None

    def __init__(self, consumer_key, consumer_secret):
        self.set_consumer(consumer_key, consumer_secret)

    def set_consumer(self, consumer_key, consumer_secret):
        """Sets the consumer attribute
        """
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)

    def prepare_request(self, method, url, body=''):
        """Adds consumer and signs the request

        :returns: headers of the signed request
        """
        req = oauth.Request(method=method, url=url,
                            parameters=_get_args(self.consumer))
        req.sign_request(self.signature_method, self.consumer, None)

        headers = req.to_header()
        headers['Content-type'] = 'application/json'
        if body:
            if method == 'GET':
                body = urllib.urlencode(body)
            else:
                body = json.dumps(body)
        return {"headers": headers, "data": body}

    @staticmethod
    def _get_error_reason(response):
        """Extract error reason from the response. It might be either
        the 'reason' or the entire response
        """
        body = response.json
        if body and 'reason' in body:
            return body['reason']
        return response.content

    def fetch(self, method, url, data=None, expected_status_code=None):
        """Prepare the headers, encode data, call API and provide
        data it returns
        """
        kwargs = self.prepare_request(method, url, data)
        response = getattr(requests, method.lower())(url, **kwargs)
        if response.status_code >= 400:
            response.raise_for_status()
        if (expected_status_code
                and response.status_code != expected_status_code):
            raise NotExpectedStatusCode(self._get_error_reason(response))
        return response

    def fetch_json(self, method, url, data=None, expected_status_code=None):
        """Return json decoded data from fetch
        """
        return self.fetch(method, url, data, expected_status_code).json()
