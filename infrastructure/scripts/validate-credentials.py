#!/usr/bin/python
import argparse
import boto
from boto_cli.iam.accountinfo import AccountInfo
from boto_cli.iam.userinfo import UserInfo
import logging
log = logging.getLogger('boto_cli')

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Validates AWS credentials and display account/user information')
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
parser.add_argument("-l", "--log", dest='log_level', default='WARNING',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help="The logging level to use. [default: WARNING]")
args = parser.parse_args()

# configure logging
log.setLevel(getattr(logging, args.log_level.upper()))
# define a Handler which writes INFO messages or higher to the sys.stderr
console_handler = logging.StreamHandler()
console_handler.setLevel(log.getEffectiveLevel())
log.addHandler(console_handler)

# execute business logic
credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}
heading = "Validating credentials:"

try:
    iam = boto.connect_iam(**credentials)
    userInfo = UserInfo(iam)
    user = userInfo.describe()
    accountInfo = AccountInfo(iam)
    account = accountInfo.describe(user)
    print "User name is '" + user.name + "' with id " + user.id
    print "Account alias is '" + account.alias + "' with id " + account.id
except boto.exception.BotoServerError, e:
    log.error(e.error_message)
