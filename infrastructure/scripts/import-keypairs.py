import argparse
import boto
import boto.ec2
from pprint import pprint

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Imports a key pair in all/some available EC2 regions')
parser.add_argument("key_name", help="A key pair name")
parser.add_argument("public_key", help="The key pair's public key")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

# execute business logic
heading = "Importing key pair named '" + args.key_name + "'"
regions = boto.ec2.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

public_key_file = open(args.public_key, 'r')
public_key_body = public_key_file.read()

print heading + ":"
for region in regions:
    pprint(region.name, indent=2)
    try:
        ec2 = boto.connect_ec2(region=region, **credentials)
        print 'Importing key pair ' + args.key_name
        ec2.import_key_pair(args.key_name, public_key_body)
    except boto.exception.BotoServerError, e:
        print e.error_message
