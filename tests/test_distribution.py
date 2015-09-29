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


class MockStorage(object):
    def find(self, spec):
        return [
            {
                "id": "abc123",
                "status": "new",
                "fees": [
                    {
                        "currency": "btc",
                        "amount": "0.0001"
                    }
                ],
                "incoming": [
                    {
                        "currency": "btc",
                        "address": "abc123",
                        "amount": "1.00010000",
                        "verified": False
                    }
                ],
                "outgoing": [
                    {
                        "currency": "btc",
                        "address": "abc123",
                        "amount": "0.50000000",
                        "sent": False,
                        "verified": False
                    },
                    {
                        "currency": "btc",
                        "address": "xyz321",
                        "amount": "0.50000000",
                        "sent": False,
                        "verified": False
                    },
                ],
                "hooks": [
                    {
                        "type": "webhook",
                        "url": "http://guillaume.vanderest.org/bitsplit.php"
                    },
                    {
                        "type": "email",
                        "address": "guillaume@vanderest.org",
                        "format": "html"
                    }
                ]
            }
        ]


class TestDistribution(object):
    def __init__(self):
        DriverLoader.clear()
        DriverLoader.set('btc', MockBitcoin)
        DriverLoader.set('xcp', MockCounterparty)
        self.distro = None

        Distribution.reset_storage()
        Distribution.set_storage(MockStorage())

    def setup(self):
        self.distro = Distribution.find_processable()[0]

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
        assert len(incoming) == 1

        assert type(incoming[0]) is MockBitcoin

    def test_outgoing_data(self):
        outgoing = self.distro.get_outgoing_transactions()
        assert len(outgoing) == 2

        assert type(outgoing[0]) is MockBitcoin
        assert type(outgoing[1]) is MockBitcoin

    def test_process(self):
        self.distro.process()
