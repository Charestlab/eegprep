from unittest import TestCase


class TestConfiguration(TestCase):

    def test_configure(self):
        from eegprep.configuration import Configuration
        config = Configuration()
        config.setDefaults({'downsample': 4096})
        self.assertEqual(config['downsample'], 4096)
        config.updateFromString('# bla bla\ndownsample=256')
        self.assertEqual(config['downsample'], 256)

    def test_toString(self):
        from eegprep.configuration import Configuration
        config = Configuration()
        config.setDefaults({'downsample': 4096})
        self.assertEqual(str(config), '\ndownsample=4096\n')
