"""
BITSPLIT DAEMON
"""
from bitsplit.models.distribution import Distribution
from util.runnable import Runnable

# TODO Handle fees, is this a pre- or post- action?


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
        self.handle_incoming_distributions()
        self.handle_outgoing_distributions()
        self.verify_completed_distributions()

    @classmethod
    def handle_incoming_distributions(cls):
        """
        Incoming transactions.
        All these are doing is waiting for funds to show up.
        If they haven't shown up, check again next time.
        """
        distros = Distribution.find_pending_incoming_funds()

        for distro in distros:
            # Mark this step as complete if funds are available.
            if distro.has_incoming_funds():
                distro.set_pending_outgoing()

    @classmethod
    def handle_outgoing_distributions(cls):
        """
        Outgoing transactions.
        Funds were verified, send all distribution funds to recipients.
        """
        distros = Distribution.find_pending_outgoing_funds()

        for distro in distros:
            # There are no unsent transactions
            if distro.has_sent_all_transactions():
                distro.set_pending_verification()

            # Any transactions were unsent
            else:
                distro.send_unsent_transactions()

    @classmethod
    def verify_completed_distributions(cls):
        """ Verification and reporting. """
        distros = Distribution.find_pending_verification()

        for distro in distros:

            # All is well.
            if distro.is_complete():
                distro.set_verified()
