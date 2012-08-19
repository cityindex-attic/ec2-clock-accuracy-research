#!/usr/bin/python
import argparse
import boto
import boto.cloudformation
from boto_cli import configure_logging
import logging
log = logging.getLogger('boto_cli')
from pprint import pprint

# NOTE: equivalent of https://github.com/boto/boto/pull/891 until upstream release catches up.
import patch9d3c9f0
boto.cloudformation.regions = patch9d3c9f0.regions
boto.cloudformation.connect_to_region = patch9d3c9f0.connect_to_region

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Describe CloudFormation stacks in all/some available CloudFormation regions')
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("-s", "--stack_name_or_id", default='', help="Name or id (ARN) of stack to describe")
parser.add_argument("--xml", action='store_true', help="Return result as XML")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
parser.add_argument("-v", "--verbose", action='store_true') # TODO: drop in favor of a log formatter?!
parser.add_argument("-l", "--log", dest='log_level', default='WARNING',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help="The logging level to use. [default: WARNING]")
args = parser.parse_args()

configure_logging(log, args.log_level)

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

# execute business logic
credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}
heading = "Describing CloudFormation stacks"
regions = boto.cloudformation.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

if args.xml:
    print "<describe-stacks>"
else:
    print heading + ":"
for region in regions:
    if args.xml:
        print "<region name='" + region.name + "'>"
    else:
        pprint(region.name, indent=2)
    try:
        cfn = boto.connect_cloudformation(region=region, **credentials)
        stacks = cfn.describe_stacks(args.stack_name_or_id)

        for stack in stacks:
            if not args.xml:
                print stack.stack_name
            if args.xml:
                print stack.connection._pool.host_to_pool.values()[0].queue[0][0]._HTTPConnection__response._cached_response.replace("xmlns=\"http://cloudformation.amazonaws.com/doc/2010-05-15/\"","")
            if args.verbose:
                pprint(vars(stack), indent=2)
            log.debug(vars(stack))
    except boto.exception.BotoServerError, e:
        log.error(e.error_message)
    if args.xml:
        print "</region>"
if args.xml:
    print "</describe-stacks>"
