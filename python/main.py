import argparse
import sys

import app.commands
import app.config as config

from lib.marketplace import Marketplace

commands = {'validate_manifest': app.commands.validate_manifest,
           'is_manifest_valid': app.commands.is_manifest_valid,
           'create': app.commands.create,
           'status': app.commands.status,
           'add_screenshot': app.commands.add_screenshot,
           'get_screenshot': app.commands.get_screenshot,
           'del_screenshot': app.commands.del_screenshot}

parser = argparse.ArgumentParser(description='Command line Marketplace client')
parser.add_argument('method', type=str, help='command to be run on arguments',
        choices=commands.keys())
parser.add_argument('attrs', metavar='attr', type=str, nargs='+',
        help='command arguments')
args = parser.parse_args()

auth = Marketplace(
        domain=config.MARKETPLACE_DOMAIN,
        protocol=config.MARKETPLACE_PROTOCOL,
        port=config.MARKETPLACE_PORT,
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET)

result = commands[args.method](auth, *args.attrs)

if result['success']:
    sys.stdout.write('%s\n' % result['message'])
else:
    sys.stderr.write('%s\n' % result['message'])
    sys.exit(1)
