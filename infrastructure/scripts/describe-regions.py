#!/usr/bin/python
import argparse
import boto
import boto.ec2
from pprint import pprint

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Describe all/some available EC2 regions')
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

# execute business logic
heading = "Describing regions for EC2"
regions = boto.ec2.regions(**credentials)
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

print heading + ":"
for region in regions:
    pprint(vars(region), indent=2)
