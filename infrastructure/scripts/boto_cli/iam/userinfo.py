import boto
import boto.iam
import logging

class UserInfo:
    """
    Represents an AWS User
    """

    def __init__(self, iam_connection):
        self.connection = iam_connection
        self.log = logging.getLogger('boto_cli.iam.UserInfo')
        # populate those attributes not leaked via the exception, if user has no permission for iam:GetUser
        self.path = '<not authorized>'
        self.create_date = '<not authorized>'
        self.id = '<not authorized>' # TODO: could be deduced from credentials in use instead.

    def __repr__(self):
        return '<UserInfo - path:%s create_date:%s id:%s arn:%s name:%s>' % (self.path, self.create_date, self.id, self.arn, self.name)

    def describe(self):
        try:
            user = self.connection.get_user()
            self.user = user['get_user_response']['get_user_result']['user']
            self.path = self.user['path']
            self.create_date = self.user['create_date']
            self.id = self.user['user_id']
            self.arn = self.user['arn']
            self.name = self.user['user_name']
        except boto.exception.BotoServerError, e:
            # NOTE: given some information can be deduced from the exception still, the lack of permissions is 
            # considered a normal condition still and the exception handled/logged accordingly. 
            self.arn = e.error_message.rpartition(' ')[2]
            self.name = e.error_message.rpartition('/')[2]
            self.log.debug(e.error_message)
        self.log.debug(self)
        return self

# Sample exercise of class functionality (requires AWS credentials to be provided externally) 
if __name__ == "__main__":
    try:
        iam = boto.connect_iam()
        userInfo = UserInfo(iam)
        user = userInfo.describe()
        print user
    except boto.exception.BotoServerError, e:
        logging.exception(e.error_message)
