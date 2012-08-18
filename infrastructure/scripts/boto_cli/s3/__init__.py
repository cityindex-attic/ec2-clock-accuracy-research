import logging
s3_log = logging.getLogger('boto_cli.s3')

RegionMap = {
    'DEFAULT': 'us-east-1',
    'USWest': 'us-west-1',
    'USWest2': 'us-west-2',
    'SAEast': 'sa-east-1',
    'EU': 'eu-west-1',
    'APNortheast': 'ap-northeast-1',
    'APSoutheast': 'ap-southeast-1'}

# NOTE: S3 region handling differs in an unfortunate way (likely a legacy issue) and requires special treatment.
def class_iterator(Class):
    return (element for element in dir(Class) if element[:2] != '__')
