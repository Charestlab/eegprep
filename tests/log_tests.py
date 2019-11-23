from unittest import TestCase
from unittest.mock import Mock

class MockNamespace(object):
    pass


class LogTests(TestCase):

    def test_received_arguments(self):
        from eegprep.log import Log
        args = MockNamespace()
        log = Log()
        log.received_arguments(args)
