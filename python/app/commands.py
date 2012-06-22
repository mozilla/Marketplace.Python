import oauth2 as oauth
import time
import requests
import json

import config
from lib.marketplace import Marketplace

def validate_manifest(auth, manifest_url):
    response = auth.validate_manifest(manifest_url)
    if response.status_code == 201:
        return {'success': True,
                'message': 'Validation issued, '
                           'id: %s' % json.loads(response.content)['id']}
    return {'success': False,
            'message': 'FAILED to issue validation. '
                       'Status code: %d' % response.status_code}

def is_manifest_valid(auth, manifest_id):
    response = auth.is_manifest_valid(manifest_id)
    if response is None:
        return {'success': True,
                'message': "Your manifest hasn't been processed yet"}
    if response is True:
        return {'success': True,
                'message': 'Your manifest is valid! '
                           'You can now add your app to the marketplace'}
    return {'success': True,
            'message': 'Your manifest is not valid:\n%s' % response}

def create(auth, manifest_id):
    response = auth.create(manifest_id)
    if response.status_code == 201:
        return {'success': True,
                'message': ('Your app has been added to marketplace!\n'
                            'id: %d, slug: %s') % (response.content['id'],
                                                   response.content['slug'])}
    else:
        return {'success': False,
                'message': response.content}

def status(auth, app_id):
    response = auth.status(app_id)
    if response.status_code != 200:
        return {'success': False,
                'message': 'Status code: %d, \n%s' % (response.status_code,
                                                      response.content)}
    content = json.loads(response.content)
    return {'success': True,
            'message': '\n'.join(
                ['%s: %s' % (k, v) for k, v in content.items()])}
