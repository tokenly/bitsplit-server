"""
TEST DAEMON
"""
from bitsplit.daemon import Daemon


class TestDaemon(object):
    def __init__(self):
        self.daemon = None

    def setup(self):
        self.daemon = Daemon()

    def test_something_here(self):
        assert self.daemon is not None
