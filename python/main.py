import sys
import app.commands as commands
import app.config as config
from lib.marketplace import Marketplace

allowed_commands = ['validate_manifest', 'is_manifest_valid', 'create',
                    'status']
if len(sys.argv) < 2 or sys.argv[1] not in allowed_commands:
    print >> sys.stderr, ('Please provide one of the commands:\n'
            '%s' % ', '.join(allowed_commands))
    sys.exit(1)

command = sys.argv[1]

auth = Marketplace(
        domain=config.MARKETPLACE_DOMAIN,
        protocol=config.MARKETPLACE_PROTOCOL,
        port=config.MARKETPLACE_PORT)
auth.consumer = config.CONSUMER

if command == 'validate_manifest':
    manifest_url = sys.argv[2] if len(sys.argv) == 3 else config.DEF_WEBAPP_URL
    result = commands.validate_manifest(auth, manifest_url)
elif command == 'is_manifest_valid':
    result = commands.is_manifest_valid(auth, sys.argv[2])
elif command == 'create':
    result = commands.create(auth, sys.argv[2])
elif command == 'status':
    result = commands.status(auth, sys.argv[2])

if result['success']:
    print result['message']
else:
    print >> sys.stderr, result['message']
    sys.exit(1)
