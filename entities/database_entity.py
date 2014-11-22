from clients.database import Database
from bson import json_util
import json


class DatabaseEntity(object):
    collection_name = None
    collection = None
    database = None

    mock_queries = []
    mock_fetches = []

    def __init__(self, database=None, _id=None, data=None):
        if not database:
            self.__class__.database = Database()

        if not self.__class__.collection:
            if not self.__class__.collection_name:
                raise Exception("Class {} needs a collection_name defined"
                                % (__name__))
            else:
                self.__class__.collection = self.__class__.database[self.__class__.collection_name]

        if not data:
            data = {}

        super(DatabaseEntity, self).__setattr__('_data', data)

        if _id:
            self.fetch_by_id(_id)

    def to_json(self):
        data = self._data
        for key in data:
            val = data[key]
            if not type(val) in [int, str, float]:
                data[key] = str(val)
        return json.dumps(data)

    @classmethod
    def add_mock_query(cls, array_of_data):
        processed = []

        for data in array_of_data:
            processed.append(cls.wrap(data))

        cls.mock_queries.append(processed)

    @classmethod
    def add_mock_fetch(cls, data):
        processed = cls.wrap(data)
        cls.mock_fetches.append(processed)

    def query(self, spec=None):
        if len(self.__class__.mock_queries) > 0:
            print("POPPED A MOCK QUERY")
            return self.__class__.mock_queries.pop(0)

        results = []

        records = self.__class__.collection.find(spec)
        print(repr(spec), records.count())
        for record in records:
            obj = self.wrap(record)
            results.append(obj)

        return results

    def fetch(self, *args, **kwargs):
        if len(self.__class__.mock_fetches) > 0:
            print("POPPED A MOCK FETCH")
            return self.__class__.mock_fetches.pop(0)

        data = self.collection.find_one(kwargs)
        if not data:
            return data

        return self.wrap(data=data)

    @classmethod
    def wrap(cls, data):
        wrapped = cls(data=data)
        return wrapped

    def fetch_by_id(self, _id):
        result = self.find_one(_id=str(_id))
        if result:
            result = self.wrap(result)
        return result

    def save(self):
        data = self._data
        print(repr(data))
        if self._id:
            self.__class__.collection.update({"_id": str(self._id)}, self._data)
        else:
            self._data['_id'] = self.__class__.collection.save(self._data)

    def delete(self):
        self.__class__.collection.remove({"_id": str(self._id)})

    def __getattr__(self, attr):
        data = self.__getattribute__('_data')

        if attr == '_data':
            return data

        if not attr in data:
            return None

        return data[attr]

    def __setattr__(self, attr, val):
        data = self._data
        data[attr] = val
