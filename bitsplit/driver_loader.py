"""
DRIVER LOADER
"""
from settings.daemon import CURRENCY_DRIVERS


class DriverLoader(object):
    """
    DRIVER LOADER
    Detector that returns the appropriate currency Driver.
    """
    drivers = None

    @classmethod
    def clear(cls):
        cls.drivers = None

    @classmethod
    def reset(cls):
        cls.drivers = dict(CURRENCY_DRIVERS)

    @classmethod
    def self_check(cls):
        if cls.drivers is None:
            cls.reset()

    @classmethod
    def set(cls, currency, driver):
        cls.self_check()
        cls.drivers[currency] = driver

    @classmethod
    def get(cls, currency):
        cls.self_check()
        cls = cls.drivers.get(currency)
        if cls is None:
            raise ValueError("Driver not found for currency '{}'".format(
                currency
            ))
        return cls
