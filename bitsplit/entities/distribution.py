"""
DISTRIBUTION
"""
from bitsplit.driver_loader import DriverLoader


class Distribution(object):

    STATUSES_HANDLED = [
        'new',
        # 'verifying_incoming',
        # 'verified_incoming',
        # 'sending_outgoing',
        # 'sent_outgoing',
        # 'verifying_outgoing',
        # 'verified_outgoing',
        # 'verifying',
        # 'verified',
        # 'reporting',
        # 'reported',
        # 'archiving',
    ]

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

    def __init__(self, data):
        """
        DISTRIBUTION
        Data structure that holds Transactions incoming and outgoing.
        """

        self.data = data
        self.get = self.data.get
        self.driver_loader = DriverLoader

    def set(self, attr, val):
        self.data[attr] = val

    def get_wrapped_transactions(self, transactions):
        """ Wrap a list of transactions. """
        return [
            self.driver_loader.get(tx['currency'])(tx)
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
            method_name = 'handle_' + status
            method = super(Distribution, self).__getattribute__(method_name)
            if self.is_status(status):
                method()

    def is_status(self, status):
        """ Is this distribution in the current status? """
        return self.data.get('status') == status

    def handle_new(self):
        """ Handle a new Distribution. """
        pass
