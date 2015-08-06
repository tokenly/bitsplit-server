"""
BITSPLIT DAEMON
"""
from bitsplit.models.distribution import Distribution
from gevent import Greenlet
from util.logger import Logger
import gevent


class Daemon(Greenlet):
    """
    BITSPLIT DAEMON
    The primary thread that runs the whole shebang:
    * Check for new Distributions
    * Handle them in their current state
    * Connect to drivers appropriate to the currencies involved
    """
    def _run(self):
        """ Main run loop. """
        NO_WORK_DELAY = 5  # FIXME move this to a settings file

        self.running = True
        while self.running:

            has_work = True
            while has_work:

                distro = self.get_next_distribution()
                if distro:
                    distro.start()
                else:
                    has_work = False

            Logger.log("No work to do.  Sleeping for {}s.".format(
                NO_WORK_DELAY
            ))
            gevent.sleep(NO_WORK_DELAY)

    def get_next_distribution(self):
        """ Get the next Distribution that needs action. """
        distro = Distribution.find_one_needing_action()
        return distro
