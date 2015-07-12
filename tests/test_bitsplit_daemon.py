"""
TEST BITSPLIT DAEMON
"""
from bitsplit.daemon import Daemon
from unittest.mock import Mock


class TestBitsplitDaemon(object):
    """
    TEST BITSPLIT DAEMON
    """
    def __init__(self):
        self.daemon = None

    def setup(self):
        """ Create Daemon instance. """
        self.daemon = Daemon()

    def test_instantiation(self):
        """ Test that it worked at least once. """
        assert self.daemon is not None

    def test_running(self):
        """ Test that it worked at least once. """
        self.daemon.tick = Mock()
        self.daemon.run(count=1, delay=0)

        assert self.daemon.tick.called

    def test_tick(self):
        """ Test that it worked at least once. """
        self.daemon.tick()
