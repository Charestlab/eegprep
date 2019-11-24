from unittest import TestCase
from unittest.mock import Mock


class MemoryTests(TestCase):

    def test_store_retrieve(self):
        from eegprep.memory import Memory
        obj1, obj2, obj3, obj4 = Mock(), Mock(), Mock(), Mock()
        ram = Memory()
        ram.store(obj1, foo='a')
        ram.store(obj2, foo='a', bar=1)
        ram.store(obj3, foo='a', bar=2, baz=0.5)
        ram.store(obj4, foo='b', bar=2)
        self.assertEqual(ram.retrieve(foo='a', bar=2), [obj1, obj3])
