import unittest

from sentences.words.punctuation import Punctuation

comma, period, exclamation, question = Punctuation


class TestPunctuation(unittest.TestCase):
    def test_values(self):
        self.assertEqual(comma.value, ',')
        self.assertEqual(period.value, '.')
        self.assertEqual(exclamation.value, '!')
        self.assertEqual(question.value, '?')
