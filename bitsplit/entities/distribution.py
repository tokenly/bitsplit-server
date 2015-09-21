"""
DISTRIBUTION
"""
from bitsplit.driver_loader import DriverLoader


class Distribution(object):

    STATUSES_HANDLED = [
        'new',
        'verifying_incoming',
        'verified_incoming',
        'sending_outgoing',
        'sent_outgoing',
        'verifying_outgoing',
        'verified_outgoing',
        'verifying',
        'verified',
        'reporting',
        'reported',
        'archiving',
    ]

    def __init__(self, data):
        """
        DISTRIBUTION
        Data structure that holds Transactions incoming and outgoing.
        """

        self.data = data
        self.driver_loader = DriverLoader

    def get_wrapped_transactions(self, transactions):
        """ Wrap a list of transactions. """
        return [
            self.driver_loader.get_transaction_driver(tx['currency'])(tx)
            for tx in transactions
        ]

    def get_incoming_transactions(self):
        """ Get the list of incoming transactions, wrapped. """
        return self.get_wrapped_transactions(self.data.get('incoming', []))

    def get_outgoing_transactions(self):
        """ Get the list of outgoing transactions, wrapped. """
        return self.get_wrapped_transactions(self.data.get('outgoing', []))

    def process(self):
        """ Process a Distribution through the states. """
        for status in self.STATUSES_HANDLED:
            method = self.__getattr__('handle_' + status)


    def is_status(self, status):
        """ Is this distribution in the current status? """
        return self.data.get('status') == status

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