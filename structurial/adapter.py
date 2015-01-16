# -*- coding: utf-8 -*-

"""
The Adapter pattern converts the interface of a class into another interface the clients expect.
Adapter lets classes work together that couldn't otherwise because of the incompatible interfaces.
There are two different kinds of this pattern: object adapters and class adapters.

Object adapters use composition and delegation to be able to mimic the adaptee interface: so it can be used
with ANY of subclasses of the adaptee class, but it needs to instantiate an adaptee class to delegate calls to it.

Class adapters use multiple inheritance and implement only absent methods and don't need an instance of the adaptee,
but it can be used only with the concrete adaptee class - it may not work with adaptee subclasses.
Also it can be a huge problem to resolve conflicts if the adaptee class differs to much from the other class.
"""


class Duck(object):
    """
    Just a duck who quacks
    """

    def quack(self):
        return 'quack!'

    def move(self):
        return 'duck is swimming'


class Turkey(object):
    """
    Just a turkey who gobbles
    """

    def gobble(self):
        return 'gobble!'

    def move(self):
        return 'turkey is walking'


class TurkeyAdapter(object):
    def __init__(self, turkey):
        self.turkey = turkey

    def quack(self):
        # delegate to turkey instance
        return self.turkey.gobble()

    def __getattr__(self, item):
        # Python provides a cool feature: we can try to delegate any missed methods in the adapter to the adaptee
        # but it may raise an AttributeError exception,
        # so the client code must be able to handle these exceptions properly
        return getattr(self.turkey, item)


if __name__ == '__main__':
    duck = Duck()
    assert duck.quack() == 'quack!'
    assert duck.move() == 'duck is swimming'
    turkey_adapted = TurkeyAdapter(Turkey())
    assert turkey_adapted.quack() == 'gobble!'
    # we haven't implemented this method in the adapter, but it will work due to __getattr__ delegation logic
    assert turkey_adapted.move() == 'turkey is walking'


class TurkeyClassAdapter(Turkey, Duck):
    """
    It is a class adapter: we inherit from both  Turkey and Duck classes
    and implement only the missed methods in Turkey class.
    Note: the order of the base classes does matter!
    """

    def quack(self):
        return self.gobble()


if __name__ == '__main__':
    duck = Duck()
    assert duck.quack() == 'quack!'
    assert duck.move() == 'duck is swimming'
    turkey_adapted = TurkeyClassAdapter()
    assert turkey_adapted.quack() == 'gobble!'
    # we haven't implemented this method in the adapter explicitly, but it will work due to inheritance
    assert turkey_adapted.move() == 'turkey is walking'