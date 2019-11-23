from unittest import TestCase
from unittest.mock import Mock


class LogTests(TestCase):

    def test_received_arguments(self):
        from eegprep.log import Log
        class MockNamespace(object):
            pass
        args = MockNamespace()
        args.foo = 'abc'
        args.bar = 1
        log = Log()
        log.write = Mock()
        log.received_arguments(args)
        log.write.assert_called_with(
            'Command arguments:\n'
            '\tfoo: abc\n'
            '\tbar: 1'
        )

    def test_found_subjects(self):
        from eegprep.log import Log
        log = Log()
        log.write = Mock()
        log.found_subjects(['pilot1', '03', 'pilot2', '02'])
        log.write.assert_called_with(
            'Found 4 subjects: pilot1, 03, pilot2, 02'
        )
