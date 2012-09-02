#!/usr/bin/python
import argparse
import boto
import boto.ec2
from pprint import pprint

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Describe EC2 security groups in all/some available EC2 regions')
parser.add_argument("-f", "--filter", action="append", help="A (key,value) pair for a filter to limit the results returned. [can be used multiple times]")
parser.add_argument("-li", "--instances", action="store_true", help="List all instances currently running within this security group")
parser.add_argument("-lr", "--rules", action="store_true", help="List all rules currently active in this security group")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

# execute business logic
heading = "Describing EC2 security groups"
regions = boto.ec2.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)
if args.filter:
    for filter in args.filter:
        heading += " (filtered by filter '" + filter + "')"

filters = dict([filter.split('=') for filter in args.filter]) if args.filter else None

print heading + ":"
for region in regions:
    pprint(region.name, indent=2)
    try:
        ec2 = boto.connect_ec2(region=region, **credentials)
        groups = ec2.get_all_security_groups(filters=filters)
        for group in groups:
            vpc_id = "|" + group.vpc_id if group.vpc_id else ""
            print("\n" + group.name + " (" + group.id + vpc_id + " - " + group.description + "):")
            if args.rules:
                print("... rules ...")
                for rule in group.rules:
                    pprint(rule)
                if group.vpc_id:
                    print("... rules (egress) ...")
                    for rule in group.rules_egress:
                        pprint(rule)
            if args.instances:
                print("... instances ...")
                for instance in group.instances():
                    pprint(instance)
    except boto.exception.BotoServerError, e:
        print e.error_message
