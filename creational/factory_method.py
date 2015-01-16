# -*- coding: utf-8 -*-

"""
The Factory Method pattern defines an interface for creating an object,
but lets subclasses decide which class to instantiate.
Factory method lets a class defer instantiation to subclass.
Factory is not very common to Python since it is actually "built-in" due to
the first class functions and classes we can pass a needed class to instantiate as an argument.
Both Python version and Java-style version are shown below.
"""
from abc import ABCMeta, abstractmethod


class OrderPizza(object):
    """
    In Python we usually don't need a dedicated method to create an instance:
    we can just pass the needed class as a parameter.
    """

    def __init__(self, pizza_cls):
        self.pizza = pizza_cls()


class RoundedPizza(object):
    def __str__(self):
        return 'Rounded pizza'


class SquaredPizza(object):
    def __str__(self):
        return 'Squared pizza'


if __name__ == '__main__':
    # make an order with rounded pizza
    order = OrderPizza(RoundedPizza)
    assert str(order.pizza) == 'Rounded pizza'
    # make an order with squared pizza
    order = OrderPizza(SquaredPizza)
    assert str(order.pizza) == 'Squared pizza'


class OrderPizzaBase(object):
    """
    Java-style factory method example.
    Here we need a dedicated method to create an instance of the pizza
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        # execute a factory method
        self.pizza = self.create_pizza()

    @abstractmethod
    def create_pizza(self):
        """
        This is a factory method.
        Every subclass must implement this method to create a concrete pizza
        """
        pass


class OrderRoundedPizza(OrderPizzaBase):
    """
    Concrete factory which produces a concrete rounded pizza
    """

    def create_pizza(self):
        return RoundedPizza()


class OrderSquaredPizza(OrderPizzaBase):
    """
    Concrete factory which produces a concrete squared pizza
    """

    def create_pizza(self):
        return SquaredPizza()


if __name__ == '__main__':
    # make an order with rounded pizza
    order = OrderRoundedPizza()
    assert str(order.pizza) == 'Rounded pizza'
    # make an order with squared pizza
    order = OrderSquaredPizza()
    assert str(order.pizza) == 'Squared pizza'