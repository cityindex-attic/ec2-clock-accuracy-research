import boto
import boto.iam

class AccountInfo:
    """
    Represents an AWS Account
    """

    def __init__(self, iam_connection):
        self.connection = iam_connection
        self.user = None

    def __repr__(self):
        return '<AccountInfo - alias:%s id:%s>' % (self.alias, self.id)

    def describe(self, user=None):
        self.account = {}
        alias = self.connection.get_account_alias()
        self.alias = alias['list_account_aliases_response']['list_account_aliases_result']['account_aliases'][0]
        if not self.user:
            from userinfo import UserInfo
            userInfo = UserInfo(self.connection)
            self.user = userInfo.describe()
        self.id = self.user.arn.replace('arn:aws:iam::', '').partition(':')[0]
        return self

# Sample exercise of class functionality (requires AWS credentials to be provided externally) 
if __name__ == "__main__":
    try:
        iam = boto.connect_iam()
        accountInfo = AccountInfo(iam)
        account = accountInfo.describe()
        print account
    except boto.exception.BotoServerError, e:
        print e.error_message
