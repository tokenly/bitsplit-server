"""
TEST DISTRIBUTION
Test a Distribution properly hands-off its tasks.
"""
from bitsplit.driver_loader import DriverLoader
from bitsplit.entities.distribution import Distribution


class MockBitcoin(object):
    pass


class TestDistribution(object):
    def __init__(self):
        DriverLoader.clear()
        DriverLoader.set('btc', MockBitcoin)
        self.distro = None

    def setup(self):
        self.distro = Distribution({
            "id": "abc123",
            "status": "new",
            "incoming": [
                {
                    "currency": "btc",
                    "amount": "0.001",
                    "address": "longbutfakeaddress"
                },
            ],
            "outgoing": [
                {
                    "currency": "btc",
                    "amount": "0.001",
                    "address": "anotherlongaddress"
                },
            ],
        })

    def test_attributes(self):
        # Valid.
        assert self.distro.get('id') == "abc123"

        # Invalid.
        assert self.distro.get('banana') is None

        # Override ID.
        self.distro.set('id', 'hello')
        assert self.distro.get('id') == "hello"

        # Create new banana value.
        self.distro.set('banana', 'zibble')
        assert self.distro.get('banana') == 'zibble'

        # Still None.
        assert self.distro.get('what') is None

    def test_process(self):
        self.distro.process()
