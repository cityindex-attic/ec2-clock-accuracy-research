import argparse
import boto
import boto.s3
from boto.s3.connection import Location
from pprint import pprint

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Create an S3 bucket in all/some available CloudFormation regions')
parser.add_argument("bucket", help="A bucket name (will get region suffix)")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if RegionMapS3[location].find(args.region) != -1 else False

# NOTE: S3 region handling differs in an unfortunate way (likely a legacy issue) and requires special treatment.
def class_iterator(Class):
    return (element for element in dir(Class) if element[:2] != '__')

RegionMapS3 = {
    'DEFAULT': 'us-east-1',
    'USWest': 'us-west-1',
    'USWest2': 'us-west-2',
    'SAEast': 'sa-east-1',
    'EU': 'eu-west-1',
    'APNortheast': 'ap-northeast-1',
    'APSoutheast': 'ap-southeast-1'}

# execute business logic
heading = "Creating S3 buckets named '" + args.bucket + "'"
locations = class_iterator(Location)
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    locations = filter(isSelected, locations)

s3 = boto.connect_s3(**credentials)

print heading + ":"
for location in locations:
    region = RegionMapS3[location]
    pprint(region, indent=2)
    try:
        bucket = args.bucket + '-' + region
        print 'Creating bucket ' + bucket
        s3.create_bucket(bucket, location=getattr(Location, location))
    except boto.exception.BotoServerError, e:
        print e.error_message
