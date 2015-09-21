"""
DRIVER LOADER
"""
from settings.bitsplit import CURRENCY_DRIVERS


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
        if not cls.drivers:
            cls.reset()

    @classmethod
    def get(cls, currency):
        cls.self_check()
        cls = cls.drivers.get(currency)
        if cls is None:
            raise Exception("Driver not found for currency '{}'".format(
                currency
            ))
