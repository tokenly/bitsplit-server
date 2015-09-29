"""
STORAGE
"""


class Storage(object):
    """
    STORAGE
    Location/System for storage of information, like a database or filesystem.
    """
    def __init__(self, table):
        self.table = table
