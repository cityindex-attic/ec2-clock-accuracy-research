#!/usr/bin/python
import argparse
import boto
import boto.ec2
from pprint import pprint

# TODO: enable cross account usage via src_security_group_owner_id?
def revokeSource():
    ec2.revoke_security_group(group_name=args.name, group_id=args.id, ip_protocol=args.ip_protocol,
                                 from_port=args.from_port, to_port=args.to_port,
                                 src_security_group_name=args.security_group_name, src_security_group_group_id=args.security_group_id)

def revokeIp():
    ec2.revoke_security_group(group_name=args.name, group_id=args.id, ip_protocol=args.ip_protocol,
                                 from_port=args.from_port, to_port=args.to_port, cidr_ip=args.cidr_ip)

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Remove an existing rule from an existing security group in all/some available EC2 regions')
target_group = parser.add_mutually_exclusive_group(required=True)
target_group.add_argument("-n", "--name", help="The security group name")
target_group.add_argument("-i", "--id", help="The security group id (required in VPC)")
parser.add_argument("--ip_protocol", choices=['tcp', 'udp', 'icmp'], required=True, help="The IP protocol you are enabling")
parser.add_argument("--from_port", type=int, required=True, help="The beginning port number you are enabling")
parser.add_argument("--to_port", type=int, required=True, help="The ending port number you are enabling")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
# sub-commands
subparsers = parser.add_subparsers(title='sub-commands', help='All available sub-commands')
# sub-command 'source'
parser_source = subparsers.add_parser('group', help='Authorize by security group')
source_group = parser_source.add_mutually_exclusive_group(required=True)
source_group.add_argument("--security_group_name", help="The name of the security group you are granting access to")
source_group.add_argument("--security_group_id", help="The id of the security group you are granting access to")
#parser_source.add_argument("--security_group_owner_id", required=True, help="The ID of the owner of the security group you are granting access to")
parser_source.set_defaults(func=revokeSource)
# sub-command 'ip'
parser_ip = subparsers.add_parser('cidr', help='Authorize by CIDR address')
parser_ip.add_argument("--cidr_ip", required=True, help="The CIDR block you are providing access to")
parser_ip.set_defaults(func=revokeIp)
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

# execute business logic
group_name = args.name if args.name else ""
group_id = args.id if args.id else ""
heading = "Revoking EC2 security groups '" + group_name + group_id + "'"
regions = boto.ec2.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

groupnames = [args.name] if args.name else None
group_ids = [args.id] if args.id else None

print heading + ":"
for region in regions:
    pprint(region.name, indent=2)
    try:
        ec2 = boto.connect_ec2(region=region, **credentials)
        args.func()
    except boto.exception.BotoServerError, e:
        print e.error_message
