# -*- coding: utf-8 -*-

"""
The Singleton design pattern has a catchy name, but the wrong focus—on identity rather than on state.
The Borg design pattern has all instances share state instead. It also handles inheritance well.
Python implementation is very easy.
"""


class Borg(object):
    _shared_state = {}

    def __init__(self, login, password):
        # set the instance state (all attributes) to a shared state
        self.__dict__ = self._shared_state
        # set any other attributes
        self.login = login
        self.password = password


if __name__ == '__main__':
    b1 = Borg('root', 'pass')
    b2 = Borg('admin', 'password')
    assert b1.login == 'admin' and b1.password == 'password'