"""
DISTRIBUTION
"""
from bitsplit.driver import Driver


class Distribution(object):
    """
    DISTRIBUTION
    Data structure that holds Transactions incoming and outgoing.
    """
    def __init__(self, data):
        self.data = data
        self.drivers = Driver

    def process(self):
        """ Process a Distribution through the states. """
        if self.is_new():
            self.handle_new()

        if self.is_verifying_incoming():
            self.handle_verifying_incoming()

        if self.is_verifying_outgoing():
            self.handle_verifying_outgoing()

        if self.is_verified():
            self.handle_verified()

        if self.is_reporting():
            self.handle_reporting()

        if self.is_reported():
            self.handle_reported()

    @classmethod
    def find_processable(cls):
        raw = [
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

        return map(lambda tx: Distribution(tx), raw)
