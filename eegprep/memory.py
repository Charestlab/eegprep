from copy import copy

class Memory(object):
    """Stores arbitrary objects by a set of key/value pairs.
    """

    def __init__(self, log):
        self.objects = {}
        self.log = log

    def store(self, obj, **filters):
        key = frozenset(filters.items())
        self.log.storing_object_in_memory(key, obj)
        self.objects[key] = obj

    def retrieve(self, **filters):
        selection = self.find_matching_keys(**filters)
        return [self.objects[k] for k in selection]

    def delete(self, **filters):
        selection = self.find_matching_keys(**filters)
        for k in selection:
            self.log.removing_object_from_memory(k, self.objects[k])
            del self.objects[k]

    def find_matching_keys(self, **filters):
        selection = []
        for object_key in self.objects.keys():
            for name, val in object_key:
                if (name in filters) and (filters.get(name) != val):
                    break
            else:
                selection.append(object_key)
        return selection
