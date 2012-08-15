#!/usr/bin/python
import argparse
import boto
from boto_cli.iam.accountinfo import AccountInfo
from boto_cli.iam.userinfo import UserInfo
from pprint import pprint

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Validates AWS credentials and display account/user information')
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

# execute business logic
heading = "Validating credentials:"

try:
    iam = boto.connect_iam(**credentials)
    userInfo = UserInfo(iam)
    user = userInfo.describe()
    accountInfo = AccountInfo(iam)
    account = accountInfo.describe(user)
    print "User is '" + user.name + "' with id " + user.id
    print "Account is '" + account.alias + "' with id " + account.id
except boto.exception.BotoServerError, e:
    print e.error_message
