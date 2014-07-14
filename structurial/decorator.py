# -*- coding: utf-8 -*-

"""
The Decorator Pattern attaches additional responsibilities to an object dynamically.
Decorators provide a flexible alternative to subclassing for extending functionality.
Python provides closures so it can be implemented slightly differently rather than in Java:
wrapping only few methods with another function (monkey-patching with decorating).
Also, Python decorators may be used to decorate the class itself (but not an instance, which is not very flexible),
but very easy to use, though hard to implement.
"""


class CoffeeBase(object):
    """
    A base class for coffee
    """

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return self.name


class Espresso(CoffeeBase):
    """
    A concrete coffee class
    """

    def __init__(self, name='Espresso', price=15):
        super(Espresso, self).__init__(name, price)


class CoffeeDecorator(CoffeeBase):
    """
    A decorator class which has a similar interface to any other coffee
    """

    def __init__(self, coffee, name, price):
        self.coffee = coffee
        super(CoffeeDecorator, self).__init__(name, price)

    @property
    def price(self):
        return self._price + self.coffee.price

    @price.setter
    def price(self, value):
        """
        We need to define a setter descriptor to mimic the original 'price' attribute
        """
        self._price = value

    def __str__(self):
        return str(self.coffee) + ' with {}'.format(self.name)


class Milk(CoffeeDecorator):
    def __init__(self, coffee, name='Milk', price=2):
        super(Milk, self).__init__(coffee, name, price)


class Sugar(CoffeeDecorator):
    def __init__(self, coffee, name='Sugar', price=1):
        super(Sugar, self).__init__(coffee, name, price)


if __name__ == '__main__':
    espresso = Espresso()
    assert espresso.price == 15
    espresso_decorated = Sugar(Milk(espresso))
    assert str(espresso_decorated) == 'Espresso with Milk with Sugar'
    assert espresso_decorated.price == 18