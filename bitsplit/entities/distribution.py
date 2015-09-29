"""
DISTRIBUTION
"""
from bitsplit.driver_loader import DriverLoader
from bitsplit.logger import Logger
from settings.daemon import STORAGE_CLASS


class Distribution(object):
    """
    DISTRIBUTION
    A package of information relating to one set-up of Bitsplit.  It will
    involve incoming and outgoing transactions and have a status.  Enclosed
    within it will be all the information needed to process a Distribution
    from end-to-end.
    """
    STATUSES_HANDLED = [
        'new',
        'verifying_incoming',  # Incoming transactions.
        'verified_incoming',
        'sending_outgoing',  # Outgoing transactions
        'sent_outgoing',
        'verifying_outgoing',
        'verified_outgoing',
        'verifying',  # Final distribution verification.
        'verified',
        'reporting',  # Queue or send out reports.
        'reported',
        'archiving',  # Finalize distribution work for "forgetting."
    ]
    TABLE = 'distributions'
    storage = None

    @classmethod
    def set_storage(cls, storage):
        cls.storage = storage

    @classmethod
    def clear_storage(cls):
        cls.storage = None

    @classmethod
    def reset_storage(cls):
        cls.clear_storage()
        cls.setup_storage()

    @classmethod
    def setup_storage(cls):
        if not cls.storage:
            cls.set_storage(STORAGE_CLASS(cls.TABLE))

    @classmethod
    def find_processable(cls):
        cls.setup_storage()
        records = cls.storage.find({
            'status': {
                '$in': cls.STATUSES_HANDLED
            }
        })
        return map(lambda tx: Distribution(tx), records)

    def __init__(self, data):
        """
        DISTRIBUTION
        Data structure that holds Transactions incoming and outgoing.
        """
        self.logger = Logger()

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

    def set_status(self, status):
        """ Update the status. """
        id = self.get("id")
        previous_status = self.get("status")

        self.set("status", status)

        self.logger.log("Updated {} status from {} to {}.".format(
            id,
            previous_status,
            status
        ))

    def handle_new(self):
        """ Stub: Handle a new Distribution. """
        self.set_status("verifying_incoming")

    def handle_verifying_incoming(self):
        """ Stub: Handle verification of incoming Transactions. """
        self.set_status("verified_incoming")

    def handle_verified_incoming(self):
        """ Stub: Handle post-verification of incoming Transactions. """
        self.set_status("sending_outgoing")

    def handle_sending_outgoing(self):
        """ Stub: Handle the sending of outgoing Transactions. """
        self.set_status("sent_outgoing")

    def handle_sent_outgoing(self):
        """ Stub: Handle the post-sending of outgoing Transactions. """
        self.set_status("verifying_outgoing")

    def handle_verifying_outgoing(self):
        """ Stub: Handle the verification of outgoing Transactions. """
        self.set_status("verified_outgoing")

    def handle_verified_outgoing(self):
        """ Stub: Handle the post-verification of outgoing Transactions. """
        self.set_status("reporting")

    def handle_reporting(self):
        """ Stub: Handle the reporting of the Ditribution. """
        self.set_status("reported")

    def handle_reported(self):
        """ Stub: Handle the post-reporting of the Ditribution. """
        self.set_status("archiving")

    def handle_archiving(self):
        """ Stub: Handle the post-reporting of the Ditribution. """
        self.set_status("archived")
