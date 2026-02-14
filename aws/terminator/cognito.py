from . import Terminator


class CognitoUserPool(Terminator):
    @staticmethod
    def create(credentials):
        return Terminator._create(
            credentials, CognitoUserPool, 'cognito-idp',
            lambda client: client.get_paginator('list_user_pools').paginate(MaxResults=60).build_full_result()['UserPools']
        )

    @property
    def id(self):
        return self.instance['Id']

    @property
    def name(self):
        return self.instance['Name']

    @property
    def created_time(self):
        return self.instance['CreationDate']

    def terminate(self):
        # User pool domains must be deleted before the user pool can be deleted
        user_pool = self.client.describe_user_pool(UserPoolId=self.id)['UserPool']
        if user_pool.get('Domain'):
            self.client.delete_user_pool_domain(
                Domain=user_pool['Domain'],
                UserPoolId=self.id,
            )
        self.client.delete_user_pool(UserPoolId=self.id)
