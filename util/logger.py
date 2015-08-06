"""
LOGGER
"""


class Logger(object):
    """
    LOGGER
    """
    @classmethod
    def warn(cls, message):
        """ Output an warning message. """
        print "WARN: " + message

    @classmethod
    def error(cls, message):
        """ Output an error message. """
        print "ERROR: " + message

    @classmethod
    def info(cls, message):
        """ Output an info message. """
        print "INFO: " + message

    @classmethod
    def log(cls, message):
        """ Output a log message. """
        print message
