import unittest

from sentences.words.punctuation import Punctuation
from sentences.words.word import Word

comma, period, exclamation, question = Punctuation


class TestPunctuation(unittest.TestCase):
    def test_values(self):
        self.assertEqual(comma.value, ',')
        self.assertEqual(period.value, '.')
        self.assertEqual(exclamation.value, '!')
        self.assertEqual(question.value, '?')

    def test_bold(self):
        self.assertEqual(comma.bold(), Word('**,**'))
        self.assertEqual(period.bold(), Word('**.**'))
        self.assertEqual(exclamation.bold(), Word('**!**'))
        self.assertEqual(question.bold(), Word('**?**'))

