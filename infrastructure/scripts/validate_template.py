import argparse
import boto
import boto.cloudformation
from pprint import pprint

# NOTE: equivalent of https://github.com/boto/boto/pull/891 until upstream release catches up.
import patch9d3c9f0
boto.cloudformation.regions = patch9d3c9f0.regions
boto.cloudformation.connect_to_region = patch9d3c9f0.connect_to_region

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Validates a CloudFormation stack template')
parser.add_argument("template", help="A stack template local file or URL (URL not supported yet!)")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

# execute business logic
heading = "Validating CloudFormation template '" + args.template + "':"
regions = boto.cloudformation.regions()

template_body = None
template_url = None
# Is this a HTTP(S) template?
if not args.template.startswith('http'):
    f = open(args.template, 'r')
    template_body = f.read()

try:
    cfn = boto.connect_cloudformation(region=regions[0], **credentials)
    template = cfn.validate_template(template_body=template_body, template_url=template_url)
    print "Template '" + args.template + "' is valid."
    print "\rDescription: " + template.description
    print "\rParameters: "
    for parameter in template.template_parameters:
        pprint (vars(parameter), indent=2)
except boto.exception.BotoServerError, e:
    print e.error_message
