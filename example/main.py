import argparse
import logging
import sys

import commands
import config

import marketplace

logger = logging.getLogger()
ch = logging.StreamHandler()
logger.addHandler(ch)

COMMANDS = {'validate_manifest': commands.validate_manifest,
            'is_manifest_valid': commands.is_manifest_valid,
            'create': commands.create,
            'list_webapps': commands.list_webapps,
            'status': commands.status,
            'update': commands.update,
            'add_screenshot': commands.add_screenshot,
            'get_screenshot': commands.get_screenshot,
            'del_screenshot': commands.del_screenshot,
            'get_categories': commands.get_categories,
            'app_state': commands.app_state}


def main():
    parser = argparse.ArgumentParser(
        description='Command line Marketplace client')
    parser.add_argument('method', type=str,
                        help='command to be run on arguments',
                        choices=COMMANDS.keys())
    parser.add_argument('attrs', metavar='attr', type=str, nargs='*',
                        help='command arguments')
    parser.add_argument('-v', action='store_true', default=False,
                        dest='verbose',
                        help='Switch to verbose mode')

    args = parser.parse_args()

    client = marketplace.Client(
        domain=config.MARKETPLACE_DOMAIN,
        protocol=config.MARKETPLACE_PROTOCOL,
        port=config.MARKETPLACE_PORT,
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET)

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    if args.attrs:
        result = COMMANDS[args.method](client, *args.attrs)
    else:
        result = COMMANDS[args.method](client)

    if result['success']:
        sys.stdout.write('%s\n' % result['message'])
    else:
        sys.stderr.write('%s\n' % result['message'])
        sys.exit(1)

if __name__ == "__main__":
    main()
