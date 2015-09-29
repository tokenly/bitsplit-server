"""
TEST STORAGE
"""
from bitsplit.storage import Storage
from mock import Mock


class TestStorage(object):
    def __init__(self):
        self.storage = None

    def setup(self):
        self.storage = Storage('test')

    def test_find(self):
        records = self.storage.find()

        assert type(records) is list
        assert len(records) == 0

    def test_find_one(self):
        record = self.storage.find_one()

        assert record is None

    def test_find_one_with_fake(self):
        results = [1, 2, 3]
        self.storage.find = Mock(return_value=results)

        spec = {"id": "abc123"}

        result = self.storage.find_one(spec)

        assert result == 1
        assert self.storage.find.called_once_with_args(spec)
