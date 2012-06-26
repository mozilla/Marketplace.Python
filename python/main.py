import sys

import app.commands
import app.config as config

from lib.marketplace import Marketplace

commands = {'validate_manifest': app.commands.validate_manifest,
           'is_manifest_valid': app.commands.is_manifest_valid,
           'create': app.commands.create,
           'status': app.commands.status}
if len(sys.argv) < 3 or sys.argv[1] not in commands:
    sys.stderr.write(('Please provide one of the commands with an '
            'argument:\n%s\n' % ', '.join(commands.keys())))
    sys.exit(1)

command = sys.argv[1]

auth = Marketplace(
        domain=config.MARKETPLACE_DOMAIN,
        protocol=config.MARKETPLACE_PROTOCOL,
        port=config.MARKETPLACE_PORT,
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET)

result = commands[command](auth, sys.argv[2])

if result['success']:
    sys.stdout.write('%s\n' % result['message'])
else:
    sys.stderr.write('%s\n' % result['message'])
    sys.exit(1)
