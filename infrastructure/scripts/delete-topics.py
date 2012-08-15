#!/usr/bin/python
import argparse
import boto
import boto.sns
from pprint import pprint

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Delete a SNS topic in all/some available SNS regions')
parser.add_argument("topic", help="A topic name")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

def createTopicArn(region_name, topic_name):
    from boto_cli.iam.accountinfo import AccountInfo
    iam = boto.connect_iam(**credentials)
    accountInfo = AccountInfo(iam)
    account = accountInfo.describe()
    return 'arn:aws:sns:' + region_name + ':' + account.id + ':' + topic_name

# execute business logic
heading = "Deleting SNS topics named '" + args.topic + "'"
regions = boto.sns.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

print heading + ":"
for region in regions:
    pprint(region.name, indent=2)
    try:
        sns = boto.connect_sns(region=region, **credentials)
        arn = createTopicArn(region.name, args.topic)
        print 'Deleting topic ' + arn
        sns.delete_topic(arn)
    except boto.exception.BotoServerError, e:
        print e.error_message
