from servers.bitsplit_daemon import BitsplitDaemon
from entities.distribution import Distribution


class MockBitcoin(object):
    pass


class MockCounterparty(object):
    pass


def test_instantiation():
    for x in xrange(1, 6):
        Distribution.add_mock_query([
            {
                "from_addresses": [
                    {
                        "currency": "btc",
                        "address": "abc123",
                        "amount": "0.00000002",
                    },
                ],
                "to_addresses": [
                    {
                        "currency": "btc",
                        "from_address": "abc",
                        "to_addresss": "bca",
                        "amount": "0.00000001",
                    },
                ],
            }
        ])

    daemon = BitsplitDaemon()
    daemon.run_once = True
    daemon.LOOP_DELAY = 0
    daemon.run()

    daemon.__class__.bitcoin = MockBitcoin()
    daemon.__class__.counterparty = MockCounterparty()

    daemon.add_error("Test error")
    daemon.report_errors()
