Command Line Marketplace Client
===============================

Install requirements::

    pip install -r requirements.txt

Usage
-----

* Set CONSUMER_KEY and CONSUMER_SECRET environment variables::

    export CONSUMER_KEY=yourconsumerkey
    export CONSUMER_SECRET=yourconsumersecret

* Change domain if you wish to work on development server::

    export MARKETPLACE_DOMAIN=marketplace-dev.allizom.org

* Validate manifest. Will return ``manifest_id`` which is needed for the next steps::

    python main.py validate_manifest http://mozilla.github.com/Marketplace.Python/manifest.webapp

* Check if the manifest is valid::

    python main.py is_manifest_valid your_manifest_id

* Add app to marketplace, app_id will be returned::

    python main.py create your_manifest_id

* Display status of the app::

    python main.py status your_app_id

* Add screenshot (currently only JPEG) to app, some data including id will be returned::

    python main.py add_screenshot your_app_id ~/data/some.jpg

Options
-------

``-v`` to show all responses::

    python main.py -v validate_manifest http://mozilla.github.com/Marketplace.Python/manifest.webapp

    {'cookies': <<class 'requests.cookies.RequestsCookieJar'>[Cookie(version=0, name='lang', value='"en-US\\054"', port=None, port_specified=False, domain='marketplace-dev.allizom.org', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={}, rfc2109=False), Cookie(version=0, name='multidb_pin_writes', value='y', port=None, port_specified=False, domain='marketplace-dev.allizom.org', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=1354189187, discard=False, comment=None, comment_url=None, rest={}, rfc2109=False), Cookie(version=0, name='region', value='us', port=None, port_specified=False, domain='marketplace-dev.allizom.org', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={}, rfc2109=False)]>, '_content': False, 'headers': {'via': 'Moz-pp-zlb09', 'x-content-security-policy-report-only': 'policy-uri /services/csp/policy?build=8585', 'transfer-encoding': 'chunked', 'set-cookie': 'lang="en-US\\054"; Path=/, region=us; Path=/, multidb_pin_writes=y; expires=Thu, 29-Nov-2012 11:36:18 GMT; Max-Age=15; Path=/', 'strict-transport-security': 'max-age=2592000', 'vary': 'X-Requested-With, Accept-Language, Cookie, X-Mobile, User-Agent', 'server': 'gunicorn/0.15.0', 'connection': 'keep-alive', 'location': 'https://marketplace-dev.allizom.org/api/apps/validation/05a4c5f051e94754a762c8ca9b958434/', 'date': 'Thu, 29 Nov 2012 11:36:03 GMT', 'x-frame-options': 'DENY', 'content-type': 'application/json; charset=utf-8'}, 'url': u'https://marketplace-dev.allizom.org:443/api/apps/validation/', 'status_code': 201, '_content_consumed': False, 'encoding': 'utf-8', 'request': <Request [POST]>, 'raw': <requests.packages.urllib3.response.HTTPResponse object at 0xb6d3d0ec>, 'error': None, 'config': {'safe_mode': False, 'pool_connections': 10, 'verbose': None, 'keep_alive': True, 'strict_mode': False, 'max_retries': 0, 'store_cookies': True, 'trust_env': True, 'base_headers': {'Accept-Encoding': 'identity, deflate, compress, gzip', 'Accept': '*/*', 'User-Agent': 'python-requests/0.13.1'}, 'pool_maxsize': 10, 'danger_mode': False, 'encode_uri': True, 'max_redirects': 30}, 'history': []}
    Validation issued, id: 05a4c5f051e94754a762c8ca9b958434

