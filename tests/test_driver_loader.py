"""
TEST DRIVER LOADER
"""
from bitsplit.drivers.bitcoin import Bitcoin
from bitsplit.driver_loader import DriverLoader


class MockDriver(object):
    pass


class TestDriverLoader(object):
    def setup(self):
        DriverLoader.clear()

    def test_bitcoin(self):
        assert DriverLoader.get('btc') is Bitcoin

    def test_overloading(self):
        DriverLoader.set('btc', MockDriver)

        assert DriverLoader.get('btc') is MockDriver
