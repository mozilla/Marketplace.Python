import json
import logging
import time
import urllib

import oauth2 as oauth
import requests

log = logging.getLogger('marketplace.%s' % __name__)

class NotExpectedStatusCode(requests.exceptions.HTTPError):
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
    signature_method = oauth.SignatureMethod_HMAC_SHA1()

    def __init__(self, consumer_key, consumer_secret):
        self.set_consumer(consumer_key, consumer_secret)

    def set_consumer(self, consumer_key, consumer_secret):
        """Sets the consumer attribute
        """
        self.consumer = self.get_consumer(consumer_key, consumer_secret)

    def get_consumer(self, consumer_key, consumer_secret):
        """Get the :class:`oauth.Consumer` instance with provided key and
        secret
        """
        return oauth.Consumer(consumer_key, consumer_secret)


    def prepare_request(self, method, url, body='', consumer=None):
        """Adds consumer and signs the request

        :returns: headers of the signed request
        """
        if not consumer:
            consumer = self.consumer
        req = oauth.Request(method=method, url=url,
                            parameters=_get_args(consumer))
        req.sign_request(self.signature_method, consumer, None)

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
        body = response.json
        if body and 'reason' in body:
            return body['reason']
        return response.content

    def fetch(self, method, url, data=None, expected_status_code=None,
            consumer=None):
        kwargs = self.prepare_request(method, url, data, consumer)
        response = getattr(requests, method.lower())(url, **kwargs)
        if response.status_code >= 400:
            response.raise_for_status()
        if expected_status_code and response.status_code != expected_status_code:
                raise NotExpectedStatusCode(self._get_error_reason(response))
        return response

    def fetch_json(self, method, url, data=None, expected_status_code=None,
            consumer=None):
        return self.fetch(method, url, data, consumer,
            expected_status_code).json()
