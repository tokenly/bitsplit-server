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

    def find(self, spec):
        return []

    def find_one(self, *args, **kwargs):
        results = self.find(*args, **kwargs)
        if results:
            return results[0]
        return None
