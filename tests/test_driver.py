"""
TEST DRIVER
Test stub driver works.
"""
from bitsplit.driver import Driver


class TestDriver(object):
    def __init__(self):
        self.driver = None

    def setup(self):
        self.driver = Driver()

    def test_incoming_stub(self):
        assert self.driver.verify_incoming({}) is None

    def test_process_outgoing(self):
        assert self.driver.process_outgoing({}) is None

    def test_verify_outgoing(self):
        assert self.driver.verify_outgoing({}) is None
