#!/usr/bin/python
import argparse
import boto
import boto.s3
from boto.s3.connection import Location
from boto_cli import configure_logging
from boto_cli.s3 import class_iterator
from boto_cli.s3 import RegionMap
import logging
log = logging.getLogger('boto_cli')
from pprint import pprint

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Create a S3 bucket in all/some available S3 regions')
parser.add_argument("bucket", help="A bucket name (will get region suffix)")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
parser.add_argument("-l", "--log", dest='log_level', default='WARNING',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help="The logging level to use. [default: WARNING]")
args = parser.parse_args()

configure_logging(log, args.log_level)

def isSelected(region):
    return True if RegionMap[region].find(args.region) != -1 else False

# execute business logic
credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}
heading = "Creating S3 buckets named '" + args.bucket + "'"
locations = class_iterator(Location)
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    locations = filter(isSelected, locations)

s3 = boto.connect_s3(**credentials)

print heading + ":"
for location in locations:
    region = RegionMap[location]
    pprint(region, indent=2)
    try:
        bucket_name = args.bucket + '-' + region
        print 'Creating bucket ' + bucket_name
        s3.create_bucket(bucket_name, location=getattr(Location, location))
    except boto.exception.BotoServerError, e:
        log.error(e.error_message)
