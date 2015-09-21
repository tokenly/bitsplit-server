"""
LOGGER
"""
import sys


class Logger(object):
    def __init__(self, output=None):
        """
        LOGGER
        Library instantiated for log, warning, and error.
        """
        # Set the default.
        if output is None:
            output = sys.stdout

        # Set output to use whatever is provided.
        self.output = output

        # Alias another method.
        self.info = self.log

    def set_output(self, output):
        self.output = output

    def log(self, *args):
        self.writeln('info', args)

    def error(self, *args):
        self.writeln('error', args)

    def warn(self, *args):
        self.writeln('warn', args)

    def writeln(self, level, args):
        self.output.write(level + ': ' + ' '.join(
            map(lambda a: str(a), args)
        ) + "\n")
