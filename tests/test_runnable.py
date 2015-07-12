"""
TEST RUNNABLE
"""
from util.runnable import Runnable
from unittest.mock import Mock
import time


class TestRunnable(object):
    """ TEST RUNNABLE """
    def __init__(self):
        self.runnable = None

    def setup(self):
        """ Create Runnable instance. """
        self.runnable = Runnable()

    def test_running_tick(self):
        """ Do nothing on tick. """
        self.runnable.tick()

    def test_running_async_loop(self):
        """ Do nothing on tick. """
        self.runnable.tick = Mock()
        self.runnable.run(async=True, count=10, delay=0.001)

        time.sleep(0.02)

        assert self.runnable.tick.call_count == 10

    def test_running_for_iterations(self):
        """ Test that it can be run once through. """
        self.runnable.tick = Mock()

        self.runnable.tick.reset_mock()
        self.runnable.run(count=1, delay=0)
        assert self.runnable.tick.call_count == 1

        self.runnable.tick.reset_mock()
        self.runnable.run(count=2, delay=0)
        assert self.runnable.tick.call_count == 2

        self.runnable.tick.reset_mock()
        self.runnable.run(count=10, delay=0)
        assert self.runnable.tick.call_count == 10

    def test_running_with_class_delay(self):
        """ Test that it can be run once through. """
        self.runnable.RUNNABLE_DELAY = 0.001
        self.runnable.tick = Mock()
        self.runnable.run(count=1)
        assert self.runnable.tick.call_count == 1

    def test_running_asynchronously(self):
        """ Test that it can be run in parallel. """
        self.runnable.tick = Mock()
        self.runnable.run_async(count=10, delay=0.001)

        for count in range(1, 10):
            time.sleep(count * 0.001)
            assert self.runnable.tick.call_count >= count

    def test_stopping(self):
        """ Test that it can be run in parallel. """
        self.runnable.tick = Mock()
        self.runnable.run_async(count=10, delay=0.01)

        time.sleep(0.01)
        print(self.runnable.tick.call_count)
        assert self.runnable.tick.call_count == 1

        time.sleep(0.01)
        print(self.runnable.tick.call_count)
        assert self.runnable.tick.call_count == 2

        self.runnable.stop()

        time.sleep(0.01)
        print(self.runnable.tick.call_count)
        assert self.runnable.tick.call_count < 4

        time.sleep(0.1)
        print(self.runnable.tick.call_count)
        assert self.runnable.tick.call_count < 4
