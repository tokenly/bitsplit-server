"""
CURRENCY DRIVER
"""


class Driver(object):
    """
    DRIVER
    Class for verifying transactions.
    """
    def __init__(self, distribution):
        """ Create the Driver, storing the distribution. """
        self.distribution = distribution

    def verify_incoming(self, transaction):
        """ Verify that an incoming transaction has been received. """
        pass

    def process_outgoing(self, transaction):
        """ Process an outgoing transaction. """
        pass

    def verify_outgoing(self, transaction):
        """ Verify an outgoing transaction was processed properly. """
        pass
