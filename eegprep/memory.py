from copy import copy

class Memory(object):
    """Stores arbitrary objects by a set of key/value pairs.
    """

    def __init__(self):
        self.objects = {}

    def store(self, obj, **filters):
        self.objects[frozenset(filters.items())] = obj

    def retrieve(self, **filters):
        selection = []
        for object_key in self.objects.keys():
            for name, val in object_key:
                if (name in filters) and (filters.get(name) != val):
                    break
            else:
                selection.append(object_key)
        return [self.objects[k] for k in selection]
