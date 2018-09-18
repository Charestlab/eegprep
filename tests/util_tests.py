from unittest import TestCase
from unittest.mock import Mock
import numpy


class TestUtil(TestCase):

    def test_resample_events_on_resampled_epochs(self):
        from eegprep.util import resample_events_on_resampled_epochs
        obj = Mock()
        obj.info = {'sfreq': 256}
        obj.events = numpy.array([
            [  2271,      0,    790],
            [  4574,      0,    590],
            [  6860,      0,    360],
            [  9113,      0,    540]])
        resample_events_on_resampled_epochs(obj, orig_sfreq=1024.)
        numpy.array_equal(obj.events, numpy.array([
            [  568,      0,    790],
            [  1144,      0,    590],
            [  1715,      0,    360],
            [  2278,      0,    540],    
        ]))
