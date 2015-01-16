# -*- coding: utf-8 -*-

"""
The State pattern allows an object to alter its behavior when its internal state changes.
The object will appear to change its class.
Python allows a very tricky thing: to change the object's class on-fly.
However in classical Java-style implementation we need to operate with instances of different states.
Both Python and then Java approaches are shown below.
"""
from abc import ABCMeta, abstractmethod


class Connection(object):
    def __init__(self):
        # initially connection is closed
        self.set_state(ConnectionClosed)

    def set_state(self, state):
        """
        Manipulate the __class__ directly so all its methods change their behavior
        """
        self.__class__ = state

    def read(self):
        raise NotImplementedError()

    def write(self, data):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class ConnectionOpened(Connection):
    """
    Opened connection state
    """

    def read(self):
        return 'reading...'

    def write(self, data):
        return 'writing ' + data

    def open(self):
        raise NotImplementedError('Connection is already opened')

    def close(self):
        # change the state
        self.set_state(ConnectionClosed)
        return 'closing connection...'


class ConnectionClosed(Connection):
    """
    Closed connection state
    """

    def read(self):
        raise NotImplementedError('Can not read from the closed connection')

    def write(self, data):
        raise NotImplementedError('Can not write to the closed connection')

    def open(self):
        # change the state
        self.set_state(ConnectionOpened)
        return 'opening connection...'

    def close(self):
        raise NotImplementedError('Connection is already closed')


if __name__ == '__main__':
    connection = Connection()
    assert connection.open() == 'opening connection...'
    assert connection.read() == 'reading...'
    assert connection.write('hello') == 'writing hello'
    assert connection.close() == 'closing connection...'


class ConnectionAbstract(object):
    """
    This is a base class for all states
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self, connection):
        """
        Read the data from an opened connection
        """
        pass

    @abstractmethod
    def write(self, connection, data):
        """
        Write the data into an opened connection
        """
        pass

    @abstractmethod
    def open(self, connection):
        """
        Opens a closed connection
        """
        pass

    @abstractmethod
    def close(self, connection):
        """
        Closes an opened connection
        """
        pass


class ConnectionOpened(ConnectionAbstract):
    """
    Opened connection state
    """

    def read(self, connection):
        return 'reading...'

    def write(self, connection, data):
        return 'writing ' + data

    def open(self, connection):
        raise NotImplementedError('Connection is already opened')

    def close(self, connection):
        # change the state
        connection.state = connection.closed_state
        return 'closing connection...'


class ConnectionClosed(ConnectionAbstract):
    """
    Closed connection state
    """

    def read(self, connection):
        raise NotImplementedError('Can not read from the closed connection')

    def write(self, connection, data):
        raise NotImplementedError('Can not write to the closed connection')

    def open(self, connection):
        # change the state
        connection.state = connection.opened_state
        return 'opening connection...'

    def close(self, connection):
        raise NotImplementedError('Connection is already closed')


class Connection(object):
    """
    Connection itself. It proxies the calls to its current state
    """

    def __init__(self, opened_state, closed_state):
        self.opened_state = opened_state
        self.closed_state = closed_state
        # by default the connection is closed
        self.state = self.closed_state

    def read(self):
        return self.state.read(self)

    def write(self, data):
        return self.state.write(self, data)

    def open(self):
        return self.state.open(self)

    def close(self):
        return self.state.close(self)


if __name__ == '__main__':
    connection = Connection(ConnectionOpened(), ConnectionClosed())
    assert connection.open() == 'opening connection...'
    assert connection.read() == 'reading...'
    assert connection.write('hello') == 'writing hello'
    assert connection.close() == 'closing connection...'