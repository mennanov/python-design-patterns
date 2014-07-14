# -*- coding: utf-8 -*-

"""
The Singleton pattern ensures a class has only one instance and provides an easy access to it.
Python implementation differs significantly than the Java implementation.
In Java the constructor becomes private in order to prevent the direct instance creation
and provides a special public static method which controls the instantiation.
In Python we have several different approaches:
1. overwrite the __new__ method which controls the instance creation (easiest)
2. create a Singleton mixin class which will be used to wrap the __new__ method (better, since it can be reused)
3. use a singleton class decorator to do the same: overwrite __new__ method (the best, but has some caveats)
4. use a Singleton metaclass and modify its __call__ method to control the instance creation (this is cool)
"""


class DBConnection(object):
    """
    A class that must be instantiated only once.
    """

    def __init__(self):
        # does some actions here which must no be executed twice
        # during the program execution
        pass


class DBConnectionSingleton(DBConnection):
    """
    This is the first option: overwrite the __new__ method
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # no instance so far: create a new one and save it to the class attribute
            cls._instance = super(DBConnectionSingleton, cls).__new__(cls, *args, **kwargs)
        # return the saved instance
        return cls._instance


if __name__ == '__main__':
    db1 = DBConnectionSingleton()
    db2 = DBConnectionSingleton()
    assert db1 is db2


class SingletonMixin(object):
    """
    A reusable singleton mixin which can be used with any class
    """

    # a dictionary with instances of different classes
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # no instance so far: create a new one and save it to the class attribute
            cls._instances[cls] = super(SingletonMixin, cls).__new__(cls, *args, **kwargs)
        # return the saved instance
        return cls._instances[cls]


class DBConnectionMixed(DBConnection, SingletonMixin):
    pass


if __name__ == '__main__':
    db1 = DBConnectionMixed()
    db2 = DBConnectionMixed()
    assert db1 is db2


def singleton(class_):
    """
    Singleton class decorator
    """

    class SingletonWrapper(class_):
        """
        This is a wrapper class which overwrites the __new__ method like we did before in the first example.
        This method has a drawback: the type of the wrapped class has changed to SingletonWrapper.
        It may lead to insidious bugs in a later code like: "if type(db) == DBConnection"
        """

        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                # no instance so far: create a new one and save it to the class attribute
                cls._instance = super(SingletonWrapper, cls).__new__(cls, *args, **kwargs)
            # return the saved instance
            return cls._instance

    return SingletonWrapper


@singleton
class DBConnectionDecorated(DBConnection):
    pass


if __name__ == '__main__':
    db1 = DBConnectionDecorated()
    db2 = DBConnectionDecorated()
    assert db1 is db2


class SingletonMeta(type):
    """
    A singleton meta class: it implements a custom __call__ method which creates an instance.
    """

    def __init__(self, what, bases, attrs):
        super(SingletonMeta, self).__init__(what, bases, attrs)
        # a class will have an _instance attribute to store its single instance
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(SingletonMeta, self).__call__(*args, **kwargs)
        return self._instance


class DBConnectionFancy(DBConnection):
    """
    Its class meta class is a SingletonMeta which handles the instance creation.
    It is a very convenient approach, but it also has a drawback: what if this class is intended to
    use another meta class besides SingletonMeta (ex. ABCMeta)?
    In this case you will have to create an ABCSingletonMetaMerge class and merge 2 meta classes into one.
    """
    __metaclass__ = SingletonMeta


if __name__ == '__main__':
    db1 = DBConnectionFancy()
    db2 = DBConnectionFancy()
    assert db1 is db2
