"""
TEST DRIVER
Test stub driver works.
"""
from bitsplit.driver import Driver


class MockDistribution(object):
    pass


class TestDriver(object):
    def __init__(self):
        self.distribution = None
        self.driver = None

    def setup(self):
        self.distribution = MockDistribution()
        self.driver = Driver(self.distribution)

    def test_incoming_stub(self):
        assert self.driver.verify_incoming({}) is None

    def test_process_outgoing(self):
        assert self.driver.process_outgoing({}) is None

    def test_verify_outgoing(self):
        assert self.driver.verify_outgoing({}) is None
