# NOTE: equivalent of https://github.com/boto/boto/pull/891 until upstream release catches up.
from boto.cloudformation.connection import CloudFormationConnection
from boto.regioninfo import RegionInfo

RegionData = {
    'us-east-1': 'cloudformation.us-east-1.amazonaws.com',
    'us-west-1': 'cloudformation.us-west-1.amazonaws.com',
    'us-west-2': 'cloudformation.us-west-2.amazonaws.com',
    'sa-east-1': 'cloudformation.sa-east-1.amazonaws.com',
    'eu-west-1': 'cloudformation.eu-west-1.amazonaws.com',
    'ap-northeast-1': 'cloudformation.ap-northeast-1.amazonaws.com',
    'ap-southeast-1': 'cloudformation.ap-southeast-1.amazonaws.com'}


def regions():
    """
    Get all available regions for the CloudFormation service.

    :rtype: list
    :return: A list of :class:`boto.RegionInfo` instances
    """
    regions = []
    for region_name in RegionData:
        region = RegionInfo(name=region_name,
                            endpoint=RegionData[region_name],
                            connection_cls=CloudFormationConnection)
        regions.append(region)
    return regions


def connect_to_region(region_name, **kw_params):
    """
    Given a valid region name, return a
    :class:`boto.cloudformation.CloudFormationConnection`.

    :param str region_name: The name of the region to connect to.

    :rtype: :class:`boto.cloudformation.CloudFormationConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
        name is given
    """
    for region in regions():
        if region.name == region_name:
            return region.connect(**kw_params)
    return None
