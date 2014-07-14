# -*- coding: utf-8 -*-

"""
The Command pattern encapsulates request as an object, thereby letting you parameterize
other objects with different requests, queue or log requests, and support undo operation.
Or in other words: the Command pattern is a design pattern in which an object is used to represent
and encapsulate all the information needed to call a method at a later time.
In Python if you need only an "execute" operation you can simply use a callable:

def greet(who):
    print "Hello %s" % who

greet_command = lambda: greet("World")
# pass the callable around, and invoke it later
greet_command()

But to implement a more complicated command with a rich functionality you'll need a classical Command pattern below:
"""
from abc import ABCMeta, abstractmethod


class Cursor(object):
    """
    The "receiver" class, it is a class which commands will operate.
    Cursor is just an imaginary cursor at the canvas.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def redraw(self):
        # some canvas redrawing logic goes here...
        pass


class CommandAbstract(object):
    """
    A command abstract class.
    It defines 2 abstract methods: execute and undo
    """
    __metaclass__ = ABCMeta

    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class MoveRightCommand(CommandAbstract):
    def execute(self):
        self.receiver.x += 50
        self.receiver.redraw()

    def undo(self):
        self.receiver.x -= 50
        self.receiver.redraw()


class MoveUpCommand(CommandAbstract):
    def execute(self):
        self.receiver.y -= 50
        self.receiver.redraw()

    def undo(self):
        self.receiver.y += 50
        self.receiver.redraw()


if __name__ == '__main__':
    cursor = Cursor(100, 200)
    move_right = MoveRightCommand(cursor)
    move_right.execute()
    assert cursor.x == 150
    move_up = MoveUpCommand(cursor)
    move_up.execute()
    assert cursor.y == 150