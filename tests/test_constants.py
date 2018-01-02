import unittest
import os

from sentences import DATA_PATH, APP_NAME, DEFAULT_CONFIG, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, VERBS_CSV


class TestConstants(unittest.TestCase):
    """
    APP_NAME = 'sentence_mangler'

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
DEFAULT_CONFIG = os.path.join(DATA_PATH, 'default.cfg')

COUNTABLE_NOUNS_CSV = 'nouns.csv'
UNCOUNTABLE_NOUNS_CSV = 'uncountable.csv'
VERBS_CSV = 'verbs.csv'
    """
    def test_APP_NAME(self):
        self.assertEqual(APP_NAME, 'sentence_mangler')

    def test_DATA_PATH(self):
        sentences_root = os.path.dirname(__file__).replace('tests', 'sentences')
        self.assertEqual(DATA_PATH, os.path.join(sentences_root, 'data'))

    def test_DEFAULT_CONFIG(self):
        self.assertEqual(DEFAULT_CONFIG, os.path.join(DATA_PATH, 'default.cfg'))

    def test_COUNTABLE_NOUNS_CSV(self):
        self.assertEqual(COUNTABLE_NOUNS_CSV, 'nouns.csv')

    def test_UNCOUNTABLE_NOUNS_CSV(self):
        self.assertEqual(UNCOUNTABLE_NOUNS_CSV, 'uncountable.csv')

    def test_VERBS_CSV(self):
        self.assertEqual(VERBS_CSV, 'verbs.csv')
