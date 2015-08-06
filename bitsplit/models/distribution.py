"""
DISTRIBUTION
"""
from bitsplit.database import Database
from util.entity import Entity


class Distribution(Entity):
    """
    DISTRIBUTION
    An entry into the system that represents:
    * Incoming funds+fees needing to be received by the system
    * Outgoing funds needing to be sent to distributees of a split
    """
    @classmethod
    def find_one_needing_action(cls):
        """ Find a Distribution that requires action next. """
        distros = Database().distributions

        record = distros.find_one({"status": "pending"})

        if record:
            return cls(distros, record)

        return None

    def start(self):
        self.status = 'processed'
        self.save()

    def save(self):
        self.collection.save(self.data)
