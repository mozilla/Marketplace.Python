""" Provide connection with Marketplace API
"""

import json
import logging
import urllib

import requests
from oauthlib import oauth1

log = logging.getLogger('marketplace.%s' % __name__)


class NotExpectedStatusCode(requests.exceptions.HTTPError):
    """ Raise if status code returned from API is not the expected one
    """
    pass


class Connection:
    """ Keeps the oauth client class and provides the way to connect to the
    Marketplace API
    """
    def __init__(self, consumer_key, consumer_secret):
        self.set_oauth_client(consumer_key, consumer_secret)

    def set_oauth_client(self, consumer_key, consumer_secret):
        """Sets the oauth_client attribute
        """
        self.oauth_client = oauth1.Client(consumer_key, consumer_secret)

    def prepare_request(self, method, url, body=''):
        """Prepare the request body and headers

        :returns: headers of the signed request
        """
        headers = {
            'Content-type': 'application/json',
        }
        # Note: we don't pass body to sign() since it's only for bodies that
        # are form-urlencoded. Similarly, we don't care about the body that
        # sign() returns.
        uri, signed_headers, signed_body = self.oauth_client.sign(
            url, http_method=method, headers=headers)
        if body:
            if method == 'GET':
                body = urllib.urlencode(body)
            else:
                body = json.dumps(body)
        headers.update(signed_headers)
        return {"headers": headers, "data": body}

    @staticmethod
    def _get_error_reason(response):
        """Extract error reason from the response. It might be either
        the 'reason' or the entire response
        """
        try:
            body = response.json()
            if body and 'reason' in body:
                return body['reason']
        except ValueError:
            pass
        return response.content

    def fetch(self, method, url, data=None, expected_status_code=None):
        """Prepare the headers, encode data, call API and provide
        data it returns
        """
        kwargs = self.prepare_request(method, url, data)
        log.debug(json.dumps(kwargs))
        response = getattr(requests, method.lower())(url, **kwargs)
        log.debug(json.dumps(response.content))
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
