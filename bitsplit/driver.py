"""
CURRENCY DRIVER
"""


class Driver(object):
    """
    DRIVER
    Class for verifying transactions.
    """

    def verify_incoming(self, transaction):
        """ Verify that an incoming transaction has been received. """
        return False

    def process_outgoing(self, transaction):
        """ Process an outgoing transaction and verify it processed. """
        return False
