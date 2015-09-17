"""
LOGGER
"""


class Logger(object):
    """
    LOGGER
    Library instantiated for log, warning, and error.
    """
    def log(self, *args):
        self.writeln('log', args)

    def info(self, *args):
        self.log(args)

    def error(self, *args):
        self.writeln('error', args)

    def warn(self, *args):
        self.writeln('warn', args)

    def writeln(self, level, args):
        print(level + ': ' + ' '.join(map(lambda a: str(a), args)))
