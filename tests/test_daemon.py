"""
TEST DAEMON
"""
from bitsplit.daemon import Daemon
import gevent


class MockDistribution(object):
    def __init__(self, distro):
        self.processed = False
        self.distro = distro

    def process(self):
        self.processed = True


class MockDistributions(object):
    processable = []
    processed = []

    @classmethod
    def reset(cls):
        cls.processable = []
        cls.processed = []

    @classmethod
    def find_processable(cls):
        wrapped = []
        for d in cls.processable:
            wrapped.append(MockDistribution(d))

        cls.processed += wrapped

        return wrapped


class TestDaemon(object):
    def __init__(self):
        self.daemon = None

    def setup(self):
        self.daemon = Daemon()
        self.daemon.distributions = MockDistributions

    def test_no_processing(self):
        self.daemon.start()
        gevent.sleep()
        assert self.daemon.running is True

    def test_one_processing(self):
        MockDistributions.processable.append({
            "id": "abc123",
            "incoming": [],
            "outgoing": []
        })

        self.daemon.start()
        gevent.sleep()

        distro = MockDistributions.processed[0]
        assert distro.processed is True
