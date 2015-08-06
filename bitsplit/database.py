"""
DATABASE
"""
from gevent import monkey
monkey.patch_all()

from pymongo import MongoClient
from settings.mongo import MONGO_URL, MONGO_DATABASE
from bitsplit.database_collection import DatabaseCollection


class Database(object):
    """
    DATABASE
    Creates the connection to the database.
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        """ Create singleton. """
        if not cls.instance:
            cls.instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        """ Instantiate the connection. """
        self.client = MongoClient(MONGO_URL)
        self.database = self.client[MONGO_DATABASE]

    def __getattr__(self, name):
        """ Return a DatabaseCollection. """
        mongo_collection = self.database[name]
        return DatabaseCollection(mongo_collection)

    def __getitem__(self, name):
        return self.__getattr__(name)
