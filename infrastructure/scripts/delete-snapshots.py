#!/usr/bin/python
import argparse
import boto
import boto.ec2
from boto_cli import configure_logging
from boto_cli.ec2 import *
import logging
log = logging.getLogger('boto_cli')
from pprint import pprint

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Delete snapshots of EBS volumes in all/some available EC2 regions')
parser.add_argument("-f", "--filter", action="append", help="An EBS volume filter. [can be used multiple times]")
parser.add_argument("-i", "--id", dest="resource_ids", action="append", help="An EBS volume id. [can be used multiple times]")
parser.add_argument("-br", "--backup_retention", type=int, default=1, help="The number of backups to retain (correlated via backup_set). [default: 1]")
parser.add_argument("-bs", "--backup_set", default=DEFAULT_BACKUP_SET, help="A backup set name (determines retention correlation). [default: 'default']")
parser.add_argument("-ns", "--no_origin_safeguard", action="store_true", help="Allow deletion of snapshots originating from other tools. [default: False]")
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
heading = "Deleting EBS snapshots"
regions = boto.ec2.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

filters = None
if args.filter:
    filters = dict([filter.split('=') for filter in args.filter])
log.info(args.filter)
log.debug(filters)
log.info(args.resource_ids)

backup_set = args.backup_set if args.backup_set else DEFAULT_BACKUP_SET
log.debug(backup_set)

print heading + ":"
for region in regions:
    try:
        ec2 = boto.connect_ec2(region=region, **credentials)
        volumes = ec2.get_all_volumes(volume_ids=args.resource_ids, filters=filters)
        print region.name + ": " + str(len(volumes)) + " volumes"
        delete_snapshots(ec2, volumes, backup_set, args.backup_retention, args.no_origin_safeguard)
    except boto.exception.BotoServerError, e:
        log.error(e.error_message)
