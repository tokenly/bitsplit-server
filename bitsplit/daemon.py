"""
DAEMON
"""
from bitsplit.entities.distribution import Distribution
from bitsplit.logger import Logger
from gevent import Greenlet
from settings.daemon import NO_WORK_DELAY

import gevent


class Daemon(Greenlet):
    def __init__(self):
        """
        DAEMON
        The running process that processes Distributions.
        """
        super(Daemon, self).__init__()
        self.running = False
        self.logger = Logger()
        self.distributions = Distribution

        with file('VERSION', 'r') as version_file:
            self.version = version_file.read().strip()

    def _run(self):
        """ Process Distributions on a loop. """
        self.display_banner()

        self.running = True

        while self.running:
            distros = self.get_distributions_to_process()
            count = len(distros)

            for distro in distros:
                distro.process()
            self.logger.log("{} jobs complete, sleeping {}s..".format(
                count,
                NO_WORK_DELAY
            ))
            gevent.sleep(NO_WORK_DELAY)

    def display_banner(self):
        """ Display the Bitsplit banner. """
        self.logger.log(79 * '=')
        self.logger.log("BITSPLIT {} ".format(self.version))
        self.logger.log(79 * '=')

    def get_distributions_to_process(self):
        """ Get the list of Distributions to process. """
        return self.distributions.find_processable()
