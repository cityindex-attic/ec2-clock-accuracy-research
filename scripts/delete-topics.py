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

def describeUser():
    import boto.iam
    iam = boto.connect_iam()
    user = iam.get_user()
    return user['get_user_response']['get_user_result']['user']

def describeAccount(user=None):
    import boto.iam
    iam = boto.connect_iam()
    account = {}
    alias = iam.get_account_alias()
    account['Alias'] = alias['list_account_aliases_response']['list_account_aliases_result']['account_aliases'][0]
    if not user:
        user = describeUser()
    account['Id'] = user['arn'].replace('arn:aws:iam::', '').partition(':')[0]
    return account

def createTopicArn(region_name, account_id, topic_name):
    return 'arn:aws:sns:' + region_name + ':' + account_id + ':' + topic_name

# execute business logic
heading = "Deleting SNS topics named '" + args.topic + "'"
regions = boto.sns.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

user = describeUser()
account = describeAccount(user)

print heading + ":"
for region in regions:
    pprint(region.name, indent=2)
    try:
        sns = boto.connect_sns(region=region, **credentials)
        arn = createTopicArn(region.name, account['Id'], args.topic)
        print 'Deleting topic ' + arn
        sns.delete_topic(arn)
    except boto.exception.BotoServerError, e:
        print e.error_message
