# -*- coding: utf-8 -*-

"""
The Strategy design pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.
Strategy lets the algorithm vary independently from clients that use it.
This pattern is practically non-existent in languages that support first class functions as Python does.
However the both implementations are provided here: Python-style and Java-style
"""


def strategy_add(a, b):
    return a + b


def strategy_minus(a, b):
    return a - b


if __name__ == '__main__':
    solver = strategy_add
    assert solver(1, 2) == 3
    solver = strategy_minus
    assert solver(2, 1) == 1


class Duck(object):
    """
    This is a base Duck class
    """

    def __init__(self, fly_behavior, quack_behavior):
        # we store the instance of the object who actually knows how to fly
        self.fly_behavior = fly_behavior
        # and quack also
        self.quack_behavior = quack_behavior

    def fly(self):
        # delegate that call the object who knows how to do it
        return self.fly_behavior.fly()

    def quack(self):
        # delegate that call the object who knows how to do it
        return self.quack_behavior.quack()


class RedHeadDuck(Duck):
    """
    This is a duck with a red head
    """

    def __init__(self, *args, **kwargs):
        # define behaviors explicitly
        super(RedHeadDuck, self).__init__(FlyingBehavior(), QuackingBehavior())


class RubberDuck(Duck):
    """
    This is a rubber duck which swims in a bath
    """

    def __init__(self, *args, **kwargs):
        # define behaviors explicitly
        super(RubberDuck, self).__init__(NoFlyBehavior(), NoQuackBehavior())


class FlyingBehavior(object):
    """
    This is called FlyingBehavior not RedHeadFlyingBehavior intentionally
    since it is not bound to any exact Duck and can be used by any Duck.
    """

    def fly(self):
        return "I'm flying!"


class QuackingBehavior(object):
    def quack(self):
        return "Quack!"


class NoFlyBehavior(object):
    def fly(self):
        return "I can't fly :("


class NoQuackBehavior(object):
    def quack(self):
        return "I can't quack :("


if __name__ == '__main__':
    redhead_duck = RedHeadDuck()
    rubber_duck = RubberDuck()

    assert redhead_duck.fly() == "I'm flying!"
    assert rubber_duck.fly() == "I can't fly :("