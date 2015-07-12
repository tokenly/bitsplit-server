"""
DISTRIBUTION
"""


class Distribution(object):
    """
    DISTRIBUTION
    An entry into the system that represents:
    * Incoming funds+fees needing to be received by the system
    * Outgoing funds needing to be sent to distributees of a split
    """

    @classmethod
    def find_pending_incoming_funds(cls):
        return []
