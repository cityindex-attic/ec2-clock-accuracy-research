import boto
import boto.iam

class UserInfo:
    """
    Represents an AWS User
    """

    def __init__(self, iam_connection):
        self.connection = iam_connection

    def __repr__(self):
        return '<UserInfo - path:%s create_date:%s id:%s arn:%s name:%s>' % (self.path, self.create_date, self.id, self.arn, self.name)

    def describe(self):
        user = self.connection.get_user()
        self.user = user['get_user_response']['get_user_result']['user']
        self.path = self.user['path']
        self.create_date = self.user['create_date']
        self.id = self.user['user_id']
        self.arn = self.user['arn']
        self.name = self.user['user_name']
        return self

# Sample exercise of class functionality (requires AWS credentials to be provided externally) 
if __name__ == "__main__":
    try:
        iam = boto.connect_iam()
        userInfo = UserInfo(iam)
        user = userInfo.describe()
        print user
    except boto.exception.BotoServerError, e:
        print e.error_message
