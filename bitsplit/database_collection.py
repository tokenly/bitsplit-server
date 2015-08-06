"""
DATABASE COLLECTION
"""


class DatabaseCollection(object):
    """
    DATABASE COLLECTION
    Largely a pass-through for Mongo, with extra functions as needed.
    """
    def __init__(self, collection):
        self.collection = collection
        self.find = collection.find
        self.find_one = collection.find_one
        self.save = collection.save
