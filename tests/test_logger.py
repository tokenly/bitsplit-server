"""
TEST LOGGER
"""
from bitsplit.logger import Logger

from cStringIO import StringIO


class TestLogger(object):
    def __init__(self):
        self.buf = None
        self.logger = None

    def setup(self):
        self.buf = StringIO()
        self.logger = Logger()
        self.logger.set_output(self.buf)

    def teardown(self):
        self.buf.close()

    def test_error(self):
        self.logger.error("Something broke.")

        output = self.buf.getvalue()
        assert "Something broke." in output
        assert "error" in output

    def test_warn(self):
        self.logger.warn("Something you might want to change.")

        output = self.buf.getvalue()
        assert "Something you might want to change." in output
        assert "warn" in output

    def test_log(self):
        self.logger.log("Basic knowledge here.")

        output = self.buf.getvalue()
        assert "Basic knowledge here." in output
        assert "info" in output
