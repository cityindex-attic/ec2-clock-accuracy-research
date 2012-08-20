#!/usr/bin/python
import argparse
import boto
import boto.cloudformation
from boto_cli import configure_logging
import logging
log = logging.getLogger('boto_cli')
import os
import platform
from pprint import pprint
import sys

# NOTE: equivalent of https://github.com/boto/boto/pull/891 until upstream release catches up.
import patch9d3c9f0
boto.cloudformation.regions = patch9d3c9f0.regions
boto.cloudformation.connect_to_region = patch9d3c9f0.connect_to_region

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Validates a CloudFormation stack template')
parser.add_argument("template", help="A stack template local file or a S3 URL. Substitutions for {REGION} and {ACCOUNT} are available to support S3 URL construction.")
parser.add_argument("-r", "--region", help="A region substring selector (e.g. 'us-west')")
parser.add_argument("--access_key_id", dest='aws_access_key_id', help="Your AWS Access Key ID")
parser.add_argument("--secret_access_key", dest='aws_secret_access_key', help="Your AWS Secret Access Key")
parser.add_argument("-v", "--verbose", action='store_true') # TODO: drop in favor of a log formatter?!
parser.add_argument("-l", "--log", dest='log_level', default='WARNING',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help="The logging level to use. [default: WARNING]")
args = parser.parse_args()

credentials = {'aws_access_key_id': args.aws_access_key_id, 'aws_secret_access_key': args.aws_secret_access_key}

def isSelected(region):
    return True if region.name.find(args.region) != -1 else False

configure_logging(log, args.log_level)

def processArgument(argument, region_name):
    return argument.replace('{REGION}', region_name)

def printResult(name, template):
    print "Template '" + name + "' is valid."
    if args.verbose:
        print "\rDescription: " + template.description
        print "\rParameters: "
        for parameter in template.template_parameters:
            pprint (vars(parameter), indent=2)

# execute business logic
heading = "Validating CloudFormation template '" + args.template + "':"
regions = boto.cloudformation.regions()
if args.region:
    heading += " (filtered by region '" + args.region + "')"
    regions = filter(isSelected, regions)

try:
    # Is this a HTTP(S) template?
    if args.template.startswith('http'):
        for region in regions:
            pprint(region.name, indent=2)
            cfn = boto.connect_cloudformation(region=region, **credentials)
            template_url = processArgument(args.template, region.name)
            # handle S3 legacy issue regarding region 'US Standard', see e.g. https://forums.aws.amazon.com/message.jspa?messageID=185820  
            if region.name == 'us-east-1':
                template_url = template_url.replace('-us-east-1', '', 1)
            template = cfn.validate_template(template_url=template_url)
            printResult(template_url, template)
    else:
        cfn = boto.connect_cloudformation(region=regions[0], **credentials)
        template_file = open(args.template, 'r')
        template_body = template_file.read()
        template = cfn.validate_template(template_body=template_body)
        printResult(args.template, template)
except boto.exception.BotoServerError, e:
    log.error(e.error_message)
    sys.exit(1)
