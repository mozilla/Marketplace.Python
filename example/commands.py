"""Commands to run on the Marketplace API
"""

import sys
import json


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
    content = json.loads(response.content)
    if response.status_code == 201:
        return {'success': True,
                'message': ('Your app has been added to marketplace!\n'
                            'id: %s, slug: %s') % (content['id'],
                                                   content['slug'])}
    else:
        return {'success': False,
                'message': response.content}


def list_webapps(auth):
    response = auth.list_webapps()
    content = json.loads(response.content)
    if response.status_code == 200:
        return {'success': True,
                'message': content}


def status(auth, app_id):
    response = auth.status(app_id)
    if response.status_code != 200:
        return {'success': False,
                'message': 'Error, status code: %d, \nMessage: %s' % (
                    response.status_code, response.content)}
    content = json.loads(response.content)
    return {'success': True,
            'message': '\n'.join(
                ['%s: %s' % (k, v) for k, v in content.items()])}


def update(auth, app_id):

    def get_value(key, val):
        variable = raw_input('%s (%s): ' % (key, val))
        if key in truthy_keys and not variable and not val:
            sys.stdout.write('This parameter is required.\n')
            variable = get_value(key, val)
        return variable

    editable_keys = ['name', 'device_types', 'summary', 'support_email',
                     'homepage', 'categories', 'description', 'privacy_policy',
                     'support_url', 'payment_type']
    truthy_keys = ['name', 'categories', 'support_email', 'device_types',
                   'payment_type', 'privacy_policy', 'summary']
    # obtaining current data
    data = json.loads(auth.status(app_id).content)
    data['payment_type'] = data['premium_type']
    for key in data.keys():
        if key not in editable_keys:
            del data[key]
    sys.stderr.write('Please provide data, hit Enter for no change\n')

    for key, val in data.items():
        if key in editable_keys:
            variable = get_value(key, val)
            if variable != '':
                if isinstance(val, list):
                    data[key] = variable.split(',')
                else:
                    data[key] = variable
    response = auth.update(app_id, data)
    if response.status_code != 202:
        return {'success': False,
                'message': 'Error, status code: %d, \nMessage: %s' % (
                    response.status_code, response.content)}
    return {'success': True,
            'message': 'Your app has been updated'}


def add_screenshot(auth, app_id, filename):
    response = auth.create_screenshot(app_id, filename)
    if response.status_code != 201:
        return {'success': False,
                'message': 'Error, status code: %d, \nMessage: %s' % (
                    response.status_code, response.content)}
    content = json.loads(response.content)
    return {'success': True,
            'message': '\n'.join(
                ['%s: %s' % (k, v) for k, v in content.items()])}


def get_screenshot(auth, screenshot_id):
    response = auth.get_screenshot(screenshot_id)
    if response.status_code != 200:
        return {'success': False,
                'message': 'Error, status code: %d, \nMessage: %s' % (
                    response.status_code, response.content)}
    content = json.loads(response.content)
    return {'success': True,
            'message': '\n'.join(
                ['%s: %s' % (k, v) for k, v in content.items()])}


def del_screenshot(auth, screenshot_id):
    response = auth.del_screenshot(screenshot_id)
    if response.status_code != 204:
        return {'success': False,
                'message': 'Error, status code: %d, \nMessage: %s' % (
                    response.status_code, response.content)}
    return {'success': True,
            'message': 'Screenshot deleted'}


def get_categories(auth):
    response = auth.get_categories()
    if response.status_code != 200:
        return {'success': False,
                'message': 'Error, status code: %d, \nMessage: %s' % (
                    response.status_code, response.content)}
    message = ''
    content = json.loads(response.content)
    for cat in content['objects']:
        message += '%s: %s\n' % (cat['id'], cat['name'])
    return {'success': True,
            'message': message}
