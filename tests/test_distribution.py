"""
TEST DISTRIBUTION
Test a Distribution properly hands-off its tasks.
"""
from bitsplit.driver_loader import DriverLoader
from bitsplit.entities.distribution import Distribution


class MockDriver(object):
    def __init__(self, data):
        self.data = data


class MockBitcoin(MockDriver):
    pass


class MockCounterparty(MockDriver):
    pass


class TestDistribution(object):
    def __init__(self):
        DriverLoader.clear()
        DriverLoader.set('btc', MockBitcoin)
        DriverLoader.set('xcp', MockCounterparty)
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
                {
                    "currency": "xcp",
                    "amount": "1234",
                    "asset": "ltbcoin",
                    "address": "longbutfakeaddress"
                },
            ],
            "outgoing": [
                {
                    "currency": "btc",
                    "amount": "0.001",
                    "address": "anotherlongaddress"
                },
                {
                    "currency": "xcp",
                    "amount": "1234",
                    "asset": "ltbcoin",
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

    def test_incoming_data(self):
        incoming = self.distro.get_incoming_transactions()
        assert len(incoming) == 2

        assert type(incoming[0]) is MockBitcoin
        assert type(incoming[1]) is MockCounterparty

    def test_outgoing_data(self):
        outgoing = self.distro.get_outgoing_transactions()
        assert len(outgoing) == 2

        assert type(outgoing[0]) is MockBitcoin
        assert type(outgoing[1]) is MockCounterparty

    def test_process(self):
        self.distro.process()
