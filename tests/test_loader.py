import unittest

from sentences.loader import load_csv, countable_nouns, uncountable_nouns
from sentences.words.noun import Noun


class TestLoader(unittest.TestCase):
    def test_load_csv_nouns(self):
        answer = load_csv('nouns.csv')
        for line in answer:
            print(line)
        self.assertIn(['person', 'people'], answer)
        self.assertIn(['witch'], answer)

    def test_load_csv_verbs(self):
        answer = load_csv('verbs.csv')
        for line in answer:
            print(line)
        self.assertIn(['hit', 'hit', 'null'], answer)
        self.assertIn(['play', 'null', 'with'], answer)
        self.assertIn(['give', 'gave', 'null', '2'], answer)

    def test_countable_nouns(self):
        answer = countable_nouns()
        self.assertIn(Noun('person', 'people'), answer)
        self.assertIn(Noun('sheep', 'sheep'), answer)
        self.assertIn(Noun('apple'), answer)

    def test_uncountable_nouns(self):
        answer = uncountable_nouns()
        self.assertIn(Noun('water'), answer)
