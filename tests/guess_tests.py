from unittest import TestCase


class TestGuess(TestCase):

    def test_guess_montage(self):
        from eegprep.guess import guess_montage
        self.assertEqual(guess_montage(['A1']*137), 'biosemi128')
        self.assertEqual(guess_montage(['A1']*67), 'biosemi64')
