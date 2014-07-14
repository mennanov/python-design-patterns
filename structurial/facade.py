# -*- coding: utf-8 -*-

"""
The Facade pattern provides a unified interface to a set of interfaces in a subsystem.
Facade defines a higher-level interface that makes the subsystem easier to use.
"""


class FuelPump(object):
    """
    This is a part of a subsystem
    """

    def __init__(self):
        # 40 litres of gasoline
        self.fuel = 40

    def check(self):
        # performs the fast system check of the pump
        if self.fuel <= 0:
            raise RuntimeError('The fuel tank is empty')

    def pump(self):
        # pump the fuel to the engine...
        return 'pumping the fuel'


class EngineStarter(object):
    """
    This is a part of a subsystem
    """

    def __init__(self):
        # battery voltage
        self.battery = 12

    def check(self):
        # performs the fast system check of the battery
        if self.battery < 10:
            raise RuntimeError('Battery is low')

    def rotate(self):
        # rotate the starter to let the engine start...
        return 'rotating the starter'


class Car(object):
    """
    This is a facade which simplifies the whole process
    """

    def __init__(self):
        self.fuel_pump = FuelPump()
        self.engine_starter = EngineStarter()

    def lock_doors(self):
        return 'locking the doors'

    def turn_key(self):
        result = []
        try:
            self.fuel_pump.check()
            self.engine_starter.check()
        except RuntimeError:
            return
        # all systems are ok
        result.append(self.fuel_pump.pump())
        result.append(self.engine_starter.rotate())
        result.append(self.lock_doors())
        return ','.join(result)


if __name__ == '__main__':
    car = Car()
    # all we need is turn the key!
    assert car.turn_key() == 'pumping the fuel,rotating the starter,locking the doors'
