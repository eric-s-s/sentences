# TODO


import unittest

from sentences.grammarizer import normalize_probability, get_nouns, Grammarizer


class TestGrammarizer(unittest.TestCase):
    def test_normalize_probability(self):
        self.assertEqual(normalize_probability(0.2), 0.2)
        self.assertEqual(normalize_probability(1), 1)
        self.assertEqual(normalize_probability(0), 0)
        self.assertEqual(normalize_probability(-1), 0)
        self.assertEqual(normalize_probability(1.2), 1.0)

