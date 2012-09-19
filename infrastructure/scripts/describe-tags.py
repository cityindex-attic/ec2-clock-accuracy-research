#!/usr/bin/python
import argparse
import boto
import boto.ec2
from boto_cli import configure_logging
import logging
log = logging.getLogger('boto_cli')

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Describe AWS resource tags in all/some available EC2 regions')
parser.add_argument("-f", "--filter", action="append", help="An AWS resource filter. [can be used multiple times]")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
parser.add_argument("-l", "--log", dest='log_level', default='WARNING',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help="The logging level to use. [default: WARNING]")
args = parser.parse_args()

configure_logging(log, args.log_level)

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

# execute business logic    
credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}
heading = "Describing AWS resource tags"
regions = boto.ec2.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

filters = None
if args.filter:
    filters = dict([filter.split('=') for filter in args.filter])
log.info(args.filter)
log.debug(filters)

print heading + ":"
for region in regions:
    try:
        ec2 = boto.connect_ec2(region=region, **credentials)
        resources = ec2.get_all_tags(filters=filters)
        print region.name + ": " + str(len(resources)) + " resources with tags"
        for resource in resources:
           print "type: " + resource.res_type + ", id: " + resource.res_id + ", key: " + resource.name + ", value: " + resource.value
    except boto.exception.BotoServerError, e:
        log.error(e.error_message)
