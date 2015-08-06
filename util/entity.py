"""
ENTITY
"""


class Entity(object):
    """
    ENTITY
    A wrapped for a data dictionary.  Allows interface with data, but also
    allows extending to allow methods to manipulate data.
    """
    def __init__(self, collection, data=None):
        if not data:
            data = {}

        super(Entity, self).__setattr__('data', data)
        super(Entity, self).__setattr__('collection', collection)

    def get(self, key, default=None):
        """ Get an attribute from the data dictionary, with a fall-back. """
        return self.data.get(key, default)

    def __eq__(self, other):
        """ Is this entity equal to another? """
        return other and self.id == other.id

    def __neq__(self, other):
        """ Is this entity inequal to another? """
        return not self.__eq__(other)

    def __getattr__(self, attr):
        """ Get a data dictionary attribute. """
        if attr in self.data:
            return self.data[attr]
        else:
            return None

    def __getitem__(self, attr):
        """ Override of __getattr__ """
        return self.__getattr__(attr)

    def __setattr__(self, attr, value):
        """ Set a data dictionary attribute. """
        self.data[attr] = value

    def __setitem__(self, attr, value):
        """ Override of __setattr__ """
        return self.__setattr__(attr, value)
