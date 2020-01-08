from unittest import TestCase
from unittest.mock import Mock


class InputOutputTests(TestCase):

    def test_build_fpath(self):
        from eegprep.input_output import InputOutput
        log, memory, layout = Mock(), Mock(), Mock()
        scope = {
            'subject': '02',
            'session': '05'
        }
        io = InputOutput(log, memory, '/data', scope, layout)
        self.assertEqual(
            io.build_fpath(suffix='hello', ext='foo'),
            '/data/derivatives/eegprep/sub-02/ses-05/sub-02_ses-05_hello.foo'
        )
