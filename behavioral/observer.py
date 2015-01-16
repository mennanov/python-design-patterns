# -*- coding: utf-8 -*-

"""
The Observer Pattern defines a one-to-many dependency between objects so that when one objects changes state,
all of its dependants are notified and updated automatically.
Python allows to simplify this pattern using decorators, though it works differently than in classic example:
we wrap the whole method which we want to observe so we can not unsubscribe.
The classical approach is at the bottom.
"""
from abc import ABCMeta, abstractmethod
from StringIO import StringIO
import weakref


class Newspaper(object):
    """
     This is a subject of observation which does not need to modify its code
     to handle the observers, so it's just an ordinary class.
    """

    def __init__(self):
        self.data = 'Good news everyone!'

    def change_state(self):
        """
        This method is called when the state is changed
        """
        return self.data


def notify(output):
    """
    This is a decorator which will log all the data
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            output.write('Newspaper changed its state:' + result)
            return result

        return wrapper

    return decorator


if __name__ == '__main__':
    output = StringIO()
    newspaper = Newspaper()
    # decorate the method on-fly
    newspaper.change_state = notify(output)(newspaper.change_state)
    newspaper.change_state()

    output.seek(0)
    assert output.read() == 'Newspaper changed its state:Good news everyone!'


class Newspaper(object):
    """
    This is a subject of observation, it keeps a set of all the subscribers
    and notifies them immediately when needed.
    """

    def __init__(self):
        self.subscribers = set()
        self.data = 'Bad news everyone!'
        # store the set of subscribers who don't want to receive updates
        self._unsubscribers = set()

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self._unsubscribers.add(subscriber)

    def _unsubscribe_flush(self):
        """
        Remove all the subscribers who don't want the updates.
        We can not do this in "notify" method since we can't modify a set of subscribers
        during the iteration.
        """
        self.subscribers = self.subscribers - self._unsubscribers
        self._unsubscribers = set()

    def notify(self):
        self._unsubscribe_flush()
        for subscriber in self.subscribers:
            subscriber.update(self.data)


class SubscriberBase(object):
    """
    This is a subscriber, it gets update via the "update" method
    which should be implemented.
    """

    __metaclass__ = ABCMeta

    def __init__(self, subject, output):
        # keep the link to the subject to be able to unsubscribe whenever we want
        # we use a weakref to make the subject garbage-collectable when it is deleted
        self.subject = weakref.proxy(subject)
        # output file-like object (needed to gather the output)
        self.output = output
        # subscribe itself
        self.subject.subscribe(self)

    @abstractmethod
    def update(self, *args):
        pass


class Betty(SubscriberBase):
    def update(self, *args):
        self.output.write('Betty got the update:' + args[0] + '\n')
        if 'Bad' in args[0]:
            # Betty is not looking for the bad news - unsubscribe
            self.subject.unsubscribe(self)


class Nancy(SubscriberBase):
    def update(self, *args):
        self.output.write('Nancy got the update:' + args[0] + '\n')


if __name__ == '__main__':
    output = StringIO()
    newspaper = Newspaper()
    betty = Betty(newspaper, output)
    nancy = Nancy(newspaper, output)
    # notify all the subscribers about the recent news
    newspaper.notify()
    # change the news content
    newspaper.data = 'Good news every one!'
    newspaper.notify()

    output.seek(0)
    # the order of the lines may differ from time to time since we're using a set, not a list
    assert output.read() == 'Betty got the update:Bad news everyone!\nNancy got the update:Bad news everyone!\nNancy got the update:Good news every one!\n'