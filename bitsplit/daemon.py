"""
BITSPLIT DAEMON
"""
# from bitsplit.models.transaction import Transaction
from util.runnable import Runnable


class Daemon(Runnable):
    """
    BITSPLIT DAEMON
    The primary thread that runs the whole shebang:
    * Check for new transactions
    * Handle them in their current state
    * Connect to drivers and link logic together
    """
    def __init__(self):
        self.running = False

    def tick(self):
        """ The main loop ticking. """
        print "Tick."
