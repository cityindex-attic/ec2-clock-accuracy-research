#!/usr/bin/python
import argparse
import boto
import boto.cloudformation
from pprint import pprint

# NOTE: equivalent of https://github.com/boto/boto/pull/891 until upstream release catches up.
import patch9d3c9f0
boto.cloudformation.regions = patch9d3c9f0.regions
boto.cloudformation.connect_to_region = patch9d3c9f0.connect_to_region

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Create a CloudFormation stack in all/some available CloudFormation regions')
parser.add_argument("stack_name", help="A stack name")
parser.add_argument("template", help="A stack template local file or URL (URL not supported yet!)")
parser.add_argument("-p", "--parameter", action="append", help="A (key,value) pair for a template input parameter. Substitutions for {REGION} and {ACCOUNT} are available to e.g. support ARN construction. [can be used multiple times]")
parser.add_argument("-n", "--notification_arn", action="append", help="A SNS topic to send Stack event notifications to. Substitutions for {REGION} and {ACCOUNT} are available to e.g. support ARN construction. [can be used multiple times]")
parser.add_argument("-d", "--disable_rollback", action="store_true", help="Indicates whether or not to rollback on failure. [default: false]")
parser.add_argument("-t", "--timeout", type=int, help="Maximum amount of time to let the Stack spend creating itself. If this timeout is exceeded, the Stack will enter the CREATE_FAILED state.")
parser.add_argument("-i", "--enable_iam", action="store_true", help="Enable 'CAPABILITY_IAM'. [default: false]")
#parser.add_argument("-c", "--cababilities", help="The list of capabilities you want to allow in the stack. Currently, the only valid capability is 'CAPABILITY_IAM'")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

def processParameter(parameter, region_name, account_id):
    replacement = parameter[1].replace('{REGION}', region_name).replace('{ACCOUNT}', account_id)
    processedParameter = tuple([parameter[0], replacement])
    return processedParameter

def processArn(arn, region_name, account_id):
    return arn.replace('{REGION}', region_name).replace('{ACCOUNT}', account_id)

# execute business logic    
heading = "Creating CloudFormation stacks named '" + args.stack_name + "'"
regions = boto.cloudformation.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

from boto_cli.iam.accountinfo import AccountInfo
iam = boto.connect_iam(**credentials)
accountInfo = AccountInfo(iam)
account = accountInfo.describe()

template_body = None
template_url = None
# Is this a HTTP(S) template?
if not args.template.startswith('http'):
    template_file = open(args.template, 'r')
    template_body = template_file.read()

parameters = dict([])
if args.parameter:
    parameters = dict([parameter.split('=') for parameter in args.parameter])

notification_arns = []
if args.notification_arn:
    notification_arns = args.notification_arn

capabilities = []
if args.enable_iam:
    capabilities.append('CAPABILITY_IAM')

print heading + ":"
for region in regions:
    pprint(region.name, indent=2)
    try:
        cfn = boto.connect_cloudformation(region=region, **credentials)
        print 'Creating stack ' + args.stack_name
        processedParameters = dict([processParameter(item, region.name, account.id) for item in parameters.items()])
        processedArns = [processArn(item, region.name, account.id) for item in notification_arns]
        cfn.create_stack(args.stack_name, template_body=template_body, template_url=template_url, parameters=tuple(processedParameters.items()),
                         notification_arns=processedArns, disable_rollback=args.disable_rollback, timeout_in_minutes=args.timeout, capabilities=capabilities)
    except boto.exception.BotoServerError, e:
        print e.error_message
