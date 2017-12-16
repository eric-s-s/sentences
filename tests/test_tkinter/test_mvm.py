import os
import unittest

from sentences.tkinter.mvm import ConfigLoader, APP_NAME



class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        self.home_dir = os.path.expanduser('~') + os.path.sep + APP_NAME

    def test_default(self):
        loader = ConfigLoader()
        text = loader.get_text()

        with open('./sentence_mangler.cfg') as f:
            default = f.read()

        self.assertEqual(text, default)
        self.assertEqual(loader.location, self.home_dir)

