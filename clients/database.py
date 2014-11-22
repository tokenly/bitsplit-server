from pymongo import MongoClient
from settings.bitsplit import BITSPLIT


class Database(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.client = MongoClient(BITSPLIT['database_url'])
        self.database = self.client.get_default_database()

    def __getitem__(self, table):
        return self.database[table]
