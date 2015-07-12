"""
BITSPLIT DAEMON
"""
from bitsplit.models.distribution import Distribution
from util.runnable import Runnable


class Daemon(Runnable):
    """
    BITSPLIT DAEMON
    The primary thread that runs the whole shebang:
    * Check for new Distributions
    * Handle them in their current state
    * Connect to drivers appropriate to the currencies involved
    """
    RUNNABLE_DELAY = 30

    def tick(self):
        """ The main loop ticking. """
        self.handle_pending_incoming_funds()
        self.handle_pending_outgoing_funds()
        self.handle_pending_verification()

    @classmethod
    def handle_pending_incoming_funds(cls):
        """ Incoming transactions. """
        distros = Distribution.find_pending_incoming_funds()
        for distro in distros:
            if distro.has_incoming_funds():
                distro.set_pending_outgoing_funds_status()

    @classmethod
    def handle_pending_outgoing_funds(cls):
        """ Outgoing transactions. """
        pass

    @classmethod
    def handle_pending_verification(cls):
        """ Verification and reporting. """
        pass
