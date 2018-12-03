from unittest import TestCase


class TestConfiguration(TestCase):

    def test_configure(self):
        from eegprep.configuration import Configuration
        config = Configuration()
        config.setDefaults({'downsample': 4096, 'out_file_format': 'fif'})
        self.assertEqual(config['downsample'], 4096)
        self.assertEqual(config['out_file_format'], 'fif')
        config.updateFromString('# bla bla\ndownsample=256\nout_file_format=mat')
        self.assertEqual(config['downsample'], 256)
        self.assertEqual(config['out_file_format'], 'mat')

    def test_toString(self):
        from eegprep.configuration import Configuration
        config = Configuration()
        config.setDefaults({'downsample': 4096})
        self.assertEqual(str(config), '\ndownsample=4096\n')
