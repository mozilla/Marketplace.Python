"""Read config from environment variables
"""

from os import environ

CONSUMER_KEY = (environ['CONSUMER_KEY']
                if 'CONSUMER_KEY' in environ
                else 'consumer_key')
CONSUMER_SECRET = (environ['CONSUMER_SECRET']
                   if 'CONSUMER_SECRET' in environ
                   else 'consumer_secret')

MARKETPLACE_PORT = (environ['MARKETPLACE_PORT']
                    if 'MARKETPLACE_PORT' in environ
                    else 443)
MARKETPLACE_DOMAIN = (environ['MARKETPLACE_DOMAIN']
                      if 'MARKETPLACE_DOMAIN' in environ
                      else 'marketplace.mozilla.org')
MARKETPLACE_PROTOCOL = (environ['MARKETPLACE_PROTOCOL']
                        if 'MARKETPLACE_PROTOCOL' in environ
                        else 'https')
