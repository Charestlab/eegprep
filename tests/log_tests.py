from unittest import TestCase
from unittest.mock import Mock


class MockNamespace(object):
    pass


class LogTests(TestCase):

    def test_received_arguments(self):
        from eegprep.log import Log
        args = MockNamespace()
        args.foo = 'abc'
        args.bar = 1
        log = Log()
        log.write = Mock()
        log.received_arguments(args)
        log.write.assert_called_with(
            'eegprep command arguments:\n'
            '\tfoo: abc\n'
            '\tbar: 1'
        )
