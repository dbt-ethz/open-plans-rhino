from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import api


class User:
    def __init__(self, email):
        self.__id = None
        self.__email = email

    @property
    def id(self):
        return self.__id

    @property
    def email(self):
        return self.__email

    def __repr__(self):
        return "{}(id={}, email={})".format(self.__class__.__name__, self.id, self.email)

    def user_login(self, password):
        resp = api.login(email=self.email, password=password)
        if resp['succeeded']:
            self.__id = resp['account_id']
            print('Login succesfull; {}'.format(self.__repr__()))
        else:
            print(resp['error'])
