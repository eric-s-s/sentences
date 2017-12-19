import os
import unittest

from sentences.tkinter.mvm import ConfigLoader, APP_NAME

from sentences import DATA_PATH


class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        self.home_dir = os.path.join(os.path.expanduser('~'), APP_NAME)

    def test_default(self):
        loader = ConfigLoader()
        text = loader.get_text()

        with open(os.path.join(DATA_PATH, 'default.cfg')) as f:
            default = f.read()

        self.assertEqual(text, default)
        self.assertEqual(loader.location, self.home_dir)

