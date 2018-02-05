import unittest

from sentences.words.punctuation import Punctuation
from sentences.words.basicword import BasicWord

comma, period, exclamation, question = Punctuation


class TestPunctuation(unittest.TestCase):
    def test_values(self):
        self.assertEqual(comma.value, ',')
        self.assertEqual(period.value, '.')
        self.assertEqual(exclamation.value, '!')
        self.assertEqual(question.value, '?')

    def test_bold(self):
        self.assertEqual(comma.bold(), BasicWord('<bold>,</bold>'))
        self.assertEqual(period.bold(), BasicWord('<bold>.</bold>'))
        self.assertEqual(exclamation.bold(), BasicWord('<bold>!</bold>'))
        self.assertEqual(question.bold(), BasicWord('<bold>?</bold>'))

