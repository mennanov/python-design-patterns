# -*- coding: utf-8 -*-

"""
The Template Method pattern defines the skeleton of an algorithm in a method,
deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an
algorithm without changing the algorithm structure.
Alex Martelli suggested another name for this pattern: "self-delegation", because it is directly descriptive.
"""
from abc import ABCMeta, abstractmethod


class CaffeineBeverage(object):
    """
    This is an abstract class where the template method is defined.
    """
    __metaclass__ = ABCMeta

    def prepare_recipe(self):
        """
        It is actually a template method: it makes calls to other
        methods which should be implemented by subclasses.
        Though in this example the code in a template method is very simple (just calling other methods one by one),
        it can be very sophisticated and complex in a real project (loops, conditions, etc..)
        """
        result = []
        result.append(self.boil_water())
        result.append(self.brew())
        result.append(self.pour_in_cup())
        if self.customer_wants_condiments():
            result.append(self.add_condiments())
        return '\n'.join(result)

    @abstractmethod
    def brew(self):
        pass

    @abstractmethod
    def add_condiments(self):
        pass

    def boil_water(self):
        """
        This method is shared by all the subclasses so we put it here
        """
        return 'water is boiling...'

    def pour_in_cup(self):
        """
        This method is shared by all the subclasses so we put it here
        """
        return 'cup is filling...'

    def customer_wants_condiments(self):
        """
        This is a hook which is called inside the template method,
        subclass can override this method, but it does not have to.
        """
        return True


class Tea(CaffeineBeverage):
    """
    A concrete implementation of an abstract class which implements all the needed abstract methods.
    """

    def brew(self):
        return 'tea is brewing...'

    def add_condiments(self):
        return 'add lemon to the tea...'


if __name__ == '__main__':
    tea = Tea()
    assert tea.prepare_recipe() == 'water is boiling...\ntea is brewing...\ncup is filling...\nadd lemon to the tea...'