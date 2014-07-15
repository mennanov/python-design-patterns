# -*- coding: utf-8 -*-

"""
The Composition pattern allows you to compose objects into tree structures to represent part-whohe hierarchies.
Composite lets clients treat individual objects and compositions of objects uniformly.
"""
from abc import ABCMeta, abstractmethod


class Component(object):
    """
    This class defines an interface for all objects in a composition: both the composite and the leaf nodes.
    It usually implements a default behavior for adding and removing children nodes.
    """
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name
        self.children = set()

    def add_child(self, child):
        self.children.add(child)

    def remove_child(self, child):
        self.children.remove(child)

    def __iter__(self):
        return iter(self.children)

    @abstractmethod
    def say(self):
        """
        This is a method which subclasses must implement to define their custom behavior
        """
        pass


class Composite(Component):
    """
    This is a node in a tree which may have children.
    """

    def say(self):
        return 'I am a composite node ' + self.name


class Leaf(Component):
    """
    This is a leaf node in a tree and it can't have any children.
    """

    def add_child(self, child):
        raise NotImplementedError('Leaf node can not have children')

    def remove_child(self, child):
        raise NotImplementedError('Leaf node can not have children')

    def __iter__(self):
        raise TypeError('Leaf node is not iterable')

    def say(self):
        return 'I am a leaf node ' + self.name


if __name__ == '__main__':
    root = Composite('root')
    root.add_child(Leaf('a'))
    root.add_child(Leaf('b'))
    c = Composite('c')
    c.add_child(Leaf('d'))
    c.add_child(Leaf('e'))
    root.add_child(c)
    result = []

    def traverse(node):
        # recursive depth-first search on a tree
        result.append(node.say())
        try:
            for c in node:
                traverse(c)
        except TypeError:
            pass

    traverse(root)
    assert '\n'.join(result) == 'I am a composite node root\nI am a leaf node b\nI am a composite node c\nI am a leaf node d\nI am a leaf node e\nI am a leaf node a'

