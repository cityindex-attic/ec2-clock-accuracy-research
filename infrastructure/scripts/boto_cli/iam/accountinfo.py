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
        try:
            alias = self.connection.get_account_alias()
            self.alias = alias['list_account_aliases_response']['list_account_aliases_result']['account_aliases'][0]
        except boto.exception.BotoServerError, e:
            print e.error_message
        try:
            # TODO: there should be a better way to retrieve the account id, which is 'leaked in the exception anyway
            # eventually; see http://stackoverflow.com/questions/10197784 for a respective question.
            if not self.user:
                from userinfo import UserInfo
                userInfo = UserInfo(self.connection)
                self.user = userInfo.describe()
            self.id = self.user.arn.replace('arn:aws:iam::', '').partition(':')[0]
        except boto.exception.BotoServerError, e:
            self.id = e.error_message.replace('User: arn:aws:iam::', '').partition(':')[0]
            print e.error_message
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
