from unittest import TestCase


class TestNaming(TestCase):

    def test_filename2tuple(self):
        from eegprep.bids.naming import filename2tuple
        fname = 'sub-03_ses-01_task-irsa_run-15_eeg.set'
        sub, ses, task, run = filename2tuple(fname)
        self.assertEqual(sub, '03')
        self.assertEqual(ses, '01')
        self.assertEqual(task, 'irsa')
        self.assertEqual(run, '15')

    def test_args2filename(self):
        from eegprep.bids.naming import args2filename
        self.assertEqual(args2filename(sub='02'), 'sub-02')
