# -*- coding: utf-8 -*-

"""
Problem:
You need to write code that processes or navigates through a complicated data structure consisting of many different
kinds of objects, each of which needs to be handled in a different way.
For example, walking through a tree structure and performing different actions depending on what kind of tree nodes are
encountered.

This pattern illustrates the "open/closed" principle: classes should be opened for extension, but closed for
modification.
"""


class Node(object):
    pass


class UnaryOperator(Node):
    def __init__(self, operand):
        self.operand = operand


class BinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOperator):
    """
    We could define a processing logic right there in this class, but in this case we would violate an open/closed
    principle: to change to logic we will have to modify this class.
    """
    pass


class Sub(BinaryOperator):
    pass


class Mul(BinaryOperator):
    pass


class Div(BinaryOperator):
    pass


class Negate(UnaryOperator):
    pass


class Number(Node):
    def __init__(self, value):
        self.value = value


class NodeVisitor(object):
    """
    To use this class, a programmer inherits from it and implements various methods of the form visit_Name(),
    where Name is substituted with the node type.
    """

    def visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        """
        If there is no special method defined for a given type of node - raise an exception.
        But besides raising the exception we could process this node somehow.
        """
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))


class Evaluator(NodeVisitor):
    """
    This class inherits from the base NodeVisitor and implements a custom logic of processing different types of nodes.
    We can have any number of different Evaluator classes which implement different logic.
    """

    def visit_Number(self, node):
        return float(node.value)

    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self, node):
        return self.visit(node.left) / self.visit(node.right)

    def visit_Negate(self, node):
        return -node.operand


# Representation of 1 + 2 * (3 - 4) / 5
t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)

e = Evaluator()
assert e.visit(t4) == 0.6