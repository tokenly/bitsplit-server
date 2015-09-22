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

    def test_overwriting_drivers(self):
        DriverLoader.set('btc', MockDriver)

        assert DriverLoader.get('btc') is MockDriver

    def test_invalid(self):
        failed = False
        try:
            DriverLoader.get('zzz')
        except ValueError:
            failed = True

        assert failed is True
