# -*- coding: utf-8 -*-

"""
The Abstract Factory pattern provides an interface for creating families of related or dependant objects
without specifying their concrete classes.
Python-style and Java-style implementations below.
"""
from abc import ABCMeta, abstractmethod


class ThinCrust(object):
    """
    A concrete ingredient
    """

    def __str__(self):
        return 'Thin crust'


class PuffPastry(object):
    """
    A concrete ingredient
    """

    def __str__(self):
        return 'Puff pastry'


class Cheese(object):
    """
    A concrete ingredient
    """

    def __str__(self):
        return 'Cheese'


class Bacon(object):
    """
    A concrete ingredient
    """

    def __str__(self):
        return 'Bacon'


class Pizza(object):
    """
    Pizza
    """

    def __init__(self, dough_cls, filling_cls):
        self.dough = dough_cls()
        self.filling = filling_cls()

    def __str__(self):
        return 'Pizza with {} and {}'.format(str(self.dough), str(self.filling))


if __name__ == '__main__':
    # in Python we don't need a dedicated factory class since we may pass the needed classes as arguments
    italian_pizza = Pizza(ThinCrust, Cheese)
    americano_pizza = Pizza(PuffPastry, Bacon)
    assert str(italian_pizza) == 'Pizza with Thin crust and Cheese'
    assert str(americano_pizza) == 'Pizza with Puff pastry and Bacon'


class IngredientsFactory(object):
    """
    Pizza needs ingredients to be baked.
    So this class is going to be an abstract factory which will let
    its subclasses implement the creation of concrete ingredients instances.
    """

    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def create_dough():
        pass

    @staticmethod
    @abstractmethod
    def create_filling():
        pass


class ItalianIngredientsFactory(IngredientsFactory):
    @staticmethod
    def create_dough():
        return ThinCrust()

    @staticmethod
    def create_filling():
        return Cheese()


class AmericanIngredientsFactory(IngredientsFactory):
    @staticmethod
    def create_dough():
        return PuffPastry()

    @staticmethod
    def create_filling():
        return Bacon()


class Pizza(object):
    """
    Pizza
    """

    def __init__(self, factory):
        self.dough = factory.create_dough()
        self.filling = factory.create_filling()

    def __str__(self):
        return 'Pizza with {} and {}'.format(str(self.dough), str(self.filling))


if __name__ == '__main__':
    italian_pizza = Pizza(ItalianIngredientsFactory())
    american_pizza = Pizza(AmericanIngredientsFactory())
    assert str(italian_pizza) == 'Pizza with Thin crust and Cheese'
    assert str(american_pizza) == 'Pizza with Puff pastry and Bacon'
