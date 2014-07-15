# -*- coding: utf-8 -*-

"""
The Proxy pattern provides a surrogate or a placeholder for another object to control
access to it.
A very simple example: we want to avoid calling a certain methods on a class - proxy handles that job.
"""


class Dog(object):
    """
    This is a dog :)
    """

    def jump(self):
        return 'jump'

    def bark(self):
        return 'bark'


class DogProxy(object):
    """
    Proxy all the attribute accesses and deny ones which are restricted.
    """

    def __init__(self, restrict, *args, **kwargs):
        self._restrict = restrict
        self.dog = Dog(*args, **kwargs)

    def __getattr__(self, item):
        if item not in self._restrict:
            return getattr(self.dog, item)
        else:
            raise AttributeError(item)


if __name__ == '__main__':
    dog = DogProxy(['bark'])
    assert dog.jump() == 'jump'
    try:
        dog.bark()
    except AttributeError:
        # this method is restricted by proxy
        pass